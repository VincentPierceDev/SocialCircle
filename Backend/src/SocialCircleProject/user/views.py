from django.shortcuts import render
from django.contrib.auth import login, logout
from .forms import RegisterForm, AccountSetupForm, AccountLoginForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('account_setup')
    else:
        form = RegisterForm()
        
    context = {
        "form": form
    }

    return render(request, 'user/register.html', context)

@login_required
def account_setup_view(request):
    if request.user.username:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AccountSetupForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
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
                return redirect('dashboard')
    else:
        form = AccountLoginForm()
            
    context = {
        "form": form
    }

    return render(request, 'user/login.html', context)

@login_required
def home_view(request):
    username = request.user.__str__()
    user_initial = username[0]

    if username == None:
        return redirect('login')

    if request.method == "GET":
        servers = request.user.servers.all()
        if servers:
            server_count = servers.count
        else:
            server_count = 0

    context = {
        "username": username,
        "user_initial": user_initial,
        "servers": servers,
        "server_count": server_count,
    }

    return render(request, 'user/dashboard.html', context)

@login_required
def logout_view(request):
    username = request.user.username

    if username != None:
        logout(request)
    
    return redirect('index')
