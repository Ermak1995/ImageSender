import os

from dotenv import load_dotenv

from s3_client import S3Client

load_dotenv()

s3 = S3Client(
    os.environ["MINIO_ENDPOINT"],
    os.environ["MINIO_ROOT_USER"],
    os.environ["MINIO_ROOT_PASSWORD"],
    os.environ["MINIO_BUCKET"],
)
image_id = s3.upload("test.jpg", "image/jpeg", b"fake data")
# image_id = '8537142a-bcc8-4084-b589-3dca6daf1a5f'
print(f"Загружено: {image_id}")
print(s3.get_info(image_id))
s3.delete(image_id)
print("Удалено")