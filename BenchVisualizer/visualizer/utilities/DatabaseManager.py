from visualizer.models import Job, Specjvm, Dacapo
from django.http import Http404

class DatabaseManager:

    def clear_database(self):

        Job.objects.all().delete()

        return "ok"

    def get_job(self, job_name):
        stored_job = Job.objects.get(name=job_name)

        job ={
            'name': stored_job.name,
            'description': stored_job.description,
            'is_running': stored_job.is_running,
            'is_enabled': stored_job.is_enabled,
        }

        return job

    def get_benchmarks(self, stored_job, build_number, details="default"):

        try:
            stored_dacapo = stored_job.dacapo_set.get(build_no=build_number, details=details)
            stored_specjvm = stored_job.specjvm_set.get(build_no=build_number, details=details)
        except Dacapo.DoesNotExist:
            raise Http404("Build <" + str(build_number) + "> of Job <" + stored_job.name + "> does not exist!")

        dacapo = {
            'build_no': stored_dacapo.build_no,
            'details': stored_dacapo.details,
            'avrora': stored_dacapo.avrora,
            'batik': stored_dacapo.batik,
            'eclipse': stored_dacapo.eclipse,
            'fop': stored_dacapo.fop,
            'h2': stored_dacapo.h2,
            'jython': stored_dacapo.jython,
            'luindex': stored_dacapo.luindex,
            'lusearch': stored_dacapo.lusearch,
            'pmd': stored_dacapo.pmd,
            'sunflow': stored_dacapo.sunflow,
            'tomcat': stored_dacapo.tomcat,
            'tradebeans': stored_dacapo.tradebeans,
            'tradesoap': stored_dacapo.tradesoap,
            'xalan': stored_dacapo.xalan
        }

        specjvm = {
            'build_no': stored_specjvm.build_no,
            'details': stored_specjvm.details,
            'startup': stored_specjvm.startup,
            'compiler': stored_specjvm.compiler,
            'compress': stored_specjvm.compress,
            'crypto': stored_specjvm.crypto,
            'derby': stored_specjvm.derby,
            'mpegaudio': stored_specjvm.mpegaudio,
            'scimark': stored_specjvm.scimark,
            'serial': stored_specjvm.serial,
            'spec_sunflow': stored_specjvm.sunflow,
            'xml': stored_specjvm.xml
        }

        bench = {
            'build_no': build_number,
            'dacapo': dacapo,
            'specjvm': specjvm
        }

        return bench

    def get_last_two_benchmarks(self, job_name):

        stored_job = Job.objects.get(name=job_name)

        '''
        The build numbers can be fetched from either the dacapo or the specjvm table (after desc sort on build_no).
        Here dacapo table is used. 
        The simplest workaround would be to take only the last_build_no from the Job and get 
        (last_build_no - 1), but this wouldn't work if build numbers are not consecutive
        '''
        recent_builds = stored_job.dacapo_set.all().order_by('-build_no')

        bench1 = self.get_benchmarks(stored_job, recent_builds[0].build_no)
        bench2 = self.get_benchmarks(stored_job, recent_builds[1].build_no)

        return [bench1, bench2]

    def get_two_selected_benchmarks(self, job_name, build_no1, build_no2):

        stored_job = Job.objects.get(name=job_name)

        bench1 = self.get_benchmarks(stored_job, build_no1)
        bench2 = self.get_benchmarks(stored_job, build_no2)

        return [bench1, bench2]

    def store_job(self, job):

        #firstly, store the new job in the Job table
        stored_job = Job(
            name=job["name"],
            description=job["description"],
            is_running=job["is_running"],
            is_enabled=job["is_enabled"])
        stored_job.save()

        '''
        #return a "reference" to the new row in the table Job. 
        Will be used to add specjvm/dacapo results to this job
        '''
        stored_job = Job.objects.get(name=job["name"])
        return stored_job

    def store_benchmarks(self, job, bench, details="default"):

        dacapo = bench['dacapo']
        specjvm = bench['specjvm']

        job.dacapo_set.create(
            build_no=bench['build_no'],
            details=details,
            avrora=dacapo['avrora'],
            batik=dacapo['batik'],
            eclipse=dacapo['eclipse'],
            fop=dacapo['fop'],
            h2=dacapo['h2'],
            jython=dacapo['jython'],
            luindex=dacapo['luindex'],
            lusearch=dacapo['lusearch'],
            pmd=dacapo['pmd'],
            sunflow=dacapo['sunflow'],
            tomcat=dacapo['tomcat'],
            tradebeans=dacapo['tradebeans'],
            tradesoap=dacapo['tradesoap'],
            xalan=dacapo['xalan'],
        )

        job.specjvm_set.create(
            build_no=bench['build_no'],
            details=details,
            startup=specjvm['startup'],
            compiler=specjvm['compiler'],
            compress=specjvm['compress'],
            crypto=specjvm['crypto'],
            derby=specjvm['derby'],
            mpegaudio=specjvm['mpegaudio'],
            scimark=specjvm['scimark'],
            serial=specjvm['serial'],
            sunflow=specjvm['spec_sunflow'],
            xml=specjvm['xml']
        )

        return "ok"

    def refresh_database(self, jobs):
        self.clear_database()

        for job in jobs:
            stored_job = self.store_job(job['details'])

            #for each job, store its build data
            for build in job['builds']:
                self.store_benchmarks(stored_job, build)


        return "ok"
