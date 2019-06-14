from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings


class MyProfile(models.Model):
    """model for storing user credentials"""
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length=10, blank=True,null=True,default='')
    last_name = models.CharField(max_length=10, blank=True,null=True,default='')
    phone_number = PhoneNumberField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(default='profile_pic/profile.png', upload_to='profile_pic')
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
        """creating a profile before saving a user"""
        if created:
            MyProfile.objects.create(user=instance)


    @receiver(post_save, sender=User)
    def save_myprofile(sender, instance, **kwargs):
        """saving the profile instance before saving user instanace"""
        instance.myprofile.first_name = instance.first_name
        instance.myprofile.last_name = instance.last_name
        instance.myprofile.save()


class Post(models.Model):
    """model for creating post """
    post_by = models.ForeignKey(User, on_delete=models.CASCADE)
    about = models.TextField(max_length=100, null=True, blank=True)
    post_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_pics',blank=True,null=True)
    text = models.TextField(max_length=800, null=True, blank=True)
    video = models.FileField(upload_to ='post_videos', null=True, blank=True)
    result = models.PositiveIntegerField(default=0)

    def __str__(self):
        return ("%s posted : %s" %(self.post_by.username,self.about))


class Vote(models.Model):
    """for countinng the number of votes on a post"""
    voter = models.ForeignKey(User, on_delete= models.CASCADE)
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    status = models.BooleanField(default= False)

    def __str__(self):
        return "%s voted %s" %(self.voter.username,self.post.about)


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete= models.CASCADE)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    comment_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s commented on %s" %(self.comment_by.username,self.post.about)


class FriendList(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='mylist')
    friends = models.ManyToManyField(User)

    def __str__(self):
        return "friend list of %s"%(self.user.username)

    @receiver(post_save, sender=User)
    def create_friendlist(sender, instance, created, **kwargs):
        if created:
            obj=FriendList.objects.create(user=instance)
            obj.save()

class FriendRequest(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='receiver')
    friend_request = models.ManyToManyField(User)

    def __str__(self):
        return "friend request to %s"%(self.user.username)

    @receiver(post_save, sender=User)
    def create_friendrequest(sender, instance, created, **kwargs):
        if created:
            obj=FriendRequest.objects.create(user=instance)
            obj.save()

class FriendRequestSent(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='sender')
    request_sent = models.ManyToManyField(User)

    @receiver(post_save, sender=User)
    def create_friendrequestsent(sender, instance, created, **kwargs):
        if created:
            obj=FriendRequestSent.objects.create(user=instance)
            obj.save()

    def __str__(self):
        return "sent request of %s"%(self.user.username)