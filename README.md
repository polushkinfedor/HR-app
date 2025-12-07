# HR-app
Курсовая работа по дисциплине "Технологии сетевого взаимодействия" (10й семестр)

# Структура проекта:
hr-system/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── routers/
│       ├── departments.py
│       ├── positions.py
│       └── employees.py
└── static/
    └── index.html

Предварительные требования

    Docker 20.10+

    Docker Compose 2.0+

Быстрый старт

    Клонирование репозитория

bash

git clone <repository-url>
cd hr-system

    Запуск системы

bash

# Запуск всех сервисов
docker compose up --build

# Или в фоновом режиме
docker compose up -d --build

    Проверка работоспособности

bash

# Проверка статуса
curl http://localhost:8000/health

# Или откройте в браузере
# http://localhost:8000/
    
