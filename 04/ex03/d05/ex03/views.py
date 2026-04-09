from django.shortcuts import render


def index(request):
    shades_data = []

    for i in range(50):
        intensity = int((i / 49) * 255)

        row = {
            'noir': f'rgb({intensity}, {intensity}, {intensity})',
            'rouge': f'rgb({intensity}, 0, 0)',
            'bleu': f'rgb(0, 0, {intensity})',
            'vert': f'rgb(0, {intensity}, 0)'
        }
        shades_data.append(row)

    return render(request, 'ex03/index.html', {'shades': shades_data})
