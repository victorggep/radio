# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-17 22:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='titular',
            field=models.CharField(max_length=500),
        ),
    ]
