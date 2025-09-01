from django.db import models
from server.models import Server

class Channel(models.Model):
    name = models.CharField(max_length=25, default="")
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="channels")

    def __str__(self):
        return self.name
    
