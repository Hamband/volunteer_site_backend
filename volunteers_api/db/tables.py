from typing import List, Optional
from enum import Enum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class DegreeType(Enum):
    BACHELOR = 1
    MASTER = 2
    PHD = 3
    POSTDOC = 4
    PROF = 5


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True)
    degrees: Mapped[List["Degree"]] = relationship(cascade="all, delete-orphan")
    first_name: Mapped[str]
    last_name: Mapped[str]
    contacts: Mapped[List["Contact"]] = relationship(cascade="all, delete-orphan")
    fields: Mapped[List["str"]]
    last_completed_degree: Mapped[Optional[DegreeType]]
    current_degree: Mapped[Optional[DegreeType]]


class Degree(Base):
    __tablename__ = "degrees"

    id: Mapped[int] = mapped_column(primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    type: Mapped[DegreeType]
    uni: Mapped[str]
    start_year: Mapped[int]
    end_year: Mapped[int]
    major: Mapped[str]


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]
    address: Mapped[str]
