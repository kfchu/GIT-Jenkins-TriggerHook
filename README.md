# Purpose
This script is to trigger the Jenkins job remotely when the code is updated using GIT.

# How does work?
The script will scan the git changes time by time. 
If change is found, it will find out which folder is changed and trigger the relative jenkins job.

# How to use?
Step1: modify the config.json to update the parameters.

* jenkins_url : your jenkins host name
* token : if you set the jenkins job run with token, then put the value here
* install_dir : the source code folder. e.g if you have a repository whose path is /opt/project1, then the install_dir should be /opt
* repository_list : the repository names, split by comma ','.
* folder_job_mappings : the git project to jenkins job name mapping.
  It contains 2 level. The 1st level is the repository name, and the 2nd level is the mapping under the specified repository context.
* running_mode : "once" means if only run once, the other value will consider it run as a loop.
* scan_interval : the interval to scan the changes, the unit here is second. The parameter is work only when you set running_mode is NOT 'once'

Step2: run it!
> python triggerJenkins.py