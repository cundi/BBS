# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs_account', '0007_auto_20150819_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='signature',
            field=DjangoUeditor.models.UEditorField(max_length=3, verbose_name='\u5185\u5bb9', blank=True),
        ),
    ]
