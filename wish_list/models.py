from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class List(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    end = models.BooleanField(default=False)

class Gifts(models.Model):
    name = models.CharField(max_length=150, verbose_name="O czym marzysz?")
    desciption = models.TextField(null=True, verbose_name="Opis")
    shop = models.CharField(max_length=250, verbose_name="Podaj link do sklepu internetowego", null=True)
    file = models.FileField(verbose_name="Dodaj zdjęcie", null=True)
    wish_list = models.ForeignKey(List, on_delete=models.CASCADE)
    person = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Darczyńca", null=True)


class Fundraiser(models.Model):
    goal = models.CharField(max_length=64, verbose_name="Na co zbierasz?")
    desciption = models.TextField(null=True, verbose_name="Powiedz o tym coś więcej")
    amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Ile chcesz zebrać pieniędzy?")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Donors(models.Model):
    amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Jaką kwotę chcesz przekazać na ten cel?")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fundraiser = models.ForeignKey(Fundraiser, on_delete=models.CASCADE)
