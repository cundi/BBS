# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bb', '0002_auto_20150818_2102'),
        ('bbs_account', '0002_auto_20150818_2102'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic', models.ForeignKey(verbose_name='Topic', to='bb.Topic')),
            ],
        ),
        migrations.CreateModel(
            name='UserLTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic', models.ForeignKey(verbose_name='Topic', to='bb.Topic')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='topic_count',
            field=models.IntegerField(default=0, verbose_name='Topic count', blank=True),
        ),
        migrations.AlterField(
            model_name='userfollower',
            name='followers',
            field=models.ManyToManyField(related_name='follower_to_me', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userltopic',
            name='user',
            field=models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userctopic',
            name='user',
            field=models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='account',
            name='collection_topic',
            field=models.ManyToManyField(related_name='collection_topics', through='bbs_account.UserCTopic', to='bb.Topic'),
        ),
        migrations.AddField(
            model_name='account',
            name='like_topic',
            field=models.ManyToManyField(related_name='like_topics', through='bbs_account.UserLTopic', to='bb.Topic'),
        ),
    ]
