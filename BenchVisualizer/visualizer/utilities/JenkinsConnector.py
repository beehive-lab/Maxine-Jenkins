from jenkinsapi.jenkins import Jenkins
from BenchMiner import BenchMiner

class JenkinsConnector:

    """
    Handles the connection of the web application to the Jenkins Server, as well as the the data passed.
    It uses the JenkinsApi python module to provide this functionality
    More on JenkinsApi: https://github.com/pycontribs/jenkinsapi/
    """

    def __init__(self, jenkins_url="http://localhost:8080", name="tsarnas", key="867fc4dc252312faf00f73e08ed6876e"):
        self.server = Jenkins(jenkins_url, name, key)

    def get_jobs_summary(self):
        server_jobs = []

        print str(self.server.get_jobs_list())
        jenkins_job_names = self.server.get_jobs_list()

        for job_name in jenkins_job_names:

            '''
            Avoid duplicate Job entries on the server, like for example:
            'Job1' and 'http:/0.0.0.0:8080/Job1'
            '''
            if not job_name.startswith('http:/'):
                job_details = self.get_job_details(job_name)
                server_jobs.append(job_details)

        # if no jobs are found on the jenkins server...
        if server_jobs == []:
            raise ValueError("No jobs found on the Jenkins server!")

        return server_jobs

    def get_job_details(self, jobname):

        job = self.server.get_job(jobname)

        fb = job.get_first_build()
        lb = job.get_last_build()

        job_details = {
            'name': job.name,
            'description': job.get_description(),
            'is_running': job.is_running(),
            'is_enabled': job.is_enabled(),
            'first_build_no': str(fb.buildno),
            'last_build_no': str(lb.buildno),
            'job_running': str(job.is_running())
        }

        return job_details

    def get_build_benchmarks(self, jobname, build_no):
        job = self.server.get_job(jobname)
        build = job.get_build(build_no)

        '''
        Jenkinsapi's get_revision() throws exception for this pipeline.
        Bypass Jenkinsapi's get_revision() to get the attribute 'git revision'
        directly from the build object.
        '''
        revision = getattr(build, '_get_git_rev', lambda: None)()
        
        spec_miner = BenchMiner(build.get_console())

        # get all specjvm results
        spec_result = spec_miner.mine_all_specjvms()

        # get all dacapo tests
        dacapo_result = spec_miner.mine_all_dacapos()

        build_details = {
            'build_no': build_no,
            'is_good': str(build.is_good()),
            'revision': revision,
            'specjvm': spec_result,
            'dacapo': dacapo_result
        }

        return build_details

    def get_job_and_benchmarks(self, job_name):

        job_dtl = self.get_job_details(job_name)
        # for each one of the job's builds, get the benchmarks
        builds = []
        print "Job: " + job_name + " --------> Searching for good builds"
        for i in range(int(job_dtl["first_build_no"]), int(job_dtl["last_build_no"]) + 1, 1):
            # exclude the failed builds
            if self.is_build_good(job_name, i) == "False":
                continue
            print "Job: " + job_name + " ----> scanning build " + str(i)
            build = self.get_build_benchmarks(job_name, i)
            builds.append(build)
        '''
        For each job, some basic details are stored ('details' part), 
        along with benchmark information for every build ('builds' part)
        '''
        job = {
            'details': job_dtl,
            'builds': builds
        }

        return job

    def is_build_good(self, jobname, build_no):

        job = self.server.get_job(jobname)
        build = job.get_build(build_no)

        return str(build.is_good())
