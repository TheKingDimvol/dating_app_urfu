from sqlalchemy import Table, Column, Integer, String, Date, DateTime
import datetime

from .base import metadata

pairs = Table(
    "pair", 
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True, index=True)
)