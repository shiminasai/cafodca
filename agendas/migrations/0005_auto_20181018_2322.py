# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-19 05:22
from __future__ import unicode_literals

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('agendas', '0004_agendas_lugar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agendas',
            name='foto',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='agendas/'),
        ),
    ]
