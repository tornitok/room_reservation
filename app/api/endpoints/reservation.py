from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.validators import (check_meeting_room_exists,
                                          check_reservation_before_edit,
                                          check_reservation_intersections)
from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.reservation import reservation_crud
from app.models import User
from app.schemas.reservation import (ReservationCreate, ReservationDB,
                                     ReservationUpdate)


router = APIRouter()


@router.post('/', response_model=ReservationDB)
async def create_reservation(
        reservation: ReservationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    await check_meeting_room_exists(
        reservation.meetingroom_id, session
    )
    await check_reservation_intersections(
        # Так как валидатор принимает **kwargs,
        # аргументы должны быть переданы с указанием ключей.
        **reservation.dict(), session=session
    )
    new_reservation = await reservation_crud.create(
        # Передаём объект пользователя в метод создания объекта бронирования.
        reservation, session, user
    )
    return new_reservation


@router.get('/', response_model=list[ReservationDB], dependencies=[Depends(current_superuser)])
async def get_all_reservations(
        session: AsyncSession = Depends(get_async_session),
):
    reservations = await reservation_crud.get_multi(session)
    return reservations


@router.delete('/{reservation_id}', response_model=ReservationDB)
async def delete_reservation(
        reservation_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    reservation = await check_reservation_before_edit(
        reservation_id, session, user
    )
    reservation = await reservation_crud.remove(
        reservation, session
    )
    return reservation


@router.patch('/{reservation_id}', response_model=ReservationDB, dependencies=[Depends(current_superuser)])
async def update_reservation(
        reservation_id: int,
        obj_in: ReservationUpdate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    # Проверяем, что такой объект бронирования вообще существует.
    reservation = await check_reservation_before_edit(
        reservation_id, session, user
    )
    # Проверяем, что нет пересечений с другими бронированиями.
    await check_reservation_intersections(
        # Новое время бронирования, распакованное на ключевые аргументы.
        **obj_in.dict(),
        # id обновляемого объекта бронирования,
        reservation_id=reservation_id,
        # id переговорки.
        meetingroom_id=reservation.meetingroom_id,
        session=session
    )
    reservation = await reservation_crud.update(
        db_obj=reservation,
        # На обновление передаем объект класса ReservationUpdate, как и требуется.
        obj_in=obj_in,
        session=session,
    )
    return reservation

# Новый эндпоинт.
@router.get(
    '/my_reservations', response_model=list[ReservationDB],response_model_exclude={'user_id'}
)
async def get_my_reservations(
        session: AsyncSession = Depends(get_async_session),
        # В этой зависимости получаем обычного пользователя, а не суперюзера.
        user: User = Depends(current_user)
):
    # Сразу можно добавить докстринг для большей информативности.
    """Получает список всех бронирований для текущего пользователя."""
    # Вызываем созданный метод.
    reservations = await reservation_crud.get_by_user(
        session=session, user=user
    )
    return reservations