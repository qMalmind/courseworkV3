from django.contrib import admin
from django.urls import path
from kyrsah.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPage.as_view()),
    path('login/', LogIn.as_view()),
    path('register/', Register.as_view()),
    path('post<int:id>', BlogContent.as_view(), name='post_detail'),
]
