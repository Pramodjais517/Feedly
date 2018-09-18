from django.db import models
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length = 100, unique= True, default='000000')

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ManyToManyField(Category)
    sub = models.CharField(max_length = 127, unique = True)

    def __str__(self):
        return self.sub

class Posts(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    posts = models.TextField(max_length = 2000)
    img = models.ImageField()

    def __str__(self):
        return self.posts
