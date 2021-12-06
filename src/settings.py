from pydantic import BaseSettings


# Мои личные данные postgres
DB_LOGIN = 'postgres'
DB_PASSWORD = 'postgres'
DB_SERVER = 'localhost'
DB_PORT = '5432'
DB_NAME = 'dating_app'


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    database_url: str = f'postgresql://{DB_LOGIN}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}'
    jwt_secret: str = 'secret'
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 3600


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
