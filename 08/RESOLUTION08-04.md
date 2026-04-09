# Django Final Module - Exercise 04: Scroll

## Objetivo
Mejorar la visualización del chat estableciendo un tamaño fijo para la lista de mensajes. Al superarse la capacidad visual (`height`) del contenedor, los mensajes más antiguos deben "desaparecer" hacia arriba, generando una barra de desplazamiento lateral (`scroll bar`). Además, el comportamiento de dicha barra debe ser automático: siempre debe anclarse a la parte inferior tras un nuevo mensaje (auto-scroll al fondo).

## Conceptos Claves
1. **Control de Desbordamiento CSS (`overflow-y`):** Poner parámetros físicos firmes (`height` o `max-height`) a una caja contenedor obliga al navegador a recalcular qué hacer con el remanente. Usar el valor `scroll` o `auto` genera la barra lateral de desplazamiento.
2. **Manipulación del DOM con jQuery (`scrollTop` y `scrollHeight`):** Ya que la especificación requiere estricto control automatizado para mantener al *scroll* anclado abajo, el navegador debe re-posicionar todo el desplazamiento (Y-axis) del contenedor en función de la suma completa de todas sus alturas internas nuevas inyectadas por WebSockets.

## ¿Cómo se hizo? (Implementación Detallada)

### 1. Las reglas de Estilos (CSS)
En el *header* del template de nuestro chat (`chat/templates/chat/room.html`), se adaptó el identificador maestro del log (`#chat-log`).

Se declaró formalmente el *height* estricto y la barra en el lado `Y` garantizada:
```css
#chat-log {
    border: 1px solid #ccc;
    height: 400px;
    overflow-y: scroll;
    padding: 10px;
    flex-grow: 1;
    display: block;
}
```
*Nota: Se aseguró que fuera `display: block` para evitar conflictos en ciertos motores de navegadores que rompen combinaciones flexboxes anidadas con scrolling interno bruto.*

### 2. Auto-Scroll con Localización de Coordenadas (JavaScript/jQuery)
El segundo requerimiento de evitar que la caja se quede "varada arriba" provocando que el usuario pierda rastro del hilo, se resolvió atándolo directamente a nuestro evento Reactivo de Websocket `onmessage`:

```javascript
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    
    // ... [Inyecciones lógicas de Chat y Lista] ...

    if (data.msg_type === "chat_message") {
        // [Inyección visual con .append()]
        
        // Auto-Scroll inferior (Bottom Anchoring)
        $('#chat-log').scrollTop($('#chat-log')[0].scrollHeight);
    }
};
```
**Desglose Técnico de esta línea:**
- `$('#chat-log')[0]` Accede al elemento puro de JavaScript nativo contenido en el array base de la variable jQuery.
- `.scrollHeight` Es una propiedad del navegador que devuelve el alto **total** del elemento *renderizado* (incluyendo las partes que están ocultas fuera de la vista y arriba de lo visible).
- `$('#chat-log').scrollTop(...)` Finalmente le indica a jQuery que recorra a juro y descienda esa distancia exacta (en este caso, enviándolo a lo absoluto más bajo).

Dado que nuestro servidor envía el listado de historiales de forma fraccionada durante el `onConnect()` inicial (del Ex02), jQuery atrapará esto y generará múltiples simulaciones visuales seguidas, por tanto; aunque el explorador trate de quedarse arriba en la inicialización (cuando carga), la suma interactiva terminará empujando por default al cliente final directito a los tres últimos históricos.

---

## Instrucciones de Montaje y Pruebas

No se requiere migraciones de SQLite, este factor ha sido un simple ajuste gráfico. 

Para testearlo y confirmarlo empíricamente:

1. **Disponibiliza el servidor:**
   ```bash
   cd ~/Documents/42/OutCore/piscine_django/django_practice/08/
   source django_venv/bin/activate
   cd d09
   python3 manage.py runserver
   ```
2. **Entra a la sala (`General`) con algún usuario.**
3. **Genera Flujo Excedido (Desbordamiento):**
   - Presiona Enter y escribe varios mensajes seguidos para superar la altura visual de `400px` establecida por el contenedor *hasta que empiecen a irse para arriba*. (Una media de 12 a 15 mensajes).
4. **Verificación de Scroll Fijo (Bottom Anchoring):**
   - Comprueba visualmente que ahora existe la *Scrollbar*.
   - Notarás que sin tocar tu mouse, y siguiendo escribiendo, la barra te mantendrá encarecidamente en la base con los nuevos mensajes a la vista *mostrando lo último primero* sin forzarte a hacer desplazamiento mecánico manual.

---
## Archivos Creados / Modificados en este Ejercicio:
- `d09/chat/templates/chat/room.html` (Adaptación CSS para forzar `overflow-y: scroll` y comportamiento jQuery `.scrollTop()` para anclaje inferior automático)
