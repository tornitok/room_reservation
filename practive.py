# from fastapi import FastAPI
# from pydantic import BaseModel
# from sqlalchemy.orm import declarative_base, declared_attr
# from sqlalchemy import Column, String, Text, Integer
#
# app = FastAPI()
#
# class PreBase:
#     # Во все таблицы будет добавлено поле ID.
#     id = Column(Integer, primary_key=True)
#
# Base = declarative_base(cls=PreBase)
#
# class SecretMessage(BaseModel):
#     # Pydantic-схема для зашифрованных сообщений.
#     # Все поля - обязательные.
#     title: str
#     message: str
#
# class ReadyNews(Base):
#     # Модель SQLAlchemy для хранения данных в БД.
#     __tablename__ = 'news'  # Указываем имя таблицы
#
#     id = Column(Integer, primary_key=True)
#     title = Column(String(100), unique=True, nullable=False)
#     message = Column(String)
#
# def decoder(data: dict[str, str]) -> dict[str, str]:
#     """
#     Сверхсекретный декодер.
#
#     Здесь всё работает, ничего менять не надо!
#     """
#     decoded_data = {}
#     for key, value in data.items():
#         decoded_str = (chr(int(chunk)) for chunk in value.split('-'))
#         decoded_data[key] = ''.join(decoded_str)
#     return decoded_data
#
# @app.post('/super-secret-base')
# def reciever(encoded_news: SecretMessage):
#     # Передаем сообщение в декодер.
#     decoded_data = decoder(encoded_news.dict())

# from fastapi import FastAPI, HTTPException
#
# app = FastAPI()
#
# COMMAND_TO_BOIL = 'Вскипятить воду'
#
#
# def boil_water():
#     pass
#
#
# @app.post('/samovar_xxi')
# def samovar_processing(command: str) -> str:
#     if command == COMMAND_TO_BOIL:
#         boil_water()
#         return 'Вода вскипела!'
#     else:
#         raise HTTPException(
#             status_code=418,  # HTTP статус-код "Я — чайник"
#             detail=f'Чайник не может выполнить команду: {command}'
#         )



# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import Optional
#
# app = FastAPI()
#
#
# class IncomingMessage(BaseModel):
#     # Модифицируйте атрибуты, чтобы они соответствовали заданию.
#     title: Optional[str] = 'У этого сообщения нет заголовка'
#     body: str
#     contacts: Optional[str]
#     secret_hash: str
#
#     def to_outgoing(self):
#         # Если заголовка нет или он равен значению по умолчанию, не включаем его в исходящее сообщение
#         data = self.dict(exclude={'secret_hash'})
#         if data.get('title') == 'У этого сообщения нет заголовка':
#             del data['title']
#         return data
#
#
# class OutgoingMessage(BaseModel):
#     # Опишите класс исходящего сообщения.
#     title: Optional[str]
#     body: str
#     contacts: Optional[str]
#
#     class Config:
#         orm_mode = True
#
#
#     # Модифицируйте эндпоинт так,
# # чтобы он выполнял поставленную задачу.
# @app.post('/post-office', response_model_exclude_none=True, response_model=OutgoingMessage)
# def sloth(message: IncomingMessage):
#     response_data = message.to_outgoing()
#     return response_data

from fastapi import FastAPI, Depends

app = FastAPI()


def limit_offset(limit: int = 100, offset: int = 0):
    return {'limit': limit, 'offset': offset}


@app.get('/squares')
def get_squares(
        paginator_params: dict = Depends(limit_offset) # Подключите параметры limit и offset.
):
    """Возвращает квадраты чисел."""
    # Не меняйте следующую строчку.
    dataset = [x**2 for x in range(300)]

    limit = paginator_params['limit']  # Напишите свой код здесь.
    offset = paginator_params['offset']

    dataset = dataset[offset:offset + limit]

    return dataset


@app.get('/unicode-symbols')
def get_unicode_symbols(
        paginator_params: dict = Depends(limit_offset)  # Подключите параметры limit и offset.
):
    """Возвращает символы юникода."""
    # Не меняйте следующие две строчки.
    dataset = [chr(x) for x in range(300)]
    dataset = ''.join(dataset)

    limit = paginator_params['limit']  # Напишите свой код здесь.
    offset = paginator_params['offset']

    dataset = dataset[offset:offset + limit]

    return dataset