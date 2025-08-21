from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'About Info',
            {
                'fields': (
                    'bio',
                )
            }
        )
    )

admin.site.register(User, CustomUserAdmin)
