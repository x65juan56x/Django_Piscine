# Resolución Módulo 08: Django Final - Ejercicio 00

## Conceptos Claves y Tecnologías Fundamentales

Antes de adentrarnos en las decisiones arquitectónicas, es vital comprender las tecnologías y conceptos que fundamentan este ejercicio:

- **AJAX (Asynchronous JavaScript and XML):** Es un conjunto de técnicas de web scripting que permite que una aplicación se comunique con un servidor web en segundo plano (de forma asíncrona). Su pertinencia aquí es central: en lugar del clásico ciclo de petición-respuesta (donde el navegador se queda en blanco y carga una nueva página tras enviar un formulario), AJAX permite mandar las credenciales y recibir la validación sin interferir con la pantalla actual. Es lo que logra la magia de "no refrescar la página".
- **jQuery:** Es una librería de JavaScript clásica, diseñada para simplificar la manipulación del árbol HTML (DOM), el manejo de eventos y, crucialmente, las peticiones AJAX (`$.ajax`). El *Subject* la exige específicamente frente a frameworks modernos (React, Vue, Angular) obligándonos a controlar manualmente las mutaciones de la interfaz y la sincronía entre front y back.
- **JSON (JavaScript Object Notation):** Dado que el servidor ya no devuelve páginas HTML completas tras un inicio de sesión por AJAX, necesitamos un estándar ligero de intercambio de datos. Django transforma sus repuestas en objetos JSON (como `{"success": true, "username": "admin"}`) que jQuery interpreta instantáneamente para saber si reaccionar con un mensaje de éxito o desglosar los errores.
- **SPA Parcial / Interfaz de Estado Mutante:** Concepto arquitectónico frontend donde el documento inicial pre-carga todas las "pantallas" posibles (el formulario y el panel de bievenida). Mediante jQuery, simplemente alteramos la opacidad y visibilidad de estos elementos (flujo de estados) dependiendo del JSON que nos devuelve el servidor. Esto emula cómo se comportan las aplicaciones modernas (Single Page Applications) pero usando herramientas rústicas.
- **Protección CSRF sobre AJAX:** Usualmente los tokens contra falsificación de peticiones trans-sitio se mandan embebidos en el recargo del formulario. En AJAX, debemos asegurarnos de recolectar dicho token (con utilidades como `.serialize()`) y adjuntarlo en los headers o cuerpo del POST asíncrono para que Django acepte la petición como segura.

## 1. Planificación y Arquitectura Base

**Decisiones tomadas:**
- Se creó el proyecto `d09` y la aplicación `account` bajo un entorno asincrónico preparado.
- Se generó y rastreó desde cero el entorno virtual guardando las dependencias en un archivo explícitamente nombrado `requirement.txt` (en singular y minúsculas), usando `pip freeze` tal como demanda el sujeto. Esto asienta las bases para que una ejecución del script `my_script.sh` lo levante en cuestión de segundos.

## 2. Paradigma del Backend (Vistas Separadas)
El ejercicio exige que la ruta `127.0.0.1:8000/account` tenga un comportamiento fluido, alternando entre el modo logueado y deslogueado sin refrescar jamás la página, y que la comunicación ocurra estrictamente a través de peticiones AJAX usando `POST`.

Para resolver esto sin mezclar lógicas, se dividieron las responsabilidades en el archivo `account/views.py`:

- **Una Vista Inicial de Renderizado (`account_view`)**: 
  Solo atiende peticiones `GET` y renderiza el molde `index.html`. Lo más importante de esta vista es que pasa la clase nativa `AuthenticationForm` pre-instanciada. Esto cumple con la directiva del subject *"AuthenticationForm, for free!"*, evitándonos tener que construir el motor de validación de contraseñas de cero.
  
- **Endpoints de Recepción AJAX (`ajax_login` y `ajax_logout`)**:
  Se crearon rutas específicas (`/account/login/` y `/account/logout/`) que únicamente esperan recibir un método `POST`. 
  - En lugar de usar `render()` o `redirect()`, devuelven un objeto `JsonResponse`. 
  - Al procesar el login, pasamos el diccionario de datos de la petición asíncrona directamente por el `AuthenticationForm`. Si las credenciales y el CSRF token son válidos, se loguea al usuario y se emite un `{"success": true, "username": "usuario"}`. En caso de fallar, extraemos del objeto del formulario sus errores exactos (`form.errors`) en objeto JSON y lo enviamos de vuelta al front-end con un `{"success": false}`.

## 3. Frontend: Interacción Estricta con jQuery
Las reglas del día prohíben frameworks como React, Vue o Reactivity, permitiendo única y exclusivamente la librería **jQuery**.

**Diseño de la Interfaz (`index.html`)**:
Para lidiar con el estado dinámico (logueado vs. deslogueado) y respetar que **una recarga manual debe preservar el estado correcto**, se optó por el enfoque de **"Vistas Sobrepuestas" (Overlapping Views)**:
- Se agruparon en el HTML dos grandes contenedores (Containers/Cards creados con Bootstrap 5): `<div id="unauth-view">` (Formulario) y `<div id="auth-view">` (Botón Logout).
- En lugar de decidir con JavaScript puro cuál de los dos contenedores debe mostrarse al inicio, usamos el motor Jinja2 nativo como pre-renderizador:
  `style="{% if user.is_authenticated %}display: none;{% endif %}"`
  De esta forma, si el usuario decide hacer un refresco manual de la página (`F5`), el servidor evalúa su sesión antes de entregar el HTML y dibuja inmediatamente la pantalla correcta, evitando así un "parpadeo" que arruinaría la experiencia.

**Gestión AJAX y Prevención de Refresco**:
- A ambos formularios (Login y Logout) se les añadió un evento jQuery de intercepción sobre el botón enviar: `$('#login-form').on('submit', function(e) { ... })`.
- El primer paso de cada evento invoca a `e.preventDefault()`. Esta es la clave del ejercicio: esta pequeña instrucción neutraliza la recarga predeterminada del navegador que un elemento `<form>` provoca.
- Acto seguido, enviamos el contenido vía asíncrona `$.ajax()`, ayudándonos con el comando `$(this).serialize()` que atrapa instantáneamente tanto las entradas textuales como nuestro fundamental `{% csrf_token %}` en una sola cadena.
- La protección CSRF sobre AJAX requiere atención especial: Django fuerza por seguridad una re-generación interna (rotación) de este Token cada vez que se llama a los métodos `login(request, user)` y `logout(request)`. Como nuestra página *no se recarga automáticamente tras el login*, nuestra variable en el DOM pre-renderizada queda de repente caduca para el siguiente submit. Si no lo manejamos, enviar un *Logout* fallaría dando un Error 403.
  **La solución:** Escribimos la función `getCookie('csrftoken')` implementada en el HTML. Cada vez que recibimos respuesta exitosa vía AJAX de un login o logout, leemos inmediatamente la nueva cookie inyectada por el servidor, y asignamos programáticamente sus nuevos valores actualizados a todos los *inputs hidden* existentes que lleven el atributo `name="csrfmiddlewaretoken"`. Así permitimos un ciclo vitalicio de logins/logouts sin el menor bloqueo ni necesidad de apretar F5.

## Conclusión Ejecutiva
La implementación superó la prueba de separar correctamente la representación inicial del DOM (con Django Templates) de las alteraciones asincrónicas reactivas impulsadas vía AJAX (con jQuery), cumpliendo a satisfacción el requisito de un cambio de estado "inmortalizado" por la recarga. La inserción del `requirement.txt` congela la arquitectura lista y prepara el terreno asíncrono ASGI para seguir empujando código en los próximos ejercicios sobre la misma rama del proyecto.

---
*Fin de la documentación del Ex00 - Módulo 08 Final.*

---
## Archivos Creados / Modificados en este Ejercicio:
- `d09/requirement.txt` (Lista de dependencias base)
- `d09/d09/settings.py` (Configuración de la app `account`)
- `d09/d09/urls.py` (Enrutamiento principal)
- `d09/account/views.py` (Lógica AJAX y manejo de sesión)
- `d09/account/urls.py` (Rutas de la aplicación account)
- `d09/account/templates/account/index.html` (Formulario y bienvenida SPA)