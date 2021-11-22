from django.db import models
from django.utils import timezone


class Role(models.Model):
    roleName = models.CharField(max_length=32, unique=True)


class User(models.Model):
    name = models.CharField(max_length=32, null=False)
    login = models.CharField(max_length=64, unique=True, null=False)
    password = models.CharField(max_length=512, null=False)
    email = models.CharField(max_length=128, null=False)
    city = models.CharField(max_length=32, null=True)
    haveBan = models.BooleanField(default=False)
    color = models.CharField(default="#ccc", max_length=16)
    dateRegistration = models.TimeField(default=timezone.now())

    idRole = models.ForeignKey(Role, on_delete=models.CASCADE)


class Article(models.Model):
    title = models.CharField(max_length=128, null=False)
    content = models.CharField(null=False, max_length=16384)
    haveBan = models.BooleanField(default=False)
    color = models.CharField(default="#ccc", max_length=16)
    countLikes = models.IntegerField()
    countDislikes = models.IntegerField()
    dateCreate = models.TimeField(default=timezone.now())

    idUser = models.ForeignKey(User, on_delete=models.CASCADE)


class Tag(models.Model):
    tagName = models.CharField(max_length=32)


class TagAndArticle(models.Model):
    idTag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    idArticle = models.ForeignKey(Article, on_delete=models.CASCADE)


class LikeOrDislike(models.Model):
    like = models.BooleanField()
    idArticle = models.ForeignKey(Article, on_delete=models.CASCADE)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.CharField(max_length=1024)

    idArticle = models.ForeignKey(Article, on_delete=models.CASCADE)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
