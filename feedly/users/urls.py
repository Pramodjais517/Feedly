from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.home.as_view(), name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate,
        name='activate'),
    url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    # url(r'^create_post/$', views.create_post_view, name='create_post'),
 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
