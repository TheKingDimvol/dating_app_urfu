import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.settings import settings

from src.db.base import database
from src.main_router import router


app = FastAPI()

# Разрешить запросы из всех источников
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Все пути будут обозначаться тут
app.include_router(router)


# Подключение к БД
@app.on_event('startup')
async def startup():
    try:
        await database.connect()
    except Exception as e:
        print(str(e))


@app.on_event('shutdown')
async def shutdown():
    try:
        await database.disconnect()
    except Exception as e:
        print(str(e))


# Запуск приложение через этот файл
if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True
    )
