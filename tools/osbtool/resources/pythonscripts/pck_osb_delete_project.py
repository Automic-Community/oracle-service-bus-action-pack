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
               raise AttributeError('No OSB project exists with name ' + projectName)
     except:
          raise

connectObj = False
try:
	try:
		username = sys.argv[1]
		password = sys.argv[2]
		url = sys.argv[3]
		sessionName = sys.argv[4]
		projectName = sys.argv[5]
		
		# connect to OSB with URL endpoint, username and password
		connectObj = connect(username, password, url)
		connectObj = True
		domainRuntime()

		# obtain ALSBConfigurationMBean to delete project
		alsbConfigurationMBean = findService(ALSBConfigurationMBean.NAME + "." + sessionName, ALSBConfigurationMBean.TYPE)
		if alsbConfigurationMBean is not None:
			deleteProject(alsbConfigurationMBean, projectName)
		else:
			raise AttributeError('No session exists with name ' + sessionName) 
	except:
		print "ERROR : Unable to delete Project. Please check input parameters ", sys.exc_info()[0]
		dumpStack()
		raise
finally:
		if connectObj is True:
			disconnect()	