from django.http import HttpResponse
from django.shortcuts import render
from .models import People


def display(request):
    try:
        characters = People.objects.filter(homeworld__climate__icontains='windy').select_related('homeworld').order_by('name')

        if not characters.exists():
            error_msg = (
                "No data available, please use the following command line before use:<br>"
                "<code>python3 manage.py loaddata ex09_initial_data.json</code>"
            )
            return HttpResponse(error_msg)

        return render(request, 'ex09/display.html', {'characters': characters})

    except Exception:
        error_msg = (
            "No data available, please use the following command line before use:<br>"
            "<code>python3 manage.py loaddata ex09_initial_data.json</code>"
        )
        return HttpResponse(error_msg)
