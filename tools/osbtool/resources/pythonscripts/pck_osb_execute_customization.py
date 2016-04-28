import wlstModule
from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.config import Ref
from com.bea.wli.config.customization import Customization
from java.io import FileInputStream

import sys

try:

    username = sys.argv[1]
    password = sys.argv[2]
    url = sys.argv[3]
    sessionName = sys.argv[4]
    customFile = sys.argv[5]

    connect(username, password, url)
    domainRuntime()

    # obtain session management mbean to create a session.
    # This mbean instance can be used more than once to
    # create/discard/commit many sessions

    sessionMBean = findService(SessionManagementMBean.NAME,
                               SessionManagementMBean.TYPE)

    # obtain the ALSBConfigurationMBean instance that operates
    # on the session that has just been created. Notice that
    # the name of the mbean contains the session name.

    alsbConfigurationMBean = findService(ALSBConfigurationMBean.NAME + '.'
                              + sessionName,
                              ALSBConfigurationMBean.TYPE)

    # read a resource config file (example a jar) into bytes and uploading it

    if alsbConfigurationMBean is None:
        print 'Session %s not found ' % sessionName
        raise
    
    # customize if a customization file is specified
    # affects only the created resources

    if customFile != None:
        print 'Loading customization File', customFile
        iStream = FileInputStream(customFile)
        customizationList = Customization.fromXML(iStream)
        alsbConfigurationMBean.customize(customizationList)
except:

    print 'Unexpected error while importing resource : ', \
        sys.exc_info()[0]
    dumpStack()
    raise


			