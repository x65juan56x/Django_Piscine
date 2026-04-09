from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model, authenticate
from django.http import JsonResponse
from django.utils.translation import gettext as _
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

def get_current_name(request):
    if request.user.is_authenticated:
        name = f"{request.user.username} ({request.user.reputation})"
    else:
        name = request.session.get('random_name', _('Unknown'))
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

    if user != tip.author and not user.has_perm('tips.can_downvote'):
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
    
    if request.user == tip.author or request.user.has_perm('tips.delete_tip'):
        tip.delete()
        
    return redirect('home')
