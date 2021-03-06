import wlstModule
from com.bea.wli.sb.management.configuration import SessionManagementMBean

connFlag = False
exitFlag = 1
try:
	try:
		if len(sys.argv) < 6:
			raise ValueError('Usage: java weblogic.WLST pythonscript.py <url> <username> <password> <timeout> <sessionName>')
		
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

		# obtain session management mbean to discard a session.
		sessionMBean = findService(SessionManagementMBean.NAME, SessionManagementMBean.TYPE)
		
		# discard a session and provide a description to it.
		sessionMBean.discardSession(sessionName)
		print "Session with the name [%s] discard successfully" %sessionName
		exitFlag = 0
	except:
		print "ERROR : Unable to discard the session. Possible error:", sys.exc_info()[1]
		print "Please check the input parameters"
	
finally:
	if connFlag:
		disconnect("true")
	exit("y",exitFlag)