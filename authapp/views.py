import requests
from django.http import request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserRegistration, UserEditForm


@login_required
def dashboard(request):
    context = {
        "welcome": "Welcome to your dashboard"
    }
    return render(request, 'authapp/dashboard.html', context=context)


def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data.get('password')
            )
            new_user.save()
            return render(request, 'authapp/register_done.html')
    else:
        form = UserRegistration()

    context = {
        "form": form
    }

    return render(request, 'authapp/register.html', context=context)

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        context = {
            'form': user_form,
        }
    return render(request, 'authapp/edit.html', context=context)

@login_required
def get_anime(request):
    context = {
        "welcome": "Welcome to your dashboard"
    }
    return render(request, 'authapp/submit_query.html', context=context)

def submit_query(request):
    context = []
    request_id = ''
    url = 'https://api.jikan.moe/v4/anime/'
    is_typed = request.POST.get('title', '')

    resp = requests.get(url)
    items = resp.json().get('data', '')
    if is_typed:
        for item in items:
            if item['title'] == is_typed:
                request_id = item['mal_id']
                url += str(request_id)
                resp = requests.get(url).json().get('data', '')
                items = [resp]
                break
            
    if items:
        for e in items:
            context.append({
                "title": e['title'],
                "image_url": e['images']['jpg']['image_url'],
                "title_english": e['title_english'],
                "type": e["type"],
                "source": e["source"],
                "episodes": e['episodes'],
                "status": e["status"],
                "airing": e['airing']
            })
    return render(request, 'authapp/jikan.html', {'context': context})
