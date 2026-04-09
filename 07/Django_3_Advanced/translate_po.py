import re
import os

es_dict = {
    "Articles": "Artículos",
    "English": "Inglés",
    "French": "Francés",
    "Spanish": "Español",
    "Language": "Idioma",
    "Home": "Inicio",
    "Login": "Iniciar Sesión",
    "Logout": "Cerrar Sesión",
    "Register": "Registrarse",
    "My Publications": "Mis Publicaciones",
    "My Favourites": "Mis Favoritos",
    "Publish New Article": "Publicar Nuevo Artículo",
    "Title": "Título",
    "Synopsis": "Sinopsis",
    "Content": "Contenido",
    "Created": "Creado",
    "You have not published any articles yet.": "Aún no has publicado ningún artículo.",
    "Add to Favourites": "Añadir a Favoritos",
    "Add this article to your favourites": "Añade este artículo a tus favoritos",
    "You have no favourite articles.": "No tienes artículos favoritos.",
    "Publish": "Publicar",
    "Publish Article": "Publicar Artículo",
    "Synopsis:": "Sinopsis:",
    "Author:": "Autor:",
    "Published on:": "Publicado el:",
    "Last Articles": "Últimos Artículos",
    "Username": "Usuario",
    "Password": "Contraseña",
    "Favourites": "Favoritos",
    "Publications": "Publicaciones",
    "Logged as": "Conectado como",
}

def translate_po(file_path, trans_dict):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    new_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Keep header info and msgid "" intact
        if line.startswith('msgid ""'):
             new_lines.append(line)
             i += 1
             continue
        
        if line.startswith('msgstr "'):
             if i > 0 and lines[i-1].startswith('msgid'):
                  msgid_match = re.match(r'^msgid "(.*)"$', lines[i-1])
                  if msgid_match:
                      msgid = msgid_match.group(1)
                      if msgid in trans_dict:
                          new_lines.append(f'msgstr "{trans_dict[msgid]}"')
                      else:
                          new_lines.append('msgstr ""') # Reset all others back to defaults empty string
                  else:
                      new_lines.append(line)
             else:
                  new_lines.append(line)
             i += 1
             continue
             
        new_lines.append(line)
        i += 1

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

es_path = 'locale/es/LC_MESSAGES/django.po'

translate_po(es_path, es_dict)
print("Translations generated successfully!")
