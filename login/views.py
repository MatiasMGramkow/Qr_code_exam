from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.forms import UserCreationForm as ucform
from django.shortcuts import reverse


def login(request):

    context = {}

    if request.method == 'POST':
        user = authenticate(request, username=request.POST['user'], password=request.POST['password'])
        if user:
            dj_login(request, user)
            return redirect(reverse('qrcodes:home'))
        else:
            context = {
                'error': 'Wrong username or password.'
            }

    return render(request, 'login/login.html', context)


def logout(request):
    dj_logout(request)
    return redirect(reverse('login:login'))


def signup(request):
    if request.method == 'POST':
        form = ucform(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(request, username=request.POST['username'], password=request.POST['password1'])
            if user:
                dj_login(request, user)
                return redirect(reverse('qrcodes:home'))
    else:
        form = ucform()
    
    return render(request, 'login/signup.html', {'form': form})