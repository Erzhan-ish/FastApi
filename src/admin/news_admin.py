from sqladmin import Admin
from fastapi import FastAPI
from src.db import engine
from src.models.models import NewsModel, NewsItemModel
from sqladmin import ModelView
from fastapi import File


# -------------------------------
#  BASE SETUP
# -------------------------------
def setup_admin(app: FastAPI):
    # Создание экземпляра админ-панели
    admin = Admin(app, engine)

    # Добавление представлений (views) для моделей
    admin.add_view(NewsAdmin)
    admin.add_view(NewsItemAdmin)

    # Возвращение экземпляра админ-панели
    return admin


# -------------------------------
#  NEWS ADMIN
# -------------------------------
class NewsAdmin(ModelView, model=NewsModel):
    # Название в панели
    name = "News"
    name_plural = "News List"
    icon = "fa-solid fa-newspaper"

    # Какие поля показывать в таблице
    column_list = [
        NewsModel.id,
        NewsModel.title,
        NewsModel.short_description,
    ]

    # Какие поля можно искать (LIKE %text%)
    column_searchable_list = [
        NewsModel.title,
    ]

    # Поля в форме
    form_columns = [
        NewsModel.title,
        NewsModel.background_image_url,
        NewsModel.short_description,
    ]


    form_args = {
        "title": {"label": "Title"},
        "background_image_url": {"label": "Background Image URL"},
        "short_description": {"label": "Short Description"},
    }


# -------------------------------
#  NEWS ITEM ADMIN
# -------------------------------
class NewsItemAdmin(ModelView, model=NewsItemModel):
    name = "News Item"
    name_plural = "News Items"
    icon = "fa-solid fa-list"

    # Поля, отображаемые в таблице
    column_list = [
        NewsItemModel.id,
        NewsItemModel.news,          # Важное: будет отображаться __str__()
        NewsItemModel.news_type,
        NewsItemModel.title,
        NewsItemModel.date,
        NewsItemModel.image_url,
    ]

    # Поля для поиска
    column_searchable_list = [
        NewsItemModel.title,
    ]

    # Поля в форме
    form_columns = [
        NewsItemModel.news,          # ВАЖНО! Это ForeignKey через relationship
        NewsItemModel.news_type,
        NewsItemModel.image_url,
        NewsItemModel.title,
        NewsItemModel.short_description,
        NewsItemModel.date,
        NewsItemModel.link_url,
    ]

    # Настройки формы
    form_args = {
        "news": {"label": "News"},
        "news_type": {"label": "Type"},
        "image_url": {"label": "Image URL"},
        "title": {"label": "Title"},
        "short_description": {"label": "Short Description"},
        "date": {"label": "Date"},
        "link_url": {"label": "Link"},
    }

    form_overrides = {
        NewsModel.background_image_url: File("Upload Image")  # Используем FileField для загрузки
    }


