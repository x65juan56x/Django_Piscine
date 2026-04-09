# Resolución Módulo 07: Django Advanced - Ejercicio 02

Este documento explicativo aborda la resolución técnica y las bases teóricas del **Ejercicio 02** ("Generic Class - CreateView"). En este peldaño, hemos aprendido cómo agilizar el proceso de insertar datos en la base de datos dejando de lado la programación farragosa del manejo de variables `POST` y aprovechando la extrema potencia de la vista genérica enfocada a la creación: `CreateView`.

## Conceptos Core del Ejercicio 02

Se nos requirió la implementación de tres lógicas de creación o guardado de datos en la base de datos: registrar cuentas, crear nuevos artículos y guardar artículos en tu biblioteca de favoritos.

### 1. El poder de `CreateView` y renderizado de formularios
La vista genérica `CreateView` se encarga por debajo de comprobar si la petición del usuario es `GET` (el usuario quiere ver e imprimir el formulario vacío de la web) o `POST` (el usuario está mandando los datos rellenos para que la web los procese).

Además, para evitarnos escribir `<input type="...">` manuales, en el HTML tan solo llamamos a `{{ form.as_p }}` (o como tablas con `as_table`).

### 2. Registro con Formularios listos para usar (`UserCreationForm`)
El primer requerimiento era crear una vista para "Register" (Registrar usuario). Django ya tiene un formulario completo que nos valida contraseñas, confirma que coinciden y verifica si el nombre de usuario ya está cogido. Lo inyectamos en nuestro `CreateView` usando `form_class`:

```python
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'articles/register.html'
    success_url = reverse_lazy('login')
```
*`reverse_lazy()` se usa aquí porque el archivo de URLs se compila al vuelo, es más seguro y evita problemas de carga cíclica de dependencias.*

### 3. Publicación e inyección de autor (`form_valid`)
Para la creación de artículos ("Publish"), la regla estricta indicaba: *The 'author' field must not be displayed.* 
¿Cómo pasamos un dato a la base de datos que obligatoriamente no puede pasarnos el usuario a través de la plantilla? 
**Interceptando la validación (`form_valid`)** de la clase `CreateView`:

```python
class PublishView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'synopsis', 'content'] # Autor excluido deliberadamente
    template_name = 'articles/publish.html'
    success_url = reverse_lazy('publications')

    # Este método de Django salta justo cuando todo el texto ha sido rellenado con éxito
    def form_valid(self, form):
        # Inyectamos de fondo a la instancia el usuario de nuestra sesión actual
        form.instance.author = self.request.user
        return super().form_valid(form)
```

### 4. Botones de "Agregar" con Formularios Ocultos (Post Invisibility)
El último reto era construir la lógica de "Add to favourite" y ubicarla directamente dentro del detalle de cada artículo.
"The 'article' field must be pre-filled [...] No field must be visible". 

Para solucionarlo de forma elegante sin crear una página extra aburrida preguntando "Desea usted agregar a favoritos?", renderizamos en el propio `article_detail.html` un tag de formulario `<form>` conteniendo un `<input type="hidden">`:

```html
<form action="{% url 'add_favourite' %}" method="post">
    <!-- El token CSRF de seguridad, ¡Obligatorio en todo POST de Django! -->
    {% csrf_token %}
    
    <!-- Campo oculto HTML rellenado usando Jinja pasándole el ID base -->
    <input type="hidden" name="article" value="{{ article.id }}">
    
    <button type="submit">Add to Favourites</button>
</form>
```

Esta mini-sección dispara al backend (`AddFavouriteView`) que, aplicando el mismo truco del `form_valid` explicado en el punto anterior, coge en segundo plano a tu usuario `user=self.request.user`, atrapa tu artículo que venía oculto en el post, y los cruza en un nuevo registro en tabla `UserFavouriteArticle`.

---
*Fin de la documentación del Ex02 - Módulo 07 Advanced.*