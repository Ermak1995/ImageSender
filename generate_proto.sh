#!/bin/bash
set -e

PROTO_DIR="proto"
OUT_DIR="."
FILENAME="image_service.proto"

# Генерируем
python -m grpc_tools.protoc \
  -I $PROTO_DIR \
  --python_out=$OUT_DIR \
  --grpc_python_out=$OUT_DIR \
  $PROTO_DIR/$FILENAME

echo "Готово! Файлы сгенерированы в $OUT_DIR/"