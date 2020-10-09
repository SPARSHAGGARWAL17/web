from django.db import models

# Create your models here.
class Register(models.Model):
    username = models.CharField(max_length=15)
    email = models.EmailField(max_length=20)
    password = models.CharField(max_length=15)
    mobile = models.IntegerField()
    date = models.DateField()
    otp = models.IntegerField(default=0)
    money = models.IntegerField(default=0)

class CardDetails(models.Model):
    email = models.CharField(max_length=20)
    card = models.IntegerField()
    date = models.DateField()
    cvv = models.IntegerField()
    name = models.CharField(max_length=20)