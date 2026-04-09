# Resolución Módulo 07: Django Advanced - Ejercicio 05

Este documento explica las soluciones técnicas implementadas durante el **Ejercicio 05** ("Internationalization"). El objetivo principal de este ejercicio fue traducir toda la funcionalidad de Artículos y la interfaz del sitio, basándose en un prefijo presente en la URL (ej. `/en/articles/`, `/es/articles/`).

## Conceptos Core del Ejercicio 05

Django proporciona un robusto framework de internacionalización (i18n) y localización (l10n) que permite adaptar la aplicación a múltiples idiomas sin necesidad de duplicar vistas o plantillas.

### 1. Configuración Global (`settings.py`)
Para habilitar el soporte multi-idioma, modificamos varios aspectos clave en la configuración:

- **Middlewares**: Añadimos `django.middleware.locale.LocaleMiddleware` justo después del `SessionMiddleware`. Este middleware es el encargado de determinar el idioma actual de la petición analizando la URL o la sesión del usuario.
- **Idiomas Soportados**: Definimos la tupla `LANGUAGES` restringiendo la aplicación a los dos únicos idiomas requeridos: Inglés (`en`) y Español (`es`).
- **Ruta de Traducciones**: Configuramos `LOCALE_PATHS` para indicarle a Django dónde debe buscar y guardar los archivos de traducción (la carpeta `locale/` en la raíz del proyecto).
- **Activación general**: Nos aseguramos de que `USE_I18N = True`.

### 2. Enrutamiento con Prefijo de Idioma (`urls.py`)
El *Subject* requería que el idioma estuviese dictaminado por la URL. Para lograrlo, modificamos `advanced/urls.py` utilizando la función `i18n_patterns`:

```python
from django.conf.urls.i18n import i18n_patterns

urlpatterns += i18n_patterns(
    path('', include('articles.urls')),
    prefix_default_language=True,
)
```
Esto provoca que todas las rutas de la aplicación `articles` queden automáticamente envueltas por el prefijo del idioma actual, mientras que rutas internas como `admin/` pueden mantenerse excluidas. Adicionalmente, agregamos la ruta de Django `path('i18n/', include('django.conf.urls.i18n'))` para habilitar el endpoint interno (`set_language`) que procesa los cambios de idioma.

### 3. Selector de Idiomas Dinámico (`base.html`)
Para permitir al usuario alternar rápida y limpiamente entre inglés y español de forma dinámica, construimos un formulario invisible de tipo *inline link* ubicado estratégicamente en la esquina superior derecha del cuerpo principal:

```html
<form action="{% url 'set_language' %}" method="post" class="d-inline">
    {% csrf_token %}
    <input name="next" type="hidden" value="{{ request.get_full_path|slice:'3:' }}">
    {% get_current_language as LANGUAGE_CODE %}
    {% if LANGUAGE_CODE == 'en' %}
      <button type="submit" name="language" value="es" class="btn btn-link text-info text-decoration-none p-0 m-0">Cambiar a español</button>
    {% else %}
      <button type="submit" name="language" value="en" class="btn btn-link text-info text-decoration-none p-0 m-0">Change to English</button>
    {% endif %}
</form>
```
Este formulario envía una petición POST a la vista nativa `set_language`. El campo oculto `next` se encarga de redirigir al usuario exactamente a la misma página en la que estaba, pero con el prefijo de URL actualizado. Usamos `request.get_full_path|slice:'3:'` de forma hábil para recortar el prefijo de idioma anterior y evitar rutas anidadas indeseadas como `/es/en/articles/`.

### 4. Preparación de Plantillas (Template Tags)
El trabajo más laborioso consistió en adaptar cada uno de los archivos HTML:
1. Añadir `{% load i18n %}` al inicio de cada plantilla (después de los tags de herencia `extends`).
2. Envolver todo el texto estático visible para el usuario con el tag de traducción `{% trans "Texto original" %}`.

Esto instruye al motor de plantillas de Django a buscar dinámicamente el equivalente traducido del string en los archivos de idioma en tiempo de ejecución.

### 5. Extracción y Compilación de Traducciones (gettext)
Una vez preparadas las plantillas, el flujo de trabajo de traducción requirió la herramienta GNU `gettext`:

- **Generación (`makemessages`)**: Ejecutamos `python3 manage.py makemessages -l es`. Esto escanea todo el código fuente y HTML en busca de tags `{% trans %}` y genera el archivo `.po` (Portable Object) en la carpeta de idioma `locale/es/`.
- **Traducción**: El archivo `.po` contiene ahora pares de `msgid` (texto original) y `msgstr` (traducción). Mediante un script automatizado escrito en Python (`translate_po.py`), rellenamos e inyectamos secuencialmente nosotros mismos las cadenas traducidas al español para evitar rellenar el archivo a mano línea por línea.
- **Compilación (`compilemessages`)**: Finalmente, ejecutamos `python3 manage.py compilemessages`. Este comando convierte los archivos `.po` legibles por humanos en binarios `.mo` (Machine Object) altamente optimizados, que Django utiliza para resolver las traducciones instantáneamente y sin penalización de rendimiento.

---
*Fin de la documentación del Ex05 - Módulo 07 Advanced.*