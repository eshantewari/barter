# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20160124_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='item',
            field=models.ForeignKey(default=0, to='main.Item'),
            preserve_default=False,
        ),
    ]
