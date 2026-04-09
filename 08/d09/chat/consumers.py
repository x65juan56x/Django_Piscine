import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message

# Diccionario global para trackear usuarios conectados
# Format: {'room_name': {'channel_name': 'username'}}
connected_users = {}

class ChatConsumer(AsyncWebsocketConsumer):
    # ex02
    @database_sync_to_async
    def get_last_messages(self, room_name):
        try:
            room = Room.objects.get(name=room_name)
        except Room.DoesNotExist:
            return []
        messages = Message.objects.filter(room=room).order_by('-timestamp')[:3]
        return reversed(list(messages))

    # ex02
    @database_sync_to_async
    def save_message(self, room_name, sender, message):
        try:
            room = Room.objects.get(name=room_name)
            Message.objects.create(room=room, sender=sender, content=message)
        except Room.DoesNotExist:
            pass

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()
        
        user = self.scope["user"]
        if user.is_authenticated:
            # Agregar usuario a la lista connected_users
            if self.room_name not in connected_users:
                connected_users[self.room_name] = {}
            
            # Ver si es un usuario completamente nuevo entrando al room
            is_new_user = user.username not in connected_users[self.room_name].values()
            connected_users[self.room_name][self.channel_name] = user.username

            # Recuperar y enviar (solo a mi como usuario) los 3 mensajes históricos más recientes
            history_messages = await self.get_last_messages(self.room_name)
            for msg in history_messages:
                await self.send(text_data=json.dumps({
                    "msg_type": "chat_message",
                    "message": msg.content,
                    "sender": msg.sender
                }))

            # Si el usuario aún no estaba en la sala con otra pestaña, envía un mensaje de incorporación al broadcast
            if is_new_user:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "message": f"{user.username} has joined the chat",
                        "sender": "System",
                    }
                )
            
            # Lista de usuarios actualizada del broadcast
            await self.broadcast_user_list()

    # ex03
    async def disconnect(self, close_code):
        user = self.scope["user"]
        if user.is_authenticated:
            # Sacar usuario de connected_users
            if self.room_name in connected_users and self.channel_name in connected_users[self.room_name]:
                del connected_users[self.room_name][self.channel_name]
                
                # Checkear se fue por completo (sin otras pestañas abiertas en ese room)
                if user.username not in connected_users[self.room_name].values():
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "chat_message",
                            "message": f"{user.username} has left the chat",
                            "sender": "System",
                        }
                    )
                
                # Limpieza del room
                if not connected_users[self.room_name]:
                    del connected_users[self.room_name]
                else:
                    # Lista de usuarios del broadcast actualizada
                    await self.broadcast_user_list()

        # Abandonar room
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def broadcast_user_list(self):
        if self.room_name in connected_users:
            users_in_room = list(set(connected_users[self.room_name].values()))
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_list",
                    "users": users_in_room
                }
            )

    # Recibir mensaje desde WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope["user"]

        if user.is_authenticated:
            # Guardar en DB (ex02)
            await self.save_message(self.room_name, user.username, message)

            # mandar mensaje al room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": user.username,
                }
            )

    # Dispatcher a websocket: Message
    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]

        await self.send(text_data=json.dumps({
            "msg_type": "chat_message",
            "message": message,
            "sender": sender
        }))

    # Dispatcher a websocket: Connected User List
    async def user_list(self, event):
        users = event["users"]
        await self.send(text_data=json.dumps({
            "msg_type": "user_list",
            "users": users
        }))

# El ORM es blockeante y síncrono, entonces tenemos que usar database_sync_to_async,
# que envía la petición SQL en un hilo de BD evitando que el websocket se bloquee.