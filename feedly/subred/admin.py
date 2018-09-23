from django.contrib import admin
from .models import Category, Subreddit, Description

admin.site.register(Category)
admin.site.register(Subreddit)
admin.site.register(Description)

