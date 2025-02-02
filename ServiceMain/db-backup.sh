#!/bin/bash

# Установите переменные
DB_PATH="/app/data/base.db"  # Путь к вашей базе данных
BACKUP_DIR="/app/backup"  # Директория для хранения резервных копий
TIMESTAMP=$(date +%Y-%m-%d-%H-%M-%S)

# Создание директории для бэкапов, если ее нет
mkdir -p $BACKUP_DIR

# Создание резервной копии базы данных
cp $DB_PATH $BACKUP_DIR/database-$TIMESTAMP.db

# Удаление старых бэкапов (например, старше 7 дней)
find $BACKUP_DIR -type f -name "*.db" -mtime +7 -exec rm {} \;


# Загрузка резервной копии на Яндекс.Диск с использованием Python
python - <<EOF
import yadisk
import os

# Инициализация клиента Яндекс.Диска
token = os.environ['YANDEX_TOKEN']
disk = yadisk.YaDisk(token=token)

# Загрузка резервной копии на Яндекс.Диск
backup_file_path = os.path.join("$BACKUP_DIR", "database-$TIMESTAMP.db")
disk.upload(backup_file_path, "/backup/database-$TIMESTAMP.db")
EOF
