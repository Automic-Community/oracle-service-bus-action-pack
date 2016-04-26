import wlstModule
from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.config import Ref

connectObj = False
try:
	try:
		username = sys.argv[1]
		password = sys.argv[2]
		url = sys.argv[3]
		sessionName = sys.argv[4]
		
		# connect to OSB with URL endpoint, username and password
		connectObj = connect(username, password, url)
		connectObj = True
		domainRuntime()

		# obtain session management mbean to discard a session.
		sessionMBean = findService(SessionManagementMBean.NAME, SessionManagementMBean.TYPE)
		
		# discard a session and provide a description to it.
		sessionMBean.discardSession(sessionName)
		print "Session with the name [%s] discard successfully" %sessionName

	except:
		print "ERROR : Unable to discard the session. Please check input parameters ", sys.exc_info()[0]
		dumpStack()
		raise
finally:
		if connectObj is True:
			disconnect()