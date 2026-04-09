from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model, authenticate
from django.http import JsonResponse
from .models import Tip
from .forms import RegistrationForm, LoginForm, TipForm

def home(request):
    if request.method == 'POST' and request.user.is_authenticated:
        form = TipForm(request.POST)
        if form.is_valid():
            tip = form.save(commit=False)
            tip.author = request.user
            tip.save()
            return redirect('home')
    else:
        form = TipForm()
        
    tips = Tip.objects.all().order_by('-date')
    return render(request, 'ex/index.html', {'form': form, 'tips': tips})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            User = get_user_model()
            user = User.objects.create_user(username=username, password=password)

            login(request, user)
            return redirect('home')

    else:
        form = RegistrationForm()

    return render(request, 'ex/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            if form.user is not None:
                login(request, form.user)
                return redirect('home')

    else:
        form = LoginForm()

    return render(request, 'ex/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def get_current_name(request):
    if request.user.is_authenticated:
        name = f"{request.user.username} ({request.user.reputation})"
    else:
        name = request.session.get('random_name', 'Unknown')
    return JsonResponse({'name': name})

def upvote_tip(request, tip_id):
    if not request.user.is_authenticated:
        return redirect('home')
    
    tip = get_object_or_404(Tip, id=tip_id)
    user = request.user

    if user in tip.upvotes.all():
        tip.upvotes.remove(user)
    else:
        tip.upvotes.add(user)
        if user in tip.downvotes.all():
            tip.downvotes.remove(user)

    return redirect('home')

def downvote_tip(request, tip_id):
    if not request.user.is_authenticated:
        return redirect('home')

    tip = get_object_or_404(Tip, id=tip_id)
    user = request.user

    if user != tip.author and not user.has_perm('ex.can_downvote'):
        return redirect('home')

    if user in tip.downvotes.all():
        tip.downvotes.remove(user)
    else:
        tip.downvotes.add(user)
        if user in tip.upvotes.all():
            tip.upvotes.remove(user)

    return redirect('home')

def delete_tip(request, tip_id):
    if not request.user.is_authenticated:
        return redirect('home')

    tip = get_object_or_404(Tip, id=tip_id)
    
    if request.user == tip.author or request.user.has_perm('ex.delete_tip'):
        tip.delete()
        
    return redirect('home')
