# Импортируем sessionmaker из файла с настройками БД.
from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import AsyncSessionLocal
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate


# Функция работает с асинхронной сессией,
# поэтому ставим ключевое слово async.
# В функцию передаём схему MeetingRoomCreate.
async def create_meeting_room(
        new_room: MeetingRoomCreate,
        session: AsyncSession,
) -> MeetingRoom:
    # Конвертируем объект MeetingRoomCreate в словарь.
    new_room_data = new_room.dict()

    # Создаём объект модели MeetingRoom.
    # В параметры передаём пары "ключ=значение",
    # для этого распаковываем словарь.
    db_room = MeetingRoom(**new_room_data)
    # Убираем контекстный менеджер.
    session.add(db_room)
    await session.commit()
    await session.refresh(db_room)
    return db_room

    # # Создаём асинхронную сессию через контекстный менеджер.
    # async with AsyncSessionLocal() as session:
    #     # Добавляем созданный объект в сессию.
    #     # Никакие действия с базой пока ещё не выполняются.
    #     session.add(db_room)
    #
    #     # Записываем изменения непосредственно в БД.
    #     # Так как сессия асинхронная, используем ключевое слово await.
    #     await session.commit()
    #
    #     # Обновляем объект db_room: считываем данные из БД,
    #     # чтобы получить его id.
    #     await session.refresh(db_room)
    # # Возвращаем только что созданный объект класса MeetingRoom.
    # return db_room

# Добавляем новую асинхронную функцию.
async def get_room_id_by_name(
        room_name: str,
        # Добавляем новый параметр.
        session: AsyncSession,
) -> Optional[int]:
    # Убираем контекстный менеджер.
    db_room_id = await session.execute(
        select(MeetingRoom.id).where(
            MeetingRoom.name == room_name
        )
    )
    db_room_id = db_room_id.scalars().first()
    return db_room_id
    # async with AsyncSessionLocal() as session:
    #     # Получаем объект класса Result.
    #     db_room_id = await session.execute(
    #         select(MeetingRoom.id).where(
    #             MeetingRoom.name == room_name
    #         )
    #     )
    #     # Извлекаем из него конкретное значение.
    #     db_room_id = db_room_id.scalars().first()
    # return db_room_id

async def read_all_rooms_from_db(
        session: AsyncSession,
) -> List[MeetingRoom]:
    db_room_list = await session.execute(
        select(MeetingRoom)
    )  # Missing closing parenthesis added here

    db_room_list = db_room_list.scalars().all()
    return db_room_list

async def get_meeting_room_by_id(
        room_id: str,
        session: AsyncSession)-> Optional[int]:
    db_room = await session.get(MeetingRoom, room_id)
    return db_room

async def update_meeting_room(
        # Объект из БД для обновления.
        db_room: MeetingRoom,
        # Объект из запроса.
        room_in: MeetingRoomUpdate,
        session: AsyncSession,
) -> MeetingRoom:
    # Представляем объект из БД в виде словаря.
    obj_data = jsonable_encoder(db_room)
    # Конвертируем объект с данными из запроса в словарь,
    # исключаем неустановленные пользователем поля.
    update_data = room_in.dict(exclude_unset=True, exclude_none=True)

    # Перебираем все ключи словаря, сформированного из БД-объекта.
    for field in obj_data:
        # Если конкретное поле есть в словаре с данными из запроса, то...
        if field in update_data:
            # ...устанавливаем объекту БД новое значение атрибута.
            setattr(db_room, field, update_data[field])
    # Добавляем обновленный объект в сессию.
    session.add(db_room)
    # Фиксируем изменения.
    await session.commit()
    # Обновляем объект из БД.
    await session.refresh(db_room)
    return db_room

async def delete_meeting_room(
        db_room: MeetingRoom,
        session: AsyncSession,
) -> MeetingRoom:
    # Удаляем объект из БД.
    await session.delete(db_room)
    # Фиксируем изменения в БД.
    await session.commit()
    # Не обновляем объект через метод refresh(),
    # следовательно он всё ещё содержит информацию об удаляемом объекте.
    return db_room