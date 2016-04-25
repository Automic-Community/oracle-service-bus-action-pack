#!/usr/bin/python
# -*- coding: utf-8 -*-
import wlstModule
from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.config import Ref
from java.io import FileInputStream

import sys

try:

    username = sys.argv[1]
    password = sys.argv[2]
    url = sys.argv[3]
    sessionName = sys.argv[4]
    jarfilepath = sys.argv[5]
    print "================================================================================"
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

    alsbSession = findService(ALSBConfigurationMBean.NAME + '.'
                              + sessionName,
                              ALSBConfigurationMBean.TYPE)

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
    result = alsbSession.importUploaded(importPlan)

    # Print out status and build a list of created references.

    if result.getFailed().isEmpty() == false:
        print 'One or more resources could not be imported properly'
        raise
    else:
        print 'The following resources have been imported: '
        for successEntry in result.getImported():
            print '-- %s' % successEntry.toString()
except:

    print 'Unexpected error while importing resource : ', \
        sys.exc_info()[0]
    dumpStack()
    raise


			