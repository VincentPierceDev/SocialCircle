from django.urls import path
from . import views

urlpatterns = [
    path('create-server/', views.create_server_view, name="create_server"),
    path('join-server/', views.join_server_view, name="join_server")
]