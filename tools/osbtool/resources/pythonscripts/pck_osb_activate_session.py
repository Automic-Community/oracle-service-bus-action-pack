import wlstModule
from com.bea.wli.sb.management.configuration import SessionManagementMBean

connFlag = False
exitFlag = 1
try:
	try:
		if len(sys.argv) < 6:
			raise ValueError('Usage: java weblogic.WLST pythonscript.py <url> <username> <password> <timeout> <sessionName> <sessionDescription-optional>')
		
		url = sys.argv[1]
		username = sys.argv[2]
		password = sys.argv[3]
		connectionTimeout = sys.argv[4]
		sessionName = sys.argv[5]
		
		#logging the inputs received
		print "URL : [%s]" %url
		print "Username : [%s]" %username
		print "Connection Timeout : [%s]" %connectionTimeout
		print "Session Name : [%s]" %sessionName
		
		
		# connect to OSB with URL endpoint, username, password, timeout
		connect(username, password, url, timeout=connectionTimeout)
		connFlag = True
		
		#to access the runtime MBean
		domainRuntime()

		# obtain session management mbean to activate a session.
		sessionMBean = findService(SessionManagementMBean.NAME, SessionManagementMBean.TYPE)
		
		sessionDesc = None
		# activate a session and provide a description to it.
		if len(sys.argv) == 7:
			print "Session Description : ", sys.argv[6]
			sessionDesc = sys.argv[6]
		sessionMBean.activateSession(sessionName, sessionDesc)
		print "Session with the name [%s] activated successfully" %sessionName
		exitFlag = 0
	except:
		print "ERROR : Unable to activate the session. Possible error:", sys.exc_info()[1]
		print "Please check the input parameters"
	
finally:
	if connFlag:
		disconnect("true")
	exit("y",exitFlag)