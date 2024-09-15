from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, ForeignKey, Integer

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_reservation_user_id_user')
    )