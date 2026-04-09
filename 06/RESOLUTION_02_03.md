# Explicación del Proyecto: Creación de Tips y Sistema de Votos
*(Ejercicios 02 y 03)*

Este documento detalla la implementación de las funcionalidades principales de nuestra aplicación web: la capacidad de que los usuarios inicien temas (Tips) y un sistema interactivo para votar positiva o negativamente estos temas.

A continuación, se explica paso a paso cómo se construyó cada pieza del sistema, por qué se tomaron ciertas decisiones técnicas y cómo interactúan entre sí.

---

## Conceptos Fundamentales

Antes de profundizar en el código, es importante comprender los siguientes conceptos de bases de datos y Django:

- **Modelos (Models):** Un modelo en Django es una representación en código Python de una tabla en la base de datos (como una hoja de cálculo gigante). Define qué tipo de datos se guardan y sus restricciones.
- **Claves Foráneas (ForeignKey):** Es una relación de "Uno a Muchos". Por ejemplo, un *Usuario* puede tener *Muchos Tips*, pero un *Tip* solo puede pertenecer a *Un Usuario*.
- **Muchos a Muchos (ManyToManyField):** Es un tipo de relación más compleja. Un *Usuario* puede dar "Me gusta" a *Muchos Tips*, y un *Tip* puede recibir "Me gusta" de *Muchos Usuarios*.
- **Migraciones (Migrations):** Cuando modificamos cómo se ven nuestros Modelos en Python, necesitamos "traducir" y aplicar esos cambios al motor de la base de datos real (SQLite, PostgreSQL, etc.). A este proceso se le llama crear y aplicar migraciones.

---

## Ejercicio 02: Creación del Sistema de "Tips"

**Objetivo:** Permitir que los usuarios autenticados creen consejos (tips) y que todos los visitantes (autenticados o no) puedan ver la lista de todos los tips ordenados por fecha.

### 1. El Modelo de Base de Datos (`models.py`)
Lo primero que necesitábamos era un lugar para guardar los Tips. Creamos una clase `Tip` con tres columnas:
- `content`: Un campo de texto grande (`TextField`) para guardar el consejo.
- `date`: Un campo de fecha (`DateTimeField`) al que le pusimos la propiedad mágica `auto_now_add=True`. Esto hace que el reloj del servidor estampe la hora exacta automáticamente apenas el tip se guarde por primera vez, sin que el usuario tenga que escribirla.
- `author`: Una relación (`ForeignKey`) apuntando al modelo oficial de `User` de Django. Le indicamos `on_delete=models.CASCADE` para que, como medida de limpieza, si algún día un usuario borra su cuenta del sitio, todos los tips que él escribió se borren automáticamente junto con su perfil.

### 2. El Formulario de Creación (`forms.py`)
Para que los usuarios puedan escribir un tip, Django nos ofrece una herramienta brillante llamada `ModelForm`. En lugar de tener que crear el formulario desde cero (como hicimos en el registro de usuarios), un `ModelForm` escanea la tabla de la base de datos y dibuja las casillas por nosotros.
Creamos la clase `TipForm` diciéndole a Django que se base en el modelo `Tip`, pero configuramos `fields = ['content']`. Esto significa que al usuario final el formulario *solo* le mostrará la gran caja de texto para escribir el consejo (el autor y la fecha los inyectaremos nosotros de forma secreta validada en el servidor por seguridad).

### 3. La Lógica de Visualización y Guardado (`views.py`)
Modificamos nuestra página principal (`def home(request):`) para que soporte dos tareas al mismo tiempo:
1. **Mostrar los tips:** Independientemente de si están logueados o no, hacemos que la base de datos nos devuelva *todos* los consejos usando `Tip.objects.all().order_by('-date')` (el guion menos significa orden de más reciente a más viejo).
2. **Procesar un nuevo tip:** Si entra una petición `POST` (alguien hizo clic en enviar formulario) confirmamos que esté logueado (`request.user.is_authenticated`). Si lo está, generamos el formulario, comprobamos que no haya caracteres raros (`form.is_valid()`) y utilizamos el truco `form.save(commit=False)`. 
*¿Qué significa `commit=False`?* Significa "Prepara este consejo, pero todavía no lo guardes en el disco duro porque le falta información". Aprovechamos esa pausa para forzar que el autor del consejo sea el usuario que hizo el envío (`tip.author = request.user`) y, ahora sí, ejecutamos `tip.save()` definitivo.

### 4. La Vista de Pantalla (`index.html`)
- Si hay una sesión activa (`{% if request.user.is_authenticated %}`), le mostramos el formulario de Bootstrap en un pequeño panel. Si no la hay, se esconde y mostramos un letrero azul invitándolos a registrarse si desean participar.
- Debajo de esa sección, corremos un bucle o ciclo iterativo (`{% for tip in tips %}`) que dibuja una por una las "tarjetas" con el contenido del tip, invocando además a `tip.author.username` y a `tip.date`.

---

## Ejercicio 03: Sistema de Votos Positivos y Negativos

**Objetivo:** Incorporar funcionalidad social para Upvotes (Me gusta), Downvotes (No me gusta) y botones para eliminar consejos. El mayor reto: un usuario solo puede dar *un voto* por tip, y si da *Me gusta*, debe soltar el *No me gusta* automáticamente para evitar trampas en la puntuación.

### 1. Actualizando el Modelo (`models.py`)
El _Subject_ nos dio una advertencia clave: *No dependan de simples contadores numéricos para los votos, ya que son inconsistentes*. 
En vez de crear un número (`votos = 5`), decidimos crear "Salas VIP" para cada tip usando `ManyToManyField`.
- Añadimos la relación `upvotes`.
- Añadimos la relación `downvotes`.
Esta genialidad de base de datos significa que un tip guarda listas o colecciones exactas de *quiénes* votaron por él. Si el usuario "Carlos" hace clic, simplemente metemos a "Carlos" a la sala VIP de `upvotes`. Si medimos cuántas personas hay en la sala (`upvotes.count()`), obtenemos nuestra puntuación verídica, segura e inflabible (es imposible que "Carlos" entre dos veces por error a la misma sala).

### 2. Formularios de Seguridad por cada Botón (`index.html`)
Cuando los usuarios hacen click en Upvote, Downvote o Eliminar, no lo hicimos mediante un simple enlace web (`<a href>`), sino que lo configuramos como mini formularios invisibles. 
**¿Por qué?** Porque en desarrollo web, cualquier operación que altere la base de datos (como contar un voto o borrar información) jamás debe hacerse mediante un simple *enlace GET*, ya que los navegadores pre-cargan los enlaces y robots maliciosos podrían hacer miles de votos automáticos. Lo aseguramos mediante botones POST cifrados con `{% csrf_token %}`.
A los usuarios no identificados simplemente les pintamos la placa decorativa (`badge`) con los números fijos pero les quitamos los botones.

### 3. La Matemática de las Reglas (Lógica en `views.py`)
Creamos tres nuevas vistas que no tienen página HTML, solo reciben la orden, y empujan rápidamente de regreso a la pantalla principal (`redirect`). Las empalmamos en `urls.py` usando `path('tip/<int:tip_id>/upvote/')` para poder saber numéricamente a cuál tip le dieron clic.

La lógica interna de los votos es un proceso de limpieza cruzada:
**Vista de Upvote:**
   1. Identificamos el Tip usando el número que llegó en la orden.
   2. Revisamos si el usuario ya está en la "sala" de `upvotes`. Si lo está, inferimos que su objetivo era "Anular su propio voto", así que lo echamos de la sala (`remove()`).
   3. Si no está en la sala, lo admitimos adentro (`add()`). 
   4. **El seguro anti-trampa:** Una vez que le dimos su voto positivo, vamos y miramos en la sala contraria (en `downvotes`). Si lo vemos allí metido, lo sacamos. De esta manera, garantizamos que, si alguien vota algo positivo, su voto negativo anterior desaparezca.

La vista de Downvote implementa exactamente el procedimiento inverso, y la vista de Eliminar es la más sencilla de todas, bastando con llamar a `tip.delete()` para erradicar el modelo entero del interior de la base de datos de Django para siempre.
