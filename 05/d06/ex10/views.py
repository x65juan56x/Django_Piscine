from django.shortcuts import render
from .forms import FilterForm
from .models import Movies


def search_view(request):
    results = None

    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            min_date = form.cleaned_data['min_date']
            max_date = form.cleaned_data['max_date']
            diam = form.cleaned_data['planet_diameter']
            gen = form.cleaned_data['gender']

            results = Movies.objects.filter(
                release_date__gte=min_date,
                release_date__lte=max_date,
                characters__gender=gen,
                characters__homeworld__diameter__gte=diam
            ).values(
                'title',
                'characters__name',
                'characters__gender',
                'characters__homeworld__name',
                'characters__homeworld__diameter'
            )
    else:
        form = FilterForm()

    return render(request, 'ex10/ex10.html', {'form': form, 'results': results})
