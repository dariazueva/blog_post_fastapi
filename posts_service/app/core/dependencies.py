from app.core.database import AsyncSessionLocal
from app.core.rabbitmq import RabbitMQCategoryValidator, category_validator_instance
from app.repositories.posts import PostRepository
from app.services.posts import PostService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db


def get_post_repository(db: AsyncSession = Depends(get_async_db)) -> PostRepository:
    return PostRepository(db=db)


def get_category_validator() -> RabbitMQCategoryValidator:
    return category_validator_instance


def get_post_service(
    post_repo: PostRepository = Depends(get_post_repository),
    category_validator: RabbitMQCategoryValidator = Depends(get_category_validator),
) -> PostService:
    return PostService(post_repo=post_repo, category_validator=category_validator)
