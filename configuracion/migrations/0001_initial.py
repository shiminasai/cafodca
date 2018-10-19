# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-19 05:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FotosPortada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=250)),
                ('descripcion', models.TextField()),
                ('foto', models.FileField(upload_to=b'fotoportada/')),
            ],
            options={
                'verbose_name': 'Foto de portada',
                'verbose_name_plural': 'Fotos de las portadas',
            },
        ),
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default=b'Site Name', max_length=255)),
                ('maintenance_mode', models.BooleanField(default=False)),
                ('acerca', models.TextField()),
            ],
            options={
                'verbose_name': 'Sitio Configuraci\xf3n',
            },
        ),
        migrations.AddField(
            model_name='fotosportada',
            name='sitio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuracion.SiteConfiguration'),
        ),
    ]
