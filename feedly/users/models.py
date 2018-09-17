from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User



def avatar_id(instance, filename):    # to give unique id to profile pic uploaded by using uuid
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('profile_pic', filename)



class MyProfile(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    avatar = models.ImageField(upload_to=avatar_id, default='static/images/avatar.jgp')

    def __str__(self):
        return self.user.username