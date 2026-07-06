import os
import grpc
import image_service_pb2 as pb2
import image_service_pb2_grpc as pb2_grpc

GRPC_HOST = os.getenv("GRPC_HOST", "localhost")
GRPC_PORT = os.getenv("GRPC_PORT", "50051")
CHUNK_SIZE = 256 * 1024  # 256 KB

CONTENT_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def upload(stub):
    filepath = input("Путь к файлу: ").strip()

    if not os.path.exists(filepath):
        print(f"Файл не найден: {filepath}")
        return

    filename = os.path.basename(filepath)
    ext = os.path.splitext(filename)[1].lower()
    content_type = CONTENT_TYPES.get(ext)

    if not content_type:
        print(f"Неподдерживаемый формат: {ext}")
        return

    def generate_chunks():
        yield pb2.UploadRequest(
            metadata=pb2.ImageMetadata(filename=filename, content_type=content_type)
        )
        with open(filepath, "rb") as f:
            while chunk := f.read(CHUNK_SIZE):
                yield pb2.UploadRequest(chunk=chunk)

    try:
        response = stub.UploadImage(generate_chunks())
        print(f"Загружено! image_id: {response.image_id}")
        print(f"Сообщение: {response.message}")
    except grpc.RpcError as e:
        print(f"Ошибка: {e.code()} — {e.details()}")


def list_images(stub):
    filename_filter = input("Фильтр по имени файла (пусто — все): ").strip()

    try:
        response = stub.ListImages(pb2.ListRequest(filename=filename_filter))
        print(f"\nНайдено: {len(response.images)}")
        for i, img in enumerate(response.images, start=1):
            print(f"\n--- #{i} ---")
            print(f"  image_id:     {img.image_id}")
            print(f"  filename:     {img.filename}")
            print(f"  size:         {img.size_bytes} байт")
            print(f"  content_type: {img.content_type}")
            print(f"  created_at:   {img.created_at}")
    except grpc.RpcError as e:
        print(f"Ошибка: {e.code()} — {e.details()}")


def download(stub):
    image_id = input("image_id: ").strip()
    save_path = input("Куда сохранить (например: /tmp/photo.jpg): ").strip()

    try:
        with open(save_path, "wb") as f:
            for chunk in stub.DownloadImage(pb2.DownloadRequest(image_id=image_id)):
                f.write(chunk.chunk)
        print(f"Сохранено: {save_path}")
    except grpc.RpcError as e:
        print(f"Ошибка: {e.code()} — {e.details()}")


def delete(stub):
    image_id = input("image_id: ").strip()

    try:
        response = stub.DeleteImage(pb2.DeleteRequest(image_id=image_id))
        print(f"Успех: {response.success}")
        print(f"Сообщение: {response.message}")
    except grpc.RpcError as e:
        print(f"Ошибка: {e.code()} — {e.details()}")


def get_info(stub):
    image_id = input("image_id: ").strip()

    try:
        info = stub.GetImageInfo(pb2.GetImageInfoRequest(image_id=image_id))
        print(f"\n  image_id:     {info.image_id}")
        print(f"  filename:     {info.filename}")
        print(f"  size:         {info.size_bytes} байт")
        print(f"  content_type: {info.content_type}")
        print(f"  created_at:   {info.created_at}")
    except grpc.RpcError as e:
        print(f"Ошибка: {e.code()} — {e.details()}")


MENU = """
========================================
1. Загрузить изображение
2. Список изображений
3. Скачать изображение
4. Удалить изображение
5. Информация об изображении
6. Выход
========================================"""


def main():
    address = f"{GRPC_HOST}:{GRPC_PORT}"
    print(f"Подключение: {address}")

    with grpc.insecure_channel(address) as channel:
        stub = pb2_grpc.ImageServiceStub(channel)

        actions = {
            "1": upload,
            "2": list_images,
            "3": download,
            "4": delete,
            "5": get_info,
        }

        while True:
            print(MENU)
            choice = input("Выбери действие: ").strip()

            if choice == "6":
                print("Выход.")
                break

            action = actions.get(choice)
            if action is None:
                print("Неизвестный пункт.")
                continue

            print()
            action(stub)
            print()


if __name__ == "__main__":
    main()
