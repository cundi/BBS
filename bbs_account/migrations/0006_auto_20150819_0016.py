# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbs_account', '0005_auto_20150819_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='last_activity',
            field=models.DateTimeField(null=True, editable=False),
        ),
    ]
