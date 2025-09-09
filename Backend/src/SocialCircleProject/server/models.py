from django.db import models
from user.models import User
from django.contrib.auth.models import Group
import uuid
from django.urls import reverse

class Server(models.Model):
    name = models.CharField(max_length=25, default="")
    description = models.CharField(max_length=200, default="")
    members = models.ManyToManyField(User, through="Membership", related_name="servers")
    u_uniqueid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        ordering = ["name"]
    
    def __str__(self):
        return self.name
    
    #if the setting owner is not created, then it is a server ownership transfer
    def set_owner(self, user):
        membership, created = Membership.objects.get_or_create(
            server=self, user=user, defaults={'status': Membership.ROLE_MAP["Owner"]}
        )
        if not created:
            membership.status = Membership.ROLE_MAP['Owner']
            membership.save()
        return membership
    
    def get_owner(self):
        owner = Membership.objects.filter(server=self, status=Membership.ROLE_MAP["Owner"]).get()
        return owner
    
    def add_member(self, user):
        membership = Membership.objects.create(server=self, user=user, status=Membership.ROLE_MAP['Member'])
        return membership

    def member_count(self):
        return Membership.objects.filter(server=self).count()
    
    def get_public_id(self):
        return self.u_uniqueid.hex;

    def get_absolute_url(self):
        return reverse("server_home", kwargs={"public_id": self.get_public_id()})
    
        
        


# Many to Many through table for Servers and Users 
class Membership(models.Model):
    
    #store an integer
    ROLE_CHOICES = (
        (1, 'Owner'),
        (2, 'Moderator'),
        (3, 'Member')
    )

    ROLE_MAP = {v: k for k, v in ROLE_CHOICES}

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    status = models.IntegerField(choices=ROLE_CHOICES, default=3)

    def __str__(self):
        return self.user.username

    def assign_admin_group(self):
        group_name = dict(self.ROLE_CHOICES)[self.status]
        group, _ = Group.objects.get_or_create(name=group_name)
        self.user.groups.add(group)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "server"], name="server_user_constraint")] # user can only be in server once