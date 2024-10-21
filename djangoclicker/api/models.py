from django.db import models
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=1337)

"""
class Core(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    click_power = models.IntegerField(default=1)
"""
# Create your models here.
