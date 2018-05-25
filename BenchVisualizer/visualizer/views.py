# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import jenkinsapi
import requests
from jenkinsapi.jenkins import Jenkins
from django.template import loader
from requests import ConnectionError
from utilities import JenkinsConnector


# Create your views here.

from django.http import HttpResponse
from django.http import Http404

#the controller for the Index page

def index(request):

    try:
        jenkins_conn = JenkinsConnector()

        server_jobs = jenkins_conn.get_jobs_summary()
        context = {
            'server_jobs': server_jobs,
        }
        template = loader.get_template('visualizer/index.html')

        return HttpResponse(template.render(context, request))

    except ConnectionError:
        raise Http404("Could not establish a connection to the Jenkins server")

#the controller for the Job details

def jobDetails(request, job_name):

    try:
        jenkins_conn = JenkinsConnector()

        job_details = jenkins_conn.get_job_details(job_name)

        context = {
            'job_name': job_name,
            'job_details': job_details
        }
        template = loader.get_template('visualizer/jobDetails.html')

        return HttpResponse(template.render(context, request))
    except ConnectionError:
        raise Http404("Could not establish a connection to the Jenkins server")
