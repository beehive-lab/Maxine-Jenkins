# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-28 22:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizer', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dacapo',
            unique_together=set([('revision', 'details')]),
        ),
        migrations.AlterUniqueTogether(
            name='specjvm',
            unique_together=set([('revision', 'details')]),
        ),
    ]