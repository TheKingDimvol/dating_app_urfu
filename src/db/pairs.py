from sqlalchemy import Table, Column, Integer, Date, Boolean, ForeignKey
import datetime

from .base import metadata

pairs = Table(
    "pairs",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True, index=True),
    Column("first_user", Integer, ForeignKey('users.id'), index=True),
    Column("second_user", Integer, ForeignKey('users.id'), index=True),
    Column("like", Boolean, nullable=True),
    Column("determined_date", Date, default=datetime.date.today())
)
