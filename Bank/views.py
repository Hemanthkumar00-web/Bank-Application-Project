from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import login as dj_login ,logout
from django.views.decorators.csrf import csrf_exempt 
from django.http import JsonResponse

from .models import User_accounts, Transcations


from decimal import Decimal
import secrets
import json
# Create your views here.
# def features(request):
#     return render(request,'features.html')

@csrf_exempt
def login(request):
    if request.method=='GET':
        return render(request,'login.html')
    if request.method=='POST':
        data=request.POST
        username=data.get('email')
        password=data.get('password')
        user=User.objects.filter(username=username)
        if len(user) <1:
            return render(request,'login.html',context={'error':'invalid username'})
        user=user[0]
        check=user.check_password(password)
        if not check:
            return render(request,'login.html',context={'error':'invalid password'})
        dj_login(request, user) 
        return redirect("feature")

def logout_here(request):
    logout(request)
    return redirect("login")

@csrf_exempt
def deposit(request):
    if not request.user.is_authenticated:
        return redirect("login")

    print(request.user, "------------------")
    User_account=User_accounts.objects.filter(user_id=request.user).first()
    if request.method=="POST":
        amount=request.POST.get('amount')
        print(amount)   
        user = request.user

        # query for saving information
        # get the account number
        account = User_accounts.objects.get(user_id=user)

        # create transaction
        new_transaction = Transcations.objects.create(
            amount=Decimal(amount),
            type="deposit",
            from_account = account,
            to_account = account,
            user_id = user
        )

        new_transaction.save()
        # update account balance
        account.current_balance += Decimal(amount)
        account.save()
        return redirect('deposit')
    account={
        

         'account_number':User_account.account_number,
    }
    print(account)
    return render(request,"deposit.html",context=account)
    

    




    

@csrf_exempt
def withdraw(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user=request.user
    account=User_accounts.objects.get(user_id=user)
    if request.method=='GET':
        data = {
                    'account_number': account.account_number
                }
        return render(request,"withdraw.html",context=data)
    elif request.method=='POST':
            amount=request.POST.get('amount')
            if Decimal(amount) > account.current_balance:
                return render(request,'withdraw.html',context={'error':'insufficient '})
            
            new_transcation=Transcations.objects.create(
            amount=Decimal(amount),
            type="withdraw",
            from_account=account,
            to_account=account,
            user_id = user
        )
            new_transcation.save()
            account.current_balance -= Decimal(amount)
            account.save()
            print(account)
            return redirect('withdraw')

@csrf_exempt
def transfer(request):
    if not request.user.is_authenticated:
        return redirect("login")
    user=request.user
    User_account=User_accounts.objects.get(user_id=user)
    if request.method=="GET":
        data = {
            'account_number': User_account.account_number
        }
        return render(request,'transfer.html', context=data)
    elif request.method=="POST":


     
        to_account=request.POST.get("to_account")
        transfer_amount=request.POST.get("amount")
        
        to_accounts=User_accounts.objects.filter(account_number=to_account)
        print(to_account)
        if len(to_accounts)<1:
            return render(request,'transfer.html',context={'error':'Account does not exist'})
        my_account=User_accounts.objects.filter(
            user_id=request.user,
            account_number=to_account
        ).exists()
        if my_account:
            return render(request,'transfer.html',context={'error':'you cannot transfer amount into your own account'})
        
        to_account=to_account.first()
        new_transcation=Transcations.objects.create(
            amount=Decimal(transfer_amount),
            type="transfer",
            from_account=User_account,
            to_account=to_accounts,
            user_id = user
        )
        new_transcation.save()
        User_account.current_balance -= Decimal(transfer_amount)
        User_account.save()
        new_transcation=Transcations.objects.create(
            amount= Decimal(transfer_amount),
            type="transfer",
            from_account=to_accounts,
            to_account=User_account,
            user_id = to_account.user_id
        )
        new_transcation.save()
        to_accounts.current_balance += Decimal(transfer_amount)
        
        return redirect('transfer')
    
@csrf_exempt
def check(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method=="GET":
        user_accounts=User_accounts.objects.filter(
            user_id=request.user
        )
    return render(request,'check.html',context={'details':user_accounts})

@csrf_exempt
def viewtranscations(request):
    if not request.user.is_authenticated:
        return redirect(request,'login')
    if request.method=="GET":
        user=request.user
        Transcation=Transcations.objects.filter(
            user_id=request.user
        )
        process={
            'Transcations':Transcation
        }
        Transcation=Transcation.first()
        return render(request,'viewtranscations.html',context=process)



@csrf_exempt
def Register(request):
    if request.method=="GET":
        return render(request,'Register.html')
    if request.method=="POST":
        data=request.POST
        username=data.get('email')
        first_name=data.get('first_name')
        last_name=data.get('last_name')
        password=data.get('password')
        confirm_password=data.get('confirm_password')
    if len(first_name)<=1:
        return render(request,'Register.html', context={'error':'name should be character'})
    if User.objects.filter(username=username).exists():
        return render(request,'Register.html',context={'error':'Email already exists'})
    if password!=confirm_password:
        return render(request,'Register.html', context={'error':' password must same as confirm password'})

    number = "".join(str(secrets.randbelow(10)) for i in range(14))
    # creating user object
    new_user=User.objects.create(username=username,first_name=first_name,last_name=last_name,password=password)
    new_user.set_password(password)
    new_user.save()
    # mappin user object to bank account
    account = User_accounts.objects.create(account_number=number,user_id=new_user)
    account.save()
    print(account )
    return redirect('login')


def features_page(request):
    if not request.user.is_authenticated: 
        return redirect('login')
    user = request.user #AnonymousUser
    user_account = User_accounts.objects.filter(user_id=user)

    if len(user_account)<1:
        return redirect('login')
    user_account = user_account[0]
    account = {
        'account_number': user_account.account_number,
        'username': user_account.user_id.username,
        'current_balace': user_account.current_balance
    }
    print(account,"------------------")
    return render(request, 'features.html', context=account)


@csrf_exempt
def check_acc_number(request):
    if request.method =='POST':
        data =json.loads(request.body.decode("utf-8"))
        acc_num= data.get('accountnumber')
        user=request.user
        user_account = User_accounts.objects.filter(
            account_number=acc_num,

        ).first()
        print("Found account:",user_account)
        if user_account:
            username=user_account.user_id.username
            print(username)
            return JsonResponse({"success":True,"username":username,"accountnumber":user_account.Account_number})
       



