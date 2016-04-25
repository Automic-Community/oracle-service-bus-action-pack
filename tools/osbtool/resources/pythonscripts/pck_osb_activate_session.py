import wlstModule
from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.config import Ref

try:
		username = sys.argv[1]
		password = sys.argv[2]
		url = sys.argv[3]
		sessionName = sys.argv[4]
		sessionDescription = sys.argv[5]
		
		# connect to OSB with URL endpoint, username and password
		connect(username, password, url)
		domainRuntime()

		# obtain session management mbean to activate a session.
		sessionMBean = findService(SessionManagementMBean.NAME, SessionManagementMBean.TYPE)
		
		# activate a session and provide a description to it.
		if not sessionDescription:
			sessionMBean.activateSession(sessionName, None)
			print "Session with the name [%s] activated successfully" %sessionName
		else:
			sessionMBean.activateSession(sessionName, sessionDescription)
			print "Session with the name [%s] activated successfully" %sessionName

except:
		print "ERROR : Unable to activate the session. Please check input parameters ", sys.exc_info()[0]
		dumpStack()
		raise
		