# Explicación del Proyecto: Autorizaciones y Permisos
*(Ejercicios 04 y 05)*

Este documento detalla cómo implementamos un sistema de seguridad y permisos basado en roles en nuestra aplicación de Django. A medida que una aplicación crece, no todos los usuarios registrados deben tener el mismo poder; aquí es donde entran en juego las Autorizaciones.

---

## Conceptos Fundamentales

- **Permisos por defecto de Django:** Cada vez que creamos un Modelo en Django (como nuestro modelo `Tip`), el marco de trabajo genera automáticamente cuatro permisos básicos de base de datos para él: `add_tip` (crear), `change_tip` (editar), `delete_tip` (borrar) y `view_tip` (ver).
- **Permisos Personalizados:** Si necesitamos restringir una acción que no encaja en "crear, editar, borrar o ver" (por ejemplo, dar un voto negativo), podemos instruir a Django para que cree permisos a la medida.
- **Doble Validación:** En desarrollo web seguro, ocultar un botón en la pantalla **(Frontend)** no es suficiente. Un usuario avanzado podría falsificar una petición para saltarse la interfaz. Por eso *siempre* debemos validar el permiso también en el código del servidor **(Backend)**.
- **Panel de Administración (Admin):** Es una herramienta integrada fantástica de Django que nos permite modificar la base de datos visualmente sin escribir código SQL, ideal para otorgar estos permisos a usuarios específicos.

---

## Ejercicio 04: Uso básico de autorizaciones (Eliminar Tips)

**Objetivo:** Permitir que solo el autor original de un Tip o los usuarios con privilegios especiales puedan borrarlo.

### 1. Seguridad en el Servidor (`views.py`)
En la vista `delete_tip`, no es suficiente con que el usuario haya iniciado sesión. Antes de procesar el borrado, interceptamos la petición e implementamos nuestra regla de negocio:
```python
def delete_tip(request, tip_id):
    # (Comprobaciones previas...)
    tip = get_object_or_404(Tip, id=tip_id)
    
    # 🔒 La regla de oro: ¿Es el autor? ¿O tiene carta blanca ('ex.delete_tip')?
    if request.user == tip.author or request.user.has_perm('ex.delete_tip'):
        tip.delete()
        
    return redirect('home')
```
Utilizar `has_perm('nombre_de_la_app.nombre_del_permiso')` lee directamente de la tabla de permisos de la sesión actual de forma súper optimizada.

### 2. Ocultando el Botón en la Plantilla (`index.html`)
Para no frustrar a los usuarios comunes mostrándoles un botón que no hace nada, bloqueamos el acceso visual utilizando la variable de contexto dinámica `perms` que nos inyecta Django en las plantillas:
```html
{% if request.user == tip.author or perms.ex.delete_tip %}
    <!-- Formulario de borrado de Tip -->
{% endif %}
```
Si el usuario no cumple ninguna de las dos condiciones, simplemente el botón no se dibuja en el HTML resultante.

---

## Ejercicio 05: Autorización Personalizada (Downvotes)

**Objetivo:** Considerando el carácter negativo de un *downvote*, el *Subject* nos pide que lo reservemos solo para ciertos usuarios avanzados. Además, el autor del tip sí puede auto-votarse negativo (si se arrepiente de lo que dijo). Debemos crear un **permiso a medida**.

### 1. Creación del Permiso Personalizado (`models.py`)
Dado que "Downvote" no es una acción base de datos común como `delete`, necesitamos forzar su creación. Añadimos una clase contenedora de meta-datos `class Meta` dentro de nuestro modelo `Tip`:
```python
class Tip(models.Model):
    # ... (campos del modelo) ...

    class Meta:
        permissions = [
            ("can_downvote", "Can downvote a tip"),
        ]
```
**Paso crítico:** Como esto alteró la "estructura" lógica de qué cosas debe rastrear la aplicación, tuvimos que empujar este cambio ejecutando constructores SQL. Corrimos los comandos `makemigrations` y `migrate` para inyectar este nuevo permiso permanentemente en la base de datos local SQLite.

### 2. Validación en el Servidor (`views.py`)
Modificamos fuertemente la función `downvote_tip` para rebotar amablemente hacia la página principal a cualquier usuario que intente forzar un downvote vía URL si no cuenta con dicha competencia:
```python
    if user != tip.author and not user.has_perm('ex.can_downvote'):
        return redirect('home')
```

### 3. Modificación Visual en la Interfaz (`index.html`)
El *Subject* recomendó "no solo borrar el botón". Para brindar una excelente experiencia de usuario (UX), optamos por mostrar el botón pero dejarlo gris e inaccesible (`disabled`), de esta manera pueden seguir viendo la estadística numérica de dislikes, pero no pueden participar.
```html
{% if request.user == tip.author or perms.ex.can_downvote %}
    <form method="POST" action="... ">
        <!-- Botón rojo vivo normal que hace POST -->
    </form>
{% else %}
    <button type="button" class="btn btn-sm btn-outline-danger m-0" disabled>
        &darr; Downvote ({{ tip.downvotes.count }})
    </button>
{% endif %}
```

---

## ¿Cómo Gestionar estos Permisos? (Activación de Admin)

La ventaja real de este sistema es que ahora el dueño del sitio tiene autoridad modular sin tocar una sola línea de código. 
1. Se expuso la URL de configuración `path('admin/', admin.site.urls)` en `urls.py`.
2. Se registró el módulo en `admin.py` (`admin.site.register(Tip)`).
3. Se crea un dueño maestro desde terminal usando `python3 manage.py createsuperuser`.
4. Ingresando a la ruta `http://.../admin`, tenemos una consola administrativa para alterar cada registro de usuario individual o asignarles nuestras nuevas llaves virtuales, como `ex | tip | Can delete tip` o la nueva marca original, `ex | tip | Can downvote a tip`.