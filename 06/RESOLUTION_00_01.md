# Explicación del Proyecto: Sesiones Anónimas y Gestión de Usuarios
*(Ejercicios 00 y 01)*

Este documento detalla la implementación de un sistema web desde cero utilizando **Django** (un entorno de trabajo para Python que facilita la creación de sitios web) y **Bootstrap** (una biblioteca de herramientas para diseño visual). 

El objetivo de estos dos primeros ejercicios es manejar dos tipos de visitantes:
1. **Anónimos:** Se les asigna temporalmente un nombre aleatorio que cambia cada 42 segundos.
2. **Autenticados:** Usuarios registrados que inician sesión.

A continuación, se explica paso a paso cómo se construyó cada pieza del sistema, por qué se tomaron ciertas decisiones técnicas y cómo interactúan entre sí.

---

## Conceptos Fundamentales

Antes de profundizar en el código, es importante comprender cuatro conceptos técnicos clave:

- **Petición y Respuesta HTTP:** Cada vez que haces clic en un enlace o envías un formulario, tu navegador envía una "Petición" (Request) al servidor. El servidor procesa esa información y devuelve una "Respuesta" (Response), que generalmente es una página HTML.
- **Sesiones (Sessions):** HTTP es un protocolo "sin estado", lo que significa que no tiene memoria. Una "sesión" es una técnica que permite al servidor recordar a un visitante entre una página y otra mediante la asignación de un identificador único guardado en el navegador.
- **Middleware:** Es una pieza de código en Django que se ejecuta en el medio del proceso. Intercepta la petición HTTP *antes* de que llegue a la lógica principal (la vista), y también puede interceptar la respuesta antes de que llegue al navegador.
- **AJAX / Fetch:** Es una tecnología útil en JavaScript que permite al navegador comunicarse con el servidor en segundo plano, sin tener que recargar toda la página web.

---

## Ejercicio 00: Sesiones Anónimas

**Objetivo:** Si un usuario no ha iniciado sesión, el sistema le asigna un nombre al azar entre 10 opciones. Este nombre dura exactamente 42 segundos. Al pasar ese tiempo, se debe cambiar por otro nuevo de forma automática, sin interrumpir la navegación del usuario.

### 1. Lista de Nombres y el Middleware
Primero, en el archivo `settings.py` (las configuraciones centrales del proyecto), se definió la lista de los 10 nombres posibles (`RANDOM_USER_NAMES`).

Para asignar los nombres, creamos un archivo llamado `middleware.py`. Elegimos hacer esto en un *Middleware* y no en una página en específico porque queríamos que la regla aplicara a *todas* las páginas de nuestro sitio automáticamente.

**¿Qué hace el Middleware exactamente?**
1. Revisa si el visitante ya tiene una cuenta abierta (`request.user.is_authenticated`). Si la tiene, ignora el resto del código y lo deja pasar.
2. Si es anónimo, revisa en su sesión si ya se le asignó un tiempo (`name_timestamp`).
3. Calcula la diferencia entre la hora actual exacta y la hora en que se asignó el nombre.
4. Si la diferencia es mayor a 42 segundos, elije un nuevo nombre al azar de la lista y actualiza la marca de tiempo a la hora actual.
5. Guarda toda esta información temporalmente en la base de datos de Django para esa sesión específica y el visitante sigue su camino.

### 2. Rotación del nombre sin recargar la página (AJAX)
El requisito más complejo pedía que el nombre en pantalla cambiara al pasar los 42 segundos sin que el usuario recargue (apriete F5) ni pierda lo que estaba haciendo (por ejemplo, llenar un formulario).

Para lograr esto, combinamos tres elementos:
1. **La Vista (El proveedor de datos):** En `views.py` creamos una función mínima llamada `get_current_name`. A diferencia de una vista normal que devuelve una página HTML completa, esta devuelve solamente texto plano en un formato de datos estructurado llamado JSON. Lo único que dice es: "El nombre actual del visitante es X".
2. **La URL:** En `urls.py` conectamos la dirección `/get-name/` a esta nueva vista.
3. **El Script (JavaScript):** Al final de nuestro documento principal visual (`base.html`), inyectamos un pequeño código que ejecuta una tarea repetitiva cada 2 segundos. Usa la función `fetch()` para llamar silenciosamente a la URL `/get-name/`, lee la respuesta JSON, y sobrescribe el interior del elemento HTML que contiene el saludo.

Gracias a este diseño, el Middleware calcula el paso del tiempo de forma invisible en el servidor. Cuando pasan los 42 segundos y actualiza el nombre, la siguiente petición silenciosa del código JavaScript se da cuenta y actualiza la pantalla del usuario suavemente.

---

## Ejercicio 01: Creación de Usuarios y Autenticación

**Objetivo:** Permitir que los visitantes dejen de ser anónimos al crear una cuenta propia con usuario y contraseña, y que puedan entrar o salir del sistema de manera segura.

### 1. Los Formularios y sus Validaciones (`forms.py`)
En Django, los formularios no solo dibujan las casillas de texto en la pantalla, sino que son filtros de seguridad de datos. Creamos dos formularios matemáticos/lógicos: `RegistrationForm` y `LoginForm`.

**En el registro (`RegistrationForm`):**
- Pedimos usuario, contraseña y confirmación de contraseña.
- Utilizamos un método llamado `clean_username`. La palabra clave `clean` en Django significa "verificar y limpiar datos". Este bloque consulta directamente a la base de datos de usuarios (`User.objects.filter`) para saber si alguien ya eligió ese nombre. Si existe, lanza un error que la página luego le mostrará en rojo al usuario.
- En el método general `clean()`, corroboramos que la primera contraseña introducida sea idéntica a la confirmación, de lo contrario, rechazamos el formulario.

**En el inicio de sesión (`LoginForm`):**
- Tomamos usuario y contraseña y ejecutamos la función `authenticate()`.
- La función `authenticate` de Django es crucial: compara el usuario, toma la contraseña enviada en texto plano y no la compara directamente. En su lugar, aplica un "algoitmo de hash" matemático para ver si el resultado cifrado coincide con el resultado indescifrable almacenado en la base de datos (Django NUNCA guarda el texto de la contraseña original). Si no coindice, la autenticación falla por completo.

### 2. Control de Vistas y Rutas (`views.py` y `urls.py`)
Las vistas de registro e inicio de sesión deben manejar dos escenarios de interacción HTTP distintos:
- **Flujo GET (Pedir algo):** Cuando el usuario hace clic en el enlace "Register", su navegador hace una petición GET. La vista simplemente crea un formulario vacío y le dibuja la página `register.html`.
- **Flujo POST (Enviar algo):** Cuando el usuario hace clic en el botón de enviar del formulario, su navegador ejecuta un POST. La vista agarra todos esos datos empaquetados y se los entrega a los validadores que describimos arriba.
  - Si los datos pasan las pruebas lógicas (`form.is_valid()`), la vista extrae la información y procede a llamar a `User.objects.create_user()` para insertar el nuevo empleado en el disco duro (base de datos) del servidor, o a abrir la sesión si era el inicio (`login(request, user)`). Inmediatamente después, lo redirige (lo empuja) hacia la página de inicio.
  - Si fallan, devuelve al usuario al mismo template `register.html` o `login.html`, pero esta vez con los mensajes de error inyectados.

### 3. La Interfaz Dinámica (`base.html`)
Diseñamos un molde de página (Base Template) estructurado mediante la biblioteca `Bootstrap`, la cual nos proporcionó un diseño de barra de navegación oscura profesional solo aplicando clases textuales como `navbar-dark` o `bg-dark`.

Dentro de esa barra de navegación, utilizamos lenguaje de plantillas de Django:
- `{% if request.user.is_authenticated %}`
Esta es una condicional. Si la solicitud HTTP que entra viene de parte de un usuario logueado (cuyo identificador la memoria de la sesión reconoció con éxito), solo le dibujamos el botón de "Cerrar sesión" y lo saludamos con su verdadero `username`.
En caso de evaluar a Falso, pintamos los enlaces de Registro e Inicio de sesión, y lo saludamos invocando la variable mágica temporal de su sesión anónima.

---

## Resumen de Flujos Paso a Paso

### Flujo 1: Un nuevo visitante entra a la página (Anónimo)
1. El usuario digita `http://127.0.0.1:8000/`. El navegador envía la solicitud.
2. El `AnonymousSessionMiddleware` atrapa la solicitud. Ve que el usuario no tiene historial.
3. El Middleware usa `random.choice()` en los nombres fijados y le abre un casillero virtual (una sesión) guardando "Rick Sanchez" y un reloj interno marcado en cero.
4. Pasa a `urls.py` buscando la dirección de inicio, luego pasa a `views.py` en la función `home`.
5. La vista ensambla el HTML con el saludo "Hello Rick Sanchez!" y los botones de Login. Se lo envía al navedor del usuario.
6. El navegador descarga la página y empieza a correr silenciosamente JavaScript. Pasan 42 segundos, JavaScript pregunta por detrás: "¿Cuál es mi nombre ahora?". 
7. En el servidor el middleware se da cuenta de que ya venció el tiempo y le cambia el nombre a "Jerry Smith". La petición JavaScript lee "Jerry" e inmediatamente repinta la palabra en pantalla.

### Flujo 2: El visitante crea una cuenta
1. Hace clic en "Register". Se ejecuta una petición GET y ve un formulario en blanco.
2. Rellena "Carlos", "contra123" y "contra123" y hace clic en Enviar. Envía una petición POST.
3. El código en `views.register_view` detecta el POST y tira los datos dentro de `RegistrationForm`.
4. `forms.py` verifica si "Carlos" existe (no existe) y si las contraseñas empatan (sí lo hacen). El formulario se declara Válido.
5. La vista manda a guardar permanentemente a "Carlos" encriptando su contraseña y se le inicia sesión automáticamente antes de forzar al navegador a llevarnos a "Inicio" (redirección).

### Flujo 3: Cerrar sesión
1. Carlos hace clic en el enlace "Log Out", el cual apunta a `/logout/`.
2. La vista `logout_view` llama a la función nativa `logout(request)`. Esta función purga automáticamente todos los identificadores de seguridad que Django había depositado en el explorador del usuario, limpiándolos y dejándolo sin una identidad validada.
3. Lo empuja de nuevo al "Inicio". Como ya no está validado, entra al **Flujo 1**, interceptado por nuestro middleware, el cual le genera automáticamente un nuevo perfil anónimo de 42 segundos.
