from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import AccountLoginForm

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('account-setup/', views.account_setup_view, name='account_setup'),
    path('login/', auth_views.LoginView.as_view(template_name="user/login.html", authentication_form=AccountLoginForm), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.home_view, name='home'),
]