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
		else:
			sessionMBean.activateSession(sessionName, sessionDescription)
except java.lang.NullPointerException:
		raise "ERROR: Cannot find session " + sys.argv[4], sys.exc_info()[0]
except:
		raise "ERROR: Please check Input parameters.", sys.exc_info()[0]