from databases import Database
from sqlalchemy import create_engine, MetaData


# Мои личные данные postgres
DB_LOGIN = 'postgres'
DB_PASSWORD = 'postgres'
DB_SERVER = 'localhost'
DB_PORT = '5432'
DB_NAME = 'dating_app'

DB_URL = f'postgresql://{DB_LOGIN}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}'


database = Database(DB_URL)

metadata = MetaData()

engine = create_engine(
    DB_URL,
    echo=True
)
