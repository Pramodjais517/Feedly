from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Vote)
admin.site.register(MyProfile)
admin.site.register(Comment)
admin.site.register(FriendList)
admin.site.register(FriendRequest)
admin.site.register(FriendRequestSent)