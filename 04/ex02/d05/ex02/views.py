from django.shortcuts import render, redirect
from datetime import datetime
from django.conf import settings  # Para leer la ruta que pusimos en settings.py
from .forms import HistoryForm


def index(request):
    log_path = settings.EX02_LOG_FILE

    if request.method == 'POST':
        form = HistoryForm(request.POST)

        if form.is_valid():
            user_text = form.cleaned_data['history_text']
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] {user_text}\n"
            with open(log_path, 'a') as f:
                f.write(log_entry)
            return redirect('/ex02/')

    else:
        form = HistoryForm()

    history_list = []
    try:
        with open(log_path, 'r') as f:
            history_list = f.readlines()
    except FileNotFoundError:
        pass

    return render(request, 'ex02/index.html', {
        'form': form,
        'history': history_list
    })
