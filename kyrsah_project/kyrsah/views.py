from django.shortcuts import render
from django.views import View
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import *
from .functions import *


class MainPage(View):

    def get(self, request):

        articles = Article.objects.all().order_by('dateCreate')
        users = User.objects.all()

        try:
            current_user = avaUser(request.user.name)
        except:
            current_user = None

        context = {
            'articles': articles,
            'users': users,
            'current_user': current_user,
        }
        return render(request, 'index.html', context=context)

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


class CreateArticle(View):
    def get(self, request):
        try:
            current_user = avaUser(request.user.name)
        except:
            current_user = None
        context = {
            'current_user': current_user,
            'current_user_ava': current_user
        }

        return render(request, 'createEditArticle.html', context=context)

    def post(self, request):

        title_article = request.POST.get('title_article')
        content_article = request.POST.get('content')
        color_article = request.POST.get('color_article')

        c = Article.objects.create(title=title_article, content=content_article, idUser=request.user, color=color_article)

        return HttpResponseRedirect('/')


class EditArticle(View):
    def get(self, request, id):

        article = Article.objects.get(id=id)

        if request.user != article.idUser:
            return HttpResponseRedirect('/')

        try:
            current_user = avaUser(request.user.name)
        except:
            current_user = None

        context = {
            'article': article,
            'current_user': current_user
        }

        return render(request, 'editArticle.html', context=context)

    def post(self, request, id):

        article = Article.objects.get(id=id)
        title_article = request.POST.get('title_article')
        content_article = request.POST.get('content')
        color_article = request.POST.get('color_article')

        article.title = title_article
        article.content = content_article
        article.color = color_article

        article.save()

        return HttpResponseRedirect('/')


class BlogContent(View):
    def get(self, request, id):
        article = Article.objects.get(id=id)
        comments = Comment.objects.filter(idArticle=id)

        userAvaComment = []
        for i in comments:
            userAvaComment.append(avaUser(i.idUser.name))

        try:
            current_user = avaUser(request.user.name)
            full_current_user = request.user
        except:
            current_user = None
            full_current_user = None

        print(full_current_user)
        print(article.idUser)
        context = {
            'article': article,
            'userAva': avaUser(article.idUser.name),
            'avaUserCommnets': userAvaComment,
            'current_user': current_user,
            'full_current_user': full_current_user,
            'comments': comments,
            'lencomment': len(comments),
            'len': zip(comments, userAvaComment)
        }
        return render(request, 'watchArticle.html', context=context)

    def post(self, request, id):
        article = Article.objects.get(id=id).delete()
        return HttpResponseRedirect('/')
