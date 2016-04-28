import wlstModule
from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.config import Ref
from java.util import Collections
from com.bea.wli.sb.util import Refs

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
		if len(sys.argv) < 6:
			raise ValueError('Missing Arguments to python script.')
		
		username = sys.argv[1]
		password = sys.argv[2]
		url = sys.argv[3]
		sessionName = sys.argv[4]
		projectName = sys.argv[5]
		
		#logging the inputs received
		print "URL : [%s]" %url
		print "Username : [%s]" %username
		print "Session Name : [%s]" %sessionName
		print "Project Name : [%s]" %projectName
		
		# connect to OSB with URL endpoint, username and password 
		connect(username, password, url)
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
		print 'ERROR: Unable to delete Project. Please check input parameters.', sys.exc_info()[1]
finally:
	if connectObj:
		print 'INFO: Disconnecting from OSB ' + sys.argv[3]
		disconnect()
	exit("y", failStatus)