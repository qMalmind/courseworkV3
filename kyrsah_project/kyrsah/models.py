import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.db.models.functions import Lower
from django.db.models import CharField


class CustomUserManager(BaseUserManager):
    def create_user(self, login, password, name, email, color):
        user = self.model(login=login, password=password)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)

        return user

    def create_superuser(self, login, password):
        user = self.model(login=login, password=password)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, login):
        return self.get(login=login)



class User(AbstractBaseUser, PermissionsMixin):
    login = models.CharField(max_length=64, unique=True, null=False)
    password = models.CharField(max_length=512, null=False)

    name = models.CharField(max_length=32, null=False)
    email = models.CharField(max_length=128, null=False)
    city = models.CharField(max_length=32, null=True)
    haveBan = models.BooleanField(default=False)
    color = models.CharField(default="#ccc", max_length=16)
    dateRegistration = models.DateField(default=datetime.date.today())

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'login'
    objects = CustomUserManager()

    def __repr__(self):
        return User()


class To_lower_field(models.CharField):
    def __init__(self, *args, **kwargs):
        super(To_lower_field, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


class Article(models.Model):
    title = To_lower_field(max_length=128, null=False)
    content = models.CharField(null=False, max_length=16384)
    haveBan = models.BooleanField(default=False)
    color = models.CharField(default="#ccc", max_length=16)
    countLikes = models.IntegerField(default=0)
    countDislikes = models.IntegerField(default=0)
    dateCreate = models.DateTimeField(default=datetime.datetime.now())

    idUser = models.ForeignKey(User, on_delete=models.CASCADE)


class LikeOrDislike(models.Model):
    like = models.BooleanField()
    idArticle = models.ForeignKey(Article, on_delete=models.CASCADE)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)

    def __repr__(self):
        return {'idUser': self.idUser, 'idArticle': self.idArticle, 'like': self.like}


class Comment(models.Model):
    text = models.CharField(max_length=1024)

    idArticle = models.ForeignKey(Article, on_delete=models.CASCADE)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
