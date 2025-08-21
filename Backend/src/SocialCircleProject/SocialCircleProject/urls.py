from django.contrib import admin
from django.urls import path, include
from . import views
from user import urls as user_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name='index'),
    path('user/', include(user_urls)),
]
