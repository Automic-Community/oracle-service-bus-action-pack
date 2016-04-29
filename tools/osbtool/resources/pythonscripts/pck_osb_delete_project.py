import wlstModule
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.config import Ref
from java.util import Collections

def deleteProject(alsbConfigurationMBean, projectName):
	try:
		projectRef = Ref(Ref.PROJECT_REF, Ref.DOMAIN, projectName)                  
		if alsbConfigurationMBean.exists(projectRef):
			print 'INFO: Removing OSB project: ' + projectName
			alsbConfigurationMBean.delete(Collections.singleton(projectRef))
			print 'INFO: Removed OSB project: ' + projectName
		else:
			raise ValueError('No OSB project exists with name ' + projectName)
	except:
		raise

connectObj = False
failStatus = 1
try:
	try:
		if len(sys.argv) < 7:
			raise ValueError('Usage: java weblogic.WLST pythonscript.py <url> <username> <password> <timeout> <sessionName> <projectname>')
		
		url = sys.argv[1]
		username = sys.argv[2]
		password = sys.argv[3]
		connectionTimeout = sys.argv[4]
		sessionName = sys.argv[5]
		projectName = sys.argv[6]
		
		#logging the inputs received
		print "URL : [%s]" %url
		print "Username : [%s]" %username
		print "Session Name : [%s]" %sessionName
		print "Connection Timeout : [%s]" %connectionTimeout
		print "Project Name : [%s]" %projectName
		
		# connect to OSB with URL endpoint, username and password 
		connect(username, password, url, timeout=connectionTimeout)
		connectObj = True
		domainRuntime()
	
		# obtain ALSBConfigurationMBean to delete project
		alsbConfigurationMBean = findService(ALSBConfigurationMBean.NAME + "." + sessionName, ALSBConfigurationMBean.TYPE)
		if alsbConfigurationMBean is not None:
			deleteProject(alsbConfigurationMBean, projectName)
			failStatus = 0
		else:
			raise ValueError('No session exists with name ' + sessionName)	
	except:
		print 'ERROR: Unable to delete Project. Possible error:', sys.exc_info()[1]
		print 'Please check the input parameters'
finally:
	if connectObj:
		disconnect("true")
	exit("y", failStatus)