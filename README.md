# ImageSender

gRPC-сервис для загрузки, скачивания и управления изображениями. Файлы хранятся в MinIO (S3-совместимое объектное хранилище).

## Стек

- Python 3 — gRPC-сервер и CLI-клиент
- gRPC / Protobuf — транспортный протокол
- MinIO — объектное хранилище
- Docker Compose — запуск MinIO

## Архитектура

```
[client.py] --gRPC:50051--> [server.py] --S3:9000--> [MinIO (Docker)]
```

MinIO поднимается в Docker. Сервер и клиент запускаются локально.

## Требования

- Python 3.10+
- Docker + Docker Compose

## Установка и запуск

**1. Клонировать репозиторий**

```bash
git clone https://github.com/Ermak1995/ImageSender.git
cd ImageSender
```

**2. Установить зависимости**

```bash
pip install -r requirements.txt
```

**3. Настроить переменные окружения**

```bash
cp .env.example .env
```

Открой `.env` и задай свои значения `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` (файл `.env` в `.gitignore` и не попадает в репозиторий).

**4. Запустить MinIO**

```bash
docker compose up -d
```

**5. Запустить gRPC-сервер**

```bash
python server.py
```

Сервер запустится на порту `50051` и автоматически создаст бакет `images` в MinIO.

**6. Запустить клиент** (в отдельном терминале)

```bash
python client.py
```

## Использование клиента

При запуске `client.py` открывается интерактивное меню:

```
========================================
1. Загрузить изображение
2. Список изображений
3. Скачать изображение
4. Удалить изображение
5. Информация об изображении
6. Выход
========================================
```

**Загрузка** — введи путь к файлу (например: `test_photos/photo.png`).  
Сервер вернёт `image_id` (UUID) — он нужен для всех остальных операций.

**Список** — показывает все загруженные файлы. Можно задать префикс для фильтрации или оставить пустым.

**Скачивание** — введи `image_id` и путь для сохранения (например: `/tmp/result.jpg`).

**Удаление** — введи `image_id` файла, который нужно удалить.

**Информация** — выводит метаданные файла: имя, размер, тип, дату загрузки.

### Поддерживаемые форматы

`.jpg` / `.jpeg` / `.png` / `.gif` / `.webp`

## Сервисы

| Сервис | Порт | Назначение |
|--------|------|------------|
| MinIO API | 9000 | S3-совместимый API |
| MinIO Console | 9001 | Веб-интерфейс |
| gRPC сервер | 50051 | API для клиента |

**MinIO консоль:** http://localhost:9001  
Логин и пароль задаются в `.env` (см. `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD`).

## Переменные окружения

Заданы в `.env` (создаётся из `.env.example`).

| Переменная | По умолчанию | Описание |
|------------|--------------|----------|
| `MINIO_ROOT_USER` | — | Логин MinIO |
| `MINIO_ROOT_PASSWORD` | — | Пароль MinIO |
| `MINIO_ENDPOINT` | `localhost:9000` | Адрес MinIO API |
| `MINIO_BUCKET` | `images` | Название бакета |
| `GRPC_HOST` | `localhost` | Хост gRPC-сервера (клиент) |
| `GRPC_PORT` | `50051` | Порт gRPC-сервера (клиент) |

## gRPC API

Определено в `proto/image_service.proto`:

| Метод | Тип | Описание |
|-------|-----|----------|
| `UploadImage` | client-streaming | Загрузить изображение |
| `DownloadImage` | server-streaming | Скачать изображение по `image_id` |
| `DeleteImage` | unary | Удалить изображение |
| `ListImages` | unary | Список изображений (с опциональным префиксом) |
| `GetImageInfo` | unary | Метаданные одного изображения |

### Перегенерация proto-файлов

```bash
bash generate_proto.sh
```

Файлы `image_service_pb2.py` и `image_service_pb2_grpc.py` генерируются из `proto/image_service.proto`.

## Остановка

```bash
docker compose down        # остановить MinIO, данные сохранятся
docker compose down -v     # остановить и удалить том с данными
```
