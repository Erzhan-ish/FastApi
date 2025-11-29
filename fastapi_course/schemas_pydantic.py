from pydantic import BaseModel, Field, EmailStr, ConfigDict
from fastapi import FastAPI

app = FastAPI()

data = {
    "email": "asd@mail.com",
    "bio": None,
    "age": 12,
}

data_wo_age = {
    "email": "asd@mail.com",
    "bio": None,
    "gender": "male",
    "birthday": "2000-01-01",
}


class UserSchema(BaseModel):
    email: EmailStr
    bio: str | None = Field(max_length=1000)  # биография максимум 1000 символов

    model_config = ConfigDict(extra='forbid')  # запрет дополнительных полей

# default — значение по умолчанию
# title — заголовок поля
# description — описание поля
# example — пример значения
# max_length — максимальная длина строки
# min_length — минимальная длина строки
# ge — минимальное значение (greater or equal)
# le — максимальное значение (less or equal)
# gt — строго больше (greater than)
# lt — строго меньше (less than)
# min_items — минимальное количество элементов в списке
# max_items — максимальное количество элементов в списке
# regex — регулярное выражение для проверки строки
# alias — альтернативное имя поля
# deprecated — пометка, что поле устарело
# const — значение должно быть константой


users = []

@app.post("/users")
def add_user(user: UserSchema):
    users.append(user)
    return {"ok": True, "message": "User added successfully"}


@app.get("/users")
def get_users() -> list[UserSchema]:
    return users



class UserAgeSchema(UserSchema):
    age: int = Field(ge=0, le=130) # возраст от 0 до 120


# user_wo_age = UserSchema(**data_wo_age)
# user = UserAgeSchema(**data)
# print(repr(user))
# print(repr(user_wo_age))