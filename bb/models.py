# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.conf import settings
from DjangoUeditor.models import UEditorField
from uuslug import uuslug
from django.db import models, transaction, DatabaseError
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from django.utils.timezone import now as time_zone_now
from bb.compat import get_atomic_func
import datetime
# from utils.fields import ExtendedImageField
# from utils.utils import upload_to


User = settings.AUTH_USER_MODEL
# 论坛目录结构：
# 论坛首页展现所有板块和分区板块，每个板块下分为若干话题，
# 用户发表话题之下是用户自己和其他用户的回帖
# 板块Category <---> 分区板块Forum <---> 帖Topic <---> 回帖Post |

YES = 1
NO = 0
STATUS_CHOICES = (
    (YES, True),
    (NO, False),
)


class Category(models.Model):
    """
    """
    title = models.CharField(max_length=40)
    slug = models.CharField(max_length=200, blank=True)
    description = models.TextField(null=True, blank=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='category_admin', blank=True, null=True)
    hidden = models.NullBooleanField(blank=False, null=False, default=False, help_text='如果选中，该板块仅对站长可见')
    position = models.IntegerField('Position',blank=True, default=0)

    class Meta:
        ordering = ["title"]
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.title

    def forum_count(self):
        return self.forum_set.all().count()

    def get_absolute_url(self):
        return reverse('bb:category_view', kwargs={'pk': self.id})

    @property
    def topics(self):
        return Topic.objects.filter(forum__category=self).select_related()

    @property
    def posts(self):
        return Post.objects.filter(topic__forum__category=self).select_related()


class Forum(models.Model):
    """
    # 分区实现功能：
    # 1. 显示该话题下每天的帖子更新数
    # 2. 话题总数，所有回帖总数
    # 3. 最后一个话题，及其作者、时间
    """
    category = models.ForeignKey(to=Category, verbose_name='Category', blank=True, null=True)
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    description = models.CharField(blank=True, null=True, max_length=300)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name='分区版主')
    position = models.IntegerField('Position', blank=True, default=0)
    updated = models.DateTimeField('Topic的编辑时间', blank=True, null=True)
    view_count = models.IntegerField('查看计数',default=0, editable=False,)
    topic_count = models.IntegerField('帖子计数', blank=True, default=0)
    post_count = models.IntegerField('回帖计数', blank=True, default=0)
    hidden = models.BooleanField('是否隐藏', blank=True, default=NO, choices=STATUS_CHOICES)
    logo = models.ImageField(blank=True, null=True)
    readed_by = models.ManyToManyField(settings.AUTH_USER_MODEL, through='ForumReadTracker', related_name='readed_forums')
    headline = models.TextField('Headline', blank=True, null=True)

    class Meta:
        ordering = ['position']
        verbose_name = _("Forum")
        verbose_name_plural = _("Forums")

    def __unicode__(self):
        return self.title

    def update_counters(self):
        self.topic_count = Topic.objects.filter(forum=self).count()
        if self.topic_count:
            posts = Post.objects.filter(topic__forum_id=self.id)
            self.post_count = posts.count()
            if self.post_count:
                try:
                    last_post = posts.order_by('-created', '-id')[0]
                    self.updated = last_post.updated or last_post.created
                except IndexError:
                    pass
            else:
                self.post_count = 0
            self.save()

    def get_absolute_url(self):
        return reverse('bb:forum_view', kwargs={'pk': self.id})

    @property
    def posts(self):
        return Post.objects.filter(topic__forum=self).select_related()

    @cached_property
    def last_post(self):
        try:
            return self.posts.order_by('-created', '-id').select_related('author')[0]
        except IndexError:
            return None

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(Forum, self).save(*args, **kwargs)

    @property
    def tp_c(self):
        return self.topic_set.count()

    def forum_view(self):
        self.view_count += 1
        self.save()

    def update_forum_view_count(self):
        view_count = 0
        for topic in self.topic_set.all():
            view_count += topic.view_count
        self.view_count = view_count
        self.save()

    def update_last_topic(self):
        try:
            self.last_topic = self.topic_set.order_by('-created')[0]
        except IndexError:
            self.last_topic = None
        self.save()

    @property
    def td_p(self):
        today = datetime.date.today()
        return self.posts.filter(created__day=today.day)


class Topic(models.Model):
    forum = models.ForeignKey(to=Forum, verbose_name='Forum')
    title = models.CharField('Title', max_length=200)
    slug = models.CharField('Slug', max_length=200, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='topic_author')
    content = UEditorField(u'内容', width=600, height=300, toolbars="full", imagePath="images/",
                           filePath="files/", upload_settings={"imageMaxSize": 1204000}, settings={}, command=None,
                           blank=True)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('编辑时间', null=True)
    view_count = models.IntegerField('查看计数', default=0, editable=False)
    sticky = models.IntegerField('置顶', default=0)
    closed = models.BooleanField('锁定', blank=True, default=False)
    subscriber = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='subscriptions', verbose_name='订阅人', blank=True)
    post_count = models.IntegerField(default=0, editable=False)
    readed_by = models.ManyToManyField(settings.AUTH_USER_MODEL, through='TopicReadTracker', related_name='readed_topics')
    is_manage = models.BooleanField('可否被管理', default=False)
    replied_time = models.DateTimeField('被回复时间', null=True, editable=False)
    subscriber_count = models.IntegerField(default=0, editable=False)

    class Meta:
        ordering = ['-created']
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

    def __unicode__(self):
        return unicode(self.author) + " - " + self.title

    @cached_property
    def head(self):
        try:
            return self.post_set.all().order_by('created', 'id')[0]
        except IndexError:
            return None

    @cached_property
    def last_post(self):
        """
        当前帖子的最后回帖
        """
        try:
            return self.post_set.order_by('-created', '-id').select_related('author')[0]
        except IndexError:
            return None

    def get_absolute_url(self):
        return reverse('bb:topic_view', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(Topic, self).save(*args, **kwargs)

    def delete(self, using=None):
        super(Topic, self).delete(using)
        self.forum.update_counters()

    def update_counters(self):
        """
        强制的对缓存进行重写，以获取真实对最新更新对回帖
        """
        self.reply_count = self.post_set.count()
        if hasattr(self, 'last_post'):
            del self.last_post
        if self.last_post:
            self.updated = self.last_post.updated or self.last_post.created
        self.save()

    def update_reply_count(self):
        self.reply_count = self.post_set.all().count()
        self.save()

    def update_subscriber_count(self):
        self.subscriber_count = self.subscriptions.filter(kind='email').count()
        self.save()

    def editable(self, user):
        """
        帖子在发布60秒之后才能编辑
        """
        if user == self.author:
            if time_zone_now() < self.created + datetime.timedelta(seconds=settings.FORUMS_EDIT_TIMEOUT):
                return True
        return False

    def subscribe(self, user):
        TopicSubscription.objects.get_or_create(topics=self, user=user)

    def unsubscribe(self, user):
        try:
            subscription = TopicSubscription.objects.get(topic=self, user=user)
        except TopicSubscription.DoesNotExist:
            return
        else:
            subscription.delete()

    def subscribed(self, user):
        if user.is_anonymous():
            return False
        try:
            TopicSubscription.objects.get(topic=self, user=user)
        except TopicSubscription.DoesNotExist:
            return False
        else:
            return True


class Post(models.Model):
    """
    对话题（帖子）的回复，即回帖
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='回帖作者')
    topic = models.ForeignKey(to=Topic, verbose_name='Topic')
    content = UEditorField(width=600, height=300, toolbars="full", imagePath="images/",
                           filePath="files/", upload_settings={"imageMaxSize": 1204000}, settings={}, command=None,
                           blank=True
                           )
    created = models.DateTimeField('回帖时间', blank=True, db_index=True)
    updated = models.DateTimeField('帖子编辑时间', blank=True, null=True)
    user_ip = models.GenericIPAddressField('发帖人IP地址', null=True, default='0.0.0.0')
    is_manage = models.BooleanField('是否可管理', default=False)


    class Meta:
        ordering = ['-created']
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __unicode__(self):
        # return str(self.id) + self.topic.title
        return self.snippet()

    def snippet(self):
        """
        回帖内容的摘要
        :return:
        """
        limit = 50
        tail = len(self.content) > limit and '...' or ''
        return self.content[:limit] + tail

    def save(self, *args, **kwargs):
        created_time = time_zone_now()
        if self.created is None:
            self.created = created_time

        new = self.pk is None
        topic_changed = False
        old_post = None
        if not new:
            old_post = Post.objects.get(pk=self.pk)
            if old_post.topic != self.topic:
                topic_changed = True

        super(Post, self).save(*args, **kwargs)

        if self.topic.head == self and not self.is_manage and self.topic.is_manage:
            self.topic.is_manage = False

        self.topic.update_counters()
        self.topic.forum.update_counters()

        if topic_changed:
            old_post.topic.update_counters()
            old_post.topic.forum.update_counters()

    def get_absolute_url(self):
        return reverse('bb:post_view', kwargs={'pk': self.id})

    def delete(self, *args, **kwargs):
        self_id = self.id
        head_post_id = self.topic.post_set.order_by('created', 'id')[0].id

        if self_id == head_post_id:
            self.topic.delete()
        else:
            super(Post, self).delete(*args, **kwargs)
            self.topic.update_counters()
            self.topic.forum.update_counters()


class Tag(models.Model):
    name = models.CharField(max_length=255)
    topic = models.ForeignKey(Topic, related_query_name='tag')
    post = models.ForeignKey(Post, related_query_name='tag')


class TopicSubscription(models.Model):
    topic = models.ForeignKey(Topic, related_name='subscriptions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='forum_subscriptions')

    class Meta:
        unique_together = ('topic', 'user')

    @classmethod
    def setup_onsite(cls):
        for user in User.objects.all():
            topics = Topic.objects.filter(author=user).values_list('pk', flat=True)
            topics_by_replies = Post.objects.filter(author=user).distinct().values_list('topic', flat=True)
            for topic in set(topics).union(topics_by_replies):
                Topic.objects.get(pk=topic).subscribe(user, "onsite")


class TopicReadTrackerManager(models.Manager):
    def get_or_create_tracker(self, user, topic):
        is_new = True
        sid = transaction.savepoint(using=self.db)
        try:
            with get_atomic_func()():
                obj = TopicReadTracker.objects.create(user=user, topic=topic)
            transaction.savepoint(sid)
        except DatabaseError:
            transaction.savepoint_rollback(sid)
            obj = TopicReadTracker.objects.get(user=user, topic=topic)
            is_new = False
        return obj, is_new


class TopicReadTracker(models.Model):
    """
    Save per user topic read tracking
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False)
    topic = models.ForeignKey(Topic, blank=True, null=True)
    time_stamp = models.DateTimeField(auto_now=True)

    objects = TopicReadTrackerManager()

    class Meta(object):
        verbose_name = _('Topic read tracker')
        verbose_name_plural = _('Topic read trackers')
        unique_together = ('user', 'topic')


class ForumReadTrackerManager(models.Manager):
    def get_or_create_tracker(self, user, forum):
        """
        Correctly create tracker in mysql db on default REPEATABLE READ transaction mode

        It's known problem when standrard get_or_create method return can raise exception
        with correct data in mysql database.
        See http://stackoverflow.com/questions/2235318/how-do-i-deal-with-this-race-condition-in-django/2235624
        """
        is_new = True
        sid = transaction.savepoint(using=self.db)
        try:
            with get_atomic_func()():
                obj = ForumReadTracker.objects.create(user=user, forum=forum)
            transaction.savepoint_commit(sid)
        except DatabaseError:
            transaction.savepoint_rollback(sid)
            is_new = False
            obj = ForumReadTracker.objects.get(user=user, forum=forum)
        return obj, is_new


class ForumReadTracker(models.Model):
    """
    Save per user forum read tracking
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False)
    forum = models.ForeignKey(Forum, blank=True, null=True)
    time_stamp = models.DateTimeField(auto_now=True)

    objects = ForumReadTrackerManager()

    class Meta(object):
        verbose_name = _('Forum read tracker')
        verbose_name_plural = _('Forum read trackers')
        unique_together = ('user', 'forum')
