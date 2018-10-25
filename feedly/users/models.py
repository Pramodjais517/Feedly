from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField




class MyProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length=10, blank=True,null=True,default='')
    last_name = models.CharField(max_length=10, blank=True,null=True,default='')
    phone_number = PhoneNumberField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
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
    post_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # subfeed = models.ForeignKey(MyProfile,on_delete=models.CASCADE,null=True,blank=True)
    about = models.TextField(max_length=100, null=True, blank=True)
    post_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_pics',blank=True,null=True)
    text = models.TextField(max_length=800, null=True, blank=True)
    video = models.FileField(upload_to ='post_videos', null=True, blank=True)
    result = models.PositiveIntegerField(default=0)

    def __str__(self):
        return ("%s posted : %s" %(self.post_by.username,self.about))

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete= models.CASCADE)
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    status = models.BooleanField(default= False)

    def __str__(self):
        return ("%s voted %s" %(self.voter.username,self.post.about))

    def get_comments(self):
        return 'hello'



class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete= models.CASCADE)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    comment_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s commented on %s" %(self.comment_by.username,self.post.about)


