from django.shortcuts import render
from django.http import HttpResponse
from .models import Movies


def populate(request):
    movies_list = [
        {"ep": 1, "tit": "The Phantom Menace", "dir": "George Lucas", "prod": "Rick McCallum", "date": "1999-05-19"},
        {"ep": 2, "tit": "Attack of the Clones ", "dir": "George Lucas", "prod": "Rick McCallum", "date": "2002-05-16"},
        {"ep": 3, "tit": "Revenge of the Sith", "dir": "George Lucas", "prod": "Rick McCallum", "date": "2005-05-19"},
        {"ep": 4, "tit": "A New Hope", "dir": "George Lucas", "prod": "Gary Kurtz, Rick McCallum", "date": "1977-05-25"},
        {"ep": 5, "tit": "The Empire Strikes Back", "dir": "Irvin Kershner", "prod": "Gary Kurtz, Rick McCallum", "date": "1980-05-17"},
        {"ep": 6, "tit": "Return of the Jedi", "dir": "Richard Marquand", "prod": "Howard G. Kazanjian, George Lucas, Rick McCallum", "date": "1983-05-25"},
        {"ep": 7, "tit": "The Force Awakens", "dir": "J. J. Abrams", "prod": "Kathleen Kennedy, J. J. Abrams, Bryan Burk", "date": "2015-12-11"},
    ]

    responses = []

    for movie in movies_list:
        try:
            movie_obj = Movies(
                episode_nb=movie['ep'],
                title=movie['tit'],
                director=movie['dir'],
                producer=movie['prod'],
                release_date=movie['date']
            )

            movie_obj.save()
            responses.append("OK")

        except Exception as e:
            responses.append(f"Error: {e}")

    return HttpResponse("<br>".join(responses))


def display(request):
    try:
        movies_data = Movies.objects.all()

        if len(movies_data) == 0:
            return HttpResponse("No data available")

        return render(request, 'ex07/display.html', {'movies': movies_data})

    except Exception:
        return HttpResponse("No data available")


def update(request):
    try:
        if request.method == 'POST':
            movie_id = request.POST.get('movie_dropdown')
            new_crawl_text = request.POST.get('new_crawl')

            try:
                movie_to_update = Movies.objects.get(episode_nb=movie_id)
                movie_to_update.opening_crawl = new_crawl_text
                movie_to_update.save()

            except Movies.DoesNotExist:
                pass

        movies = Movies.objects.all()

        if len(movies) == 0:
            return HttpResponse("No data available")

        return render(request, 'ex07/update.html', {'movies': movies})

    except Exception:
        return HttpResponse("No data available")
