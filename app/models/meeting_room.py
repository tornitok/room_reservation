# app/models/meeting_room.py

# Импортируем из Алхимии нужные классы.
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

# Импортируем базовый класс для моделей.
from app.core.db import Base
from app.schemas.meeting_room import MeetingRoomCreate
from app.models.reservation import Reservation


class MeetingRoom(Base):
    # Имя переговорки должно быть не больше 100 символов,
    # уникальным и непустым.
    name = Column(String(100), unique=True, nullable=False)
    # Новый атрибут модели. Значение nullable по умолчанию равно True,
    # поэтому его можно не указывать.
    description = Column(Text)
    my_meeting_room = MeetingRoomCreate(
        name='Главная переговорка',
        description='Очень большая, модная и помпезная комната.'
    )
    # Установите связь между моделями через функцию relationship.
    reservations = relationship(Reservation, cascade='delete')
