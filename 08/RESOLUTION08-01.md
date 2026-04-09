# Django Final Module - Exercise 01: Basic chat

## Objetivo
El objetivo de este ejercicio es implementar un sistema de chat en tiempo real utilizando WebSockets mediante Django Channels y la librería frontend jQuery, abandonando por completo las peticiones AJAX tradicionales para esta comunicación.

## Conceptos Claves
1. **Django Channels & ASGI:** Django nativamente opera bajo WSGI (síncrono), lo cual no es apto para mantener conexiones persistentes abiertas como requieren los WebSockets. ASGI resuelve esto. Instalamos `daphne` como servidor ASGI y `channels` para manejar el enrutamiento asíncrono.
2. **WebSockets (ws:// / wss://):** Protocolo de comunicación bidireccional sobre un único socket TCP. Permite al servidor "empujar" (push) datos al cliente sin que este lo solicite iterativamente (a diferencia del polling en AJAX).
3. **Channel Layers:** Mecanismo de Django Channels que permite a diferentes instancias de nuestra aplicación (y diferentes WebSockets) hablar entre sí. Utilizamos el backend `InMemoryChannelLayer` para enrutar los mensajes entre usuarios.
4. **Consumers:** Son equivalentes a las "Vistas" (Views) de Django pero diseñados para WebSockets. Manejan asíncronamente los eventos de ciclo de vida del socket: cuando se conecta, cuando se desconecta y cuando se recibe un mensaje.

## Implementación Detallada

### 1. Configuración del Servidor ASGI y Channel Layers
Para que Django pueda escuchar y gestionar conexiones de WebSockets en lugar de solo HTTP, se tuvieron que modificar de raíz las configuraciones en `d09/settings.py`:
- Se añadió `'daphne'` y `'chat'` (nuestra app) al `INSTALLED_APPS`. `daphne` obligatoriamente va al inicio para interceptar el servidor de desarrollo.
- Se reemplazó el tradicional `WSGI_APPLICATION` instaurando explícitamente `ASGI_APPLICATION = 'd09.asgi.application'`.
- Configuramos la capa de canales añadiendo la variable `CHANNEL_LAYERS`, conectando mediante memoria `channels.layers.InMemoryChannelLayer`. Esto permite crear "grupos" donde varios sockets pueden escucharse al mismo tiempo.

Al mismo tiempo, preparamos `d09/asgi.py`, anidando la aplicación ASGI de Django con `ProtocolTypeRouter`, `AuthMiddlewareStack` (para tener acceso de sesión a `self.scope["user"]` sobre webscoket) y `URLRouter` señalando a nuestras rutas ws.

### 2. Creación del Modelo Room
El primer requisito indicaba modelar salas almacenadas en la base de datos. En `chat/models.py` definimos el modelo `Room`:
```python
class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
```
Esto da soporte dinámico a nuestra página index inicial, iterando las salas almacenadas e inyectando las rutas a sus instanciaciones `/chat/<room_name>/`.

### 3. Vistas Intermedias y Seguridad
Limitamos el acceso al chat utilizando la anotación `@login_required`. En `chat/views.py`:
- `index(request)`: Obtiene todas las instancias de Rooms registradas para plasmarlas en el listado inicial.
- `room(request, room_name)`: Ubica la sala mediante `get_object_or_404(Room, name=room_name)`. Traspasa información vital al frontend usando los _template tags_ de Django de tipo `|json_script:"id"`, evitando que el nombre de usuario o salón se impriman de manera insegura exponiéndose a un ataque XSS, para que jQuery puro los pueda consumir después.

### 4. El Consumer (`ChatConsumer`)
El corazón del chat fue creado en `chat/consumers.py`. Se programó el controlador asíncrono heredando de `AsyncWebsocketConsumer`:
- **`connect`:** Al abrir la ventana, el cliente llama esta función. Asignamos un grupo individual, digamos "chat_General" (`self.room_group_name`), y conectamos la sesión con `await self.accept()`. Luego comprobamos quién es el emisor: notificamos un envío (`group_send`) al resto de personas conteniendo el evento "Sistema: juan ha ingresado" (`<username> has joined the chat`).
- **`receive`:** Captura el `chatSocket.send()` que envía el navegador, toma su diccionario JSON y lo distribuye (`group_send`) replicándolo fielmente a toda otra conexión unida al mismo layer name.
- **`chat_message`:** Por último, actúa como un emisor "hacia afuera". Envía a quien escucha a través del websocket la resolución del evento. 

### 5. Lógica de UI (Frontend: jQuery)
Diseñado en base al marco en `chat/templates/chat/room.html`, cumple estrictamente la restricción de que solo jQuery se comunique.
- **Instanciación:** Utiliza la API nativa de navegadores apuntando al _endpoint ws:_ (o _wss:_): `new WebSocket(wsScheme + '://' + window.location.host + '/ws/chat/' + roomName + '/');`.
- **Lectura en Vivo (`onmessage`):** Ante la llegada de un payload vía WebSocket, se procesa en el front (`JSON.parse`). Dependiendo de si el _sender_ fue marcado como "System" o como un "Usuario", se hace un `$('#chat-log').append()` en cursiva o normal.
- **Autoscroll:** Se calcula dinámicamente un `$(...).scrollTop` apuntando hacia abajo post-añadido para conservar y facilitar la lectura en orden ascendente (Bottom to Top).

---

## Instrucciones de Montaje y Pruebas

Para desplegar este entorno de chat asíncrono e ilustrar la teoría antes detallada, efectúa los siguientes pasos en la terminal:

### Paso A: Montaje del Entorno
1. **Activar tu Entorno Virtual:** Instanciar dependencias es crítico (Daphne/Channels requeridos en el ejercicio pasado).
   ```bash
   cd ~/Documents/42/OutCore/piscine_django/django_practice/08/
   source django_venv/bin/activate
   cd d09
   ```

2. **Aplicar la Estructura de BD (Migraciones):**
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

3. **Poblar Contexto y Cuentas de Pruebas:**
   Necesitan existir cuentas en el sistema para chatear entre sí y las salas para unirse. (Nota: Esto ya lo he creado en tu base de datos actual para agilizar). Si deseas regenerarlos:
   ```bash
   python3 manage.py shell
   ```
   ```python
   # 1. Crear Salas
   from chat.models import Room
   Room.objects.get_or_create(name='General')
   Room.objects.get_or_create(name='Random')

   # 2. Crear Usuarios (Ej. 'juan' y 'test')
   from django.contrib.auth.models import User
   User.objects.create_user('juan', 'juan@a.com', 'pass1')
   User.objects.create_user('test', 'test@a.com', 'pass1')
   exit()
   ```

### Paso B: Pruebas de Comprobación y Testeo Directo
1. **Desplegar Servidor Local Daphne:**
   Al usar Channels, `runserver` detecta ASGI y lanza a Daphne.
   ```bash
   python3 manage.py runserver
   ```
2. **Entornos Aislados (Usuario 1):**
   - Accede a tu entorno en `http://127.0.0.1:8000/account/` y haz tu Log In. (Ejemplo: *juan*)
   - Navega por el listado de salas en `http://127.0.0.1:8000/chat/`
   - Ingresa a la sala **"General"**.
3. **Entornos Aislados (Usuario 2):**
   - Lanza una **nueva ventana en modo Incógnito** de tu explorador u ocupa un navegador alternativo (Firefox / Chrome). Es imperativo usar incógnito para ignorar el uso de sesiones de la cookie.
   - En la nueva ventana ingresa a `http://127.0.0.1:8000/account/` e inicia sesión como el otro usuario (Ejemplo: *test*).
   - Ve a `http://127.0.0.1:8000/chat/General/`.
4. **Verificación de Eventos (Push):**
   - Al unirse _test_, en la ventana de **ambos navegadores** el cliente inyectará instantáneamente: *"test has joined the chat"*, confirmando el broadcast asíncrono al realizar el `WebSocket Accept()`.
5. **Conversación:**
   - Comienza a mandar un par de frases cortas de una ventana a la otra. 
   - No verás recargas en la barra de direcciones o HTTP en la consola de Django, todo fluye al unísono de modo limpio en `ws/chat/General/`. Las ventanas se poblarán simétricamente, completando así este ejercicio Final.

---
## Archivos Creados / Modificados en este Ejercicio:
- `d09/d09/settings.py` (Integración de ASGI, Daphne, Channels y Channel Layers)
- `d09/d09/asgi.py` (Configuración del enrutamiento asíncrono base)
- `d09/chat/routing.py` (Creación del enrutador de WebSockets `ws/chat/`)
- `d09/chat/models.py` (Creación del modelo `Room`)
- `d09/chat/views.py` (Vistas `index` y `room` con protección de acceso)
- `d09/chat/urls.py` (Rutas estáticas de la aplicación chat)
- `d09/chat/consumers.py` (Implementación de `ChatConsumer` básico)
- `d09/chat/templates/chat/index.html` (Listado de salas disponibles)
- `d09/chat/templates/chat/room.html` (Estructura de la sala y lógica AJAX WebSocket base)
