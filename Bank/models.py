from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Branch(models.Model):
    branch_name=models.CharField(max_length=150)
    code=models.CharField(max_length=100)
    address=models.TextField(max_length=300)



class User_id(models.Model):
    choices=[('debit',"DEBIT"),('credit',"CREDIT")]
    role=models.CharField(choices)
    user_id=models.ForeignKey(User,on_delete=models.DO_NOTHING)

    


class User_accounts(models.Model):
    account_number=models.CharField(max_length=14)
    user_id=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    current_balance=models.DecimalField(max_digits=10,decimal_places=2, default=0.0)
    is_active=models.BooleanField(default=True)
    created_data=models.DateTimeField(auto_now=True)


class Transcations(models.Model):
    choices=[('transcation','TRANSCATION'), ('deposit', "DEPOSIT"), ("withdraw", "WITHDRAW")]
    date=models.DateTimeField(auto_now=True)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    type=models.CharField(choices=choices)
    from_account=models.ForeignKey(User_accounts,related_name='unique', on_delete=models.DO_NOTHING)
    to_account=models.ForeignKey(User_accounts,related_name='odd',on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    

    