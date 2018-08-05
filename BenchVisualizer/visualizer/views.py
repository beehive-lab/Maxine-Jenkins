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

    if 'build_rev' in request.POST:
        # "do stuff related to specific build comparison"

        revisions = request.POST.getlist('build_rev')
        tags = request.POST.getlist('build_tag')

        benchmarks = db.get_selected_benchmarks(job_name, revisions, tags)
    else:
        # "take and compare last two builds"
        benchmarks = db.get_last_benchmarks(job_name)

    context = {
        'job_name': job_name,
        'job_details': job_details,
        'benchmarks': benchmarks,
        'hide_in_table': ["build_no", "details", "revision", "timestamp"],
        'no_bench': len(benchmarks)
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

            titles = ['revision', 'details', 'build_no', 'startup', 'compiler', 'compress', 'crypto', 'derby', 'mpegaudio',
                           'scimark', 'serial', 'spec_sunflow', 'xml']

            zipped_list = zip(
                request.POST.getlist('revision'),
                request.POST.getlist('details'),
                request.POST.getlist('build_no'),
                request.POST.getlist('startup'),
                request.POST.getlist('compiler'),
                request.POST.getlist('compress'),
                request.POST.getlist('crypto'),
                request.POST.getlist('derby'),
                request.POST.getlist('mpegaudio'),
                request.POST.getlist('scimark'),
                request.POST.getlist('serial'),
                request.POST.getlist('spec_sunflow'),
                request.POST.getlist('xml')
            )

            benchs = {

                'titles': titles,
                'zipped_list': zipped_list

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

    if bench_type == "dacapo":

        if 'avrora' in request.POST:

            titles = ["revision", "details", "build_no", "avrora", "batik", "eclipse", "fop", "h2", "jython", "luindex",
                      "lusearch", "pmd", "sunflow", "tomcat", "tradebeans", "tradesoap", "xalan"]

            zipped_list = zip(
                request.POST.getlist('revision'),
                request.POST.getlist('details'),
                request.POST.getlist('build_no'),
                request.POST.getlist('avrora'),
                request.POST.getlist('batik'),
                request.POST.getlist('eclipse'),
                request.POST.getlist('fop'),
                request.POST.getlist('h2'),
                request.POST.getlist('jython'),
                request.POST.getlist('luindex'),
                request.POST.getlist('lusearch'),
                request.POST.getlist('pmd'),
                request.POST.getlist('sunflow'),
                request.POST.getlist('tomcat'),
                request.POST.getlist('tradebeans'),
                request.POST.getlist('tradesoap'),
                request.POST.getlist('xalan'),
            )

            benchs = {

                'titles': titles,
                'zipped_list': zipped_list

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

            if 'refresh' in request.POST:

                for job_name in job_names:
                    job = jenkins_conn.get_job_and_benchmarks(job_name)
                    jobs.append(job)

                result = db.refresh_database(jobs)
            else:

                for job_name in job_names:
                    try:
                        db.get_job(job_name)
                    except Http404:
                        job = jenkins_conn.get_job_and_benchmarks(job_name)
                        jobs.append(job)

                result = db.update_database(jobs)
        except ConnectionError:
            raise Http404("Could not establish a connection to the Jenkins server")

        return HttpResponse(result)

    else:
        raise Http404("You cannot call this page directly. If this is not the case, at least one job most be selected")


