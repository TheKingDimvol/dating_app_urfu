from typing import List

from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from fastapi.responses import HTMLResponse

from src.controllers.auth import AuthController
from src.controllers.dialogs import DialogController
from src.controllers.pairs import PairController
from src.schemas.pairs import MsgCreate

router = APIRouter(prefix='/ws')

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <input type="number" id="addressee" autocomplete="off"/>
        <a>Partner's id</a>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(JSON.parse(event.data).message)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                var addressee = document.getElementById("addressee")
                ws.send(JSON.stringify({'message': input.value, 'addressee': addressee.value}))
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        # При первом подключении будет приходить массив Диалогов пользователя
        user_dialogs = await DialogController.get_user_dialogs({'id': client_id})
        await websocket.send_json({'dialogs': user_dialogs})

    def disconnect(self, client_id: int):
        del self.active_connections[client_id]

    async def send_personal_message(self, websocket: WebSocket, message: str, addressee: int, author: int):
        created_msg = await DialogController.create_msg(
            MsgCreate(text=message, pair=addressee, author=author)
        )
        # Надо ли отправлять его себе? Целиком или только ИД?
        await websocket.send_json({
            'id': created_msg,
            'message': message,
            'author': author,
            'is_read': True
        })
        addressee_is_online = self.active_connections.get(addressee)
        if addressee_is_online:
            await addressee_is_online.send_json({
                'id': created_msg,
                'message': message,
                'author': author,
                'is_read': False
            })

    async def send_partner_read_msgs(self, pair: int, sender: int, reader: int):
        addressee_is_online = self.active_connections.get(sender)
        if addressee_is_online:
            await addressee_is_online.send_json({'dialog': pair, 'reader': reader})

    async def sympathy_alert(self, liked_user: int, client_id: int, pair: int):
        # TODO додумать и доделать
        liked_online = self.active_connections.get(liked_user)
        if liked_online:
            await liked_online.send_json({'liked': True, 'dialog': pair})
        await self.active_connections[client_id].send_json({'liked': True, 'dialog': pair})

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_json({'message': message, 'author': 'server'})


manager = ConnectionManager()


@router.get("/client")
async def get():
    return HTMLResponse(html)


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    # try:
    #     a = AuthController.validate_token('fdsfdsfds')
    # except:
    #     return 'No'
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            # Что должно приходить
            # data = {
            #     'message', 'dialog', 'addressee', 'like'
            # }
            if 'addressee' not in data:
                # TODO не знаю что делать пока если нет обязательных полей
                pass
            elif 'like' in data:
                pair = await PairController.like_user(int(data['addressee']), client_id, bool(data['like']))
                if pair['like']:
                    await manager.sympathy_alert(int(data['addressee']), client_id, pair['id'])
            elif 'message' not in data or not data['message']:
                # Если нет сообщения - значит читаем пришедшие
                # обновляем БД
                await DialogController.messages_read(int(data['dialog']), int(data['addressee']))
                # отправляем пользователю о прочтении его сообщений
                await manager.send_partner_read_msgs(int(data['dialog']), int(data['addressee']), client_id)
            else:
                # отправляем пользователю новое сообщение от текущего пользователя
                await manager.send_personal_message(websocket, data['message'], int(data['dialog_id']), client_id)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast(f"Client #{client_id} left the chat")
