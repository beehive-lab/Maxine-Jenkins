# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Dacapo(models.Model):
    bench1 = models.CharField(max_length=50)
    bench_date = models.DateTimeField('date of benchmark')

    def __str__(self):
        return self.bench1


class Specjvm(models.Model):
    startup = models.CharField(max_length=50, default="0")
    compiler = models.CharField(max_length=50, default="0")
    compress = models.CharField(max_length=50, default="0")
    crypto = models.CharField(max_length=50, default="0")
    derby = models.CharField(max_length=50, default="0")
    mpegaudio = models.CharField(max_length=50, default="0")
    scimark = models.CharField(max_length=50, default="0")
    serial = models.CharField(max_length=50, default="0")
    sunflow = models.CharField(max_length=50, default="0")
    xml = models.CharField(max_length=50, default="0")
    bench_date = models.DateTimeField('date of benchmark')

    def __str__(self):
        return self.startup
