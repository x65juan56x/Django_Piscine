# Explicación del Proyecto: Modelo de Usuario Personalizado y Reputación Dinámica
*(Ejercicio 06 - Final)*

En este último ejercicio, dimos un paso avanzado en el ecosistema de Django: reemplazar el  modelo de `User` que viene integrado de fábrica por uno nuestro, hecho a la medida. 

El requisito era crear una "economía" para nuestra aplicación donde la posibilidad de moderar o vigilar el sitio no recaiga solo en el Superadministrador dándole permisos a mano a la gente, sino en la reputación automática (Reputation) que consigue cada usuario basada en lo que aporta a la comunidad.

---

## 1. Configurando el CustomUser en Django

Sustituir el administrador de la cuenta (Usuario) en Django cuando el proyecto ya tiene datos es una operación de alto riesgo, pues Django liga todos los registros históricos al usuario antiguo.

### Paso A: Creando la clase en `models.py`
Para no reinventar la rueda (las contraseñas encriptadas, login, sesiones, etc.), heredamos toda la funcionalidad del usuario común de Django e inyectamos lo nuestro:
```python
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Aquí irá nuestro código de reputación
```
`AbstractUser` nos regala todos los atributos que ya conocíamos (`username`, `password`, `is_superuser`, y todo su núcleo de encriptación).

### Paso B: Instruir a Settings (`settings.py`)
Le dijimos formalmente a Django de ahora en adelante, cuando cualquier función pida `get_user_model()`, en realidad apunte a nuestro usuario mejorado:
```python
AUTH_USER_MODEL = 'ex.CustomUser'
```

### Paso C: Actualizar las Claves Foráneas de los Tips (`models.py`)
En ejercicios pasados, conectábamos el "Autor" y los listados de votos usando la variable genérica `User`. Tuvimos que cambiarla por `settings.AUTH_USER_MODEL` para que construya la nueva relación de base de datos sin generar una paradoja circular de importaciones:
```python
class Tip(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, ...)
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, ...)
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, ...)
```

---

## 2. La Matemática de la Reputación

El subject pedía las siguientes reglas de obtención de experiencia:
- +5 puntos por cada `upvote` recibido en un Tip creado por este usuario.
- -2 puntos por cada `downvote` recibido en un Tip creado por este usuario.
- Si un Tip se borra, todo su balance desaparece con él.

Para ello usamos el decorador de Python `@property`. Este decorador permite que un método interno (una función) se disfrace ante los ojos de la app como si fuera un atributo estático o columna constante, ahorrándonos guardar esta información en disco, calculándola *al vuelo* en el instante en que alguien pregunte por ella:

```python
class CustomUser(AbstractUser):
    @property
    def reputation(self):
        rep = 0
        # self.tips.all() nos arroja todos los tips escritos por ESTE usuario específico.
        for tip in self.tips.all():
            rep += tip.upvotes.count() * 5
            rep -= tip.downvotes.count() * 2
        return rep
```
*Garantía del requerimiento: Si se borra un Tip, el ciclo `for tip in self.tips.all()` ya no lo arrojará y simple y llanamente su impacto en la puntuación dejará de existir al instante en que volvamos a refrescar la propiedad.*

---

## 3. Automatizando las Autorizaciones (El corazón del ejercicio)

En los ejercicios pasados insertábamos permisos vía el panel de administración a las tablas, e invocábamos `request.user.has_perm('permiso')` desde Frontend y Backend.

El truco estelar para volver esto dinámico fue invadir y sobrescribir (`override`) esa mismísima gran función central interna de Django: `has_perm`, indicando que ahora las condiciones las ponemos nosotros numéricamente para *Downvotes* y *Deletes*, pero para el resto de permisos en el mundo de Django, los siga resolviendo usando la función original (mediante la invocación de `super()`).

```python
    def has_perm(self, perm, obj=None):
        if perm == 'ex.can_downvote' and self.reputation >= 15:
            return True
        if perm == 'ex.delete_tip' and self.reputation >= 30:
            return True
        return super().has_perm(perm, obj)
```

**Beneficio secundario espectacular:** Como las plantillas de visualización en `index.html` ya estaban blindadas con la etiqueta condicional de plantilla `{% if perms.ex.can_downvote %}`, ni siquiera tuvimos que volver a tocarlas. Simplemente le delegarán la pregunta al `CustomUser` y este les regresará `True` o `False` dinámicamente si los upvotes varían en tiempo real. 

---

## 4. Visualización de la Reputación 

El toque final estricto era mostrar la evaluación del autor junto al nombre de usuario. 

1. **En la tarjeta de cada Tip** (`index.html`): 
   Usamos la propiedad mágica para encajonarla entre paréntesis.
   ```html
   <small>By <strong>{{ tip.author.username }} ({{ tip.author.reputation }})</strong></small>
   ```

2. **En la barra superior de Sesión** (`base.html`):
   Lo añadimos para ver tu propio status global actual.
   ```html
   Hello {{ request.user.username }} ({{ request.user.reputation }})!
   ```

3. **La API Asíncrona (AJAX):** 
   Dado que en el ejercicio 00 programamos la barra superior para recargarse independientemente en un bucle JavaScript, no bastaba con solo ponerlo en `base.html`, tuvimos que actualizar la función interna `get_current_name` responsable de mandar la actualización de texto crudo de la sesión.
   ```python
   def get_current_name(request):
       if request.user.is_authenticated:
           name = f"{request.user.username} ({request.user.reputation})"
       # ...
       return JsonResponse({'name': name})
   ```

---
*Fin de la Serie Piscine Django. El ecosistema está enlazado a la perfección de principio a fin, priorizando la robustez de validación por bases de datos, prevención cruzada en M2M con `upvotes` relacionales, y la automatización dinámica de autorizaciones subyacentes con `AbstractUser`.*