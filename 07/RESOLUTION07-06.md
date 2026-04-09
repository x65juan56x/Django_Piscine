# Resolución Módulo 07: Django Advanced - Ejercicio 06

Este documento explica las soluciones implementadas durante el **Ejercicio 06** ("Testing"). El objetivo fue crear una suite de pruebas para verificar las reglas de negocio de la aplicación y arreglar cualquier vulnerabilidad que las pruebas revelaran.

## Conceptos Clave del Ejercicio 06

En Django, el testing se basa en la extensión de `unittest.TestCase` contenida en `django.test.TestCase`. Esta interfaz nos otorga un cliente de prueba robusto que puede simular peticiones `GET` y `POST` aislando el entorno en una base de datos temporal que se limpia después de cada test.

### 1. Pruebas de Acceso a Vistas Privadas (Login Required)
La primera instrucción requería *"favourites views, publications and publish as well as their templates are only accessible by registered users."*

Para comprobar esto adecuadamente:
- Escribimos `test_favourites_requires_login`, `test_publications_requires_login` y `test_publish_requires_login` en `articles/tests.py`.
- **Qué probamos**: Que hacer una petición GET como usuario anónimo devuelva un redireccionamiento HTTP (código 302) a la página de login (la URL devuelta por `reverse('login')`), pero devuelva éxito absoluto (`200 OK`) luego de usar `self.client.login()`.
- **Fallo original**: El enrutamiento de Internacionalización (i18n) introducía un error sutil. `LANGUAGE_CODE = 'en-us'` en el sistema generaba que las reversiones de URL para redirecciones buscaran `/en-us/login/`, pero nuestro prefijo válido en `LANGUAGES` era solo `/en/`. Las peticiones POST fracasaban dando un error `404` por pérdida de seguimiento del middleware entre subdirecciones.
- **Solución implementada**: Corregimos `LANGUAGE_CODE = 'en'` globalmente para que coincida limpiamente con nuestro `prefix_default_language` y nos aseguramos de que cada vista privada estuviese construida heredando de `LoginRequiredMixin`.

### 2. Bloquear Registro a Usuarios Autenticados
La segunda regla fue: *"A registered user cannot access the new user creation form."*

- **El test**: Construimos `TestRegisterViewAccess.test_register_denied_for_registered`. Validamos que un usuario anónimo recibiera un código `200` y al estar logueado no pudiera ver la página (idealmente devolviendo un 302 hacia el inicio o 403 denegado).
- **El error**: Nuestra `RegisterView` era un `CreateView` normal que no prestaba atención a la sesión actual, fallando nuestro test al devolver un `200` a un usuario ya registrado.
- **La solución**: Usamos `UserPassesTestMixin`. Programamos `def test_func(self):` para verificar explícitamente `not self.request.user.is_authenticated`. Anulamos el método `handle_no_permission` para que no emita un error feo `403 Forbidden`, sino que reconduzca amigablemente (`redirect`) al usuario logueado de vuelta a `articles/`.

### 3. Restricción de Favoritos Duplicados
La tercera regla establecía: *"A user cannot add the same article twice in their favorite list."*

- **El test**: `test_cannot_add_same_favourite_twice` probó agregar un favorito usando una petición POST válida con estado logueado (`self.client.post(...)`). Seguido a eso, se emitía la misma petición, aseverando vía `self.assertEqual(...)` que el conteo final en la base de datos se mantuviera exactamente en `1` registro y no en `2`.
- **El error**: Al ejecutarlo, nuestra vista reintentaba la creación y arrojaba `AssertionError: 0 != 1` en la prueba, ya que no había restricciones en la Base de Datos ni interceptores formales.
- **La solución**: 
  1. Fuimos a `models.py` para la clase `UserFavouriteArticle` y aplicamos a nivel Base de Datos una restricción `unique_together = ('user', 'article')` y construimos las migraciones pertinentes.
  2. Fuimos a la vista `AddFavouriteView` y alteramos `form_valid()`. Capturamos dinámicamente si el modelo ya contenía la relación usuario-artículo, de manera que la vista retorne un redireccionamiento inmersivo en lugar de reventar provocando un `IntegrityError` o un error `500 Server Error`.

Con todos estos ajustes, al correr `python3 manage.py test articles`, Django reportó `Ran 6 tests in 2.366s - OK`, dando el ejercicio por satisfactoriamente evaluado y la aplicación perfectamente blindada ante usos erráticos.

---
*Fin de la documentación del Ex06 - Módulo 07 Advanced.*