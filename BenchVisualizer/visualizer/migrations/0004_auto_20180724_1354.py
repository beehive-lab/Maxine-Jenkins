# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-24 13:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizer', '0003_auto_20180724_1135'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dacapo',
            unique_together=set([('job', 'revision', 'details')]),
        ),
        migrations.AlterUniqueTogether(
            name='specjvm',
            unique_together=set([('job', 'revision', 'details')]),
        ),
    ]
