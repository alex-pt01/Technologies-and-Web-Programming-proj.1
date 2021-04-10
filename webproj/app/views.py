from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest
from django.shortcuts import render, redirect

# Create your views here.
from app.forms import newUserForm


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('user')
            password = request.POST.get('pass')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                loginUser(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)


def signup(request):

    if request.user.is_authenticated:
        messages.info(request, 'You are already registered' )
        return redirect('home')
    else:
        form = newUserForm()
        if request.method == 'POST':
            form = newUserForm(request.POST)
            if form.is_valid():
                form.save()
                # clean field
                user = form.cleaned_data.get('username')
                # messages (dict)
                messages.success(request, 'Account was created for ' + user)

                return redirect('home')

        return render(request, 'signup.html', {'form': form})

def logout(request):
    logoutUser(request)
    return redirect('home')



def home(request):
    assert isinstance(request, HttpRequest)
    tparams = {}
    return render(request, 'index.html', tparams)

    return render(request, 'signup.html', tparams)


def shop(request):
    assert isinstance(request, HttpRequest)
    tparams = {

    }

    return render(request, 'shop.html', tparams)


def productDetails(request):
    assert isinstance(request, HttpRequest)
    tparams = {

    }

    return render(request, 'product-details.html', tparams)


def checkout(request):
    assert isinstance(request, HttpRequest)
    tparams = {

    }

    return render(request, 'checkout.html', tparams)


def cart(request):
    assert isinstance(request, HttpRequest)
    tparams = {

    }

    return render(request, 'cart.html', tparams)
