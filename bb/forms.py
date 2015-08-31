# coding:utf-8
from django import forms
from DjangoUeditor.forms import UEditorWidget, UEditorModelForm, UEditorField
from bb.models import Topic
from django.forms.models import model_to_dict


class PostReplyForm(forms.Form):
    Content = forms.CharField(
        widget=UEditorWidget({'width': 600, 'height': 300, 'imagePath': 'images/',
                              'filePath': 'files/'})
    )


class TopicUEditorForm(forms.Form):
    Name = forms.CharField(label=u'文章标题', widget=forms.TextInput(attrs={'width': 300, 'height': 30}))
    Content = forms.CharField(label=u'content',
                              widget=UEditorWidget({'width': 600, 'height': 500, 'imagePath': 'images/',
                                                    'filePath': 'files/'})
                              )


class AdminTopicForm(forms.Form):
    content = forms.CharField(label=u'content',
                              widget=UEditorWidget({'width': 600, 'height': 500, 'imagePath': 'images/',
                                                    'filePath': 'files/'}))


class FastReplyForm(forms.Form):
    Name = forms.CharField(label=u'文章标题', widget=forms.TextInput(attrs={'width': 300, 'height': 30}),
                           error_messages={'error': '检查文章标题的输入'}
                           )
    Content = forms.CharField(
        widget=UEditorWidget({'width': 600, 'height': 150, 'imagePath': 'images/',
                              'filePath': 'files/'})
    )


class FastTopicReplyForm(forms.Form):
    Content = forms.CharField(
        widget=UEditorWidget({'width': 600, 'height': 150, 'imagePath': 'images/',
                              'filePath': 'files/'})
    )


class TopicAdminForm(UEditorModelForm):
    class Meta:
        model = Topic
        exclude = ('',)
