from django.shortcuts import render
from django.views import View
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q

from .models import *
from .functions import *


class MainPage(View):

    def get(self, request):

        articles = Article.objects.filter(haveBan=False).order_by('-dateCreate')
        users = User.objects.all()


        try:
            current_user = avaUser(request.user.name)
            full_current_user = request.user
        except:
            current_user = None
            full_current_user = None

        query = self.request.GET.get('q')
        if query:
            articles = Article.objects.filter(
                Q(title__icontains=query)
            ).filter(haveBan=False)


        len_articles = len(articles)

        trends = self.request.GET.get('order-likes')
        if trends:
            articles = Article.objects.filter(haveBan=False).order_by('-countLikes')
            print('trends')

        anti_trends = self.request.GET.get('order-dislikes')
        if anti_trends:
            articles = Article.objects.filter(haveBan=False).order_by('-countDislikes')
            print('anti-trends')

        news_articles = self.request.GET.get('order-date')
        if news_articles:
            articles = Article.objects.filter(haveBan=False).order_by('-dateCreate')
            print('news')

        context = {
            'articles': articles,
            'len_articles': len_articles,
            'users': users,
            'current_user': current_user,
            'full_current_user': full_current_user
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

        if (User.objects.filter(email=login_or_email) or User.objects.filter(login=login_or_email)):
            try:
                usr = User.objects.get(login=login_or_email)
            except:
                usr = User.objects.get(email=login_or_email)

            if usr.check_password(password):

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
        color = request.POST.get('color')
        print(email)
        print(login)
        print(name)
        print(password)
        print(color)

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
            User.objects.create(name=name, email=email, login=login, color=color, password=make_password(password))
            print("create user")
            return HttpResponseRedirect('/')


class Profile(View):

    def get(self, request, id):

        user = User.objects.get(id=id)
        user_avatar = avaUser(user.name)
        articles = Article.objects.filter(idUser=id, haveBan=False).order_by('dateCreate')

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


class Edit_profile(View):

     def get(self, request, id):
         user = User.objects.get(id=id)

         try:
             current_user = avaUser(request.user.name)
             full_current_user = request.user
         except:
             current_user = None
             full_current_user = None

         if user.id != full_current_user.id:
             return HttpResponseRedirect("/")



         context = {
             'current_user': current_user,
             'full_current_user': full_current_user,
             'user': user,
         }

         return render(request, 'changeProfile.html', context=context)

     def post(self, request, id):

         user = User.objects.get(id=id)

         login = request.POST.get('login')
         name = request.POST.get('name')
         mail = request.POST.get('email')
         city = request.POST.get('city')
         color = request.POST.get('color')

         user.login = login
         user.name = name
         user.email = mail
         user.city = city
         user.color = color

         user.save()

         return HttpResponseRedirect(f"/user/{user.id}")


class Ban_user(View):
    def get(self, request, id):
        if not(request.user.is_staff):
            return HttpResponseRedirect('/')

        user = User.objects.get(id=id)
        user.haveBan = True
        user.save()

        return HttpResponseRedirect('/')

#     ======== Всё что связно со статьями

class CreateArticle(View):
    def get(self, request):
        try:
            current_user = avaUser(request.user.name)
            full_current_user = request.user
        except:
            current_user = None
            full_current_user = None
        context = {
            'current_user': current_user,
            'current_user_ava': current_user,
            'full_current_user': full_current_user

        }

        if full_current_user.haveBan:
            return HttpResponseRedirect("/")

        return render(request, 'createEditArticle.html', context=context)

    def post(self, request):

        title_article = request.POST.get('title_article')
        content_article = request.POST.get('content')
        color_article = request.POST.get('color_article')

        c = Article.objects.create(title=title_article,
                                   content=content_article,
                                   idUser=request.user,
                                   color=color_article)

        return HttpResponseRedirect('/')


class EditArticle(View):
    def get(self, request, id):

        article = Article.objects.get(id=id)

        if request.user != article.idUser:
            return HttpResponseRedirect('/')

        try:
            current_user = avaUser(request.user.name)
            full_current_user = request.user
        except:
            current_user = None
            full_current_user = None

        context = {
            'article': article,
            'current_user': current_user,
            'full_current_user': full_current_user
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
        del_article = Delete_article()

        userAvaComment = []
        for i in comments:
            userAvaComment.append(avaUser(i.idUser.name))

        try:
            current_user = avaUser(request.user.name)
            full_current_user = request.user
        except:
            current_user = None
            full_current_user = None

        check_like = LikeOrDislike.objects.filter(idUser=request.user.id, idArticle=id, like=True)
        check_dislike = LikeOrDislike.objects.filter(idUser=request.user.id, idArticle=id, like=False)
        like = False
        dislike = False
        if check_like:
            like = True
        if check_dislike:
            dislike = True

        context = {
            'article': article,
            'userAva': avaUser(article.idUser.name),
            'avaUserCommnets': userAvaComment,
            'current_user': current_user,
            'full_current_user': full_current_user,
            'comments': comments,
            'lencomment': len(comments),
            'len': zip(comments, userAvaComment),
            'del_article': del_article,
            'like': like,
            'dislike': dislike
        }
        return render(request, 'watchArticle.html', context=context)

    def post(self, request, id):

       text_comment = request.POST.get('commnet-text')
       article = Article.objects.get(id=id)
       comment = Comment.objects.create(text=text_comment, idArticle=article, idUser=request.user)

       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class Delete_article(View):
    def get(self, request, id):
        article = Article.objects.get(id=id)

        if request.user.id == article.idUser.id or request.user.is_staff:
            article.delete()

        return HttpResponseRedirect('/')


class Delete_comment(View):
    def get(self, request,  id):
        comment = Comment.objects.get(id=id)
        if request.user.id == comment.idUser.id or request.user.is_superuser:
            comment.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class Ban_article(View):
    def get(self, request, id):
        if not(request.user.is_staff):
            return HttpResponseRedirect('/')

        article = Article.objects.get(id=id)
        article.haveBan = True
        article.save()

        return HttpResponseRedirect('/')


class Add_like(View):
    def get(self, request, id):
        article = Article.objects.get(id=id)

        likeOrDislike = LikeOrDislike.objects.filter(idUser=request.user.id, idArticle=id, like=True)

        if likeOrDislike:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        article.countLikes += 1
        article.save()
        l1 = LikeOrDislike.objects.create(idUser=request.user, idArticle=article, like=True)


        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class Add_dislike(View):
    def get(self, request, id):
        article = Article.objects.get(id=id)


        likeOrDislike = LikeOrDislike.objects.filter(idUser=request.user.id, idArticle=id, like=False)

        if likeOrDislike:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        article.countDislikes += 1
        article.save()
        l1 = LikeOrDislike.objects.create(idUser=request.user, idArticle=article, like=False)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




















