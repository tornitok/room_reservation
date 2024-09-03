# Импортируем sessionmaker из файла с настройками БД.
from app.core.db import AsyncSessionLocal
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate


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