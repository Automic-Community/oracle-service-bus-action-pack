import wlstModule
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean

connFlag = False
exitFlag = 1
try:
	try:
		if len(sys.argv) < 7:
			raise ValueError('Usage: java weblogic.WLST pythonscript.py <url> <username> <password> <timeout> <sessionName> <configurationfile> <passPhrase:optional>')
		
		url = sys.argv[1]
		username = sys.argv[2]
		password = sys.argv[3]
		connectionTimeout = sys.argv[4]
		sessionName = sys.argv[5]
		configFile = sys.argv[6]
		
		#logging the inputs received
		print "URL : [%s]" %url
		print "Username : [%s]" %username
		print "Connection Timeout : [%s]" %connectionTimeout
		print "Session Name : [%s]" %sessionName
		print "Configuration File Path : [%s]" %configFile
		
		# connect to OSB with URL endpoint, username, password, timeout
		connect(username, password, url, timeout=connectionTimeout)
		connFlag = True
		
		#to access the runtime MBean
		domainRuntime()

		# obtain the ALSBConfigurationMBean instance that operates
		# on the session that has just been created. Notice that
		# the name of the mbean contains the session name.

		alsbSession = findService(ALSBConfigurationMBean.NAME + '.'+ sessionName, ALSBConfigurationMBean.TYPE)

		# read a resource config file (example a jar) into bytes and uploading it

		if alsbSession is None:
			raise ValueError('No session exists with name ' + sessionName)
			
		print 'Reading imported configuration file....'

		fh = open(configFile, 'rb')
		filebytes = fh.read()
		fh.close()

		print 'Uploading Configuration file.....'
		alsbSession.uploadJarFile(filebytes)
		print 'Configuration File Uploaded.......'

		print 'ALSB Project will now get imported'
		jarInfo = alsbSession.getImportJarInfo()
		importPlan = jarInfo.getDefaultImportPlan()
		if len(sys.argv) == 8:
			importPlan.setPassphrase(sys.argv[7])
			print 'Passphrase has been set'
		result = alsbSession.importUploaded(importPlan)

		# Print out status and build a list of created references.

		if result.getFailed().isEmpty() == false:
			raise ValueError('One or more resources could not be imported properly')			
		else:
			print 'The following resources have been imported: '
			for successEntry in result.getImported():
				print '-- %s' % successEntry.toString()
		exitFlag = 0
	except:
		print "ERROR : Unable to import resource. Possible error:", sys.exc_info()[1]
		print "Please check the input parameters"
	
finally:
	if connFlag:
		disconnect("true")
	exit("y",exitFlag)