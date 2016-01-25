# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='item',
            field=models.ForeignKey(blank=True, null=True, to='main.Item'),
        ),
    ]
