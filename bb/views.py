# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import operator

from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http.response import JsonResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.contrib.auth import get_user_model, get_user
from django.utils.timezone import now as time_zone_now

from bb.models import Category, Forum, Topic, Post
from bb.forms import PostReplyForm, TopicUEditorForm, FastReplyForm, FastTopicReplyForm
from bb.permission import perms
from utils import jsoncode, add_item, CoinsController

User = get_user_model()

categories = Category.objects.all()
forums = Forum.objects.all()
forum = Forum()
today = datetime.date.today()
today_tp = Topic.objects.filter(created__day=today.day).count()
yesterday_tp = Topic.objects.filter(created__day=today.day - 1).count()
users_count = User.objects.count()
posts_count = Post.objects.count()
TOPICS_PAGE = 10


def site_error(request, msg, back=None):
    ctx = {
        'title': 'notice',
        'msg': msg,
        'back': back
    }
    return render(request, 'common/error.html', ctx)


def index(request):
    """
    :param posts_count:所有的帖子包括回帖在内
    :return:
    """
    user_all = User.objects.all()
    try:
        user_latest = user_all.latest(field_name='date_joined')
    except:
        user_latest = 0
    user = get_user(request)
    last_replied_topics = Topic.objects.all().order_by('-replied_time')
    paginator = Paginator(last_replied_topics, TOPICS_PAGE)
    page = request.GET.get('page')
    try:
        last_replied_topics = paginator.page(page)
    except PageNotAnInteger:
        last_replied_topics = paginator.page(1)
    except EmptyPage:
        last_replied_topics = paginator.page(paginator.num_pages)
    ctx = {'lrt': last_replied_topics, 'forums': forums, 'paginator': paginator, 'user': user,
           'uc': users_count, 'tt': today_tp, 'yt': yesterday_tp, 'ul': user_latest,
           'categories': categories, 'pc': posts_count,
           }
    return render(request, 'deepin/zui_xin_hui_tie.html', ctx)


def tag_cloud(request):
    pass


def search(request, kw):
    k = kw.split(' ')
    condition = reduce(operator.and_, [Q(title__contains=x) for x in k])
    topics = Topic.objects.filter(condition)
    try:
        page = request.GET['page']
    except ValueError:
        page = None
    if page == '1':
        page = None
    ctx = {
        'title': '%s-search result' % k,
        'page': page,
        'topics': topics,
        'post_list_title': 'search %s' % k
    }
    return render(request, 'common/index.html', ctx)


def category_view(request, cid):
    category = Category.objects.get(id=cid)
    ctx = {
        'category': category, 'today_topics_count': today_tp, 'yesterday_topics_count': yesterday_tp,
    }
    return render(request, 'deepin/category_view.html', ctx)


def category_all(request):
    c_forum = [c for c in categories]
    ctx = {
        'categories': categories, 'forums': forums, 'cf': c_forum,
    }
    return render(request, 'deepin/category_all.html', ctx)


def forum_view(request, forum_id):
    id_forum = Forum.objects.get(id=forum_id)
    topics = Topic.objects.filter(forum__id=id_forum.id, closed=False).order_by('-replied_time')
    tlp = topics.first()
    paginator = Paginator(topics, TOPICS_PAGE)
    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    ctx = {
        'topics': topics,
        'forum': id_forum,
        'paginator': paginator,
        'tlp': tlp,
    }
    return render(request, 'deepin/forum_view.html', ctx)


def forum_topics(request, forum_id):
    id_forum = Forum.objects.get(id=forum_id)
    topics = id_forum.topic_set.all()  # 列出当前单个分区下属的帖子，而不是所有分区的全部帖子
    paginator = Paginator(topics, TOPICS_PAGE)
    page = request.POST.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        topics = paginator.page(paginator.num_pages)
    ctx = {'forum': id_forum,
           'forums': forums,
           'topics': topics,
           }
    return render(request, 'bbs/forum_topic_list.html', ctx)


def all_forum_topics(request):
    """
    所有分区的所有帖子
    """
    return render(request, 'bbs/forums_all_topics.html', {'forums': forums})


def topic_view(request, pk):
    """
    view single topic
    """
    user = get_user(request)
    form = PostReplyForm()
    fast_form = FastReplyForm(initial={'label': ''})
    id_topic = Topic.objects.get(id=pk)
    id_topic.view_count += 1
    id_topic.save()
    topic_forum = id_topic.forum
    posts = id_topic.post_set.order_by('created').filter()
    paginator = Paginator(posts, TOPICS_PAGE)
    page = request.POST.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    ctx = {'topic': id_topic,
           'topic_forum': topic_forum,
           'form': form,
           'fast_form': fast_form,
           'posts': posts,
           'paginator': paginator,
           'user': user,
           }
    return render(request, 'deepin/topic_view.html', ctx)


@login_required()
def create_topic(request, forum_id):
    id_forum = Forum.objects.get(id=forum_id)
    msg = []
    if request.method == 'GET':
        form = TopicUEditorForm(initial={'content': u'测试'})
        ctx = {'forum': id_forum, 'title': 'create_new_topic', 'form': form}
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('user:login'))
        return render(request, 'deepin/topic_create.html', ctx)
    if request.method == 'POST':
        topic = Topic()
        form = TopicUEditorForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['Content']
            name = form.cleaned_data['Name']
            user = request.user
            topic.content = content
            topic.title = name
            topic.forum = id_forum
            topic.author = user
            topic.save()
            id_forum.topic_count += 1
            id_forum.save()
        # if not topic.title:
        #     msg.append('title cannot be empty')
        #     return render(request, 'bbs/topic_create.html', {'msg': msg})
            return HttpResponseRedirect(reverse('bb:forum_view', kwargs={'forum_id': forum_id}))


@login_required()
def edit_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method == 'GET':
        form = TopicUEditorForm(initial={'Content': topic.content, 'Name': topic.title} )
        ctx = {
            'topic': topic,
            'form': form,
        }
        return render(request, 'deepin/topic_edit.html', ctx)
    if request.method == 'POST':
        form = TopicUEditorForm(request.POST, request.FILES)
        if form.is_valid():
            topic.title = form.cleaned_data['Name']
            topic.content = form.cleaned_data['Content']
            topic.forum = topic.forum
            topic.updated = time_zone_now()
            topic.save()
        return HttpResponseRedirect(reverse('bb:topic_view', kwargs={'pk': topic.pk}))


@login_required()
def create_topic_reply(request, topic_id):
    if request.method == 'POST':
        topic = Topic.objects.get(id=topic_id)
        p = Post()
        # 回帖所属的那个帖子
        p.topic = topic
        p.content = request.POST['Content']
        p.author = request.user
        p.save()
        # 帖自被回复的时间就等于reply的创建时间
        topic.replied_time = p.created
        topic.post_count += 1
        topic.save()
        # 当前论坛的回帖总数
        forum.post_count += 1
        forum.save()
        return HttpResponseRedirect(reverse('bb:topic_view', kwargs={'pk': topic_id}))
    if request.method == 'GET':
        return render(request, 'deepin/topic_view.html')


def fast_topic_reply(request, tid):
    topic = Topic.objects.get(id=tid)
    id_forum = Forum.objects.get(topic__id=tid)
    if request.method == 'GET':
        form = FastTopicReplyForm(initial={'Content': '<p style="color:red">RE:'+ topic.content + '</p>'})
        ctx = {
            'form':form,
            'topic':topic,
        }
        return render(request, 'deepin/fast_topic_rp.html', ctx)
    if request.method == 'POST':
        form = FastTopicReplyForm(request.POST)
        if form.is_valid():
            post = Post()
            content = form.cleaned_data['Content']
            post.content = content
            post.author = request.user
            post.topic = topic
            post.save()
            topic.replied_time = post.created
            topic.reply_count += 1
            id_forum.post_count +=1
            id_forum.topic_count +=1
            id_forum.save()
            return HttpResponseRedirect(reverse('bb:topic_view', kwargs={'pk': topic.id}))


@staff_member_required
def delete_topic_reply(request, post_id):
    post = Post.objects.get(id=post_id)
    # 被回帖的那个主题的id
    t_id = post.topic.id
    post.deleted = True
    post.save()
    post.topic.save()
    return HttpResponseRedirect(reverse('bb:topic_view', kwargs={'topic_id': t_id}))


@login_required()
def delete_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.user != topic.author and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('bb:topic_view', kwargs={'topic_id': topic.id}))
    t_forum_id = topic.forum.id
    topic.deleted = True
    topic.save()
    return HttpResponseRedirect(reverse('bb:Forum_view', kwargs={'Forum_id': t_forum_id}))


def close_topic(request, tid):
    if request.method == 'POST':
        topic = Topic.objects.get(id=tid)
        if not perms.may_close_topic(request.user, topic):
            raise PermissionDenied
        topic.closed = True
        topic.save()
        return HttpResponseRedirect(topic.get_absolute_url())


def open_topic(request, tid):
    if request.method == 'POST':
        topic = Topic.objects.get(id=tid)
        if not perms.may_open_topic(request.user, topic):
            raise PermissionDenied
        topic.closed = False
        topic.save()
        return HttpResponseRedirect(topic.get_absolute_url())


def like_topic(request):
    topic_id = request.POST['topic_id']
    if request.method != 'POST':
        return JsonResponse(jsoncode.fail)
    if Topic.objects.filter(id=topic_id).exists():
        topic = Topic.objects.get(id=topic_id)
        if topic.author.id == request.user.id:
            return JsonResponse(add_item(jsoncode.fail, 'msg', '不能赞自己哦！'))
        user = get_user(request)
        user.like_topic.add(topic)
        CoinsController.commit(topic.author, CoinsController.VOTED)
        return JsonResponse(jsoncode.success)
    else:
        return JsonResponse(jsoncode.fail)


def collection_topic(request):
    topic_id = request.POST.get('topic_id')
    if request.method != 'POST':
        return JsonResponse(jsoncode.fail)

    if Topic.objects.filter(id=topic_id).exists():
            topic = Topic.objects.get(id=topic_id)
            user = get_user(request)
            user.collection_topic.add(topic)
            user.save()
            return JsonResponse(jsoncode.success)
    else:
        return JsonResponse(jsoncode.fail)


@login_required()
def create_repost(request, pid):
    if request.method == 'POST':
        post = Post.objects.get(id=pid)
