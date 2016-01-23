# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20160123_1153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='short_name',
            new_name='last_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='full_name',
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(verbose_name='First Name', max_length=254, default=0),
            preserve_default=False,
        ),
    ]
