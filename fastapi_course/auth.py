from fastapi import FastAPI, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig
from pydantic import BaseModel

app = FastAPI()

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

class UserLoginSchema(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(creds: UserLoginSchema, response: Response):
    if creds.username == 'test' and creds.password == 'test':
        token = security.create_access_token(uid='12345')
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")




@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected():
    return {"data": "SECRET DATA"}


# from fastapi import FastAPI, HTTPException, Response, Depends, status
# from pydantic import BaseModel
# from passlib.context import CryptContext  # для безопасного хэширования паролей
# from datetime import timedelta, datetime
# from authx import AuthX, AuthXConfig
# from typing import Optional
#
# # Инициализация FastAPI
# app = FastAPI()
#
# # Конфигурация для JWT
# config = AuthXConfig()
# config.JWT_SECRET_KEY = "SECRET_KEY"  # В продакшн-решениях используйте секреты из переменных окружения
# config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
# config.JWT_TOKEN_LOCATION = ["cookies"]
#
# # Инициализация AuthX с конфигурацией
# security = AuthX(config=config)
#
# # Контекст для хэширования паролей
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
#
# # Схема для входа
# class UserLoginSchema(BaseModel):
#     username: str
#     password: str
#
#
# # Пользовательская база данных для хранения хэшированных паролей
# # В реальной жизни вы бы использовали настоящую базу данных
# fake_users_db = {
#     "test": {
#         "username": "test",
#         "hashed_password": pwd_context.hash("test")  # Хэшируем пароль
#     }
# }
#
#
# # Функция для проверки пароля
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# # Функция для создания нового токена с истечением через 15 минут
# def create_access_token(uid: str, expires_delta: timedelta = timedelta(minutes=15)) -> str:
#     to_encode = {"sub": uid}
#     expire = datetime.utcnow() + expires_delta
#     to_encode.update({"exp": expire})
#     return security.create_access_token(**to_encode)
#
#
# # Роут для логина
# @app.post("/login")
# def login(creds: UserLoginSchema, response: Response):
#     # Проверка существования пользователя и правильности пароля
#     user = fake_users_db.get(creds.username)
#     if not user or not verify_password(creds.password, user['hashed_password']):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
#
#     # Генерация токена
#     token = create_access_token(uid=creds.username)
#
#     # Установка cookie с токеном
#     response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
#     return {"access_token": token}
#
#
# # Роут для получения защищенных данных
# @app.get("/protected")
# def protected(token: str = Depends(security.access_token_required)):
#     return {"data": "SECRET DATA"}
#
#
# # Роут для выхода из системы (удаляет токен из cookie)
# @app.post("/logout")
# def logout(response: Response):
#     response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
#     return {"msg": "Successfully logged out"}
#
#
# # Роут для обновления токена (используется refresh_token)
# @app.post("/refresh")
# def refresh_token(token: str = Depends(security.access_token_required)):
#     try:
#         # Попытка обновить токен, если он еще действителен
#         new_token = create_access_token(uid=token["sub"])
#         return {"access_token": new_token}
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
