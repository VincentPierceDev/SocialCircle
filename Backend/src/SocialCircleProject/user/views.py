from django.shortcuts import render
from .forms import RegisterForm, AccountSetupForm
from django.shortcuts import redirect

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/account-setup')
        else:
            form = RegisterForm(request.POST)
    else:
        form = RegisterForm()
        
    context = {
        "form": form
    }

    return render(request, 'user/register.html', context)

def account_setup_view(request):
    if request.method == 'POST':
        form = AccountSetupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/home')
        else:
            form = AccountSetupForm(request.POST)
    else:
        form = AccountSetupForm()
    
    context = {
        "form": form
    }

    return render(request, 'user/account-setup.html', context)

def login_view(request):
    return render(request, 'user/login.html')

def home_view(request):
    return render(request, 'user/home.html')