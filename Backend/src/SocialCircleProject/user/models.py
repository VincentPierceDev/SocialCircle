from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    last_active = models.DateTimeField(auto_now=True)
    bio = models.TextField(max_length=250, default="");

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{self.username}"