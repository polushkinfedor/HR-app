import os
from motor.motor_asyncio import AsyncIOMotorClient

# Настройки подключения
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "hr_system")

# Создаем клиент и базу данных
client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]

print(f"Подключено к MongoDB: {MONGO_URL}")
print(f"База данных: {DATABASE_NAME}")