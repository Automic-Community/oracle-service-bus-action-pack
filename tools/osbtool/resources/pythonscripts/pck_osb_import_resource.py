import wlstModule
from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.config import Ref
from java.io import FileInputStream

import sys

connFlag = False
exitFlag = 1
try:
	try:
		if len(sys.argv) < 7:
			raise ValueError('Usage: java weblogic.WLST pythonscript.py <url> <username> <password> <timeout> <sessionName> <jarfilepath> <passPhrase:optional>')
		
		url = sys.argv[1]
		username = sys.argv[2]
		password = sys.argv[3]
		connectionTimeout = sys.argv[4]
		sessionName = sys.argv[5]
		jarfilepath = sys.argv[6]
		
		#logging the inputs received
		print "URL : [%s]" %url
		print "Username : [%s]" %username
		print "Connection Timeout : [%s]" %connectionTimeout
		print "Session Name : [%s]" %sessionName
		print "JAR File Path : [%s]" %jarfilepath
		
		# connect to OSB with URL endpoint, username, password, timeout
		connect(username, password, url, timeout=connectionTimeout)
		connFlag = True
		
		#to access the runtime MBean
		domainRuntime()

		# obtain session management mbean to create a session.
		# This mbean instance can be used more than once to
		# create/discard/commit many sessions

		sessionMBean = findService(SessionManagementMBean.NAME, SessionManagementMBean.TYPE)

		# obtain the ALSBConfigurationMBean instance that operates
		# on the session that has just been created. Notice that
		# the name of the mbean contains the session name.

		alsbSession = findService(ALSBConfigurationMBean.NAME + '.'+ sessionName, ALSBConfigurationMBean.TYPE)

		# read a resource config file (example a jar) into bytes and uploading it

		if alsbSession is None:
			print 'Session %s not found ' % sessionName
			raise 
		print 'Reading imported jar file....'

		fh = open(jarfilepath, 'rb')
		filebytes = fh.read()
		fh.close()

		# Uploading jar file

		print 'Uploading Jar file.....'
		alsbSession.uploadJarFile(filebytes)
		print 'Jar Uploaded.......'

		print 'ALSB Project will now get imported'
		jarInfo = alsbSession.getImportJarInfo()
		importPlan = jarInfo.getDefaultImportPlan()
		if len(sys.argv) == 8:
			importPlan.setPassphrase(sys.argv[7])
		result = alsbSession.importUploaded(importPlan)

		# Print out status and build a list of created references.

		if result.getFailed().isEmpty() == false:
			print 'One or more resources could not be imported properly'
			raise
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