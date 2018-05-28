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

#the controller for the raw page

def raw(request, job_name, bench_type):

    '''
    If one of the POST variables exists, all the others exist.
    If there aren't any POST variables, the user has called the page directly.
    '''
    if bench_type == "specjvm":

        if 'startup' in request.POST:
            benchs = {
                'startup': request.POST['startup'],
                'compiler': request.POST['compiler'],
                'compress': request.POST['compress'],
                'crypto': request.POST['crypto'],
                'derby': request.POST['derby'],
                'mpegaudio': request.POST['mpegaudio'],
                'scimark': request.POST['scimark'],
                'serial': request.POST['serial'],
                'spec_sunflow': request.POST['spec_sunflow'],
                'xml': request.POST['xml']
            }
        else:
            raise Http404("Cannot call this page directly")

    return HttpResponse("Raw here")
