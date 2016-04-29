import wlstModule
from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.config import Ref
from com.bea.wli.config.customization import Customization
from java.io import FileInputStream 

import sys

connFlag = False
exitFlag = 1

try:
    try:

        if len(sys.argv) < 7:
            raise ValueError('Usage: java weblogic.WLST pythonscript.py <url> <username> <password> <timeout> <sessionName> <customFile>'
                             )

        url = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]
        connectionTimeout = sys.argv[4]
        sessionName = sys.argv[5]
        customFile = sys.argv[6]

        # logging the inputs received

        print 'URL : [%s]' % url
        print 'Username : [%s]' % username
        print 'Connection Timeout : [%s]' % connectionTimeout
        print 'Session Name : [%s]' % sessionName
        print 'Customization File : [%s]' % customFile

        # connect to OSB with URL endpoint, username, password, timeout

        connect(username, password, url, timeout=connectionTimeout)
        connFlag = True

        # to access the runtime MBean

        domainRuntime()

        # obtain the ALSBConfigurationMBean instance that operates
        # on the session that has just been created. Notice that
        # the name of the mbean contains the session name.

        alsbConfigurationMBean = findService(ALSBConfigurationMBean.NAME + '.'
                        + sessionName, ALSBConfigurationMBean.TYPE)

        # read a resource config file (example a jar) into bytes and uploading it

        if alsbConfigurationMBean is None:
            raise ValueError('No session exists with name '
                             + sessionName)

        # customizing

        print 'Executing customization '

        print 'Loading customization File', customFile
        iStream = FileInputStream(customFile)
        customizationList = Customization.fromXML(iStream)
        alsbConfigurationMBean.customize(customizationList)
        print 'Execution of customization done successfully'
        exitFlag = 0
    except:

        print 'ERROR : Unable to execute customization. Possible error:', \
            sys.exc_info()[1]
        print 'Please check the input parameters'
finally:

    if connFlag:
        disconnect('true')
    exit('y', exitFlag)


			