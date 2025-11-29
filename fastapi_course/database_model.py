from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from fastapi import FastAPI, Depends
from typing import Annotated
from sqlalchemy import select

app = FastAPI()

# engine — это объект движка SQLAlchemy, который управляет соединением с базой данных.
# В данном случае он создаётся асинхронно для работы с SQLite по адресу books.db.
# Движок нужен для выполнения запросов, создания сессий и управления транзакциями в базе данных.
engine = create_async_engine('sqlite+aiosqlite:///books.db')

# new_session: фабрика асинхронных сессий, созданная на основе движка.
# Позволяет создавать новые подключения к базе данных для каждого запроса.
new_session = async_sessionmaker(engine, expire_on_commit=False)


# get_session: асинхронная функция-зависимость, которая создаёт и отдаёт сессию для работы с базой данных.
# Используется для передачи подключения к БД в эндпоинты FastAPI.
async def get_session():
    async with new_session() as session:
        yield session

# SessionDep: аннотация для автоматического внедрения зависимости сессии БД в эндпоинты FastAPI.
# Упрощает передачу сессии в функции.
SessionDep = Annotated[AsyncSession, Depends(get_session)]


# Base: базовый класс для всех моделей SQLAlchemy. Через него описываются таблицы и их поля.
class Base(DeclarativeBase):
    pass

class BookModel(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]

@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True, "message": "Database setup complete."}


class BookCreateSchema(BaseModel):
    title: str
    author: str

class BookSchema(BookCreateSchema):
    id: int

@app.post("/books")
async def create_book(data: BookCreateSchema, session: SessionDep):
    new_book = BookModel(
        title=data.title,
        author=data.author,
    )
    session.add(new_book)
    await session.commit()
    return {"ok": True, "message": "Book created successfully."}


@app.get("/books")
async def read_books(session: SessionDep):
    query = select(BookModel)
    result = await session.execute(query)
    return result.scalars().all()