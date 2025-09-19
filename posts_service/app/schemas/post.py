from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    category_id: int


class Post(PostBase):
    id: int

    class Config:
        from_attributes = True
