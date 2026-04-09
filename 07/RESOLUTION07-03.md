# Resolución Módulo 07: Django Advanced - Ejercicio 03

Este documento explica las soluciones técnicas implementadas durante el **Ejercicio 03** ("Template tags and Filters"). El principal desafío de este nivel ha sido trasladar responsabilidades que normalmente tendríamos en las Vistas (Backend) directamente al Sistema de Plantillas (Frontend) de Django.

## Conceptos Core del Ejercicio 03

El *Subject* requería construir un menú global persistente en todas las páginas e incluir herramientas de filtrado directo sobre la lista de artículos para alterar su visualización sin cambiar el modelo de base de datos.

### 1. Inyección Global del Formulario de Login (Custom Template Tags)
Uno de los puntos más complejos del *Subject* era: *"Login functionality. you must include the whole form IN the menu... accessible from every page"*.
Normalmente, una vista como `ArticleListView` no le pasa al HTML de contexto el formulario de autenticación `AuthenticationForm`. Para no tener que sobrescribir la función `get_context_data` en **todas** nuestras vistas una por una, creamos un **Custom Template Tag**:

1. Creamos la carpeta `templatetags/` dentro de la app `articles` con su respectivo `__init__.py`.
2. Creamos el archivo `login_tags.py` donde instanciamos el formulario directamente:
   ```python
   from django import template
   from django.contrib.auth.forms import AuthenticationForm

   register = template.Library()

   @register.simple_tag(takes_context=True)
   def get_login_form(context):
       # Si la vista actual (ej: LoginView) ya pasó un formulario (con errores), lo usamos.
       form = context.get('form', None)
       if form and isinstance(form, AuthenticationForm):
           return form
       # Si no hay formulario en el contexto, creamos uno limpio.
       return AuthenticationForm()
   ```

Luego, en el `base.html`, simplemente cargamos este "Tag" mediante `{% load login_tags %}` y guardamos su resultado en una variable de Jinja para renderizarlo con `{{ login_form.as_p }}`.

### 2. Filtros de Plantilla Integrados (Built-in Filters)
Django cuenta con una sintaxis de filtros que se aplican usando el símbolo `|` (pipe) dentro de las dobles llaves `{{ variable|filtro }}`. Estos fueron dictados estrictamente por el sujeto:

- **Truncado de strings (`truncatechars`)**:
  Para reducir la sinopsis a un máximo de 20 caracteres y añadir los puntos suspensivos automáticamente, escribimos:
  `{{ article.synopsis|truncatechars:20 }}`

- **Ordenamiento invertido sin tocar el ORM (`dictsortreversed`)**:
  Para mostrar la lista de artículos ordenada desde el más nuevo al más antiguo sin modificar la consulta SQL ni la vista genérica, aplicamos el filtro de ordenado general sobre el tag `{% for %}`:
  `{% for article in articles|dictsortreversed:"created" %}`

- **Tiempo Transcurrido (`timesince`)**:
  Para calcular inmediatamente cuánto tiempo hace que se publicó el artículo respecto a la hora y fecha actual (ej. "2 hours, 10 min"), se usó otro filtro nativo potente en una nueva columna:
  `{{ article.created|timesince }}`

### 3. Persistencia de Errores
El *Subject* requería que: *"this page must always display error messages if the form is invalid"*. 
Nuestra lógica combinada resuelve esto maravillosamente: 
Si un usuario introduce mal la contraseña desde `publications/`, el submit viaja a la URL `/login/` (que está configurada en nuestro `urls.py`). Cuando `LoginView` detecta el fallo, devuelve la página `/login/` (que hereda de `base.html`) inyectando el objeto `form` con todos sus errores adjuntos. Nuestro Custom Template Tag detecta que el objeto existe en este contexto y lo renderiza de forma prioritaria, enseñando dinámicamente los errores en rojo dentro del menú global.

---
*Fin de la documentación del Ex03 - Módulo 07 Advanced.*