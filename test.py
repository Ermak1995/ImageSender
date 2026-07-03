from s3_client import S3Client

s3 = S3Client("localhost:9000", "admin", "password12345", "images")
image_id = s3.upload("test.jpg", "image/jpeg", b"fake data")
# image_id = '8537142a-bcc8-4084-b589-3dca6daf1a5f'
print(f"Загружено: {image_id}")
print(s3.get_info(image_id))
s3.delete(image_id)
print("Удалено")