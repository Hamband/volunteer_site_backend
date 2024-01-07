from fastapi import FastAPI, Security, HTTPException, Depends
from fastapi.openapi.models import APIKey
from fastapi.security import APIKeyQuery
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from volunteers_api import i18n, config
from volunteers_api.db.db import engine
from volunteers_api.db.tables import Person, Field, Degree, Contact
from volunteers_api.util.data_models import NewEntryRequestBody

path_prefix = config.path_prefix

app = FastAPI(
    openapi_url=(f"{path_prefix}/openapi.json" if config.show_docs else None),
    docs_url=f"{path_prefix}/docs",
    redoc_url=f"{path_prefix}/redoc",
    title=config.api_title,
    summary=config.api_summary,
    description=config.api_description,
    version=config.version,
)

app.add_middleware(GZipMiddleware)
if config.no_http:
    app.add_middleware(HTTPSRedirectMiddleware)

api_key_query = APIKeyQuery(name="api_key", auto_error=False)


async def get_api_key(api_key_query: str = Security(api_key_query)):
    if api_key_query in config.api_keys:
        return api_key_query
    raise HTTPException(
        status_code=403,
        detail=i18n.get("api_key_invalid")
    )


@app.put(f"{path_prefix}/new", status_code=200)
async def new_entry(data: NewEntryRequestBody, api_key: APIKey = Depends(get_api_key)):
    """
    Submit a new entry in the database. The request body must conform to the schema. The fields are described below:

    - **first_name**: first name of the person. must have len > 0 or you will get error first_name_invalid.
    - **last_name**: last name of the person. must have len > 0 or you will get error last_name_invalid.
    - **last_completed_degree**: last completed educational degree of the person. should default to diploma. optional.
    - **current_degree**: current degree of the person. optional.
    - **fields**: list of mathematics and computer science fields the person works in / is interested in. can be empty.
    - **degrees**: list of `degree` objects. can be empty.
    - **contacts**: list of `contact` objects. can not be empty or you will get error contacts_empty. also must have at least an entry with `type == "email"` or you will get error contacts_no_email.
    - **misc**: any other info. optional. length must be less than 1024.

    Fields of `degree` object:

    - **type**: degree type (bachelor's, etc.).
    - **uni**: university name. must have len > 0 or you will get error uni_invalid.
    - **major**: major name. must have len > 0 or you will get error major_invalid.
    - **start_year**: start year of degree. must be present and > 1300 or you will get error start_year_invalid.
    - **end_year**: end year (or expected end year) of degree. must be present and > start_year or you will get error end_year_invalid.

    Fields of `contact` object:

    - **type**: contact type. can be anything (e.g. email, telegram, phone). must have len > 0 or you will get error invalid_contact_type.
    - **address**: contact address (e.g. email address, telegram handle, phone number). must have len > 0 or you will get error invalid_contact_address.

    **All fields should be present. Optional fields that are to be omitted should have a value of `null`.**

    Upon success, `{"status": "new_ok"}` will be returned.
    """
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
            ) for i in data.contacts],
            misc=data.misc
        )
        session.add(person)
        session.commit()
    return {"status": i18n.get("new_ok")}


@app.post(f"{path_prefix}/validate")
async def validate(data: NewEntryRequestBody, api_key: APIKey = Depends(get_api_key)):
    """
    Validate data. Note that the response isn't the full errors, only one of them.
    The data format is the same as for new.

    Upon success, `{"status": "validation_ok"}` will be returned.
    """
    return {"status": i18n.get("validation_ok")}


@app.get(f"{path_prefix}/get_completions/fields")
async def fields_completion(prefix: str = "", num: int | None = None, api_key: APIKey = Depends(get_api_key)):
    """
    Get list of entries currently submitted as a field.

    - **prefix**: only get entries beginning with prefix. can be absent, in which case all entries will be returned.
    - **num**: limit returned data to num entries. should be used to avoid the whole list being returned. a good value is 10.
    """
    with Session(engine) as session:
        stmt = select(Field.name).where(Field.name.like(f"{prefix}%")).distinct().limit(num)
        r = session.scalars(stmt).all()
        if len(r) > 0:
            return r
    if prefix == "":
        return config.completion_defaults["fields"]
    return []


@app.get(f"{path_prefix}/get_completions/degrees/uni")
async def uni_completion(prefix: str = "", num: int | None = None, api_key: APIKey = Depends(get_api_key)):
    """
    Get list of entries currently submitted as a university.

    - **prefix**: only get entries beginning with prefix. can be absent, in which case all entries will be returned.
    - **num**: limit returned data to num entries. should be used to avoid the whole list being returned. a good value is 10.
    """
    with Session(engine) as session:
        stmt = select(Degree.uni).where(Degree.uni.like(f"{prefix}%")).distinct().limit(num)
        r = session.scalars(stmt).all()
        if len(r) > 0:
            return r
    if prefix == "":
        return config.completion_defaults["degrees/uni"]
    return []


@app.get(f"{path_prefix}/get_completions/degrees/major")
async def major_completion(prefix: str = "", num: int | None = None, api_key: APIKey = Depends(get_api_key)):
    """
    Get list of entries currently submitted as a major.

    - **prefix**: only get entries beginning with prefix. can be absent, in which case all entries will be returned.
    - **num**: limit returned data to num entries. should be used to avoid the whole list being returned. a good value is 10.
    """
    with Session(engine) as session:
        stmt = select(Degree.major).where(Degree.major.like(f"{prefix}%")).distinct().limit(num)
        r = session.scalars(stmt).all()
        if len(r) > 0:
            return r
    if prefix == "":
        return config.completion_defaults["degrees/major"]
    return []


@app.get(f"{path_prefix}/get_completions/contacts/type")
async def contact_type_completion(prefix: str = "", num: int | None = None, api_key: APIKey = Depends(get_api_key)):
    """
    Get list of entries currently submitted as a contact type.

    - **prefix**: only get entries beginning with prefix. can be absent, in which case all entries will be returned.
    - **num**: limit returned data to num entries. should be used to avoid the whole list being returned. a good value is 10.
    """
    with Session(engine) as session:
        stmt = select(Contact.type).where(Contact.type.like(f"{prefix}%")).distinct().limit(num)
        r = session.scalars(stmt).all()
        if len(r) > 0:
            return r
    if prefix == "":
        return config.completion_defaults["contacts/type"]
    return []
