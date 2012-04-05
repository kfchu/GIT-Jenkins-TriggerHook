import json, os, httplib, datetime, base64
from time import sleep

def run():
	global configs
	configs = loadJsonData("./config.json")
	repository_list = configs['repository_list']
	
	while True:
		print "scan change @", datetime.datetime.now()
		for repository in repository_list:
			oldPath = os.getcwd()
			realTemplateFilePath = configs['install_dir'] + '/' +repository
			os.chdir(realTemplateFilePath)
			# call 'git pull'
			pullResult = os.popen('git pull').read()
			print "pull result: ", pullResult
			if len(pullResult) < 1:
				print "ERROR: cannot execute 'git pull' in folder %s" % repository 		
			elif not "up to date" in pullResult:
				for jobName in configs['folder_job_mappings'][repository]:
					compareResult = os.popen('git log --quiet HEAD~..HEAD ' + jobName).read()
					if len(compareResult) > 0:
						trigger(jobName)
			# change the folder back			
			os.chdir(oldPath)
		# sleep for a while...
		sleep(configs["scan_interval"])

def trigger(jobName):
	print "######## triggering jenkins job: {%s} ########" % jobName
	path = "/jenkins/job/" + jobName + "/build"
	conn = httplib.HTTPConnection(configs['jenkins_url'])
	if configs['jenkins_username'] is not None:
		encodeStr = base64.encodestring('%s:%s' % (configs['jenkins_username'], configs['jenkins_password']))[:-1]
		authheader =  "Basic %s" % encodeStr
		headers = {"Authorization": authheader}
		conn.request("GET", path, None, headers)
	else:
		conn.request("GET", path)
	
	
def loadJsonData(path):
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

	