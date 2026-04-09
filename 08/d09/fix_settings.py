with open("d09/settings.py", "r") as f:
    content = f.read()

import re
content = re.sub(r"INSTALLED_APPS = \[\n    'daphne',\n    'chat',\n    'daphne',\n    'chat',\n", "INSTALLED_APPS = [\n    'daphne',\n    'chat',\n", content)
content = re.sub(r"WSGI_APPLICATION = 'd09.wsgi.application'\nASGI_APPLICATION = 'd09.asgi.application'\n\nCHANNEL_LAYERS = \{\n    'default': \{\n        'BACKEND': 'channels.layers.InMemoryChannelLayer',\n    \}\n\}\nASGI_APPLICATION.*", "WSGI_APPLICATION = 'd09.wsgi.application'\nASGI_APPLICATION = 'd09.asgi.application'\n\nCHANNEL_LAYERS = {\n    'default': {\n        'BACKEND': 'channels.layers.InMemoryChannelLayer',\n    }\n}", content, flags=re.DOTALL)

with open("d09/settings.py", "w") as f:
    f.write(content)
