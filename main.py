import grpc
import image_service_pb2_grpc as pb2_grpc

from concurrent import futures
from s3_client import S3Client


class ImageServiceServicer(pb2_grpc.ImageServiceServicer):

    def __init__(self, s3):
        self.s3 = s3

    def UploadImage(self, request_iterator, context):
        pass

    def DownloadImage(self, request, context):
        pass

    def DeleteImage(self, request, context):
        pass

    def ListImages(self, request, context):
        pass

    def GetImageInfo(self, request, context):
        pass


def serve():
    s3 = S3Client("localhost:9000", "admin", "password12345", "images")
    print(s3.health_check())
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ImageServiceServicer_to_server(ImageServiceServicer(s3), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Сервер запущен на порту 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
