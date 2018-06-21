from visualizer.models import Job, Specjvm, Dacapo

class DatabaseManager:

    def clear_database(self):

        Job.objects.all().delete()

        return "ok"

    def store_job(self, job):

        #firstly, store the new job in the Job table
        job = Job(name=job["name"], description=job["description"], is_running=job["is_running"], is_enabled=job["is_enabled"])
        job.save()

        '''
        #return a "reference" to the new row in the table Job. 
        Will be used to add specjvm/dacapo results to this job
        '''
        return job

    def store_dacapo(self, job, bench):
        job.dacapo_set.create()

        return "ok"

    def store_specjvm(self, job, bench):
        job.specjvm_set.create()
        return "ok"

    def refresh_database(self, jobs):
        self.clear_database()

        for job in jobs:
            self.store_job(job)

            #for each job, store its build data


        return "ok"
