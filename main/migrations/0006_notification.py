# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20160123_1216'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('from_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='from_user')),
                ('item', models.ForeignKey(to='main.Item')),
                ('to_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='to_user')),
            ],
        ),
    ]
