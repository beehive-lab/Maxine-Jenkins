from visualizer.models import Job, Specjvm, Dacapo

class DatabaseManager:

    def clear_database(self):

        Job.objects.all().delete()

        return "ok"

    def store_job(self, job):

        #firstly, store the new job in the Job table
        stored_job = Job(name=job["name"], description=job["description"], is_running=job["is_running"], is_enabled=job["is_enabled"])
        stored_job.save()

        '''
        #return a "reference" to the new row in the table Job. 
        Will be used to add specjvm/dacapo results to this job
        '''
        stored_job = Job.objects.get(name=job["name"])
        return stored_job

    def store_benchmarks(self, job, bench):

        dacapo = bench['dacapo']
        specjvm = bench['specjvm']

        job.dacapo_set.create(
            build_no=bench['build_no'],
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
