from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "1984",
        "author": "George Orwell"
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee"
    }
]

@app.get("/books",tags=["Books"],summary="Получить список всех книг")
def get_books():
    return books

@app.get("/books/{book_id}", tags=["Books"], summary="Получить книгу по ID")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


class NewBook(BaseModel):
    title: str
    author: str

@app.post("/books", tags=["Books"], summary="Добавить новую книгу")
def create_book(new_book: NewBook):
    books.append({
        "id": len(books) + 1,
        "title": new_book.title,
        "author": new_book.author,
    })
    return {"success": True, "message": "Book added successfully"}

@app.get("/", summary="Главная ручка", tags=["Основные ручки"])
def root():
    return "Hello, World!"

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)