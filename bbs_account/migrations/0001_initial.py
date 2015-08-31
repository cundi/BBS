# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bbs_account.models
import django.utils.timezone
from django.conf import settings
import django.core.validators
import utils.utils


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('bb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(primary_key=True, serialize=False, error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username', db_index=True)),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='email address')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('nickname', models.CharField(max_length=50, null=True, blank=True)),
                ('avatar_img', models.ImageField(default='da/small.gif', upload_to=utils.utils.upload_to)),
                ('description', models.TextField(null=True, blank=True)),
                ('address', models.CharField(max_length=50, null=True, blank=True)),
                ('phone', models.CharField(max_length=11, null=True, blank=True)),
                ('born_date', models.DateField(default=None, null=True, verbose_name='\u51fa\u751f\u65e5\u671f', blank=True)),
                ('coins', models.IntegerField(default=0, null=True, blank=True)),
                ('location', models.CharField(max_length=20, null=True, blank=True)),
                ('last_activity', models.DateTimeField(auto_now_add=True)),
                ('signature', models.CharField(max_length=1024, verbose_name='Signature', blank=True)),
                ('show_signature', models.BooleanField(default=True, verbose_name='Show Signatures')),
                ('post_count', models.IntegerField(default=0, verbose_name='Post count', blank=True)),
                ('website', models.URLField(null=True, blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'db_table': 'user',
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', bbs_account.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('size', models.IntegerField(verbose_name='Size')),
                ('file', models.FileField(upload_to=utils.utils.upload_to, verbose_name='File')),
                ('post', models.ForeignKey(related_name='attachments', verbose_name='Post', to='bb.Post')),
            ],
            options={
                'verbose_name': 'Attachment',
                'verbose_name_plural': 'Attachments',
            },
        ),
        migrations.CreateModel(
            name='UserFollower',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('count', models.IntegerField(default=1)),
                ('followers', models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
