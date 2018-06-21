from jenkinsapi.jenkins import Jenkins
from BenchMiner import BenchMiner

class JenkinsConnector:

    def __init__(self, jenkins_url="http://localhost:8080", name="tsarnas", key="867fc4dc252312faf00f73e08ed6876e"):
        self.server = Jenkins(jenkins_url, name, key)

    def get_jobs_summary(self):
        server_jobs = []

        print str(self.server.get_jobs_list())

        for job_name, job_instance in self.server.get_jobs():
            name = job_instance.name
            description = job_instance.get_description()
            is_running = str(job_instance.is_running())
            is_enabled = str(job_instance.is_enabled())

            server_jobs.append({
                'name': name,
                'description': description,
                'is_running': is_running,
                'is_enabled': is_enabled})

        return server_jobs

    def get_job_details(self, jobname):

        job = self.server.get_job(jobname)

        fb = job.get_first_build()
        lb = job.get_last_build()

        spec_miner = BenchMiner(lb.get_console())

        #get all specjvm results
        spec_result = spec_miner.mine_all_specjvms()

        #get all dacapo tests
        dacapo_result = spec_miner.mine_all_dacapos()

        job_details = {
            'name': job.name,
            'description': job.get_description(),
            'is_running': job.is_running(),
            'is_enabled': job.is_enabled(),
            'first_build_no': str(fb.buildno),
            'last_build_no': str(lb.buildno),
            'job_running': str(job.is_running()), #TODO: remove later this and the rest below
            'is_good': str(lb.is_good()),
            'specjvm': spec_result,
            'dacapo': dacapo_result
        }

        return job_details

    def get_build_benchmarks(self, jobname, build_no):
        job = self.server.get_job(jobname)
        build = job.get_build(build_no)

        spec_miner = BenchMiner(build.get_console())

        # get all specjvm results
        spec_result = spec_miner.mine_all_specjvms()

        # get all dacapo tests
        dacapo_result = spec_miner.mine_all_dacapos()

        build_details = {
            'build_no': str(build_no),
            'is_good': str(build.is_good()),
            'specjvm': spec_result,
            'dacapo': dacapo_result
        }

        return build_details
