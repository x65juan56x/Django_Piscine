import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'd09.settings')
django_asgi_app = get_asgi_application()

import chat.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        )
    ),
})

# ProtocolTypeRouter
# Gestiona el tipo de petición recibida (http o websocket)
# Si dice http (ej. cargar la página web inicial): Se la manda al núcleo normal de Django (django_asgi_app), que usará el urls.py las vistas convencionales.
# Si dice websocket (ej. el chat intentando conectarse): La manda a través del siguiente Stack de Channels.

# AuthMiddlewareStack crea el diccionario scop, que usamos como self.scope["user"] para saber quien se conecta o escribe un mensaje
# Esto es necesario porque websocket no tiene un request.user

# URLRouter
# Es el equivalente asíncrono al archivo urls.py.
# Una vez que ProtocolTypeRouter vio que es un WebSocket, y AuthMiddlewareStack le puso la etiqueta del usuario, la petición llega al URLRouter.
# Este revisa la ruta específica (ej. ws/chat/General/) usando las reglas definidas en d09/chat/routing.py, y finalmente conecta al usuario con su respectivo controlador (el ChatConsumer).