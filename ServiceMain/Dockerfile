# ServiceMain/Dockerfile

FROM python:3.10-slim

RUN apt-get update && apt-get install -y git curl cron awscli && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY db-backup.sh /usr/local/bin/db-backup.sh
RUN chmod +x /usr/local/bin/db-backup.sh

# Настройка cron для автоматического выполнения бэкапов
RUN echo '0 2 * * * /usr/local/bin/db-backup.sh' >> /etc/crontab

# Установка переменной окружения
ENV YANDEX_TOKEN="y0__wgBEMn84L0GGJrSNCDstPmLEj3mibU9UTJQhVvzwdQpi-g7DeLm"

CMD ["sh", "-c", "cron && python main.py"]
