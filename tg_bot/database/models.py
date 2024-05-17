from sqlalchemy import Date, DateTime, String, Text, Boolean, func, Column, BigInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(30), nullable=True)


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    user: Mapped[str] = mapped_column(ForeignKey('users.tg_id', ondelete='CASCADE'))

    users: Mapped['User'] = relationship(backref='groups')


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    is_done = Column(Boolean)
    group: Mapped[str] = mapped_column(ForeignKey('groups.id', ondelete='CASCADE'))

    groups: Mapped['Group'] = relationship(backref='task')