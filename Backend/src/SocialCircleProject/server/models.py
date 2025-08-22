from django.db import models
from user.models import User

class Server(models.Model):
    name = models.CharField(max_length=25, default="")



# Many to Many through table for Servers and Users 
class Membership(models.Model):
    
    #store an integer
    ROLE_CHOICES = (
        (1, 'Owner'),
        (2, 'Moderator'),
        (3, 'Member')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    status = models.IntegerField(choices=ROLE_CHOICES, default=3)

    class Meta:
        unique_together = ("user", "server") # user can only be in server once