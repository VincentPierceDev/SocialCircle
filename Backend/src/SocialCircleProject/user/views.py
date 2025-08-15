from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, AccountSetupForm, AccountLoginForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('/user/account-setup')
    else:
        form = RegisterForm()
        
    context = {
        "form": form
    }

    return render(request, 'user/register.html', context)

@login_required
def account_setup_view(request):
    if request.method == 'POST':
        form = AccountSetupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
        else:
            form = AccountSetupForm(request.POST)
    else:
        form = AccountSetupForm()
    
    context = {
        "form": form
    }

    return render(request, 'user/account-setup.html', context)

def login_view(request):
    if request.method == "POST":
        form = AccountLoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('/dashboard')
    else:
        form = AccountLoginForm()
            
    context = {
        "form": form
    }

    return render(request, 'user/login.html', context)

@login_required
def home_view(request):
    username = user_logged_in(request)

    if username == None:
        return redirect('/login')

    context = {
        "username": username
    }

    return render(request, 'user/home.html', context)

def logout_view(request):
    username = user_logged_in(request)
    if username != None:
        return logout(request)
    
    return redirect('/login')


def user_logged_in(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    return username