from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class List(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    end = models.BooleanField(default=False)

class Gifts(models.Model):
    name = models.CharField(max_length=150)
    desciption = models.TextField(null=True)
    shop = models.CharField(max_length=250)
    file = models.FileField()
    wish_list = models.ForeignKey(List, on_delete=models.CASCADE)
    person = models.ForeignKey(User, on_delete=models.CASCADE)

