
## Python template
   (https://github.com/AlanLatte/Python/actions/workflows/main.yml)

## Управления задачами на FastAPI

   Проект представляет собой веб-приложение для управления задачами с помощью FastAPI и PostgreSQL на шаблоне AlanLatte.

---

### Структура проекта

.
├── app                      - Основное приложение
│   ├── configuration        - Конфигурация приложения
│   ├── internal             - Внутренняя логика приложения
│   │   ├── pkg              - Вспомогательные пакеты и утилиты
│   │   ├── repository       - Слой репозитория для работа с базой данных
│   │   ├── routes           - Слой контроллеров
│   │   └── services         - Сервисный слой бизнес-логики 
│   ├── pkg                  - Пакеты и модули общего назначения
│   │   ├── connectors       - Коннекторы к внешним сервисам
│   │   ├── handlers         - Обработчики событий и запросов
│   │   ├── logger           - Логгеры и журналирование
│   │   ├── models           - Модели представления данных
│   │   └── settings         - Глобальная конфигурация приложения
│   └── 
├── docker                   - Dockers для развёртывания сервиса
│   ├── api                  - Конфигурация docker API-сервера
│   ├── grafana              - Графические панели и дашборды Grafana
│   │   └── provisioning     - Автоматическое заполнение панелей Grafana
│   ├── migrations           - Миграции базы данных через Docker
│   ├── postgresql           - Конфигурация docker PostgreSQL
│   └── prometheus           - Конфигурация docker Prometheus
├── migrations               - Каталог для скриптов миграции базы данных
│   └── 001-create_tasks.py  - Скрипт миграции базы данных
├── scripts                  - Вспомогательные скрипты
├── src                      - Рабочие ресурсы приложения
│   ├── logs                 - Папка для лог-файлов
│   └── prometheus           - Локальные данные и конфиги Prometheus
└── tests                    - Тесты
├── docker-compose.yml       - Основной конфигурационный файл docker compose для создания и запуска контейнеров
├── poetry.lock              - Блокировка зависимостей
├── poetry.toml              - Зависимости проекта
├── pyproject.toml           - Конфигурация Poetry
├── README.md                - Документация проекта
├── yoyo.ini                 - Конфигурация для менеджера миграций Yoyo
├── .dockerignore            - Игнорируемые файлы и директории для Docker
├── .env                     - Переменные окружения проекта
├── .gitignore               - Игнорируемые файлы и директории для Git

---

### Установка и запуск

Чтобы запустить проект, выполните следующие шаги:

1. Скачать с резитория проект

2. Распаковать проект 

3. Перейти в каталог TemplateAlanLatte

4. Отключить локальный postgresql
   systemctl stop postgresql (debian)
   systemctl stop  postgresql-15.service (redos)
   pg_ctl -D "C:\Program Files\PostgreSQL\15\data" (windows)

4. Развернуть проект командой:
   docker-compose up --build

5. Запустить браузер и перейти по ссылкам:
   http://0.0.0.0:8000/docs (проверка работы FastAPI)
   http://0.0.0.0:9000 (вход в Prometheus)
   http://0.0.0.0:3000 (вход в Grafana, admin:admin, выбрать dashboards - FastAPI и посмотреть)
   
6. По адресу http://0.0.0.0:8000/docs, нажав на кнопку "Authorize" ввести X-ACCESS-TOKEN

   94c1482c96930b37c57abd7b23bf3864
   
   авторизация успешно пройдена, замочки закрылись, можно проверять работу api приложения
   
   
