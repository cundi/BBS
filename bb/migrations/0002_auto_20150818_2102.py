# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumReadTracker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_stamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Forum read tracker',
                'verbose_name_plural': 'Forum read trackers',
            },
        ),
        migrations.CreateModel(
            name='TopicReadTracker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_stamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Topic read tracker',
                'verbose_name_plural': 'Topic read trackers',
            },
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='reply_count',
            new_name='post_count',
        ),
        migrations.RemoveField(
            model_name='post',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='post',
            name='edited_by',
        ),
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='is_read',
        ),
        migrations.AddField(
            model_name='category',
            name='manager',
            field=models.ForeignKey(related_name='category_admin', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='forum',
            name='category',
            field=models.ForeignKey(verbose_name='Category', blank=True, to='bb.Category', null=True),
        ),
        migrations.AddField(
            model_name='forum',
            name='headline',
            field=models.TextField(null=True, verbose_name='Headline', blank=True),
        ),
        migrations.AddField(
            model_name='forum',
            name='manager',
            field=models.ForeignKey(verbose_name='\u5206\u533a\u7248\u4e3b', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(default=0, verbose_name='\u56de\u5e16\u4f5c\u8005', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='is_manage',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u53ef\u7ba1\u7406'),
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(default='', verbose_name='Topic', to='bb.Topic'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='post',
            field=models.ForeignKey(related_query_name='tag', default='', to='bb.Post'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='topic',
            field=models.ForeignKey(related_query_name='tag', default='', to='bb.Topic'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='author',
            field=models.ForeignKey(default='', verbose_name='topic_author', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='closed',
            field=models.BooleanField(default=False, verbose_name='\u9501\u5b9a'),
        ),
        migrations.AddField(
            model_name='topic',
            name='forum',
            field=models.ForeignKey(default='', verbose_name='Forum', to='bb.Forum'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='is_manage',
            field=models.BooleanField(default=False, verbose_name='\u53ef\u5426\u88ab\u7ba1\u7406'),
        ),
        migrations.AddField(
            model_name='topic',
            name='subscriber',
            field=models.ManyToManyField(related_name='subscriptions', verbose_name='\u8ba2\u9605\u4eba', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='topicsubscription',
            name='user',
            field=models.ForeignKey(related_name='forum_subscriptions', default='', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='position',
            field=models.IntegerField(default=0, verbose_name='Position', blank=True),
        ),
        migrations.AlterField(
            model_name='forum',
            name='hidden',
            field=models.BooleanField(default=0, verbose_name='\u662f\u5426\u9690\u85cf', choices=[(1, True), (0, False)]),
        ),
        migrations.AlterField(
            model_name='forum',
            name='updated',
            field=models.DateTimeField(null=True, verbose_name='Topic\u7684\u7f16\u8f91\u65f6\u95f4', blank=True),
        ),
        migrations.AlterField(
            model_name='forum',
            name='view_count',
            field=models.IntegerField(default=0, verbose_name='\u67e5\u770b\u8ba1\u6570', editable=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(null=True, verbose_name='\u5e16\u5b50\u7f16\u8f91\u65f6\u95f4', blank=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='replied_time',
            field=models.DateTimeField(verbose_name='\u88ab\u56de\u590d\u65f6\u95f4', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='topic',
            name='slug',
            field=models.CharField(max_length=200, null=True, verbose_name='Slug', blank=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='sticky',
            field=models.IntegerField(default=0, verbose_name='\u7f6e\u9876'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='updated',
            field=models.DateTimeField(null=True, verbose_name='\u7f16\u8f91\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='view_count',
            field=models.IntegerField(default=0, verbose_name='\u67e5\u770b\u8ba1\u6570', editable=False),
        ),
        migrations.AlterUniqueTogether(
            name='topicsubscription',
            unique_together=set([('topic', 'user')]),
        ),
        migrations.AddField(
            model_name='topicreadtracker',
            name='topic',
            field=models.ForeignKey(blank=True, to='bb.Topic', null=True),
        ),
        migrations.AddField(
            model_name='topicreadtracker',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='forumreadtracker',
            name='forum',
            field=models.ForeignKey(blank=True, to='bb.Forum', null=True),
        ),
        migrations.AddField(
            model_name='forumreadtracker',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='topicsubscription',
            name='kind',
        ),
        migrations.AddField(
            model_name='forum',
            name='readed_by',
            field=models.ManyToManyField(related_name='readed_forums', through='bb.ForumReadTracker', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='topic',
            name='readed_by',
            field=models.ManyToManyField(related_name='readed_topics', through='bb.TopicReadTracker', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='topicreadtracker',
            unique_together=set([('user', 'topic')]),
        ),
        migrations.AlterUniqueTogether(
            name='forumreadtracker',
            unique_together=set([('user', 'forum')]),
        ),
    ]
