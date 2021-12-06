"""
Инициализация БД.
Таблицы надо импортировать.
"""

from .users import users
from .base import metadata, engine


def create_tables():
    """Метод создаст таблицы в БД"""
    metadata.create_all(bind=engine)
