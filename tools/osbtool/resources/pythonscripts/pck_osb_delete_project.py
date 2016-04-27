import wlstModule
from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.config import Ref

def deleteProject(alsbConfigurationMBean, projectName):
     try:
          print "Trying to remove " + projectName
          projectRef = Ref(Ref.PROJECT_REF, Ref.DOMAIN, projectName)                  
          if alsbConfigurationMBean.exists(projectRef):
               print "#### removing OSB project: " + projectName
               alsbConfigurationMBean.delete(Collections.singleton(projectRef))
               print "#### removed project: " + projectName
          else:
               failed = "OSB project <" + projectName + "> does not exist"
               print failed
          print
     except:
          print "Error while removing project:", sys.exc_info()[0]
          raise
try:
	username = sys.argv[1]
	password = sys.argv[2]
	url = sys.argv[3]
	sessionName = sys.argv[4]
	projectName = sys.argv[5]
		
	# connect to OSB with URL endpoint, username and password
	connect(username, password, url)
	domainRuntime()

	# obtain session management mbean to activate a session.
	sessionMBean = findService(SessionManagementMBean.NAME, SessionManagementMBean.TYPE)
	
	# obtain ALSBConfigurationMBean to delete project
	alsbConfigurationMBean = findService(ALSBConfigurationMBean.NAME + "." + sessionName, ALSBConfigurationMBean.TYPE)
	deleteProject(alsbConfigurationMBean, projectName)


except:
	raise "ERROR: Please check Input parameters.", sys.exc_info()[0]
