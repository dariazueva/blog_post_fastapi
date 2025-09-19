from contextlib import asynccontextmanager

from app.api.routers import posts
from app.core.database import create_db_and_tables
from app.core.rabbitmq import category_validator_instance
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(
        "Приложение постов запускается. Создаем базу данных и подключаемся к RabbitMQ..."
    )
    await create_db_and_tables()
    await category_validator_instance.connect()
    print("Инициализация завершена.")
    yield
    print("Приложение постов завершает работу. Закрываем соединение с RabbitMQ...")
    await category_validator_instance.close()
    print("Работа завершена.")


app = FastAPI(title="Сервис для постов", lifespan=lifespan)

app.include_router(posts.router)


@app.get("/")
async def root():
    """Корневой эндпоинт."""
    return {"message": "Это проект написан на FastAPI."}
