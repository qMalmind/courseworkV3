from django.shortcuts import render
from django.views import View
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import *
from .functions import *
from .forms import *

@login_required
def my_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


class LogIn(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        context = {}
        return render(request, 'login.html', context=context)

    def post(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')

        context = {}

        login_or_email = request.POST.get('email')
        # password = request.POST['password']
        password = request.POST.get('password')

        print(login_or_email)
        print(password)

        if (User.objects.filter(email=login_or_email) or User.objects.filter(login=login_or_email)) and User.objects.filter(password=password):
            try:
                usr = User.objects.get(login=login_or_email)
            except:
                usr = User.objects.get(email=login_or_email)

            login(request, usr)
            print(request.user)
            return HttpResponseRedirect('/')
        else:
            print("not login")

        return HttpResponseRedirect('/login')


class Register(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        context = {}
        return render(request, 'register.html', context=context)

    def post(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')

        email = request.POST.get('email')
        login = request.POST.get('login')
        name = request.POST.get('name')
        password = request.POST.get('password')
        print(email)
        print(login)
        print(name)
        print(password)

        context = {

        }

        errors = []

        if User.objects.filter(login=login):
            print("bad login")
            errors.append("Логин не уникален")
        elif len(password) < 6:
            print("bad password")
            errors.append("Пароль слишком короткий")

        if len(errors) != 0:
            print("have err")
            context['err'] = errors
            return render(request, 'register.html', context=context)
        else:
            User.objects.create(name=name, email=email, login=login, password=password)
            print("create user")
            return HttpResponseRedirect('/')


class Profile(View):

    def get(self, request, id):

        user = User.objects.get(id=id)
        user_avatar = avaUser(user.name)
        articles = Article.objects.filter(idUser=id).order_by('dateCreate')

        try:
            current_user = avaUser(request.user.name)
            full_current_user = request.user
        except:
            current_user = None
            full_current_user = None

        context = {
            'current_user': current_user,
            'full_current_user': full_current_user,
            'user': user,
            'user_avatar': user_avatar,
            'articles': articles
        }

        return render(request, 'profile.html', context=context)


class Ban_user(View):
    def get(self, request, id):
        if not(request.user.is_staff):
            return HttpResponseRedirect('/')

        user = User.objects.get(id=id)
        user.haveBan = True
        user.save()

        return HttpResponseRedirect('/')