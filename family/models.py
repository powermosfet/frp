from django.db import models
from django.contrib.auth.models import *
from django.db.models.signals import post_save

class Family(models.Model):
    name = models.CharField(max_length = 80)

    def __unicode__(self):
        return self.name

class FamilyMember(models.Model):  
    user = models.OneToOneField(User)
    families = models.ManyToManyField(Family)
    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email']

def create_family_member(*args, **kwargs):
    u = kwargs['instance']
    if not hasattr(u, 'familymember'):
        fm = FamilyMember()
        fm.user = u
        fm.save()

post_save.connect(create_family_member, sender = User)
