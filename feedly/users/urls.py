from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.Activate.as_view(),
        name='activate'),
    url(r'^profile/(?P<user_id>[0-9]+)/$', views.ProfileView.as_view(), name='profile'),
    url(r'^profile/(?P<user_id>[0-9]+)/edit/$', views.EditProfileView.as_view(),
        name='edit_profile'),
    url(r'^profile/(?P<user_id>[0-9]+)/delete/$', views.DeleteAccount.as_view(),
        name='account_del'),
    url(r'^profile/(?P<user_id>[0-9]+)/create_post/(?P<ch>[0-9A-Za-z]+)$', views.CreatePostView.as_view(),
        name='createpost'),
 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)