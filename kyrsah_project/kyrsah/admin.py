from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(TagAndArticle)
admin.site.register(LikeOrDislike)
admin.site.register(Comment)
admin.site.register(Role)
