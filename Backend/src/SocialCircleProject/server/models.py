from django.db import models
from user.models import User
from django.contrib.auth.models import Group

class Server(models.Model):
    name = models.CharField(max_length=25, default="")
    members = models.ManyToManyField(User, through="Membership", related_name="servers")

    class Meta:
        ordering = ["name"]
    
    def __str__(self):
        return self.name
        


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

    def assign_group(self):
        group_name = dict(self.ROLE_CHOICES)[self.status]
        group, _ = Group.objects.get_or_create(name=group_name)
        self.user.groups.add(group)


    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "server"], name="server_user_constraint")] # user can only be in server once