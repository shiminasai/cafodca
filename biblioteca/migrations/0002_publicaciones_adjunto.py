# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2020-04-25 04:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicaciones',
            name='adjunto',
            field=models.FileField(blank=True, null=True, upload_to='biblioteca/'),
        ),
    ]
