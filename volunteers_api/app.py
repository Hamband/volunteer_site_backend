from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from volunteers_api import i18n
from volunteers_api.db.db import engine
from volunteers_api.db.tables import Person, Field, Degree, Contact
from volunteers_api.util.data_models import NewEntryRequestBody

app = FastAPI()


@app.put("/new", status_code=200)
async def new_entry(data: NewEntryRequestBody):
    with Session(engine) as session:
        person = Person(
            first_name=data.first_name,
            last_name=data.last_name,
            current_degree=data.current_degree,
            last_completed_degree=data.last_completed_degree,
            fields=[Field(name=i) for i in data.fields],
            degrees=[Degree(
                type=i.type,
                uni=i.uni,
                start_year=i.start_year,
                end_year=i.end_year,
                major=i.major
            ) for i in data.degrees],
            contacts=[Contact(
                type=i.type,
                address=i.address
            ) for i in data.contacts]
        )
        session.add(person)
        session.commit()
    return {"status": i18n.get("new_ok")}


@app.post("/validate")
async def validate(data: NewEntryRequestBody):
    return {"status": i18n.get("validation_ok")}


@app.get("/get_completions/fields")
async def fields_completion(prefix: str = "", num: int | None = None):
    with Session(engine) as session:
        stmt = select(Field.name).where(Field.name.like(f"{prefix}%")).limit(num)
        return session.scalars(stmt).all()


@app.get("/get_completions/degrees/uni")
async def uni_completion(prefix: str = "", num: int | None = None):
    with Session(engine) as session:
        stmt = select(Degree.uni).where(Degree.uni.like(f"{prefix}%")).limit(num)
        return session.scalars(stmt).all()


@app.get("/get_completions/degrees/major")
async def major_completion(prefix: str = "", num: int | None = None):
    with Session(engine) as session:
        stmt = select(Degree.major).where(Degree.major.like(f"{prefix}%")).limit(num)
        return session.scalars(stmt).all()


@app.get("/get_completions/contacts/type")
async def major_completion(prefix: str = "", num: int | None = None):
    with Session(engine) as session:
        stmt = select(Contact.type).where(Contact.type.like(f"{prefix}%")).limit(num)
        return session.scalars(stmt).all()
