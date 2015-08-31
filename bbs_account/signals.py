from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from bbs_account import models


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_handler(sender, instance, created, **kwargs):
    if not created:
        return
    # create user object, only if it is newly created
    account = models.Account(username=instance)
    account.save()

