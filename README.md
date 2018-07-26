# Maxine - Jenkins

# Benchvisualizer

A web application that visualizes the results from the benchmarks SPECJVM2008 and Dacapo. The application connects on a running Jenkins Server and gets useful information about a specific job, if it has ran either of the specific tests.

## Installation Instructions

Please make sure that the system supports Python 2.7.x along with `pip` before proceeding.
Also the system should have the Jenkins server up and running.
Internet connection is required to use BenchVisualizer.

 - Install the JenkinsApi Python module: `pip install jenkinsapi`
 - Install Django, version 1.11: `pip install Django==1.11`. After this, make sure that the installation is successful by typing in the Python shell: `import Django` and `print(django.get_version())`.
 - Set up an RDBMS of your choice. To install mysql server: `sudo apt-get install mysql-server`. The following steps assume mysql is installed.
 - Optional: Install a GUI tool for the RDBMS, such Mysql workbench: `sudo apt install mysql-workbench`
 - Create a new empty schema in the RDBMS with a name of your choice ('bench_database' will be used for the following steps)
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
   If any error pops up, you can delete the BenchVisualizer/visualizer/migrations folder and try the commands again.

 - If you have protection enabled on the Jenkins server, you will need to go into the file BenchVisualizer/visualizer/utilities/JenkinsConnector.py and modify the user name and access token in line 12.

 - To start the built-in Django server, run: `python manage.py runserver` from the project root directory. This will run the server on the   port 8000. The command takes an optional argument if you want a different, specific port.
 - Open a web browser and paste the url `http://127.0.0.1:8000/visualizer/`. The application interface is displayed with no data (no Jenkins jobs registered yet). Click the button "Register Job" on the upper right corner. If the connection to Jenkins is successfull, a list of all the Jenkins Job is displayed. Select the Jobs to be registered and submit (without checking the purge box). Checking again on `http://127.0.0.1:8000/visualizer/` will have the list of registered jobs. Select one to display the benchmark details for the job's builds.

# Benchmark Pipeline



