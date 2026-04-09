# RESOLUTION - Exercise 04 - Bootstrap (Django 3 Advanced)

## Conceptos Clave
- **Integración de Frontend en Django**: Unir un framework de CSS (Bootstrap 5) a nuestro proyecto en Django para mejorar la interfaz de usuario (UI), haciéndola responsiva y visualmente más atractiva.
- **django_bootstrap5**: Aplicación que nos facilita la renderización de formularios, alertas y etiquetas CSS directamente desde nuestras plantillas, sin tener que construir manualmente cada clase de Bootstrap.

## Pasos Realizados

1. **Instalación y Configuración**:
   - Aseguramos que `django-bootstrap5` estaba en nuestros `requirements.txt` y lo cargamos en nuestro fichero `settings.py` bajo `INSTALLED_APPS`.
   
2. **Refactorización de `base.html` (Navbar & Layout)**:
   - Modificamos el archivo principal de layout (`base.html`). 
   - A través del tag `{% load django_bootstrap5 %}` inyectamos `{% bootstrap_css %}` y `{% bootstrap_javascript %}`.
   - Todo el contenedor se definió bajo `<div class="container mt-4">` para lograr márgenes y centrado adecuados.
   - Refactorizamos nuestro viejo menú `<nav>` para utilizar la navbar por defecto de Bootstrap (`navbar navbar-expand-lg navbar-light bg-light...`). El botón de *Login* se acomodó alineado usando `d-flex` en un form inline.

3. **Estilización de los Formularios (`publish.html`, `register.html`)**:
   - Aplicamos `{% load django_bootstrap5 %}` y cambiamos el aburrido `{{ form.as_p }}` por `{% bootstrap_form form %}`.
   - Botones ahora usan clases estándar: `class="btn btn-primary"`.

4. **Estilización de las Tablas (`article_list.html`, etc.)**:
   - Añadimos clases de tabla de Bootstrap: `table table-striped table-bordered`. Esto enriquece de inmediato las listas donde los usuarios consultan datos.

## Conclusión
Con `django-bootstrap5`, evitamos reescribir docenas de líneas de HTML por cada formulario y logramos replicar los wireframes propuestos por los pantallazos de prueba de la asignatura, permitiendo una experiencia de usuario mucho más pulida.
