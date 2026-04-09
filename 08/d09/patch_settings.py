with open("d09/settings.py", "r") as f:
    content = f.read()

content = content.replace("INSTALLED_APPS = [", "INSTALLED_APPS = [\n    'daphne',\n    'chat',")
content = content.replace("WSGI_APPLICATION = 'd09.wsgi.application'", "WSGI_APPLICATION = 'd09.wsgi.application'\nASGI_APPLICATION = 'd09.asgi.application'\n\nCHANNEL_LAYERS = {\n    'default': {\n        'BACKEND': 'channels.layers.InMemoryChannelLayer',\n    }\n}")

with open("d09/settings.py", "w") as f:
    f.write(content)
