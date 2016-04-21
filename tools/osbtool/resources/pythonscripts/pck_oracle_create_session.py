import wlstModule
from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.config import Ref

try:
		username = sys.argv[1]
		password = sys.argv[5]
		hostname = sys.argv[2]
		sessionName = sys.argv[4]
		port = sys.argv[3]
		
		connect(username, password, 't3://'+ hostname + ':' + port)
		domainRuntime()

		# obtain session management mbean to create a session.
		sessionMBean = findService(SessionManagementMBean.NAME,SessionManagementMBean.TYPE)
		
		# create a session
		sessionMBean.createSession(sessionName)
except:
		print "Unexpected error: ", sys.exc_info()[0]
		dumpStack()
		raise
