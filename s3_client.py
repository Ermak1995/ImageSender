import uuid
from io import BytesIO

from minio import Minio

class S3Client:
    def __init__(self, endpoint, access_key, secret_key, bucket_name):
        self.bucket = bucket_name
        self.client = Minio(endpoint=endpoint,
                       access_key=access_key,
                       secret_key=secret_key,
                       secure=False)
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(bucket_name=bucket_name)
            print(f"[S3] Создан бакет: {self.bucket}")
        else:
            print(f"[S3] Бакет уже существует: {self.bucket}")

    def health_check(self):
        return self.client.bucket_exists(self.bucket)

    def upload(self, filename: str, content_type: str, data: bytes) -> str:
        image_id = str(uuid.uuid4())  # генерируем уникальный ключ

        self.client.put_object(
            bucket_name=self.bucket,
            object_name=image_id,  # ключ в MinIO = UUID
            data=BytesIO(data),
            length=len(data),
            content_type=content_type,
            metadata={"filename": filename}  # оригинальное имя храним в метаданных
        )

        return image_id
