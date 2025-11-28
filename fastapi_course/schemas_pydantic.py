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