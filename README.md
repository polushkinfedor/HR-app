# HR-система

Курсовая работа по дисциплине "Технологии сетевого взаимодействия" (10-й семестр)

## Структура проекта
```
hr-system/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── app/
│     ├── main.py
│     ├── database.py
│     ├── models.py
│     └── routers/
│         ├── departments.py
│         ├── positions.py
│         └── employees.py
├── static/
│     └── index.html
└── README.md
```

## Предварительные требования

- Docker 20.10+
- Docker Compose 2.0+

## Быстрый старт

### Клонирование репозитория

```
git clone <repository-url>
cd hr-system
```

## Запуск системы
Запуск всех сервисов
```docker compose up --build```

Или в фоновом режиме
```docker compose up -d --build```

## Проверка работоспособности
Проверка статуса
```curl http://localhost:8000/health```

Или откройте в браузере
```http://localhost:8000/```

# API Эндпоинты
Сотрудники

    GET /api/employees - Получить список сотрудников

    GET /api/employees/{id} - Получить сотрудника по ID

    POST /api/employees - Создать нового сотрудника

    PUT /api/employees/{id} - Обновить данные сотрудника

    DELETE /api/employees/{id} - Удалить сотрудника

Отделы

    GET /api/departments - Получить список отделов

    GET /api/departments/{id} - Получить отдел по ID

    POST /api/departments - Создать новый отдел

    PUT /api/departments/{id} - Обновить данные отдела

    DELETE /api/departments/{id} - Удалить отдел

Должности

    GET /api/positions - Получить список должностей

    GET /api/positions/{id} - Получить должность по ID

    POST /api/positions - Создать новую должность

    PUT /api/positions/{id} - Обновить данные должности

    DELETE /api/positions/{id} - Удалить должность

## Остановка системы
Остановка контейнеров
```docker compose down```

Остановка с удалением volumes
```docker compose down -v```

### Технологии

    Backend: FastAPI, Python

    База данных: MongoDB

    Frontend: HTML, JavaScript

    Контейнеризация: Docker, Docker Compose
