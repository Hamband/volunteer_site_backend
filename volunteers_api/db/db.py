from sqlalchemy import create_engine
from .. import config
import tables

engine = create_engine(config.db_uri)
tables.Base.metadata.create_all(engine)