
from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile, posts

admin.site.register(UserProfile)
admin.site.register(posts)
