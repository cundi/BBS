# coding:utf-8

from __future__ import unicode_literals
from django.contrib.auth.models import Permission
from django.contrib.auth.models import ContentType
from bb.subscription import notify_topic_subscribers
from bb import utils, compat
from django.conf import settings
from bb.permission import perms


def post_saved(instance, **kwargs):
    if not settings.FORUM_DISABLE_NOTIFICATIONS:
        notify_topic_subscribers(instance)

        if utils.get_bb_profile(instance.author).autosubscribed and \
                perms.may_subscribe_topic(instance.author, instance.topic):
            instance.topic.subscriber.add(instance.author)

    if kwargs['created']:
        profile = utils.get_bb_profile(instance.author)
        profile.post_count = instance.author.posts.count()
        profile.save()


def post_deleted(instance, **kwargs):
    Profile = utils.get_pybb_profile_model()
    User = compat.get_user_model()
    try:
        profile = utils.get_bb_profile(instance.author)
    except (Profile.DoesNotExist, User.DoesNotExist) as e:
        # When we cascade delete an user, profile and posts are also deleted
        pass
    else:
        profile.post_count = instance.author.posts.count()
        profile.save()
