from django.contrib import admin
from django.urls import path
from kyrsah.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPage.as_view()),
    path('login/', LogIn.as_view()),
    path('register/', Register.as_view()),
    path('post<int:id>', BlogContent.as_view(), name='post_detail'),
    path('logout/', my_logout),
    path('create-article/', login_required(CreateArticle.as_view())),
    path('edit-arctile<int:id>', login_required(EditArticle.as_view())),
]
