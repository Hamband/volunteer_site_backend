from sqlalchemy import create_engine
from .. import config
from . import tables

engine = create_engine(config.db_uri)
tables.Base.metadata.create_all(engine)
