# Image Sender
Сервис для загрузки и хранения изображений. 
Backend на gRPC/FastAPI, хранилище на MinIO (S3-совместимое).

## Стек технологий
- Python / FastAPI / gRPC — бэкенд
- MinIO — объектное хранилище
- Docker / Docker Compose — контейнеризация и оркестрация

## Требования к запуску
- Docker Desktop [(ссылка на скачивание)](https://docs.docker.com/desktop/)
- Git

## Быстрый старт

Последовательность команд — от нуля до работающего сервиса:

    git clone https://github.com/Ermak1995/ImageSender.git
    cd ImageSender
    docker compose up -d

Проверить что всё поднялось:

    docker compose ps

Открыть в браузере:
- MinIO консоль: http://localhost:9001
- Логин: admin / Пароль: password12345

## Требования

Что должно быть установлено на машине чтобы всё запустить:
- Docker Desktop (ссылка на скачивание)
- Git

## Быстрый старт

Последовательность команд — от нуля до работающего сервиса:

    git clone https://github.com/Ermak1995/ImageSender.git
    cd ImageSender
    docker compose up -d

Проверить что всё поднялось:

    docker compose ps

Открыть в браузере:
- MinIO консоль: http://localhost:9001
  Логин: admin / Пароль: password12345

## Сервисы

| Сервис | Образ | Порты | Назначение |
|--------|-------|-------|------------|
| minio  | quay.io/minio/minio:RELEASE.2025-04-22T22-12-26Z | 9000, 9001 | Объектное хранилище |

(позже сюда добавится строка с сервисом Ильи)

## Переменные окружения

| Переменная | Значение по умолчанию | Описание |
|------------|----------------------|----------|
| MINIO_ROOT_USER | admin | Логин администратора MinIO |
| MINIO_ROOT_PASSWORD | password12345 | Пароль (минимум 8 символов) |

## Данные и хранилище

Данные MinIO хранятся в томе `minio_data`.
Том переживает перезапуск контейнера — 
файлы не теряются при `docker compose down`.

Убедиться что том создан:

    docker volume ls

## Остановка

    docker compose down        # остановить, данные сохранятся
    docker compose down -v     # остановить И удалить данные тома

## Загрузка и передача изображений через gRPC
*в разработке