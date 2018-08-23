from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.http import Http404
from django.utils import timezone
from visualizer.models import Job
from datetime import datetime
from visualizer.utilities import DatabaseManager, JenkinsConnector, BenchMiner
from requests import ConnectionError
import os
import subprocess


class Command(BaseCommand):

    """
    addBenchToJob is a CLI tool that fetches the more recent benchmarks from the Jenkins pipeline OR
    starts executing the benchmarks locally. In both cases, the results are stored in the DB

    Usage:
     addBenchToJob <JobName> --get_jenkins_latest //gets the benchmarks results from the Jenkins pipeline and stores them with
        the TAG "default"
     addBenchToJob <JobName> --revision <Git revision> --tag <TAG> //starts the benchmarks and stores the results on the DB
     addBenchToJob <JobName> --revision <Git revision> --tag <TAG> --overwrite //same as above, but overwrites the existing record
        with the same (revision,TAG)
    """

    help = 'Stores a new set of benchmarks for a specified Job in the database'

    def add_arguments(self, parser):

        parser.add_argument('job_name', type=str, help="The name of the Job in the Database")

        parser.add_argument(
            '--get_jenkins_latest',
            action="store_true",
            default=False,
            help="Specify this flag to get the benchmarks from the latest Jenkins build"
        )

        parser.add_argument(
            '--revision',
            type=str,
            default="no_revision_specified",
            help="The GIT revision of the executed build"
        )

        parser.add_argument(
            '--tag',
            type=str,
            default="default",
            help="The Tag/Details of the executed build"
        )

        parser.add_argument(
            '--overwrite',
            action="store_true",
            default=False,
            help="Specify this flag to overwrite benchmarks of the specified revision/tag, if they exist in the DB"
        )

    def handle(self, *args, **options):

        job_name = options['job_name']

        # new_job is True when the pipeline runs for the first time, and a new Job must be added to DB.
        new_job = False

        try:
            stored_job = Job.objects.get(name=job_name)
        except Job.DoesNotExist:
            self.stdout.write(self.style.ERROR('Specified Job not found in the Database'))
            if options['get_jenkins_latest']:
                new_job = True
            else:
                exit()

        if options['get_jenkins_latest']:

            '''
            If --get_jenkins_latest is specified, the benchmarks are fetched from the output of the latest Jenkins build.
            Considering that this tool is integrated inside the pipeline, it will fetch the benchmarks from the
            "current" build.
            For the first build of the Pipeline, a new Job is registered automatically in the DB.
            '''

            self.stdout.write(self.style.WARNING('Getting Jenkins latest build benchmarks...'))
            try:
                jenkins_conn = JenkinsConnector()
                db = DatabaseManager()

                job_details = jenkins_conn.get_job_details(job_name)
                bench = jenkins_conn.get_build_benchmarks(job_name, int(job_details['last_build_no']))

                # if the pipeline runs for the first time, create a new Job
                if new_job:
                    self.stdout.write(self.style.WARNING('First build. Registering new Job...'))
                    stored_job = db.store_job(job_details)

                db.store_benchmarks(stored_job, bench)
            except ConnectionError:
                self.stdout.write(self.style.ERROR('Could not establish a connection to the Jenkins server'))
            except IntegrityError:
                self.stdout.write(self.style.ERROR('There is already a set of benchmarks for the specific TAG and revision'))
            exit()

        if options['revision'] != "no_revision_specified":

            '''
            If a revision is specified through the CLI, the 'manual' insertion of benchmarks in the database starts.
            The command fetches the revision and the tag fields (default tag is "default") from the CLI and searches
            if a record exists in the DB. If it exists, it checks if the --overwrite option is present to update the data.
            Otherwise it exits with an error message
            '''

            # CLI input length checking
            if len(options['revision']) > 40:
                self.stdout.write(
                    self.style.ERROR('The revision specified is over 40 characters long'))
                exit()

            if len(options['tag']) > 50:
                self.stdout.write(
                    self.style.ERROR('The TAG specified is over 40 characters long'))
                exit()

            self.stdout.write(self.style.WARNING('Inserting benchmarks for a specific revision...'))
            # Running the pipeline via python

            # copy the env vars from the system
            env = dict(os.environ)


            dacapo_benchs = [

                "avrora", "batik", "eclipse", "fop", "h2", "jython", "luindex", "lusearch", "pmd", "sunflow", "tomcat",
                "tradebeans", "tradesoap", "xalan"
            ]

            specjvm_benchs = [
                "startup", "compiler", "compress", "crypto", "derby", "mpegaudio", "scimark", "serial", "spec_sunflow", "xml"
            ]

            outp = ""
            for dacapo_bench in dacapo_benchs:
                self.stdout.write(self.style.WARNING('Initiating Dacapo ' + dacapo_bench + '...'))
                shell_command = env['MX'] + ' --vm=maxine vm -jar dacapo-9.12-bach.jar ' + dacapo_bench + ' || true'
                outp += "Executing: " + shell_command + '\n'
                outp += subprocess.check_output(
                    shell_command,
                    shell=True, env=env, cwd=env['DACAPO'], stderr=subprocess.STDOUT
                )
            self.stdout.write(self.style.SUCCESS('Dacapo Benchmarks Complete!'))

            for specjvm_bench in specjvm_benchs:
                self.stdout.write(self.style.WARNING('Initiating Specjvm ' + specjvm_bench + '...'))

                shell_command = 'timeout -s SIGINT 7m ' + env['MX'] +\
                        ' --vm=maxine vm -jar SPECjvm2008.jar -bt 2 ' + specjvm_bench + ' || true'

                outp += "Executing: " + shell_command + '\n'
                outp += subprocess.check_output(
                    shell_command,
                    shell=True, env=env, cwd=env['SPECJVM2008'], stderr=subprocess.STDOUT
                )

                # '+ true' marks the end of the specjvm subbenchmark output. DO NOT remove
                outp += '+ true\n'

            self.stdout.write(self.style.SUCCESS('Specjvm Benchmarks Complete!'))

            # print "======OUTPUT IS=======:\n" + outp
            miner = BenchMiner(outp)
            dacapo_res = miner.mine_all_dacapos()
            specjvm_res = miner.mine_all_specjvms()
            print str(dacapo_res) + "\n" + str(specjvm_res)

            '''
            Construct the dict that contains the two sets of benchmarks and store it in the DB
            '''

            self.stdout.write(self.style.WARNING('Storing the benchmarks to the DB...'))

            all_benchs = {
                'build_no': 0,
                'revision': options['revision'],
                'timestamp': datetime.now(tz=timezone.utc),
                'specjvm': specjvm_res,
                'dacapo': dacapo_res
            }
            db = DatabaseManager()
            try:
                db.get_benchmarks(stored_job, options['revision'], options['tag'])
            # if a record does not exist, create a new one and exit successfully
            except Http404:
                db.store_benchmarks(stored_job, all_benchs, options['tag'])
                self.stdout.write(self.style.SUCCESS('Complete.'))
                exit()

            # if a record with the specified revision/tag exists in the database
            self.stdout.write(self.style.WARNING('Found an existing set of benchmarks for this tag/revision'))
            if options['overwrite']:
                self.stdout.write(self.style.WARNING('Overwriting...'))
                db.update_benchmarks(stored_job, options['revision'], all_benchs, options['tag'])
            else:
                self.stdout.write(self.style.ERROR('Specify --overwrite option if you want to update the data'))
                exit()

        else:
            self.stdout.write(self.style.ERROR('You must specify a GIT revision or the --get_jenkins latest option'))
            exit()


        self.stdout.write(self.style.SUCCESS('Complete.'))
