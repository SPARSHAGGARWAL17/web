from typing import Dict

from django.contrib.auth.models import User
# from django.http import request
from mysite.settings import STATIC_URL
from django.shortcuts import redirect, render
from datetime import datetime
from mini.models import CardDetails, Register
from django.contrib.auth import login, logout, authenticate

contexts = {'STATIC_URLS': STATIC_URL}
fraudNo = 0


def index(request):
    if request.user.is_anonymous:
        return redirect('login/', contexts)
    return redirect('money/', contexts)


# Create your views here.
def loginUser(request):
    # print(contexts)
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        print(f'username = {username} password = {password}')
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            print('here')
            return redirect('/path/money/', contexts)
        return redirect('/path/login/', contexts)
    else:
        return render(request, 'mini/login.html', contexts)


def register(request):
    return render(request, 'mini/register.html', context={'STATIC_URLS': STATIC_URL, 'button': 'ADD'})


def main(request):
    if request.method == "POST":
        name: str = request.POST.get('name')
        lastname: str = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        register = Register(username=name, email=email, password=password, mobile=mobile, date=datetime.today())
        register.save()
        print(name,lastname,email,password)
        user = User.objects.create_user(username=email,email= email,password= password)
        user.first_name = name
        user.last_name = lastname
        user.save()
        new_user = authenticate(request,username=email,password=password)
        login(request,user=new_user)
        return render(request, 'mini/card.html', context={'STATIC_URLS': STATIC_URL, 'button': 'ADD'})
    return render(request, 'mini/login.html', context=contexts)


def logoutUser(request):
    logout(request)
    return redirect('/path/', contexts)


def check(request, money=0):
    if request.method == "POST":
        name = request.POST.get('name')
        date = request.POST.get('date')
        cvv = request.POST.get('cvv')
        card = request.POST.get('card')
        cardDetails = CardDetails.objects.all().filter(email=str(request.user))
        for i in cardDetails:
            register = Register.objects.all().filter(email=i.email)
            number = register[0].mobile
            if i.name == name and str(i.date) == date and i.cvv == int(cvv) and i.card == int(card) and i.email == str(
                    request.user):
                print('verified')
                for reg in register:
                    reg.money = money
                    reg.save()
                return redirect(f'/path/money/', context=contexts)
            else:
                global fraudNo
                fraudNo = fraudNo + 1
                print("fraud = ", fraudNo)
                if fraudNo == 3:
                    return redirect('/path/fraud/', contexts)
        return redirect(f'/path/check/0', context=contexts)
    return redirect(f'/path/money/', context=contexts)


def verify(request):

    if request.method == "POST":
        print('if')
        email = User.get_username(request.user)
        name = request.POST.get('name')
        date = request.POST.get('date')
        cvv = request.POST.get('cvv')
        card = request.POST.get('card')
        details = CardDetails(email=email, card=card, date=date, cvv=cvv, name=name)
        details.save()
        return redirect('/path/check/0')
    else:
        return render(request, 'mini/money.html', context=contexts)


def money(request):
    register = Register.objects.all().filter(email=User.get_username(request.user))
    for i in register:
        money: float = i.money
        print(i.email)
        if request.method == "POST":
            if request.POST.get('card') != '':
                money = money + int(request.POST.get('card'))
                return render(request, 'mini/addcard.html',
                              {'STATIC_URLS': STATIC_URL, 'button': 'VERIFY', 'money': money})
    return render(request, 'mini/money.html', {'STATIC_URLS': STATIC_URL, 'money': money})


def fraud(request):
    print(request)
    print(request.method)
    if fraudNo == 3:
        logout(request)
        return redirect('/path/', contexts)
    else:
        return render(request, 'mini/addcard.html', contexts)
