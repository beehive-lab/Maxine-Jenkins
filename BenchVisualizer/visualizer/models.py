# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Job(models.Model):
    name = models.CharField(max_length=50, default="n/a", unique=True)
    description = models.CharField(max_length=50, default="n/a")
    is_running = models.CharField(max_length=5, default="n/a")
    is_enabled = models.CharField(max_length=5, default="n/a")

    def __str__(self):
        return self.name

class Dacapo(models.Model):
    # avrora batik eclipse fop h2 jython luindex lusearch pmd sunflow tomcat tradebeans tradesoap xalan
    job = models.ForeignKey(Job, on_delete=models.CASCADE, default=1)
    build_no = models.IntegerField(default=0)
    timestamp = models.DateTimeField()
    revision = models.CharField(max_length=50, default="0")
    details = models.CharField(max_length=50, default="default")
    avrora = models.CharField(max_length=50, default="0")
    batik = models.CharField(max_length=50, default="0")
    eclipse = models.CharField(max_length=50, default="0")
    fop = models.CharField(max_length=50, default="0")
    h2 = models.CharField(max_length=50, default="0")
    jython = models.CharField(max_length=50, default="0")
    luindex = models.CharField(max_length=50, default="0")
    lusearch = models.CharField(max_length=50, default="0")
    pmd = models.CharField(max_length=50, default="0")
    sunflow = models.CharField(max_length=50, default="0")
    tomcat = models.CharField(max_length=50, default="0")
    tradebeans = models.CharField(max_length=50, default="0")
    tradesoap = models.CharField(max_length=50, default="0")
    xalan = models.CharField(max_length=50, default="0")

    class Meta:
        unique_together = ('job', 'revision', 'details')

    def __str__(self):
        return str(self.job) + str(self.build_no)


class Specjvm(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, default=1)
    build_no = models.IntegerField(default=0)
    timestamp = models.DateTimeField()
    revision = models.CharField(max_length=50, default="0")
    details = models.CharField(max_length=50, default="default")
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

    class Meta:
        unique_together = ('job', 'revision', 'details')

    def __str__(self):
        return str(self.job) + str(self.build_no)
