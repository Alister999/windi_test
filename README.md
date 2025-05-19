# windi_test


windi_test — проект мессенджера на FastAPI. Он реализует REST API для всех сущностей (пользователи, чаты, группы, сообщения), а также включает два WebSocket-эндпоинта — для чатов и групп — с полной поддержкой асинхронной работы.

 - Основные возможности
	•	Регистрация и аутентификация пользователей
	•	Создание и управление чатами и группами
	•	Отправка и получение сообщений
	•	WebSocket для обмена сообщениями в реальном времени:
	•	/ws/chat/{chat_id}
	•	/ws/group/{group_id}
	•	Асинхронное взаимодействие с PostgreSQL через SQLAlchemy
	•	Тесты с использованием pytest и httpx

 - Запуск через Docker Compose

    Убедитесь, что у вас установлен Docker и Docker Compose.

 - Запуск приложения

    docker-compose up --build

    После запуска приложение будет доступно по адресу:

    http://localhost:8000

 - Документация Swagger будет доступна по адресу:

    http://localhost:8000/docs

 - Переменные окружения

    Для работы в проект нужно включить файл .env в корень проекта, и его содержимое выглядит примерно так:

    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_HOST=db
    DB_NAME=windi_db
    TEST_DB_HOST=localhost
    TEST_DB_NAME=windi_test_db
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    REFRESH_TOKEN_EXPIRE_DAYS=7
    SECRET_KEY=your_secret_key

 - Запуск тестов

    Для запуска тестов выполните:

    docker-compose exec <айди или имя контейнера приложения> pytest

 - Тесты покрывают:
	•	авторизацию (регистрацию, вход, refresh токен),
	•	работу с чатами и группами,
	•	отправку сообщений,
	•	WebSocket-соединения,
	•	неавторизованный доступ (проверка ограничений).

 - Структура проекта

    windi_test/
    ├── src/
    │   ├── main.py                 # Точка входа в приложение
    │   ├── models/                 # SQLAlchemy-модели
    │   ├── services/               # Бизнес-логика
    │   ├── api/                    # Эндпоинты REST и WebSocket
    │   ├── core/                   # База данных, конфигурации
    │   └── tests/                  # Pytest-тесты
    ├── docker-compose.yml          # Файл Docker Compose
    ├── Dockerfile                  # Docker-образ приложения
    ├── requirements.txt            # Зависимости проекта
    ├── .env                        # Переменные окружения
    └── README.md                   # Документация проекта

 - Лицензия

    Проект распространяется под лицензией MIT.



