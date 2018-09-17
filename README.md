# Benchvisualizer

A web application that visualizes the results from the benchmarks SPECJVM2008 and Dacapo. The application connects on a running Jenkins Server and gets useful information about a specific job, if it has ran either of the specific tests.

## Installation Instructions (development server on localhost)

Please make sure that the system supports Python 2.7.x along with `pip` before proceeding.
Also the system should have the Jenkins server up and running.
Internet connection is required to use BenchVisualizer.

 - Install the JenkinsApi Python module: `pip install jenkinsapi`
 - Install Django, version 1.11: `pip install Django==1.11`. After this, make sure that the installation is successful by typing in the Python shell: `import Django` and `print(django.get_version())`.
 - Set up an RDBMS of your choice. To install mysql server: `sudo apt-get install mysql-server`. The following steps assume mysql is installed.
 - Optional: Install a GUI tool for the RDBMS, such Mysql workbench: `sudo apt install mysql-workbench`
 - Create a new empty schema in the RDBMS with a name of your choice ('bench_database' will be used for the following steps):
   ```echo "create database `database-name`" | mysql -u username -p```
 - Now we will set up the connection between Django and mysql. Run the following commands:
   `sudo apt-get install libmysqlclient-dev` and then `sudo pip install MySQL-python`
 - Download the project folder (BenchVisualizer/) from git and extract it to a directory of your choice. The full path of the root of the     project will be needed for the Jenkins pipeline later on.
 - Open the file BenchVisualizer/BenchVisualizer/settings.py and edit this part (depending on the schema name, username and pwd you specified):
  ```
  DATABASES = {
    'default': {
	'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'bench_database',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}
  ```
 - Now go to the root of the project (BenchVisualizer/) and run:
   `python manage.py makemigrations visualizer` and `python manage.py migrate`.
   This will create the DB on the RDBMS. If any error pops up, you can delete the BenchVisualizer/visualizer/migrations folder and try the commands again.

 - If you have protection enabled on the Jenkins server, you will need to go into the file BenchVisualizer/visualizer/utilities/JenkinsConnector.py and modify the user name and access token in line 12. In the case that Jenkis runs remotely, you can also specify the IP.

 - To start the built-in Django server, run: `python manage.py runserver` from the project root directory. This will run the server on the   port 8000. The command takes an optional argument if you want a different, specific port.


# Benchmark Pipeline

This Jenkins pipeline builds MaxineVM and then runs all the specjvm and dacapo benchmarks. In the end, it adds the benchmarks to the DB of BenchVisualizer.

## Setup Instructions

Before proceeding, make sure that SPECJVM2008 is installed on the machine (that runs Jenkins) and `dacapo-9.12-bach.jar` is available.

 - Download the file `bench_Jenkinsfile` from the repo and paste it into the root directory of MaxineVM ($MAXINE_HOME, along the existing Jenkinsfile).
 - edit the pipeline file (`bench_Jenkinsfile`), more scpecifically the environment variables `DJANGO` (Full path to the root of BenchVisualizer), `DACAPO` (full path to the directory containing the dacapo .jar), `SPECJVM2008` (full path to the root directory of SPECJVM2008 installation). For simplicity, you can place the dacapo .jar into specjvm's directory.
 - You may also need to modify specjvm execution steps, to specify different iteration/warmup times.
 - Open Jenkins GUI and create a new pipeline/job following the instructions at `https://jenkins.io/doc/book/pipeline/getting-started/#defining-a-pipeline-in-scm`. Name the pipeline "MaxinePipeline".
 - Under the Configurations tab of the new Job, specify the following:
 	* Under "Build Triggers" select "Poll SCM" and in the schedule field define the time when Jenkins will check the repo for changes. Checking should be done daily, so a value like `30 03 * * *` will check the repo daily at 03:30. If there are new commits until then, the pipeline will start.
 	* Under "Advanced build options": Pipeline->Definition: "Pipeline as scm", SCM: "Git", Repository URL: "https://github.com/beehive-lab/Maxine-VM/", token:(your jenkins token), branch: "*/develop", script path: "bench_Jenkinsfile".
	* Press "Save"
 - Run the pipeline once and let it finish

# Final steps

 - Open a web browser and paste the url `http://127.0.0.1:8000/visualizer/`. You should see the new job "MaxinePipeline". Click on it to view the benchmarks of the first build. Every day the DB will be updated with benchmarks from new builds, if new commits are made into the develop branch.

# Deploying Django to production

 - Deploy a Django project with Apache: https://docs.djangoproject.com/en/1.11/howto/deployment/ . 
 - Deploy the project into a remote Django - ready (PaaS) server with minimum configuration needed: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Deployment

It is recommended that you use the same machine that hosts Jenkins, as a web server. If the server is remote, then the Jenkins pipeline (`DB update` stage) must use the `ssh step` to communicate with the application. Also the server environment must set the following variables:
 - `export DJANGO_DEBUG=''`, which sets Django debug mode on False
 - `export DJANGO_SECRET_KEY=<your_secret_key>`, which sets a large random value used for CSRF protection.


