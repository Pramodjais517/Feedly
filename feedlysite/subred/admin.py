from django.contrib import admin
from .models import Category, Posts, Subcategory

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Posts)

