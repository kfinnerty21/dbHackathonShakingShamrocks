from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name="db_user",on_delete=models.CASCADE)
    account_number = models.CharField(max_length=150)
    account_name = models.CharField(max_length=150)
    address = models.CharField(max_length=200)
    bank_name = models.CharField(max_length=200)
    branch = models.CharField(max_length=200)
    phone = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    cash_balance = models.IntegerField(default=500)
    credit_balance = models.IntegerField(default=500)



  
