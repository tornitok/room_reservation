# # Импортируем класс Depends.
# from fastapi import APIRouter, Depends, HTTPException
# # Импортируем класс асинхронной сессии для аннотации параметра.
# from sqlalchemy.ext.asyncio import AsyncSession
#
# # Импортируем асинхронный генератор сессий.
# from app.core.db import get_async_session
# from app.crud.meeting_room import (create_meeting_room, get_room_id_by_name,
#                                    read_all_rooms_from_db, update_meeting_room, get_meeting_room_by_id, delete_meeting_room)
# from app.models.meeting_room import MeetingRoom
# from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomDB, MeetingRoomUpdate
#
# router = APIRouter(prefix='/meeting_rooms', tags=['Meeting Rooms'])
#
# @router.get(
#     '/',
#     response_model=list[MeetingRoomDB],
#     response_model_exclude_none=True,
# )
# async def get_all_meeting_rooms(session: AsyncSession = Depends(get_async_session)):
#     room_list = await read_all_rooms_from_db(session)
#     if room_list is None:
#         raise HTTPException(
#             status_code=204,
#             detail='Список пуст'
#     )
#     return room_list
#
#
# @router.post(
#     '/',
#     response_model=MeetingRoomDB,
#     response_model_exclude_none=True,
# )
# async def create_new_meeting_room(
#         meeting_room: MeetingRoomCreate,
#         # Указываем зависимость, предоставляющую объект сессии, как параметр функции.
#         session: AsyncSession = Depends(get_async_session),
# ):
#     # Вторым параметром передаём сессию в CRUD-функцию:
#     room_id = await get_room_id_by_name(meeting_room.name, session)
#     if room_id is not None:
#         raise HTTPException(
#             status_code=422,
#             detail='Переговорка с таким именем уже существует!',
#         )
#     # Вторым параметром передаём сессию в CRUD-функцию:
#     new_room = await create_meeting_room(meeting_room, session)
#     return new_room
#
#
# @router.patch(
#     '/{meeting_room_id}',
#     response_model=MeetingRoomDB,
#     response_model_exclude_none=True,
# )
# async def partially_update_meeting_room(
#         meeting_room_id: int,
#         obj_in: MeetingRoomUpdate,
#         session: AsyncSession = Depends(get_async_session),
# ):
#     # Выносим повторяющийся код в отдельную корутину.
#     meeting_room = await check_meeting_room_exists(
#         meeting_room_id, session
#     )
#
#     if obj_in.name is not None:
#         await check_name_duplicate(obj_in.name, session)
#
#     meeting_room = await update_meeting_room(
#         meeting_room, obj_in, session
#     )
#     return meeting_room
#
# # @router.patch(
# #     # ID обновляемого объекта будет передаваться path-параметром.
# #     '/{meeting_room_id}',
# #     response_model=MeetingRoomDB,
# #     response_model_exclude_none=True,
# # )
# # async def partially_update_meeting_room(
# #         # ID обновляемого объекта.
# #         meeting_room_id: int,
# #         # JSON-данные, отправленные пользователем.
# #         obj_in: MeetingRoomUpdate,
# #         session: AsyncSession = Depends(get_async_session),
# # ):
# #     # Получаем объект из БД по ID.
# #     # В ответ ожидается либо None, либо объект класса MeetingRoom.
# #     meeting_room = await get_meeting_room_by_id(
# #         meeting_room_id, session
# #     )
# #
# #     if meeting_room is None:
# #         raise HTTPException(
# #             # Для отсутствующего объекта вернем статус 404 — Not found.
# #             status_code=404,
# #             detail='Переговорка не найдена!'
# #         )
# #
# #     if obj_in.name is not None:
# #         # Если в запросе получено поле name — проверяем его на уникальность.
# #         await check_name_duplicate(obj_in.name, session)
# #
# #     # Передаём в корутину все необходимые для обновления данные.
# #     meeting_room = await update_meeting_room(
# #         meeting_room, obj_in, session
# #     )
# #     return meeting_room
# #
# #
# # Корутина, проверяющая уникальность полученного имени переговорки.
# async def check_name_duplicate(
#         room_name: str,
#         session: AsyncSession,
# ) -> None:
#     room_id = await get_room_id_by_name(room_name, session)
#     if room_id is not None:
#         raise HTTPException(
#             status_code=422,
#             detail='Переговорка с таким именем уже существует!',
#         )
#
#
# @router.delete(
#     '/{meeting_room_id}',
#     response_model=MeetingRoomDB,
#     response_model_exclude_none=True,
# )
# async def remove_meeting_room(
#         meeting_room_id: int,
#         session: AsyncSession = Depends(get_async_session),
# ):
#     # Выносим повторяющийся код в отдельную корутину.
#     meeting_room = await check_meeting_room_exists(
#         meeting_room_id, session
#     )
#     meeting_room = await delete_meeting_room(
#         meeting_room, session
#     )
#     return meeting_room
#
#
# # Оформляем повторяющийся код в виде отдельной корутины.
# async def check_meeting_room_exists(
#         meeting_room_id: int,
#         session: AsyncSession,
# ) -> MeetingRoom:
#     meeting_room = await get_meeting_room_by_id(
#         meeting_room_id, session
#     )
#     if meeting_room is None:
#         raise HTTPException(
#             status_code=404,
#             detail='Переговорка не найдена!'
#         )
#     return meeting_room

# app/api/meeting_room.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.validators import (check_meeting_room_exists,
                                          check_name_duplicate)
from app.core.db import get_async_session
# Вместо импортов 6 функций импортируйте объект meeting_room_crud.
from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
from app.schemas.meeting_room import (MeetingRoomCreate, MeetingRoomDB,
                                      MeetingRoomUpdate)
from app.schemas.reservation import ReservationDB

router = APIRouter()


@router.post(
    '/',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def create_new_meeting_room(
        meeting_room: MeetingRoomCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(meeting_room.name, session)
    # Замените вызов функции на вызов метода.
    new_room = await meeting_room_crud.create(meeting_room, session)
    return new_room


@router.get(
    '/',
    response_model=list[MeetingRoomDB],
    response_model_exclude_none=True,
)
async def get_all_meeting_rooms(
        session: AsyncSession = Depends(get_async_session),
):
    # Замените вызов функции на вызов метода.
    all_rooms = await meeting_room_crud.get_multi(session)
    return all_rooms


@router.get(
    '/{meeting_room_id}/reservations',
    response_model=list[ReservationDB],
)
async def get_reservations_for_room(
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    await check_meeting_room_exists(meeting_room_id, session)
    reservations = await reservation_crud.get_future_reservations_for_room(
        room_id=meeting_room_id,session=session
    )
    return reservations


@router.patch(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def partially_update_meeting_room(
        meeting_room_id: int,
        obj_in: MeetingRoomUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    # Замените вызов функции на вызов метода.
    meeting_room = await meeting_room_crud.update(
        meeting_room, obj_in, session
    )
    return meeting_room


@router.delete(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def remove_meeting_room(
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    meeting_room = await check_meeting_room_exists(meeting_room_id, session)
    # Замените вызов функции на вызов метода.
    meeting_room = await meeting_room_crud.remove(meeting_room, session)
    return meeting_room
