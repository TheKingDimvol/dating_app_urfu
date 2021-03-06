from sqlalchemy import Table, Column, Integer, String, Date

from .base import metadata

users = Table(
    "users", 
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True, index=True),
    Column("name", String),
    Column("phone", String, unique=True),
    Column("password", String, nullable=False),
    Column("img", String),
    Column("date_of_birth", Date),
    Column("age", Integer),
    Column("description", String),
    Column("city", Integer),  # БД, или таблица, или апи городов
    Column("zodiac_sign", Integer, index=True),
    Column("number", Integer, index=True),
    Column("socionic_type", Integer, index=True),
    Column("sixteen_pers_type", Integer, index=True)
)

UPDATE_COLUMNS = [
    "name",
    "password",
    "img",
    "date_of_birth",
    "age",
    "description",
    "city",
    "zodiac_sign",
    "number",
    "socionic_type",
    "sixteen_pers_type"
]
