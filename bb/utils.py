# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import uuid
from datetime import datetime
import hashlib
import types

from django.utils.importlib import import_module
from django.utils.six import string_types
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from bb.compat import get_username_field, get_user_model

# from pybb.defaults import (
#     PYBB_MARKUP, PYBB_MARKUP_ENGINES_PATHS,
#     PYBB_MARKUP_ENGINES, PYBB_QUOTE_ENGINES
# )
# from pybb.markup.base import BaseParser

# TODO in the next major release : delete _MARKUP_ENGINES_FORMATTERS and _MARKUP_ENGINES_QUOTERS
_MARKUP_ENGINES = {}
_MARKUP_ENGINES_FORMATTERS = {}
_MARKUP_ENGINES_QUOTERS = {}

deprecated_func_warning = ('Deprecated function. Please configure correctly the PYBB_MARKUP_ENGINES_PATHS and'
                           'use get_markup_engine().%(replace)s() instead of %(old)s()(content).'
                           'In the next major release, this function will be deleted.')


def resolve_class(name):
    """ resolves a class function given as string, returning the function """
    if not name:
        return None
    modname, funcname = name.rsplit('.', 1)
    return getattr(import_module(modname), funcname)()


def resolve_function(path):
    if path:
        path = path.split('.')
        to_import = path.pop()
        module = import_module('.'.join(path))
        if module:
            return getattr(module, to_import)
    return None


# def get_markup_engine(name=None):
#     """
#     Returns the named markup engine instance, or the default one if name is not given.
#     This function will replace _get_markup_formatter and _get_markup_quoter in the
#     next major release.
#     """
#     name = name or PYBB_MARKUP
#     engine = _MARKUP_ENGINES.get(name)
#     if engine:
#         return engine
#     if name not in PYBB_MARKUP_ENGINES_PATHS:
#         engine = BaseParser()
#     else:
#         engine = PYBB_MARKUP_ENGINES[name]
#         # TODO In a near future, we should stop to support callable
#         if isinstance(engine, string_types):
#             # This is a path, import it
#             engine = resolve_class(engine)
#     _MARKUP_ENGINES[name] = engine
#     return engine


# TODO In the next major release, delete this function
# def _get_markup_formatter(name=None):
#     """
#     Returns the named parse engine, or the default parser if name is not given.
#     """
#     warnings.warn(deprecated_func_warning % {'replace': 'format', 'old': '_get_markup_formatter'},
#                   DeprecationWarning)
#     name = name or PYBB_MARKUP
#
#     engine = _MARKUP_ENGINES_FORMATTERS.get(name)
#     if engine:
#         return engine
#     if name not in PYBB_MARKUP_ENGINES:
#         engine = BaseParser().format
#     else:
#         engine = PYBB_MARKUP_ENGINES[name]
#         if isinstance(engine, string_types):
#             # This is a path, import it
#             engine = resolve_class(engine).format
#
#     _MARKUP_ENGINES_FORMATTERS[name] = engine
#     return engine
#
#
# # TODO In the next major release, delete this function
# def _get_markup_quoter(name=None):
#     """
#     Returns the named quote engine, or the default quoter if name is not given.
#     """
#     warnings.warn(deprecated_func_warning % {'replace': 'quote', 'old': '_get_markup_quoter'},
#                   DeprecationWarning)
#     name = name or PYBB_MARKUP
#
#     engine = _MARKUP_ENGINES_QUOTERS.get(name)
#     if engine:
#         return engine
#
#     if name not in PYBB_QUOTE_ENGINES:
#         engine = BaseParser().quote
#     else:
#         engine = PYBB_QUOTE_ENGINES[name]
#         if isinstance(engine, string_types):
#             # This is a path, import it
#             engine = resolve_class(engine).quote
#
#     _MARKUP_ENGINES_QUOTERS[name] = engine
#     return engine


def get_body_cleaner(name):
    return resolve_function(name) if isinstance(name, string_types) else name


def unescape(text):
    """
    Do reverse escaping.
    """
    escape_map = [('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&#39;', '\'')]
    for escape_values in escape_map:
        text = text.replace(*escape_values)
    return text


def get_bb_profile(user):
    from django.conf import settings

    if not user.is_authenticated():
        if settings.FORUM_ENABLE_ANONYMOUS_POST:
            user = get_user_model().objects.get(**{get_username_field(): settings.FORUM_ANONYMOUS_USERNAME})
        else:
            raise ValueError(_('Can\'t get profile for anonymous user'))

    if settings.FORUM_PROFILE_RELATED_NAME:
        return getattr(user, settings.FORUM_PROFILE_RELATED_NAME)
    else:
        return user


def get_pybb_profile_model():
    from django.conf import settings

    if settings.FORUM_PROFILE_RELATED_NAME:
        return getattr(get_user_model(), settings.FORUM_PROFILE_RELATED_NAME).related.model
    else:
        return get_user_model()


def build_cache_key(key_name, **kwargs):
    if key_name == 'anonymous_topic_views':
        return 'pybbm_anonymous_topic_%s_views' % kwargs['topic_id']
    else:
        raise ValueError('Wrong key_name parameter passed: %s' % key_name)


class FilePathGenerator(object):
    """
    Special class for generating random filenames
    Can be deconstructed for correct migration
    """

    def __init__(self, to, *args, **kwargs):
        self.to = to

    def deconstruct(self, *args, **kwargs):
        return 'pybb.util.FilePathGenerator', [], {'to': self.to}

    def __call__(self, instance, filename):
        """
        This function generate filename with uuid4
        it's useful if:
        - you don't want to allow others to see original uploaded filenames
        - users can upload images with unicode in filenames wich can confuse browsers and filesystem
        """
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join(self.to, filename)


# code for a json-request
class jsoncode():
    success = {'data': 1}

    fail = {'data': 0}


# add extra message
def add_item(dic, key, value):
    dic.__setitem__(key, value)
    return dic


# input a datetime,return string for display depending on (now-time_in)
def get_delta_time(time_in):
    time_delta = datetime.today() - time_in
    day = time_delta.days
    sec = time_delta.seconds
    if day > 0:
        if day / 365 > 0:
            return '%d 年前' % (day / 365)
        else:
            return '%d 天前' % (day % 365)
    else:
        if sec < 60:
            return '1 分钟前'
        elif sec < 3600:
            return '%d 分钟前' % (sec / 60)
        else:
            return '%d 小时 %d 分钟前' % (sec / 3600, (sec % 3600) / 60)


# get token for sending email depending on user
def get_token(user):
    m = hashlib.md5()
    m.update(user.username)
    m.update(user.password)
    m.update(user.email)
    return m.hexdigest()


# send an email
def my_send_email(url, email):
    msg = '点击链接继续重置密码: '.decode('utf-8')
    send_mail(subject='珠海BBS密码重置验证', message=msg + url,
              from_email='ljq430001098@126.com', recipient_list=[email],
              fail_silently=False)


PAGE_SIZE = 5


# paging the queryset depending on 'page' attribute
def paging(request, query_set):
    paginator = Paginator(query_set, PAGE_SIZE)  # Show PAGE_SIZE contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return contacts


class CoinsController:
    # replying topic: get 1
    REPLY_TOPIC = 0
    POST_TOPIC = 1
    VOTED = 2
    UNUSED = 3
    CUT = 4

    delta = (5, 10, 1, -15, -50)

    @staticmethod
    def commit(user, ctype, coins=None):
        coins = CoinsController.delta[ctype] if type(coins) != types.IntType else coins
        try:
            user.userinfo.coins += coins
            user.userinfo.save()
            return True
        except:
            return False
