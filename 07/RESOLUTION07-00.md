# Resolución Módulo 07: Django Advanced - Ejercicio 00

Este documento detalla la resolución y los conceptos clave aprendidos durante el **Ejercicio 00** del módulo "Advanced" de Django. En este módulo, abandonamos la separación de ejercicios estructurados en carpetas independientes para construir **un proyecto único y acumulativo** (`advanced`), que irá creciendo con cada ejercicio implementando nuevas funcionalidades.

## Conceptos Core del Ejercicio 00

El Ejercicio 00 sienta las bases del proyecto, enfocándose en la restricción más drástica impuesta por el subject: **Está ESTRICTAMENTE PROHIBIDO usar vistas basadas en funciones (FBV)**, así como el "hardcoding" (escribir en crudo) las URLs. Todo debe abstraerse en **Vistas Genéricas basadas en Clases (CBV)** y variables referenciadas usando el motor de URLs nativo.

### 1. Preparación del Entorno y PostgreSQL (Docker)
En lugar de SQLite, hemos optado por PostgreSQL. Para ello:
1. Instalamos `psycopg2-binary` en el entorno virtual, actuando como conector entre el ORM de Django y PostgreSQL.
2. Utilizamos un `docker-compose.yml` para levantar la BBDD en un contenedor.
3. **Resolución de conflictos de puertos**: Al detectar que el puerto `5432` nativo ya estaba en uso por un servicio local, mapeamos el puerto del contenedor al `5433` indicándolo en nuestro `settings.py` de Django. Esto aísla nuestro desarrollo limpio sin interferir con otros procesos del SO.

### 2. Creación de los Modelos
Hemos creado dos modelos siguiendo escrupulosamente los requisitos, incluyendo metadatos básicos y claves foráneas `ForeignKey`:

```python
from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=64, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    created = models.DateTimeField(auto_now_add=True, null=False)
    synopsis = models.CharField(max_length=312, null=False)
    content = models.TextField(null=False)

    def __str__(self):
        return self.title

class UserFavouriteArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.article.title
```
> **Nota de Diseño**: El campo `created` se auto-asigna a la fecha de creación utilizando `auto_now_add=True`. Todo modelo sobrescribe su método `__str__` para devolver el título amigable al Admin Panel.

### 3. Vistas Básicas en Clases (Generic CBVs)
El hito principal del ejercicio fue la arquitectura basada en las clases genéricas de *Django `django.views.generic`*:

- **Listar Artículos (`ArticleListView`)**: Hereda de `ListView`. Automáticamente va a la BBDD, recolecta todo de `model = Article` y se lo envía a un template que nombramos por defecto. Te ahorra hacer en crudo el código `Article.objects.all()`.
- **Login (`LoginView`)**: Utilizamos la vista incorporada de `django.contrib.auth.views`. En vez de programar una lógica manual de validación de contraseñas, enrutamos este componente que ya valida y procesa el POST correctamente.
- **Redirección de la raíz (`RedirectView`)**: Al recibir un request en `/`, es interceptado por un Redirect que emite un código HTTP 302 redirigiendo a la ruta principal de "Articles". 

### 4. Zero Hard-URLs y Patrones de Vistas en el template
Para cumplir con "Implementing a 'hard' url is STRICTLY prohibited":
- Cada ruta registrada lleva adjunto un kwarg `name="..."`. Ej: `path('articles/', ArticleListView.as_view(), name='articles')`.
- En las plantillas (`{% url 'articles' %}`), o en el enrutamiento interno (`RedirectView.as_view(pattern_name='articles')`), llamamos a esa etiqueta literal, nunca a la ruta estática explícita.
- Para el post-login y log-out general configuramos en `settings.py`:
  ```python
  LOGIN_REDIRECT_URL = 'articles'
  LOGOUT_REDIRECT_URL = 'login'
  ```

### 5. Configuración de Fixtures (`initial_data.json`)
El Subject requería "at least five articles examples from three different users". En vez de usar el Admin Panel de forma manual repetitiva tras cada refactorización, lo idealizamos de manera profesional creando el directorio y cargando un archivo `.json` mediante **Data Fixtures**.

Un fixture es una colección de datos de los modelos que Django sabe interpretar e introducir a su motor de base de datos independientemente de si usas SQLite o Postgres. Los inyectamos ejecutando:
`python3 manage.py loaddata initial_data.json`

## Resumen del Workflow de Comandos Utilizados

```bash
# Iniciar DB en Docker esquivando el puerto 5432 local
docker compose up -d

# Realizar y aplicar migraciones tras configurar postgres/psycopg2
python3 manage.py makemigrations
python3 manage.py migrate

# Cargar los datos Mock (los usuarios y artículos dummy)
python3 manage.py loaddata initial_data.json

# Inicializar y comprobar proyecto
python3 manage.py runserver
```

---
*Fin del resumen Ex00 - Módulo 07 Advanced*. Preparados para las ampliaciones venideras sobre estos cimientos.