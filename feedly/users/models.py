import uuid
from django.db import models
from django.contrib.auth.models import User
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


class MyProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True,null=True,default='')
    last_name = models.CharField(max_length=100, blank=True,null=True,default='')
    phone_number = PhoneNumberField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    avatar = models.ImageField(default='profile.png', upload_to='profile_pic')
    GENDER_CHOICES=(
        ('Male','Male'),
        ('Female','Female'),
        ('Others','Others')
    )
    gender=models.CharField(max_length=10,choices=GENDER_CHOICES,default='')

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_myprofile(sender, instance, created, **kwargs):
        if created:
            MyProfile.objects.create(user=instance)


    @receiver(post_save, sender=User)
    def save_myprofile(sender, instance, **kwargs):
        instance.myprofile.save()