import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


# -----------------------------
# CRUD tests for NEWS
# -----------------------------

@pytest.mark.asyncio
async def test_create_news():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.post("/news", json={
            "background_image_url": "bg.jpg",
            "title": "My Title",
            "short_description": "Short desc"
        })

        assert resp.status_code == 200
        assert resp.json()["ok"] is True


@pytest.mark.asyncio
async def test_get_news():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/news")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_get_news_id():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:

        # Создаём запись
        created = await ac.post("/news", json={
            "background_image_url": "bg.jpg",
            "title": "Test ID",
            "short_description": "desc"
        })
        assert created.status_code == 200

        # Берём ID из БД
        all_news = await ac.get("/news")
        news_id = all_news.json()[-1]["id"]

        resp = await ac.get(f"/news/{news_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == news_id


@pytest.mark.asyncio
async def test_update_news():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:

        # Создаём новость
        await ac.post("/news", json={
            "background_image_url": "bg.jpg",
            "title": "Old",
            "short_description": "Old desc"
        })

        all_news = await ac.get("/news")
        news_id = all_news.json()[-1]["id"]

        # Обновляем
        resp = await ac.put(f"/news/{news_id}", json={
            "background_image_url": "new.jpg",
            "title": "Updated",
            "short_description": "Updated desc"
        })

        assert resp.status_code == 200
        assert resp.json()["ok"] is True

        # Проверяем обновление
        updated = await ac.get(f"/news/{news_id}")
        assert updated.json()["title"] == "Updated"


@pytest.mark.asyncio
async def test_delete_news():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:

        # Создаём новость
        await ac.post("/news", json={
            "background_image_url": "bg.jpg",
            "title": "To Delete",
            "short_description": "desc"
        })

        all_news = await ac.get("/news")
        news_id = all_news.json()[-1]["id"]

        # Удаляем
        resp = await ac.delete(f"/news/{news_id}")
        assert resp.status_code == 200
        assert resp.json()["ok"] is True

        # Проверяем отсутствие
        deleted = await ac.get(f"/news/{news_id}")
        assert deleted.json() is None


# -----------------------------
# CRUD tests for NEWS_ITEM
# -----------------------------

@pytest.mark.asyncio
async def test_create_news_item():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:

        # Сначала создаём NEWS
        await ac.post("/news", json={
            "background_image_url": "bg.jpg",
            "title": "Parent",
            "short_description": "desc"
        })
        all_news = await ac.get("/news")
        parent_id = all_news.json()[-1]["id"]

        resp = await ac.post("/news_item", json={
            "news_id": parent_id,
            "news_type": "news",
            "image_url": "img.jpg",
            "title": "Item",
            "short_description": "desc",
            "date": "2025-01-01",
            "link_url": "http://example.com"
        })

        assert resp.status_code == 200
        assert resp.json()["ok"] is True


@pytest.mark.asyncio
async def test_get_news_items():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/news_item")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_get_news_item_id():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:

        # Создаём новость и news_item
        await ac.post("/news", json={
            "background_image_url": "bg.jpg",
            "title": "Parent2",
            "short_description": "desc"
        })
        parent_id = (await ac.get("/news")).json()[-1]["id"]

        await ac.post("/news_item", json={
            "news_id": parent_id,
            "news_type": "news",
            "image_url": "img.jpg",
            "title": "Item2",
            "short_description": "desc",
            "date": "2025-01-01",
            "link_url": "http://example.com"
        })

        all_items = await ac.get("/news_item")
        item_id = all_items.json()[-1]["id"]

        resp = await ac.get(f"/news_item/{item_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == item_id


@pytest.mark.asyncio
async def test_update_news_item():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:

        # Создаём родительскую новость
        await ac.post("/news", json={
            "background_image_url": "bg.jpg",
            "title": "Parent3",
            "short_description": "desc"
        })
        parent_id = (await ac.get("/news")).json()[-1]["id"]

        # Создаём item
        await ac.post("/news_item", json={
            "news_id": parent_id,
            "news_type": "news",
            "image_url": "img.jpg",
            "title": "Old item",
            "short_description": "old",
            "date": "2025-01-01",
            "link_url": "http://example.com"
        })

        item_id = (await ac.get("/news_item")).json()[-1]["id"]

        # Обновляем
        resp = await ac.put(f"/news_item/{item_id}", json={
            "news_id": parent_id,
            "news_type": "announcement",
            "image_url": "updated.jpg",
            "title": "Updated item",
            "short_description": "updated",
            "date": "2025-01-02",
            "link_url": "http://updated.com"
        })

        assert resp.status_code == 200
        assert resp.json()["ok"] is True

        updated = await ac.get(f"/news_item/{item_id}")
        assert updated.json()["title"] == "Updated item"


@pytest.mark.asyncio
async def test_delete_news_item():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:

        # Создаём новости + item
        await ac.post("/news", json={
            "background_image_url": "bg.jpg",
            "title": "Parent4",
            "short_description": "desc"
        })
        parent_id = (await ac.get("/news")).json()[-1]["id"]

        await ac.post("/news_item", json={
            "news_id": parent_id,
            "news_type": "news",
            "image_url": "img.jpg",
            "title": "Delete This",
            "short_description": "desc",
            "date": "2025-01-01",
            "link_url": "http://example.com"
        })

        item_id = (await ac.get("/news_item")).json()[-1]["id"]

        resp = await ac.delete(f"/news_item/{item_id}")
        assert resp.status_code == 200
        assert resp.json()["ok"] is True

        deleted = await ac.get(f"/news_item/{item_id}")
        assert deleted.json() is None

