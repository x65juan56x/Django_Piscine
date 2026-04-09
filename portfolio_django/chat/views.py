from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Room

@login_required
def index(request):
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})

@login_required
def room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    return render(request, 'chat/room.html', {'room': room})

# Cuando se ejecuta get_object_or_404(Room, name=room_name) Django va a la base de datos y busca una fila en el modelo Room que coincida con el nombre pasado por la URL (por ejemplo, "General").
# Si existe la extrae, la guarda en la variable room y el código continúa para renderizar el HTML.
# Si no existe Django devuelve página de "Error 404 - Página no encontrada".