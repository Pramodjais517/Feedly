import uuid
from django.db import models
from django.contrib.auth.models import User
import os



def avatar_id(instance, filename):    # to give unique id to profile pic uploaded by using uuid
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('static/images', filename)



class MyProfile(models.Model):
    account = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True,null=True)
    last_name = models.CharField(max_length=100, blank=True,null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    avatar = models.ImageField(upload_to=avatar_id, default='static/images/avatar.jgp',null=True)
    GENDER_CHOICES=(
        ('Male','Male'),
        ('Female','Female'),
        ('Others','Others')
    )
    gender=models.CharField(max_length=10,choices=GENDER_CHOICES,default='Male')

    def __str__(self):
        return self.account.username