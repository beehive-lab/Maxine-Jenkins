# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import jenkinsapi
import requests
from jenkinsapi.jenkins import Jenkins
from django.template import loader
from requests import ConnectionError
from utilities import JenkinsConnector, RawDataMaker, DatabaseManager


# Create your views here.

from django.http import HttpResponse
from django.http import Http404

# the controller for the Index page

def index(request):

    db = DatabaseManager()
    server_jobs = db.get_jobs()

    context = {
        'server_jobs': server_jobs,
    }
    template = loader.get_template('visualizer/index.html')

    return HttpResponse(template.render(context, request))

# the controller for the Job details

def jobDetails(request, job_name):

    db = DatabaseManager()
    job_details = db.get_job(job_name)

    if 'build_rev1' in request.POST:
        # "do stuff related to specific build comparison"
        benchmarks = db.get_two_selected_benchmarks(job_name, request.POST['build_rev1'], request.POST['build_rev2'])
    else:
        # "take and compare last two builds"
        benchmarks = db.get_last_two_benchmarks(job_name)

    context = {
        'job_name': job_name,
        'job_details': job_details,
        'benchmarks': benchmarks
    }
    template = loader.get_template('visualizer/jobDetails.html')
    return HttpResponse(template.render(context, request))

# the controller for the raw page

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

            rawmaker = RawDataMaker(benchs)

            template = loader.get_template('visualizer/raw.html')
            context = {
                'job_name': job_name,
                'bench_type': bench_type,
                'data': rawmaker.get_raw_data()
            }
            return HttpResponse(template.render(context, request))

        else:
            raise Http404("Cannot call this page directly")

    return HttpResponse("Raw here")

# Job register controller

def registerJobs(request):

    try:
        jenkins_conn = JenkinsConnector()

        server_jobs = jenkins_conn.get_jobs_summary()
        context = {
            'server_jobs': server_jobs,
        }
        template = loader.get_template('visualizer/registerJobs.html')

        return HttpResponse(template.render(context, request))

    except ConnectionError:
        raise Http404("Could not establish a connection to the Jenkins server")
    except ValueError:
        raise Http404("Could not find any jobs on the Jenkins server")

# Job register status controller

def registerStatus(request):

    if 'jobs' in request.POST:

        job_names = request.POST.getlist('jobs')
        db = DatabaseManager()
        try:
            jenkins_conn = JenkinsConnector()

            '''
            jobs array will contain information about all the registered/selected jobs.
            '''
            jobs = []

            for job_name in job_names:
                job_dtl = jenkins_conn.get_job_details(job_name)
                #for each one of the job's builds, get the benchmarks
                builds = []
                print "Job: " + job_name + " --------> Searching for good builds"
                for i in range(int(job_dtl["first_build_no"]), int(job_dtl["last_build_no"])+1, 1):
                    # exclude the failed builds
                    if jenkins_conn.is_build_good(job_name, i) == "False":
                        continue
                    print "Job: " + job_name + " ----> scanning build " + str(i)
                    build = jenkins_conn.get_build_benchmarks(job_name, i)
                    builds.append(build)
                '''
                For each job, some basic details are stored ('details' part), 
                along with benchmark information for every build ('builds' part)
                '''
                job = {
                    'details': job_dtl,
                    'builds': builds
                }
                jobs.append(job)

            result = db.refresh_database(jobs)
        except ConnectionError:
            raise Http404("Could not establish a connection to the Jenkins server")

        return HttpResponse(result)

    else:
        raise Http404("You cannot call this page directly. If this is not the case, at least one job most be selected")


