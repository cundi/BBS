# The views used below are normally mapped in django.contrib.admin.urls.py
# This URLs file is used to provide a reliable view deployment for test purposes.
# It is also provided as a convenience to those who want to deploy these URLs
# elsewhere.

from django.conf.urls import url
from bbs_account import views

urlpatterns = [
    url(r'^register_ask/$', views.register_ask, name='register_ask'),
    url(r'^register_ask/done$', views.register_ask_done, name='register_ask_done'),
    url(r'^login/$', views.login, name='login'),
    url(r'^profile/(?P<username>\w+)$', views.others_profile, name='others_profile'),
    url(r'^profile/(?P<username>\w+)/topic&post/$', views.user_topic_post, name='user_topic_post'),
    url(r'^my_profile/$', views.my_profile, name='my_profile'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^password_change/$', views.password_change, name='password_change'),
    url(r'^password_change/done/$', views.password_change_done, name='password_change_done'),
    url(r'^password_reset/$', views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete, name='password_reset_complete'),
]
