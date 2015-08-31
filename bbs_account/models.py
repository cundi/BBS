# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

try:
    from urllib.parse import urlencode
except ImportError:  # python 2
    from urllib import urlencode
from django.core import validators
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from utils.utils import upload_to
import django.utils.timezone
from bb.models import Post, Topic
from DjangoUeditor.models import UEditorField
from bb import utils

USER_STATUS = (
    (False, 'Disable'),
    (True, 'Enable'),
)

TZ_CHOICES = [(float(x[0]), x[1]) for x in (
    (-12, '-12'), (-11, '-11'), (-10, '-10'), (-9.5, '-09.5'), (-9, '-09'),
    (-8.5, '-08.5'), (-8, '-08 PST'), (-7, '-07 MST'), (-6, '-06 CST'),
    (-5, '-05 EST'), (-4, '-04 AST'), (-3.5, '-03.5'), (-3, '-03 ADT'),
    (-2, '-02'), (-1, '-01'), (0, '00 GMT'), (1, '+01 CET'), (2, '+02'),
    (3, '+03'), (3.5, '+03.5'), (4, '+04'), (4.5, '+04.5'), (5, '+05'),
    (5.5, '+05.5'), (6, '+06'), (6.5, '+06.5'), (7, '+07'), (8, '+08'),
    (9, '+09'), (9.5, '+09.5'), (10, '+10'), (10.5, '+10.5'), (11, '+11'),
    (11.5, '+11.5'), (12, '+12'), (13, '+13'), (14, '+14'),
)]

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user class.
    """
    username = models.CharField(_('username'), max_length=30, unique=True, db_index=True, primary_key=True,
                                help_text=_('Required. 30 characters or fewer. Letters, digits and '
                                            '@/./+/-/_ only.'),
                                validators=[
                                    validators.RegexValidator(r'^[\w.@+-]+$',
                                                              _('Enter a valid username. '
                                                                'This value may contain only letters, numbers '
                                                                'and @/./+/-/_ characters.'), 'invalid'),
                                ],
                                error_messages={
                                    'unique': _("A user with that username already exists."),
                                })
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField('email address', unique=True)
    date_joined = models.DateTimeField(default=django.utils.timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = u'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def get_group(self):
        return self.objects.values('groups')

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Account(User):
    nickname = models.CharField(max_length=50, blank=True, null=True)
    avatar_img = models.ImageField(upload_to=upload_to, default='da/small.gif')
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    born_date = models.DateField(
        verbose_name=u'出生日期', null=True, blank=True, default=None)
    coins = models.IntegerField(default=0, blank=True, null=True)
    like_topic = models.ManyToManyField(to=Topic, through='UserLTopic', through_fields=('user', 'topic'),
                                        related_name='like_topics')
    collection_topic = models.ManyToManyField(to=Topic, through='UserCTopic', through_fields=('user', 'topic'),
                                              related_name='collection_topics')
    location = models.CharField(max_length=20, blank=True, null=True)
    last_activity = models.DateTimeField(null=True)
    signature = UEditorField(u'内容', width=600, height=300, toolbars="full", imagePath="images/",
                           filePath="files/", upload_settings={"imageMaxSize": 1204000}, settings={}, command=None,
                           blank=True, max_length=settings.SIGNATURE_MAX_LINES)
    time_zone = models.FloatField('时区选择', choices=TZ_CHOICES, default=float(settings.DEFAULT_TIME_ZONE))
    show_signature = models.BooleanField(_('Show Signatures'), blank=True, default=True)
    topic_count = models.IntegerField(_('Topic count'), blank=True, default=0)
    post_count = models.IntegerField('Post count', blank=True, default=0)
    website = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return str(self.username)

    class Meta(object):
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def get_my_absolute_url(self):
        return reverse('bb:my_profile', kwargs={'username': self.username})

    def get_ot_absolute_url(self):
        return reverse('bb:other_profile', kwargs={'username': self.username})

class UserFollower(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=1)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='follower_to_me')

    def __unicode__(self):
        return self.user.username


class UserLTopic(models.Model):
    """
    like and collection
    """
    user = models.ForeignKey(Account, verbose_name='User')
    topic = models.ForeignKey(Topic, verbose_name='Topic')


class UserCTopic(models.Model):
    """
    like and collection
    """
    user = models.ForeignKey(Account, verbose_name='User')
    topic = models.ForeignKey(Topic, verbose_name='Topic')


class Attachment(models.Model):
    """
    """
    class Meta(object):
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')

    post = models.ForeignKey(Post, verbose_name=_('Post'), related_name='attachments')
    size = models.IntegerField(_('Size'))
    file = models.FileField(_('File'), upload_to=upload_to)

    def save(self, *args, **kwargs):
        self.size = self.file.size
        super(Attachment, self).save(*args, **kwargs)

    def size_display(self):
        size = self.size
        if size < 1024:
            return '%db' % size
        elif size < 1024 * 1024:
            return '%dKb' % int(size / 1024)
        else:
            return '%.2fMb' % (size / float(1024 * 1024))
