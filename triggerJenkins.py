import json, os, httplib, datetime
from time import sleep

def run():
	global configs
	configs = loadjsondata("./config.json")
	repository_list = configs['repository_list']
	
	while True:
		print "scan source code change @", datetime.datetime.now()
		for repository in repository_list:
			oldPath = os.getcwd()
			realTemplateFilePath = configs['install_dir'] + '/' +repository
			os.chdir(realTemplateFilePath)
			# call 'git pull'
			pullResult = os.popen('git pull').read()
			print "pull result: ", pullResult
			if len(pullResult) < 1:
				print "ERROR: cannot execute 'git pull' in folder %s" % repository 		
			elif not "up-to-date" in pullResult:
				for moduleName in configs['folder_job_mappings'][repository]:
					compareResult = os.popen('git log --quiet HEAD~..HEAD ' + moduleName).read()
					if len(compareResult) > 0:
						jobName = configs['folder_job_mappings'][repository][moduleName]
						trigger(jobName)
			# change the folder back			
			os.chdir(oldPath)
		
		runningMode = configs['running_mode']
		if runningMode == 'once':
			break
		else:
			# sleep for a while...
			sleep(configs["scan_interval"])

def trigger(jobName):
	print "######## triggering jenkins job: {%s} ########" % jobName
	path = "/job/" + jobName + "/build"
	conn = httplib.HTTPConnection(configs['jenkins_url'])
	# using token in the query parameter
	if configs['token'] is not None:
		path += '?token=' + configs['token']	
	conn.request("GET", path)
	
	
def loadjsondata(path):
	with open(path, 'r') as f:
		text = f.read()
		try:
			return json.loads(text);
		except:
			return None
			
def main():
	run()
		
if __name__ == '__main__':
    main()

	
