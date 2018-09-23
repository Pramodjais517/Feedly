
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length = 100, unique= True, default = '')

    def __str__(self):
        return self.name


class Subreddit(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub = models.CharField(max_length = 127, unique = True)

    def __str__(self):
        return self.sub


class Description(models.Model):
    cat = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    description = models.TextField(max_length = 2000)
    img = models.ImageField()

    def __str__(self):
        return self.description
