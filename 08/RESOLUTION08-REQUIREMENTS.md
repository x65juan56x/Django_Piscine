# Análisis del archivo `requirement.txt`

## ¿Cómo se armó la lista con `pip freeze`?

El archivo `requirement.txt` fue generado automáticamente utilizando el comando:

```bash
pip freeze > requirement.txt
```

Este comando se debe ejecutar **dentro de un entorno virtual activado** (`django_venv`). Lo que hace `pip freeze` es escanear el entorno virtual activo y listar **todas** las librerías instaladas actualmente, junto con su versión exacta (`lired==X.Y.Z`).

A simple vista, el usuario instala solo un par de paquetes (por ejemplo, `pip install django channels daphne channels_redis`), pero el manejador de paquetes `pip` también instala silenciosamente todas las librerías secundarias (las *dependencias de tus dependencias*) que estas necesitan para poder funcionar. Al hacer `pip freeze`, capturamos todo el ecosistema. Esto certifica que el proyecto sea 100% reproducible en cualquier otra máquina de la escuela 42 sin fallos de compatibilidad por diferencia de versiones.

---

## ¿Por qué cada una de estas dependencias es necesaria?

Aunque nosotros solo solicitamos `Django`, `channels` y `daphne`, estas herramientas son sistemas muy complejos construidos a partir de librerías más pequeñas. Aquí tienes la explicación técnica de por qué cada dependencia listada en tu archivo existe:

### 1. El Núcleo de la Aplicación (Nuestras dependencias directas)
* **`Django==6.0.3`**: Nuestro framework web o núcleo central.
* **`channels==4.3.2`**: La extensión oficial de Django que le otorga soporte para WebSockets y peticiones asíncronas.
* **`daphne==4.2.1`**: El servidor ASGI mantenido por la misma gente de Django. Sustituye al viejo `runserver` WSGI.

### 2. Capa ASGI y Análisis de Base de Datos
* **`asgiref==3.11.1`**: Son las especificaciones asíncronas y las herramientas puente que permiten a Django (síncrono) hablar con protocolos asíncronos (ASGI). Es el corazón de Channels y Daphne.
* **`sqlparse==0.5.5`**: Analizador de código SQL no validador. Django lo usa internamente para procesar, formatear y ejecutar sus consultas a la base de datos subyacente de ORM.

### 3. Ecosistema Twisted (El Motor Asíncrono)
Daphne no hace el trabajo de red por sí solo. Por debajo, utiliza `Twisted`, uno de los motores asíncronos por eventos más antiguos y estables de Python. Las siguientes librerías vienen a causa de Twisted:
* **`Twisted==25.5.0`**: El framework de redes conducido por eventos.
* **`zope.interface==8.2`**: Provee el concepto de "Interfaces" a Python. Twisted la usa excesivamente para declarar cómo deben interactuar sus componentes internos.
* **`hyperlink==21.0.0`**: Estructuras inmutables para el análisis y creación de URLs puras.
* **`constantly==23.10.4`**: Librería pequeña que provee constantes simbólicas y enumeradores seguros, usada por la arquitectura de red de Twisted.
* **`Automat==25.4.16`**: Librería para manejar "Máquinas de Estados Finitos" (State machines). Ayuda a Twisted a saber en qué estado de una conexión se encuentra (ej. "conectando", "conectado", "cerrando").
* **`Incremental==24.11.0`**: Pequeña herramienta de Twisted para el manejo automatizado de numeración de versiones entre sus dependencias.

### 4. Implementación de Servidor WebSockets (`Autobahn`)
Twisted sabe cómo escuchar IPs y puertos TCP, pero alguien tiene que entender cómo procesar los *frames* puros del protocolo WebSocket. Para eso Daphne recurre a Autobahn:
* **`autobahn==25.12.2`**: Es la implementación open-source que traduce y codifica WebSockets para Twisted y Asyncio.
* **`txaio==25.12.2`**: Helper interno de compatibilidad. Ayuda a Autobahn a funcionar y mandar promesas indistintamente para Asyncio o para Twisted.
* **`cbor2==5.9.0`**: Librería para codificar en *Concise Binary Object Representation* (CBOR). Dependencia útil de Autobahn para serializaciones más rápidas que JSON.
* **`py-ubjson==0.16.1`**: Universal Binary JSON (UBJSON). Otra extensión de decodificación recomendada y traída por Autobahn para acelerar paquetes de redes.

### 5. La Capa de Channels (Redis y Serializaciones)
Para nuestro Ejercicio Inicial usamos `InMemoryLayer` en `settings.py`, pero la estructura que construiste en el `my_script.sh` incluyó inteligentemente a Redis, preparando el proyecto para escalamiento real (como requeriría Nginx/producción).
* **`channels_redis==4.3.0`**: El backend oficial de la capa de canales basado en el motor de Redis (el cual permite a múltiples workers de Django enviarse mensajes a las salas).
* **`redis==7.4.0`**: El cliente en Python puro que provee la conexión socket real hacia la base de datos externa de Redis.
* **`msgpack==1.1.2`**: Serializador ultra-veloz de datos binarios intermedios que usa `channels_redis` para compactar nuestros diccionarios antes de enviarlos a Redis.

### 6. Criptografía, Seguridad TLS / SSL
Cuando un servidor ASGI web como Daphne acepta conexiones (especialmente seguras `https` o `wss`), exige un gran esquema de verificación SSL manejada por la librería de encriptamiento base.
* **`cryptography==46.0.6`**: Provee el núcleo de operaciones criptográficas fiables en C y Python.
* **`cffi==2.0.0`**: "C Foreign Function Interface". Un puente vital que permite a Python (ej. a cryptography) llamar directamente e interactuar con funciones compiladas en código `C` del sistema operativo para encriptar súper rápido.
* **`pycparser==3.0`**: Analizador de código compilado de lenguajes C escrito en Python; ayuda a `cffi` a entender los encabezados en C del SO.
* **`pyOpenSSL==26.0.0`**: El contenedor (wrapper) o intérprete entre tu entorno y el OpenSSL real de la máquina para configurar las firmas de la web.
* **`service-identity==24.2.0`**: Asegura que el certificado presentado para un servidor SSL es realmente para la URL conectada, impidiendo ataques de *Man-in-the-Middle*.
* **`pyasn1==0.6.3`** y **`pyasn1_modules==0.4.2`**: Proveen codecs para ASN.1 (Abstract Syntax Notation One), que es la estructura mundial de datos base que utilizan los certificados digitales (como X.509 firmados asimétricamente) para describir su criptografía.
* **`idna==3.11`**: "Internationalized Domain Names in Applications". Usada para traducir nombres de dominio internacionales (que contienen tildes, caracteres árabes o emojis) al formato estándar US-ASCII validando la sintaxis del URL seguro frente al OpenSSL.

### 7. Formateadores Rápidos y Extras Fundamentales
* **`ujson==5.12.0`**: "Ultra JSON", un descodificador de JSON increíblemente extensible optimizado en C++ (mucho más rápido que el `import json` nativo). Daphne/Autobahn lo prefiere para leer mensajes de WebSockets inmediatamente.
* **`attrs==26.1.0`**: Agrega clases sin "boilerplate"; usada masivamente por todo Twisted y Autobahn para generar clases robustas sin tener que escribir los métodos `__init__` repetitivamente.
* **`typing_extensions==4.15.0`**: A veces las librerías necesitan indicar cómo se usarán tipos especiales de variables asíncronas en versiones anteriores o modernas. Este backport provee ese tipado dinámico para la comunidad en las declaraciones de funciones.
* **`packaging==26.0`**: Funciones primordiales y herramientas estándar que el ecosistema y `pip` utilizan para interpretar, armar y verificar números de sus mismas versiones en Python.
