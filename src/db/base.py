import os

from dotenv import load_dotenv

from databases import Database
from sqlalchemy import create_engine, MetaData

from src.settings import settings


load_dotenv()
DB_URL = os.environ.get('DATABASE_URL', settings.database_url)

database = Database(DB_URL)

metadata = MetaData()

engine = create_engine(
    DB_URL,
    echo=True
)
