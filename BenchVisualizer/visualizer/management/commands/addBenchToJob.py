from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from visualizer.models import Job
from visualizer.utilities import DatabaseManager, JenkinsConnector
from requests import ConnectionError


class Command(BaseCommand):
    help = 'Stores a new set of benchmarks for a specified Job in the database'

    def add_arguments(self, parser):
        parser.add_argument('job_name', type=str, help="The name of the Job in the Database")
        parser.add_argument(
            '--get_jenkins_latest',
            action="store_true",
            default=False,
            help="Specify this flag to get the benchmarks from the latest Jenkins build"
        )

    def handle(self, *args, **options):

        job_name = options['job_name']
        try:
            stored_job = Job.objects.get(name=job_name)
        except Job.DoesNotExist:
            self.stdout.write(self.style.ERROR('Specified Job not found in the Database'))
            # TODO: specify a proper return code for the pipeline
            exit()

        if options['get_jenkins_latest']:
            self.stdout.write(self.style.WARNING('Getting Jenkins latest build benchmarks...'))
            try:
                jenkins_conn = JenkinsConnector()
                db = DatabaseManager()

                job_details = jenkins_conn.get_job_details(job_name)
                bench = jenkins_conn.get_build_benchmarks(job_name, int(job_details['last_build_no']))
                db.store_benchmarks(stored_job, bench)
            except ConnectionError:
                self.stdout.write(self.style.ERROR('Could not establish a connection to the Jenkins server'))
            except IntegrityError:
                self.stdout.write(self.style.ERROR('There is already a set of benchmarks for the specific TAG and revision'))
            exit()
        



        self.stdout.write(self.style.SUCCESS('Complete.'))
