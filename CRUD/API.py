from fastapi import APIRouter, UploadFile, File
from .db import SessionDep
from .schemas import NewsSchema, NewsItemSchema
from sqlalchemy import select
from .models import NewsModel, NewsItemModel
import os

router = APIRouter()  # ← правильный объект

@router.post("/upload-image/")
async def upload_image(image: UploadFile = File(...)):
    save_dir = "images"
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, image.filename)
    contents = await image.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    image_url = f"/{save_dir}/{image.filename}"
    return {"image_url": image_url}


@router.post("/news")
async def create_news(data: NewsSchema, session: SessionDep):
    new_news = NewsModel(
        title=data.title,
        background_image_url=data.background_image_url,
        short_description=data.short_description
    )
    session.add(new_news)
    await session.commit()
    return {"ok": True, "message": "News created successfully."}


@router.get("/news")
async def get_news(session: SessionDep):
    result = await session.execute(select(NewsModel))
    return result.scalars().all()


@router.get("/news/{id}")
async def get_news_id(id: int, session: SessionDep):
    result = await session.execute(select(NewsModel).where(NewsModel.id == id))
    return result.scalar_one_or_none()

@router.put("/news/{id}")
async def update_news(id: int, data: NewsSchema, session: SessionDep):
    result = await session.execute(select(NewsModel).where(NewsModel.id == id))
    news_item = result.scalar_one_or_none()
    if news_item:
        news_item.title = data.title
        news_item.background_image_url = data.background_image_url
        news_item.short_description = data.short_description
        await session.commit()
        return {"ok": True, "message": "News updated successfully."}
    return {"ok": False, "message": "News item not found."}

@router.delete("/news/{id}")
async def delete_news(id: int, session: SessionDep):
    result = await session.execute(select(NewsModel).where(NewsModel.id == id))
    news_item = result.scalar_one_or_none()
    if news_item:
        await session.delete(news_item)
        await session.commit()
        return {"ok": True, "message": "News deleted successfully."}
    return {"ok": False, "message": "News item not found."}




@router.post("/news_item")
async def create_news_item(data: NewsItemSchema, session: SessionDep):
    new_news_item = NewsItemModel(
        news_id=data.news_id,
        news_type=data.news_type.value,
        image_url=data.image_url,
        title=data.title,
        short_description=data.short_description,
        date=data.date,
        link_url=data.link_url
    )
    session.add(new_news_item)
    await session.commit()
    return {"ok": True, "message": "News item created successfully."}


@router.get("/news_item")
async def get_news_items(session: SessionDep):
    result = await session.execute(select(NewsItemModel))
    return result.scalars().all()


@router.get("/news_item/{id}")
async def get_news_item_id(id: int, session: SessionDep):
    result = await session.execute(select(NewsItemModel).where(NewsItemModel.id == id))
    return result.scalar_one_or_none()


@router.put("/news_item/{id}")
async def update_news_item(id: int, data: NewsItemSchema, session: SessionDep):
    result = await session.execute(select(NewsItemModel).where(NewsItemModel.id == id))
    news_item = result.scalar_one_or_none()
    if news_item:
        news_item.news_id = data.news_id
        news_item.news_type = data.news_type.value
        news_item.image_url = data.image_url
        news_item.title = data.title
        news_item.short_description = data.short_description
        news_item.date = data.date
        news_item.link_url = data.link_url
        await session.commit()
        return {"ok": True, "message": "News item updated successfully."}
    return {"ok": False, "message": "News item not found."}


@router.delete("/news_item/{id}")
async def delete_news_item(id: int, session: SessionDep):
    result = await session.execute(select(NewsItemModel).where(NewsItemModel.id == id))
    news_item = result.scalar_one_or_none()
    if news_item:
        await session.delete(news_item)
        await session.commit()
        return {"ok": True, "message": "News item deleted successfully."}
    return {"ok": False, "message": "News item not found."}