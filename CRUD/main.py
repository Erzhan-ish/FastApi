from fastapi import FastAPI
from .db import Base, engine
from .API import router  # импортируем router, НЕ app

app = FastAPI()

@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True, "message": "Database setup complete."}

# Подключаем все маршруты из api.py
app.include_router(router)

