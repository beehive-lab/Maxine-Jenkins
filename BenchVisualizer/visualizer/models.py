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
    startup = models.CharField(max_length=50, default="-1")
    compiler = models.CharField(max_length=50, default="-1")
    compress = models.CharField(max_length=50, default="-1")
    crypto = models.CharField(max_length=50, default="-1")
    derby = models.CharField(max_length=50, default="-1")
    mpegaudio = models.CharField(max_length=50, default="-1")
    scimark = models.CharField(max_length=50, default="-1")
    serial = models.CharField(max_length=50, default="-1")
    sunflow = models.CharField(max_length=50, default="-1")
    xml = models.CharField(max_length=50, default="-1")
    bench_date = models.DateTimeField('date of benchmark')

    def __str__(self):
        return self.startup
