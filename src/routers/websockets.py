from typing import List

from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from fastapi.responses import HTMLResponse

from src.controllers.auth import AuthController
from src.controllers.dialogs import DialogController
from src.controllers.pairs import PairController
from src.controllers.users import UserController
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
        <form action="" onsubmit="login(event)">
            <a>Phone: </a> 
            <input type="text" id="phone" autocomplete="off"/>
            <a>Password: </a> 
            <input type="text" id="password" autocomplete="off"/>
            <button>Authenticate</button>
        </form>
        <form action="" onsubmit="connect(event)">
            <a>Token: </a> 
            <input type="text" id="token" autocomplete="off"/>
            <button>Connect via WebSocket</button>
        </form>
        <a>Partner's id:</a>
        <input type="number" id="addressee" autocomplete="off"/>
        <form action="" onsubmit="likeUser(event)">
            <a>Like/dislike user: </a> 
            <select id="like">
                <option value='like'>like</option>
                <option value='dislike'>dislike</option>
            </select>
            <button>Press</button>
        </form>
        <form action="" onsubmit="sendMessage(event)">
            <a>Send message to user: </a> 
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            if (window.location.protocol == "https:") {
                var ws_scheme = "wss://";
            } else {
                var ws_scheme = "ws://"
            };
            let connected = false
            var ws = null
            function connect(event) {
                event.preventDefault()
                var token = document.getElementById('token').value
                ws = new WebSocket(ws_scheme + location.host + `/ws/${token}`);
                connected = true
                ws.onmessage = function(event) {
                    var msg = JSON.parse(event.data)
                    console.log(msg)
                    if ('message' in msg) {
                        var messages = document.getElementById('messages')
                        var message = document.createElement('li')
                        var content = document.createTextNode(JSON.parse(event.data).message)
                        message.appendChild(content)
                        messages.appendChild(message)   
                    }
                }
            }
            function likeUser(event) {
                event.preventDefault()
                var like = document.getElementById("like")
                var addressee = document.getElementById("addressee")
                var liked = true
                if (like == 'dislike') liked = false
                if (!connected) return 
                ws.send(JSON.stringify({'like': liked, 'addressee': addressee.value}))
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                var addressee = document.getElementById("addressee")
                if (!connected) return 
                ws.send(JSON.stringify({'message': input.value, 'addressee': addressee.value}))
                input.value = ''
                event.preventDefault()
            }
            function login(event) {
                event.preventDefault();
                fetch("https://" + location.host + '/auth/login', {
                    method: 'POST',
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({
                        'phone': document.getElementById("phone").value,
                        'password': document.getElementById("password").value,
                    })
                }).then((res) => res.json())
                    .then((data) => console.log(data.access_token))
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
        dialogs = [dict(rec.items()) for rec in user_dialogs]
        await websocket.send_json({'dialogs': dialogs})

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
        initial_message = await DialogController.get_messages_by_pair(pair)
        initial_message = dict(initial_message[0].items())
        initial_message['send_time'] = str(initial_message.get('send_time'))
        liked_online = self.active_connections.get(liked_user)
        if liked_online:
            await liked_online.send_json(initial_message)
        await self.active_connections[client_id].send_json(initial_message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_json({'message': message, 'author': 'server'})


manager = ConnectionManager()


@router.get("/client")
async def get():
    return HTMLResponse(html)


@router.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    user_id = None
    try:
        user_id = AuthController.validate_token(token)['id']
        print(f'User "{user_id}" has connected!')
    except:
        await websocket.accept()
        await websocket.send_json({'error': 'Could not validate token!'})
        await websocket.close()
        return

    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            # Что должно приходить
            # data = {
            #     'message', 'dialog', 'addressee', 'like'
            # }
            if 'addressee' not in data or not data.get('addressee') or not data['addressee'].isdigit():
                await websocket.send_json({'error': 'Need addressee id to send a message or like!'})
                continue
            addressee = await UserController.get_by_id(int(data['addressee']))
            if not addressee:
                await websocket.send_json({'error': 'No such addressee!'})
                continue

            if 'like' in data:
                pair = await PairController.like_user(int(data['addressee']), user_id, bool(data['like']))
                pair = dict(pair.items())
                if pair.get('like'):
                    await manager.sympathy_alert(
                        int(data['addressee']),
                        user_id,
                        pair['id']
                    )
            elif 'message' not in data or not data['message']:
                # Если нет сообщения - значит читаем пришедшие
                # обновляем БД
                await DialogController.messages_read(int(data['dialog']), int(data['addressee']))
                # отправляем пользователю о прочтении его сообщений
                await manager.send_partner_read_msgs(int(data['dialog']), int(data['addressee']), user_id)
            else:
                # отправляем пользователю новое сообщение от текущего пользователя
                await manager.send_personal_message(websocket, data['message'], int(data['dialog_id']), user_id)
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        await manager.broadcast(f"Client #{user_id} left the chat")
