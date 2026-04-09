# Django Final Module - Exercise 02: Message History

## Objetivo
El objetivo de este ejercicio es implementar un historial persistente de chat. Al conectarse a una sala, el usuario debe poder ver los **últimos tres mensajes** enviados históricamente a ese canal, ordenados cronológicamente desde el más viejo hasta el más reciente, y esto todo a través de WebSockets sin usar AJAX.

## Conceptos Claves
1. **Persistencia en Base de Datos (`models.Model`):** A diferencia del Ejercicio 01, donde la capa en memoria perdía los mensajes inmediatamente al desconectarse todos, en este ejercicio se requiere guardar permanentemente los mensajes asociados a una `Room`.
2. **`database_sync_to_async`:** Al trabajar con Django Channels (específicamente la clase `AsyncWebsocketConsumer`), el flujo principal se maneja asíncronamente con el _Event Loop_ (`async/await`). Sin embargo, el ORM de Django (consultas a base de datos) es bloqueante y síncrono. Esta anotación de Channels _enmascara_ una función para enviar la petición SQL a un "Hilo de BD" paralelo, evitando que nuestro websocket se bloquee mientras espera a la base de datos.

## ¿Cómo se hizo? (Implementación Detallada)

### 1. Modelo `Message` (Historial)
Se añadió a `chat/models.py` la tabla estructurada para almacenar temporalmente los historiales de los mensajes:
```python
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
```
Efectuamos el correspondiente `python3 manage.py makemigrations` y el `python3 manage.py migrate` para inyectarlo al SQLite. Aprovechamos `auto_now_add=True` para grabar el timestamp preciso en milisegundos y usarlo más tarde en el ordenamiento temporal (Oldest to Newest).

### 2. Modificaciones asíncronas en `ChatConsumer`
En lugar de únicamente empujar cadenas (texto puro), nuestro script `chat/consumers.py` necesitaba interceptar las llegadas con las funciones de BD:

**a. Grabar el mensaje (`save_message`)**
```python
@database_sync_to_async
def save_message(self, room_name, sender, message):
    room = Room.objects.get(name=room_name)
    Message.objects.create(room=room, sender=sender, content=message)
```
Esta función fue inyectada justo en la validación principal dentro del método `receive()`. Justo antes de que nuestro servidor dispare efusivamente el `await self.channel_layer.group_send`, logramos salvaguardar el contenido de la petición internamente.

**b. Recuperar Históricos (`get_last_messages`)**
```python
@database_sync_to_async
def get_last_messages(self, room_name):
    room = Room.objects.get(name=room_name)
    messages = Message.objects.filter(room=room).order_by('-timestamp')[:3]
    return reversed(list(messages))
```
Efectuamos un filtro a base de la sala deseada y tomamos los **tres** `[:3]` más "nuevos" listándolos con timestamp descendiente (`-timestamp`). Para cumplir la norma impuesta por 42 (_"... top down, oldest to newest."_), regresamos la lista revertiéndola para que al inyectarse en el Front-End sigan un flujo normal de lectura.

### 3. Emisión Individual (Unicast) vs Emisión de Grupo (Broadcast)
El mayor desafío de WebSockets es dominar la topología del tráfico. Hasta ahora nuestro `group_send` mandaba cosas a **toda la sala**.
```python
async def connect(self):
    ...
    await self.accept()
    if user.is_authenticated:
        history_messages = await self.get_last_messages(self.room_name)
        for msg in history_messages:
            # Envío Unicast (Solo a ti)
            await self.send(text_data=json.dumps({
                "message": msg.content,
                "sender": msg.sender
            }))
```
Para evitar enviarle 3 mensajes antiguos a las personas que _ya_ están leyendo el chat activamente y solo enseñarlos a quien se **acaba de incorporar**, ocupamos `await self.send()` (Sin pasar por el dictamen grupal del Channel Layer), para enviarle estrictamente la información por ese tubo directo.

### 4. Respeto de Reglas Frontend 
Dado que el frontend (jQuery puro) no sufrió el más mínimo cambio y el endpoint original de renderización JSON a través del parser sigue intacto (`$('#chat-log').append()`), los tres mensajes inyectados fluyen sin que la vista se percate de que estaban "retrasados", integrándose a la misma caja `#chat-log` sin refrescar, conservándose bajo jQuery, libre de llamadas XMLHttpRequest adicionales (Sin AJAX).

---

## Instrucciones de Montaje y Pruebas

Para revisar que el comportamiento es correcto en tiempo real:

1. Ingresa a la sala (ejemplo: `/chat/General/`).
2. Escribe una serie de mensajes arbitrarios como prueba temporal, por ejemplo:
   - "Hola uno"
   - "Hola dos"
   - "Hola tres"
   - "Hola cuatro"
   - "Hola cinco"
3. El *log* mostrará los cinco mensajes, además del de `juan has joined the chat`.
4. Refresca la ventana de tu navegador con el F5 / O en otra pestaña únete de improvisto.
5. Inmediatamente el log de chat se poblará de arriba hacia abajo con:
   - "Hola tres"
   - "Hola cuatro"
   - "Hola cinco"
   - `juan has joined the chat` (Emitido dinámicamente)

Este comportamiento comprueba que el ORM está almacenando el dictamen bidireccional y el servidor se encargó de efectuar un Unicast transparente con los 3 últimos (`LIMIT 3`) del historial previo a lanzar el *broadcast* a todo el grupo de que "entró a la sala" según las reglas estrictas.

---
## Archivos Creados / Modificados en este Ejercicio:
- `d09/chat/models.py` (Añedido del modelo persistente `Message`)
- `d09/chat/consumers.py` (Se agregaron `save_message()`, `get_last_messages()` y ajustes dentro de `connect()`/`receive()`)
- `d09/chat/migrations/` (Archivos de migración para aplicar el nuevo modelo a SQLite)
