from sqlalchemy import Table, Column, Integer, DateTime, Boolean, ForeignKey, Text
import datetime

from .base import metadata

users = Table(
    "messages",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True, index=True),
    Column("author", Integer, ForeignKey('users.id')),
    Column("pair", Integer, ForeignKey('pairs.id'), index=True),
    Column("text", Text, nullable=False),
    Column("send_time", DateTime, default=datetime.datetime.utcnow()),
    Column("is_read", Boolean, nullable=False, default=False)
)
