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
    if request.user.username:
        return redirect('/user/dashboard')
    
    if request.method == 'POST':
        form = AccountSetupForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/user/dashboard')
    else:
        form = AccountSetupForm(instance=request.user)
    
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
    user_string = request.user.__str__()
    user_initial = username[0]

    if username == None:
        return redirect('/login')

    context = {
        "username": username,
        "user_string": user_string,
        "user_initial": user_initial
    }

    return render(request, 'user/dashboard.html', context)

@login_required
def logout_view(request):
    username = user_logged_in(request)
    if username != None:
        logout(request)
    
    return redirect('/')


def user_logged_in(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    return username