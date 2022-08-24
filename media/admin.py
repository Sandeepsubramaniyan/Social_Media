from django.contrib import admin
from .models import  FollowerCount, Post, Profile, LikePost
# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowerCount)


