from django.shortcuts import render
from django.views import View
from django.db.models import Q

from .models import *
from .functions import *
from .forms import *

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

        context = {
            'article': article,
            'userAva': avaUser(article.idUser.name),
            'avaUserCommnets': userAvaComment,
            'current_user': current_user,
            'full_current_user': full_current_user,
            'comments': comments,
            'lencomment': len(comments),
            'len': zip(comments, userAvaComment),
            'del_article': del_article
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