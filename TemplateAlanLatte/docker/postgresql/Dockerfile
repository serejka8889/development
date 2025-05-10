# Используем официальный образ PostgreSQL
FROM postgres:15-alpine

# Переменные окружения для PostgreSQL
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV POSTGRES_DB=${POSTGRES__DATABASE_NAME}
ENV POSTGRES_USER=${POSTGRES_USER}

# Экспонируем порт
EXPOSE 5432
