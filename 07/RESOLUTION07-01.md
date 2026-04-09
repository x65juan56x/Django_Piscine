# Resolución Módulo 07: Django Advanced - Ejercicio 01

Este documento detalla la resolución teórica y técnica del **Ejercicio 01** de este módulo unificado. El objetivo principal de este paso ha sido dotar de profundidad al ecosistema de vistas, usando nuevamente **única y exclusivamente Class-Based Views genericas** (`ListView`, `DetailView`) e integrando mecánicas de restricción de acceso de usuarios.

## Conceptos Core del Ejercicio 01

El *Subject* exigía agregar cuatro endpoints nuevos (`Publications`, `Detail`, `Logout`, `Favourites`), requiriendo cruces de información con el usuario actualmente logueado. 

### 1. Vistas Restringidas y Mutación del QuerySet (`LoginRequiredMixin`)
Cuando queremos que un listado o cualquier vista bloquee a usuarios anónimos de acceder a secciones protegidas (como "Mis publicaciones" o "Mis favoritos"), Django provee un "Mixin" súper útil: `LoginRequiredMixin`. 

Al heredar de él, la vista automáticamente redirigirá a los usuarios no identificados a la página de login. 

Además, para filtrar la base de datos de manera que el usuario **solo vea sus propios artículos** o **sus propios favoritos**, debemos sobrescribir la función `get_queryset` de estas Vistas Genéricas:

```python
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article

class PublicationsView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'articles/publications.html'
    context_object_name = 'articles'

    # Interceptamos la consulta a Base de Datos
    def get_queryset(self):
        # request.user contiene el objeto del usuario logeado en este momento
        return Article.objects.filter(author=self.request.user)
```

Esa misma mecánica fue extendida idénticamente a los Favoritos (clase `FavouritesView`) apuntando al modelo `UserFavouriteArticle` cruzando `user=self.request.user`.

### 2. Vistas de Detalle (`DetailView`)
El componente de *Django Views* `DetailView` toma un objeto de tu modelo y un "Primary Key" (`pk`) de los parámetros de la URL base para buscar automáticamente un único registro en la base de datos y mandarlo a tu plantilla como contexto:

```python
# articles/views.py
from django.views.generic import DetailView

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'  # Genera el objeto 'article' dinámico

# articles/urls.py
path('detail/<int:pk>/', views.ArticleDetailView.as_view(), name='detail')
```

Esto automatiza todo el proceso de atrapar el id de la url, verificar que existe (lanzando `404` si no), y mandarlo al layout (ej: `{{ article.author }}`).

### 3. LogOut Directo (`LogoutView`)
No necesitamos vistas manuales ni plantillas para hacer "Log Out" (a menos que quieras una confirmación). 
Hemos usado directamente el sistema nativo del módulo de autenticación genérico (`auth_views.LogoutView`) y enrutar la redirección final mediante el kwarg `next_page`.

```python
path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
```

### 4. Layout Base Unificado (`base.html`)
Dado que se añadió el enlace de `Logout`, aprovechamos la flexibilidad nativa del motor de plantillas Jinja con `{% if request.user.is_authenticated %}` para montar todos estos botones solo si la sesión del cliente está activa y válida.

```html
{% if request.user.is_authenticated %}
    <a href="{% url 'publications' %}">Publications</a> |
    <a href="{% url 'favourites' %}">Favourites</a> |
    <span>Hello, {{ request.user.username }}</span> |
    <!-- Botón nativo POST de logout por seguridad -->
    <form action="{% url 'logout' %}" method="post" style="display:inline;">
        {% csrf_token %}
        <button type="submit">Logout</button>
    </form>
{% endif %}
```

> **Nota Adicional de Seguridad**: En Django 4.x/5, el `LogoutView` y la deslogueación general de perfiles espera fuertemente peticiones tipo método `POST` y su debida inclusión del CSRF Token de seguridad. Esto previene ataques CSRF en los que un hacker puede desloguear a los usuarios remotamente mediante un simple `<a href='logout'>` de GET.

### 5. Edición de Fixtures Dinámica
Para testear con eficiencia, en vez de usar el Admin Panel de Django, creamos un micro-script en la consola de Django (`python3 manage.py shell`) que inyecta programáticamente dos instancias válidas en tu tabla de Favoritos pre-existentes modificando y grabando el `initial_data.json` y ejecutando `loaddata`. El conocimiento de cómo manipular JSON serializados y la carga programática acelera increíblemente las fases de testeo inicial (mocking).

---
*Fin de Resolución del Ejercicio 01.*