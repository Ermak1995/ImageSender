import os

import grpc
from dotenv import load_dotenv
from minio import S3Error

import image_service_pb2
import image_service_pb2_grpc

from concurrent import futures
from s3_client import S3Client

load_dotenv()


class ImageServiceServicer(image_service_pb2_grpc.ImageServiceServicer):

    def __init__(self, s3):
        self.s3 = s3

    def UploadImage(self, request_iterator, context):
        metadata = None
        chunks = []

        # Читаем поток: первый пакет — метаданные, остальные — куски файла
        for request in request_iterator:
            if request.HasField("metadata"):
                metadata = request.metadata
            elif request.HasField("chunk"):
                chunks.append(request.chunk)

        # Валидация
        if metadata is None:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Первый пакет должен содержать метаданные")
            return

        if not chunks:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Файл пустой")
            return

        # Склеиваем куски в один файл
        data = b"".join(chunks)

        # Загружаем в MinIO
        try:
            image_id = self.s3.upload(metadata.filename, metadata.content_type, data)
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, f"Ошибка загрузки: {e}")
            return

        return image_service_pb2.UploadResponse(
            image_id=image_id,
            message=f"Файл '{metadata.filename}' загружен успешно"
        )

    def DownloadImage(self, request, context):
        try:
            data = self.s3.download(request.image_id)
        except S3Error as e:
            context.abort(grpc.StatusCode.NOT_FOUND, f"Файл не найден: {request.image_id}")
            return
 
        chunk_size = 256 * 1024
        for i in range(0, len(data), chunk_size):
            yield image_service_pb2.DownloadResponse(chunk=data[i:i + chunk_size])
 
    def DeleteImage(self, request, context):
        if not self.s3.object_exists(request.image_id):
            context.abort(grpc.StatusCode.NOT_FOUND, f"Файл не найден: {request.image_id}")
            return
 
        self.s3.delete(request.image_id)
        return image_service_pb2.DeleteResponse(success=True, message=f"Удалено: {request.image_id}")
 
    def ListImages(self, request, context):
        try:
            objects = self.s3.list_objects(prefix=request.prefix, filename_filter=request.filename)
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, f"Ошибка получения списка: {e}")
            return
 
        images = [
            image_service_pb2.ImageInfo(
                image_id=obj["image_id"],
                filename=obj["filename"],
                size_bytes=obj["size_bytes"],
                content_type=obj["content_type"],
                created_at=obj["created_at"],
            )
            for obj in objects
        ]
 
        return image_service_pb2.ListResponse(images=images)
 
    def GetImageInfo(self, request, context):
        try:
            info = self.s3.get_info(request.image_id)
        except S3Error:
            context.abort(grpc.StatusCode.NOT_FOUND, f"Файл не найден: {request.image_id}")
            return
 
        return image_service_pb2.ImageInfo(
            image_id=info["image_id"],
            filename=info["filename"],
            size_bytes=info["size_bytes"],
            content_type=info["content_type"],
            created_at=info["created_at"],
        )


def serve():
    s3 = S3Client(
        os.environ["MINIO_ENDPOINT"],
        os.environ["MINIO_ROOT_USER"],
        os.environ["MINIO_ROOT_PASSWORD"],
        os.environ["MINIO_BUCKET"],
    )
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    image_service_pb2_grpc.add_ImageServiceServicer_to_server(ImageServiceServicer(s3), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Сервер запущен на порту 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
