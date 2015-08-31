# coding:utf-8

from django.conf.urls import url
from bb import  views

urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^category/all/$', views.category_all, name='category_all'),
    url(r'^category/(?P<cid>\d+)/$', views.category_view, name='category_view'),
    url(r'^forum/(?P<forum_id>\d+)/$', views.forum_view, name='forum_view'),
    url(r'^forums/topics/$', views.all_forum_topics, name='forums_topics'),
    url(r'^forum/(?P<forum_id>\d+)/create_topic/$', views.create_topic, name='create_topic'),
    url(r'^forum/(?P<forum_id>\d+)/topic_all/$', views.forum_topics, name='forum_topic_all'),
    url(r'^topic/(?P<pk>\d+)/$', views.topic_view, name='topic_view'),
    url(r'^topic/(?P<topic_id>\d+)/reply/$', views.create_topic_reply, name='create_topic_reply'),
    url(r'^topic/(?P<tid>\d+)/fast_reply$', views.fast_topic_reply, name='fast_topic_reply'),
    url(r'^topic/(?P<topic_id>\d+)/edit/$', views.edit_topic, name='edit_topic'),
    url(r'^topic(?P<topic_id>\d+)/delete/$', views.delete_topic, name='delete_topic'),
    url(r'^post/(?P<post_id>\d+)/delete/$', views.delete_topic_reply, name='delete_topic_reply'),
    url(r'^search(?P<kw>.*?)/$', views.search, name='search'),
]
