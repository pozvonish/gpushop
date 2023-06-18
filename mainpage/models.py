from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=128)
