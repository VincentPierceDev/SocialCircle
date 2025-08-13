from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('account-setup/', views.account_setup_view, name='account_setup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/<int:user_id>/', views.home_view, name='home'),
]