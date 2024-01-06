from typing import List, Optional
from sqlalchemy import ForeignKey, DateTime, func, String
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from volunteers_api.util.enums import DegreeType


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True)
    degrees: Mapped[List["Degree"]] = relationship(cascade="all, delete-orphan")
    first_name: Mapped[str] = mapped_column(String(128))
    last_name: Mapped[str] = mapped_column(String(128))
    contacts: Mapped[List["Contact"]] = relationship(cascade="all, delete-orphan")
    fields: Mapped[List["Field"]] = relationship(cascade="all, delete-orphan")
    last_completed_degree: Mapped[Optional[DegreeType]]
    current_degree: Mapped[Optional[DegreeType]]
    submission_time: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())


class Degree(Base):
    __tablename__ = "degrees"

    id: Mapped[int] = mapped_column(primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    type: Mapped[DegreeType]
    uni: Mapped[str] = mapped_column(String(128))
    start_year: Mapped[int]
    end_year: Mapped[int]
    major: Mapped[str] = mapped_column(String(128))


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    type: Mapped[str] = mapped_column(String(128))
    address: Mapped[str] = mapped_column(String(256))


class Field(Base):
    __tablename__ = "fields"

    id: Mapped[int] = mapped_column(primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    name: Mapped[str] = mapped_column(String(128))


class Admin(Base):
    __tablename__ = "admins"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(128))
    password_hash: Mapped[str] = mapped_column(String(128))