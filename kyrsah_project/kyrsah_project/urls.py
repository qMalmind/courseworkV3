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
    path('edit-arctile<int:id>', login_required(EditArticle.as_view()), name="edit_article"),
    path('delete-arctile<int:id>', login_required(Delete_article.as_view()), name="delete_article"),
    path('ban-arctile<int:id>', login_required(Ban_article.as_view()), name="ban_article"),
    path('ban-user<int:id>', login_required(Ban_user.as_view()), name="ban_user"),
    path('delete-comment<int:id>', login_required(Delete_comment.as_view()), name="delete_comment"),
    path('add_like<int:id>', login_required(Add_like.as_view()), name="add_like"),
    path('add_dislike<int:id>', login_required(Add_dislike.as_view()), name="add_dislike"),
    path('user/<int:id>', Profile.as_view(), name='profile'),
    path('edit-profile/<int:id>', Edit_profile.as_view(), name='edit_profile'),
]
