from sqlalchemy import Table, Column, Integer, String, Date, DateTime
import datetime

from .base import metadata

users = Table(
    "users", 
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True, index=True),
    Column("name", String),
    Column("phone", String, unique=True),
    Column("password", String, nullable=False),
    Column("date_of_birth", Date),
    Column("age", Integer),
    Column("description", String),
    Column("city", Integer),  # БД, или таблица, или апи городов
    Column("zodiac_sign", Integer, index=True),
    Column("number", Integer, index=True),
    Column("socionic_type", Integer, index=True),
    Column("sixteen_pers_type", Integer, index=True),
    Column("created_at", DateTime, default=datetime.datetime.utcnow)
)