# from django.db import models
#
# # Create your models here.
# class MyUsers(models.Model):
#     user = models.OneToOneField(User)
#     first_name = models.CharField(max_length=100, blank=True)
#     last_name = models.CharField(max_length=100, blank=True)
#     email = models.EmailField(max_length=100, blank=True, unique=True)
#     company = models.CharField(max_length=100, blank=True, null=True)
#     website = models.URLField(max_length=100, blank=True, null=True)
#     phone_number = models.CharField(max_length=100, blank=True, null=True)
#
#     def __str__(self):
#         return self.user.username