import uvicorn
from fastapi import FastAPI

from settings import settings

from db.base import database
from main_router import router


app = FastAPI()

# Все пути будут обозначаться тут
app.include_router(router)


# Подключение к БД
@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


# Запуск приложение через этот файл
if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True
    )
