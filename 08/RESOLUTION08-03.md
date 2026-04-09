# Django Final Module - Exercise 03: Userlist

## Objetivo
Implementar un listado lateral interactivo y auto-suficiente que muestre exactamente quién se encuentra conectado en el chat *en ese momento*. Ese estado debe actualizarse automáticamente tanto al unirse a la sala como cuando un participante se desconecta, gatillando también un mensaje explícito `"<username> has left the chat"`. No se puede utilizar AJAX, solo jQuery y WebSockets.

## Conceptos Claves
1. **Control de Presencia Dinámico (State Management):** Las Channel Layers se encargan de enrutar mensajes a un "grupo", pero no nos proveen nativamente de un diccionario global que resuelva un listado explícito de qué usuarios específicos componen el grupo. Hemos programado esta lógica al nivel de memoria del servicio del consumer.
2. **Payloads tipados (Multiplexor):** Nuestro túnel único WebSocket maneja el 100% de la comunicación. Antes su único objetivo era traer cadenas ("chat message"). Ahora, transporta diccionarios complejos: un mensaje incluye una etiqueta `msg_type` que nos permite separar lógicamente en Front-End si el payload que acaba de llegar pertenece al chat o si es una orden para sustituir a la lista de usuarios.
3. **Mapas de Diccionarios y Exclusión de Tabs (Pestañas Múltiples):** El reto técnico al controlar la presencia es que un mismo usuario puede abrir el chat en dos pestañas diferentes (2 `channel_names`). Si cerramos una pestaña, no debemos decirle a la sala general que "el usuario se ha ido" si en la sala _seguimos_ teniendo abierta la segunda pestaña. Lograr esto requirió atar el `username` al `channel_name` individual.

## ¿Cómo se hizo? (Implementación Detallada)

### 1. El Diccionario de Control (Backend - `ChatConsumer`)
En **`chat/consumers.py`** se introdujo un diccionario global de alto nivel:
```python
# Format: {'room_name': {'channel_name': 'username'}}
connected_users = {}
```
Gracias a esta arquitectura anidada, al momento de la conexión (`connect()`):
- Tomamos registro asociando la sala y un número de socket único (`self.channel_name`) al usuario.
- Analizamos temporalmente si en la sala de estar (valores totales del dict de la sesión actual de la room) el usuario ya existía `is_new_user = user.username not in connected_users[self.room_name].values()`.
- De ser "nuevo" de verdad (no era otra pestaña duplicada de `juan`), se avisa formalmente a la room con `... has joined the chat`.

Luego, disparamos una petición (`broadcast_user_list()`) a la capa de canales, informándoles del actual `list(set())` único de los presentes a todos.

### 2. Control de Desconexión (`disconnect()`)
Similarmente al punto anterior, cuando se detecta el cierre involuntario (o intencional) de un WebSocket `onclose=()`:
- Borramos al `channel_name` (sesión individual) del mapeo global de nuestra app.
- Evaluamos: *¿Quedan más pestañas (`channel_name`) con este mismo nombre de usuario en esta sala?*
- Si la respuesta es NO y sus valores de `.values()` se fueron con él, empujamos el mensaje *broadcast* para notificar a la room que **"ha abandonado la sala"** (`user.username + " has left the chat"`). Emitido siempre a través de nuestro manejador emisor fantasma, "System".

### 3. Multiplexación en el Frontend (jQuery)
Adicional a que le generamos a la barra lateral el `div#user-list-container` estipulado con estricta composición flex y layout lateral limpio en `chat/templates/chat/room.html`, tuvimos que adaptar a nuestro receptor:
```javascript
const data = JSON.parse(e.data);
if (data.msg_type === "user_list") {
    $('#user-list').empty(); // Clear old list
    data.users.forEach(function(user) {
        $('#user-list').append('<li>' + user + '</li>');
    });
} else if (data.msg_type === "chat_message") {
    // Tratamiento de Chat Normal ...
}
```
Aquí radica el truco principal de evitar múltiples subscripciones. Nuestro único WebSocket interpreta lo que entra del Consumer. Si el Servidor le avisa por el canal con `msg_type = 'user_list'`, JS/jQuery de inmediato interviene el DOM destrozando la versión inactiva del `<ul>` `.empty()` para recorrer y sobreescribir `.append()` exactamente con los activos sincronizados del backend.

---

## Instrucciones de Montaje y Pruebas

Para revisar el comportamiento y testear la correcta concurrencia asimétrica:

1. **Inicia el proceso ASGI normal:**
   ```bash
   cd ~/Documents/42/OutCore/piscine_django/django_practice/08/
   source django_venv/bin/activate
   cd d09
   python3 manage.py runserver
   ```
2. **Prueba de "Lista y unirse" (Join):**
   - Entra con "juan" al chat `General`. Debería aparecer inmediatamente *tu propio nombre* en la barra lateral "Connected Users".
   - Entra con tu cuenta 2 (por consola incógnito) "test". Instantáneamente verás a *Ambas cuentas* reflejadas como _LI_ (ítem de lista) en ambos navegadores.
3. **Prueba de Resistencia de Pestañas Múltiples:**
   - Con el usuario "juan", en una pestaña secundaria o *duplicada*, métete al mismo `/chat/General/`.
   - Cierra únicamente la segunda pestaña duplicada de `juan`:
   - El sistema NO disparará "juan has left the chat" todavía, pues de verdad, un canal asíncrono para juan sigue existiendo. Y evitarás espameo fantasma.
4. **Prueba de Desconexión:**
   - Cierra a voluntad las pestañas netas del usuario o presiona "Logout". El WebSocket detectará la caída del socket, efectuará la limpieza en diccionarios, y el explorador remanente verá automáticamente imprimirse: **"<username> has left the chat"** en su fondo, a medida que su Userlist pierde de refilón ese ítem para refrescar la lista general.

---
## Archivos Creados / Modificados en este Ejercicio:
- `d09/chat/consumers.py` (Implementación de rastreo en memoria `connected_users`, lógica de multi-pestaña para Join/Leave y `broadcast_user_list()`)
- `d09/chat/templates/chat/room.html` (Reestructuración Flexbox para el modal de usuarios y soporte de multiplexación JavaScript `msg_type`)
