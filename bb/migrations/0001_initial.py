# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=40)),
                ('slug', models.CharField(max_length=200, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('hidden', models.NullBooleanField(default=0, help_text='\u5982\u679c\u9009\u4e2d\uff0c\u8be5\u677f\u5757\u4ec5\u5bf9\u7ad9\u957f\u53ef\u89c1')),
                ('position', models.IntegerField(default=0, blank=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=300, null=True, blank=True)),
                ('position', models.IntegerField(default=0, verbose_name='Position', blank=True)),
                ('updated', models.DateTimeField(null=True, verbose_name='Updated', blank=True)),
                ('view_count', models.IntegerField(default=0, verbose_name='forum view count', editable=False)),
                ('topic_count', models.IntegerField(default=0, verbose_name='\u5e16\u5b50\u8ba1\u6570', blank=True)),
                ('post_count', models.IntegerField(default=0, verbose_name='\u56de\u5e16\u8ba1\u6570', blank=True)),
                ('hidden', models.BooleanField(default=0, verbose_name='\u5206\u533a\u9ed8\u8ba4\u4e0d\u9690\u85cf', choices=[(1, 'YES'), (0, 'NO')])),
                ('logo', models.ImageField(null=True, upload_to=b'', blank=True)),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'Forum',
                'verbose_name_plural': 'Forums',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=200)),
                ('content', DjangoUeditor.models.UEditorField(blank=True)),
                ('created', models.DateTimeField(db_index=True, verbose_name='\u56de\u5e16\u65f6\u95f4', blank=True)),
                ('updated', models.DateTimeField(null=True, verbose_name='\u5e16\u5b50\u88ab\u7f16\u8f91\u65f6\u95f4', blank=True)),
                ('user_ip', models.GenericIPAddressField(default='0.0.0.0', null=True, verbose_name='\u53d1\u5e16\u4ebaIP\u5730\u5740')),
                ('deleted', models.BooleanField(default=0, choices=[(1, 'YES'), (0, 'NO')])),
                ('edited_by', models.CharField(max_length=25, blank=True)),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('slug', models.CharField(max_length=200, verbose_name='Slug')),
                ('content', DjangoUeditor.models.UEditorField(verbose_name='\u5185\u5bb9', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(null=True)),
                ('view_count', models.IntegerField(default=0, editable=False)),
                ('reply_count', models.IntegerField(default=0, editable=False)),
                ('replied_time', models.DateTimeField(null=True, editable=False)),
                ('is_active', models.BooleanField(default=1, choices=[(1, 'YES'), (0, 'NO')])),
                ('is_read', models.BooleanField(default=0, choices=[(1, 'YES'), (0, 'NO')])),
                ('sticky', models.IntegerField(default=0)),
                ('deleted', models.BooleanField(default=0, choices=[(1, 'YES'), (0, 'NO')])),
                ('subscriber_count', models.IntegerField(default=0, editable=False)),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
            },
        ),
        migrations.CreateModel(
            name='TopicSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.CharField(max_length=15)),
                ('topic', models.ForeignKey(related_name='subscriptions', to='bb.Topic')),
            ],
        ),
    ]
