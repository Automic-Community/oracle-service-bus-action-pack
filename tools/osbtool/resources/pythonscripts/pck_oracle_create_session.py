import wlstModule
from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.config import Ref

try:
		username = sys.argv[1]
		password = sys.argv[4]
		hostname = sys.argv[2]
		sessionName = sys.argv[3]
		
		if len(sys.argv) == 6:
				connect(username, password, 't3://'+ hostname + ':' + sys.argv[5])
		else:
				connect(username, password, 't3://'+ hostname)
		
		domainRuntime()

		# obtain session management mbean to create a session.
		sessionMBean = findService(SessionManagementMBean.NAME,SessionManagementMBean.TYPE)
		
		# create a session
		sessionMBean.createSession(sessionName)
except:
		print "Unexpected error: ", sys.exc_info()[0]
		dumpStack()
		raise
