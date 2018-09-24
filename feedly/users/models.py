from django.db import models
from django.contrib.auth.models import User
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
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    )
    gender=models.CharField(max_length=10, choices=GENDER_CHOICES, default='')

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_myprofile(sender, instance, created, **kwargs):
        if created:
            MyProfile.objects.create(user=instance)


    @receiver(post_save, sender=User)
    def save_myprofile(sender, instance, **kwargs):
        instance.myprofile.save()


#creating posts on timeline
class Post(models.Model):
    post_by = models.ForeignKey(User,on_delete=models.CASCADE)
    # subfeed = models.ForeignKey(Subfeed,on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True)
    post_on = models.DateTimeField(auto_now_add=True)
    image_post = models.ImageField(upload_to='post_pics')
    text_post = models.CharField(max_length=800, null=True, blank=True)

    def __str__(self):
        return self.title

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return "%s voted %s", (self.voter.username, self.link.title)