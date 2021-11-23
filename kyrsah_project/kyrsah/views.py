from django.shortcuts import render
from django.views import View
from django.contrib.auth import logout, login

from .models import *
from .functions import *


class MainPage(View):

    def get(self, request):

        articles = Article.objects.all().order_by('dateCreate')
        user = User.objects.all()

        context = {
            'articles': articles,
            'users': user
        }
        return render(request, 'index.html', context=context)


class LogIn(View):
    def get(self, request):
        context = {}
        return render(request, 'login.html', context=context)

    def post(self, request):
        context = {}
        return render(request, 'index.html', context=context)


class Register(View):
    def get(self, request):
        context = {}
        return render(request, 'register.html', context=context)

    def post(self, request):
        email = request.POST.get('email')
        login = request.POST.get('login')
        name = request.POST.get('name')
        password = request.POST.get('password')
        print(email)
        print(login)
        print(name)
        print(password)

        User.objects.create(name=name, email=email, login=login, password=password)

        context = {}
        return render(request, 'index.html', context=context)

class BlogContent(View):
    def get(self, request, id):
        article = Article.objects.get(id=id)
        comments = Comment.objects.filter(idArticle=id)
        userAvaComment = []
        for i in comments:
            userAvaComment.append(avaUser(i.idUser.name))
        print(userAvaComment)
        context = {
            'article': article,
            'userAva': avaUser(article.idUser.name),
            'comments': comments,
            'lencomment': len(comments),
            'avaUserCommnets': userAvaComment,
            'len': zip(comments, userAvaComment)
        }
        return render(request, 'watchArticle.html', context=context)
