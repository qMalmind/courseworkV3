from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, login, password):
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
    dateRegistration = models.TimeField(default=timezone.now())

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'login'
    objects = CustomUserManager()

    def __str__(self):
        return self.login


class Article(models.Model):
    title = models.CharField(max_length=128, null=False)
    content = models.CharField(null=False, max_length=16384)
    haveBan = models.BooleanField(default=False)
    color = models.CharField(default="#ccc", max_length=16)
    countLikes = models.IntegerField(default=0)
    countDislikes = models.IntegerField(default=0)
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
