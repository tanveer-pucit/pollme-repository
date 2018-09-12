from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .forms import UserRegistrationForm


def accounts_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            redirect_url = request.GET.get('next', 'home_view')
            return redirect(redirect_url)
        else:
            # print(username)
            # print(password)
            messages.error(request, 'Invalid cridentials!')
    return render(request, 'accounts/login.html', {})


def accounts_logout_view(request):
    logout(request)
    return redirect('accounts:login')


def accounts_register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username, email=email, password=password)
            messages.success(request, 'Thanks for registering {}'.format(user.username))
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})
