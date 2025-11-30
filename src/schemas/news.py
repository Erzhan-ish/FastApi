from pydantic import BaseModel, Field
from .enums import NewsType

class NewsSchema(BaseModel):
    background_image_url: str = Field(description="URL фонового изображения")
    title: str = Field(max_length=100, description="Заголовок")
    short_description: str = Field(max_length=250, description="Краткое описание")

class NewsItemSchema(BaseModel):
    news_id: int = Field(description="ID новости")
    news_type: NewsType = Field(description="Тип новости")
    image_url: str = Field(description="URL изображения новости")
    title: str = Field(max_length=100, description="Заголовок новости")
    short_description: str = Field(max_length=250, description="Краткое описание новости")
    date: str = Field(description="Дата в формате DD-MM-YYYY")
    link_url: str = Field(description="URL")