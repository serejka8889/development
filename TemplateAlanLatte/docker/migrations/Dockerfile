# Используем базовый образ Python для работы с YOYO
FROM python:3.11-slim

# Устанавливаем YOYO и прочие зависимости
RUN pip install yoyo-migrations psycopg2-binary

# Копируем миграционные файлы
COPY ./migrations /migrations

# Переключаемся в рабочую директорию
WORKDIR /migrations

#
CMD ["yoyo", "apply", "--database", "$POSTGRES_DATABASE_URL", "/migrations"]
