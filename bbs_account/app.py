# coding: utf-8
from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'bbs_account'
    verbose_name = 'BBS Account'

    def ready(self):
        from bbs_account import signals
