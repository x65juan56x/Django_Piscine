# Explicación de los Templates (Plantillas) en Django
*(Vistas y Frontend con Bootstrap)*

En Django, la interfaz gráfica («Frontend») se maneja mediante un sistema de plantillas (Templates) que permite combinar código HTML estático con procesamiento dinámico de Python (a través de etiquetas como `{% %}` y variables como `{{ }}`). 

En este proyecto, hemos usado **Django Bootstrap 5** para estilizar la página de manera rápida y profesional.

A continuación, se detalla la arquitectura de las 4 plantillas utilizadas: `base.html`, `index.html`, `login.html` y `register.html`.

---

## 1. La Arquitectura de Herencia
El proyecto utiliza un sistema de herencia. Todas las páginas de la web (`index`, `login`, `register`) "heredan" de un esqueleto maestro llamado `base.html`. 

Esto significa que no tenemos que escribir el `<head>`, los menús de navegación o importar los scripts de Bootstrap en cada archivo. Se escribe una sola vez en el padre, y los hijos se inyectan dentro del bloque llamado `{% block content %}`.

---

## 2. Archivo: `base.html`
**¿Quién / Cuándo lo llama?**
Ninguna vista (View) de Python llama directamente a este archivo. Sin embargo, **todos** los otros templates lo solicitan en su primera línea usando la etiqueta `{% extends 'ex/base.html' %}`.

**¿Qué contiene y cómo se ve en pantalla?**
- Actúa como el armazón o "Master Page" de todo el sitio web.
- Contiene la barra de navegación superior (Navbar). Esta barra intercepta si el usuario está autenticado (`request.user.is_authenticated`) para mostrarle los botones de "Login / Register" o el botón de "Log Out".
- Contiene el script de JavaScript (AJAX/Fetch) en la parte inferior que recarga el saludo (`#user-greeting`) cada 2 segundos buscando el nombre al azar o la reputación.

**Uso de Bootstrap:**
- `{% bootstrap_css %}` y `{% bootstrap_javascript %}`: Importan mágicamente todos los archivos y librerías de Bootstrap al proyecto en el `<head>`.
- `navbar navbar-dark bg-dark`: Crea una barra de navegación superior de color gris oscuro/negro.
- `container-fluid`: Hace que el contenedor de la Navbar ocupe todo el ancho de la pantalla.
- `d-flex justify-content-between align-items-center`: Usa *Flexbox* para alinear elementos horizontalmente, empujando el logo a la izquierda y el saludo a la derecha.

---

## 3. Archivo: `index.html`
**¿Quién / Cuándo lo llama?**
Es llamado por la vista `home` en `views.py` cuando se visita la raíz del sitio web (`/`).

**¿Qué contiene y cómo se ve en pantalla?**
- Muestra el formulario para publicar un nuevo "Life Pro Tip" en la parte superior, pero **sólo** si el usuario está conectado. Si no lo está, pinta un cartel azul de aviso.
- Debajo, contiene un bucle `{% for tip in tips %}` que recorre todos los tips de la base de datos y los dibuja uno sobre otro.
- Gestiona los botones para votar (Upvote / Downvote) y borrar (Delete) evaluando condicionales lógicos (`{% if request.user == tip.author or perms.ex... %}`). 

**Uso de Bootstrap:**
- `col-md-8 mx-auto`: Limita el ancho del contenido a 8/12 columnas de Bootstrap y lo centra en la pantalla (dejando márgenes a los lados en pantallas grandes).
- `card shadow-sm`: Convierte los formularios y cada uno de los Tips en "Tarjetas" (cajas con bordes redondeados y una pequeña sombra para que parezcan elevadas).
- `alert alert-info`: Dibuja un cuadro de información azul que dice "Log in or register to share...".
- `{% bootstrap_form form %}`: Esta es una etiqueta especial de Django-Bootstrap que toma el formulario limpio de Python (`TipForm`) y lo convierte en HTML puro con todas las clases de diseño y validación automática de Bootstrap integradas.

---

## 4. Archivos: `login.html` y `register.html`
**¿Quién / Cuándo los llama?**
Son llamados por las vistas `login_view` (`/login/`) y `register_view` (`/register/`) en `views.py` respectivamente. 

**¿Qué contienen y cómo se ven en pantalla?**
- Ambas plantillas son estructuralmente idénticas. Su única función es pintar los formularios de inicio de sesión o creación de cuenta.
- Inyectan sus contenidos justo en el medio del bloque `{% block content %}` de `base.html`.

**Uso de Bootstrap:**
- `row justify-content-center`: Se asegura de que la fila contenedora empuje todo su contenido al centro exacto de la pantalla.
- `col-md-6`: Hace que los formularios no ocupen todo el ancho de lado a lado, sino exactamente la mitad de la pantalla (6 columnas de 12), logrando un diseño más estético y parecido a los "login cards" modernos.
- `btn btn-primary w-100` y `btn btn-success`: Convierten un simple enlace/boton en un botón estilizado (Azul para primario/registro, Verde para success/login). El utilitario `w-100` (width 100%) hace que el botón se estire y ocupe todo el ancho del formulario.
- Al igual que en `index`, recurren a la magia de `{% bootstrap_form form %}` para que campos como el usuario y contraseña tomen el aspecto moderno de Bootstrap inmediatamente.