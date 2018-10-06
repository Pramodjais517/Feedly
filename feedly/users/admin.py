from django.contrib import admin
from .models import MyProfile
from .models import Post,Vote,Comment

admin.site.register(Post)
admin.site.register(Vote)
admin.site.register(MyProfile)
admin.site.register(Comment)