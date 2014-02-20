from django.db import models
from django.contrib.auth.models import *
from django.db.models.signals import post_save

class Family(models.Model):
    name = models.CharField(max_length = 80)

class FamilyMember(AbstractBaseUser):  
    login = models.CharField(max_length=30, unique=True)
    email = models.EmailField()
    families = models.ManyToManyField(Family)
    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email']

