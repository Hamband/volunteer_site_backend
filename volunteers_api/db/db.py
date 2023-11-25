from sqlalchemy import create_engine
from volunteers_api import config
from volunteers_api.db import tables

engine = create_engine(config.db_uri)
tables.Base.metadata.create_all(engine)
