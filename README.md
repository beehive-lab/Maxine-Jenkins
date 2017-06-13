# Maxine-Jenkins

1) Download Jenkins
	-mirrors.jenkins.io/war-stable/latest/jenkins.war

2) Start Jenkins
	-From jenkins.war directory: java -jar jenkins.war
	
	-Browse to http://localhost:8080 and follow the instructions to complete the installation

3) Multiple SCM plug-in installation
	-to build and run Maxine on Jenkins we need to check out from both Maxine and Graal repositories, so we need Multiple SCM plugin!
	
	-go to Manage Jenkins/Manage Plug-ins/available tab/Multiple SCMs plugin - install and restart jenkins

4) Configure Maxine build and run in Jenkins
	4.1-New freestyle project - name (MaxineBench)

	4.2-Source Code Management options
		-Multiple SCMs
			-add new SCM
				-git -> Maxine-VM repositiry url (git clone https://github.com/beehive-lab/Maxine-VM.git)
		-Additional Behaviours 
			-check out to sub-directory 
				-Local subdirectory for repo -> maxine
	
	4.3-Source Code Management options
		-Multiple SCMs
			-add new SCM
				-git -> Maxine-Graal repositiry url (https://github.com/beehive-lab/Maxine-Graal.git)
		-Additional Behaviours 
			-check out to sub-directory 
				-Local subdirectory for repo -> graal
	
	4.4-Build options
		-Execute Shell

			sed -i -e 's/%as /%ms /g' $WORKSPACE/maxine/com.oracle.max.vm.native/tele/linux/linuxTask.c
			export WORKDIR=$WORKSPACE
			export JAVA_HOME=/usr/lib/jvm/jdk1.7.0_25
			export MAXINE_HOME=$WORKDIR/maxine
			export GRAAL_HOME=$WORKDIR/graal
			export PATH=$PATH:$GRAAL_HOME/mxtool/:$MAXINE_HOME/com.oracle.max.vm.native/generated/linux/
			#export BENCHDIR=$WORKSPACE/Benchmarks
			#export SPECJVM98_ZIP=$BENCHDIR/SPECjvm2008.jar
			#export DACAPOBACH_JAR=$BENCHDIR/dacapo-9.12-bach.jar
		
			cd $MAXINE_HOME
			mx build
			mx image
			mx helloworld
			#mx test -insitu -tests=dacapobach
			#mx test -insitu -tests=specjvm98

5) Maxine build and run benchmarks in Jenkins:
	
	5.1-make a test build (runs helloworld)
	
	5.2-if all ok go to .jenkins/Workspace/MaxineBench and create the Benchmarks folder
	
	5.3-place inside the SPECjvm2008.zip and dacapo-9.12-bach.jar
	
	5.4-then configure the build : 	comment 	mx helloworld
									uncomment	export BENCHDIR=$WORKSPACE/Benchmarks
												export SPECJVM98_ZIP=$BENCHDIR/SPECjvm2008.jar
												export DACAPOBACH_JAR=$BENCHDIR/dacapo-9.12-bach.jar
												mx test -insitu -tests=dacapobach
												OR
												mx test -insitu -tests=specjvm98