import wlstModule
from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.config import Ref

try:
		connect(sys.argv[1], sys.argv[2], 't3://'+ sys.argv[3] + ':' + sys.argv[4])
		domainRuntime()

		# obtain session management mbean to create a session.
		# This mbean instance can be used more than once to
		# create/discard/commit many sessions
		sessionMBean = findService(SessionManagementMBean.NAME,SessionManagementMBean.TYPE)
		
		# create a session
		sessionMBean.createSession(sys.argv[5])
except:
		print "Unexpected error: ", sys.exc_info()[0]
		dumpStack()
		raise
