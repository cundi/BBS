# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from bb.models import Category, Forum, Topic, Post
from bb.forms import TopicAdminForm


class BaseModelAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        # disabled, because delete_selected ignoring delete model method
        actions = super(BaseModelAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class CategoryAdmin(BaseModelAdmin):
    list_display = ['title', 'description', 'slug', 'admin', 'position', ]

admin.site.register(Category)


def update_forum_state_info(modeladmin, request, queryset):
    for forum in queryset:
        forum.update_state_info()


update_forum_state_info.short_description = _("Update forum state info")


class ForumAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'topic_count', 'post_count',)
    list_filter = ('category',)
    actions = [update_forum_state_info]
    raw_id_fields = ['manager',]

admin.site.register(Forum, ForumAdmin)


class  TopicInline(admin.TabularInline):
    model = Post


def update_topic_state_info(modeladmin, request, queryset):
    for topic in queryset:
        topic.update_state_info()


update_topic_state_info.short_description = _("Update topic state info")


def update_topic_attr_as_not(modeladmin, request, queryset, attr):
    for topic in queryset:
        if attr == 'sticky':
            topic.sticky = not topic.sticky
        elif attr == 'close':
            topic.closed = not topic.closed
        elif attr == 'hide':
            topic.hidden = not topic.hidden
        topic.save()


def sticky_unsticky_topic(modeladmin, request, queryset):
    update_topic_attr_as_not(modeladmin, request, queryset, 'sticky')


sticky_unsticky_topic.short_description = _("sticky/unsticky topics")


def close_unclose_topic(modeladmin, request, queryset):
    update_topic_attr_as_not(modeladmin, request, queryset, 'close')


close_unclose_topic.short_description = _("close/unclose topics")


def hide_unhide_topic(modeladmin, request, queryset):
    update_topic_attr_as_not(modeladmin, request, queryset, 'hide')


hide_unhide_topic.short_description = _("hide/unhide topics")



class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'forum', 'author', 'sticky', 'closed',
                    'view_count', 'post_count', 'created', 'updated',)
    list_filter = ('forum', 'sticky', 'closed',)
    search_fields = ('title', 'author__username', 'content',)
    inlines = (TopicInline,)
    form = TopicAdminForm
    formfield_overrides = {'content': Topic.objects.get().content}
    actions = [update_topic_state_info, sticky_unsticky_topic, close_unclose_topic, hide_unhide_topic]


admin.site.register(Topic, TopicAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'topic', 'author', 'user_ip',
                    'created', 'updated',)
    search_fields = ('topic__subject', 'posted_by__username', 'message',)


admin.site.register(Post, PostAdmin)
