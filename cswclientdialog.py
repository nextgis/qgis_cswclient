# -*- coding: utf-8 -*-

#******************************************************************************
#
# CSW Client
# ---------------------------------------------------------
# QGIS Catalogue Service client.
#
# Copyright (C) 2010 Alexander Bruy (alexander.bruy@gmail.com)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/copyleft/gpl.html>. You can also obtain it by writing
# to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.
#
#******************************************************************************

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *

from qgis.core import *
from qgis.gui import *

import sys, os.path

from urllib2 import HTTPError
from xml.parsers.expat import ExpatError

# Set up current path, so that we know where to look for modules
sys.path.append( os.path.abspath( os.path.dirname( __file__ ) ) )

from owslib.csw import CatalogueServiceWeb as csw

import cswclient_utils as utils

from cswsearchdialog import CSWSearchDialog
from cswresponsedialog import CSWResponseDialog
from newcswconnectiondialog import NewCSWConnectionDialog
from managecswconnectionsdialog import ManageCSWConnectionsDialog

from cswclientdialogbase import Ui_CSWClientDialog

class CSWClientDialog( QDialog, Ui_CSWClientDialog ):
  def __init__( self, iface ):
    QDialog.__init__( self )
    self.setupUi( self )

    self.iface = iface
    self.catalog = None

    QObject.connect( self.cmbConnections, SIGNAL( "activated( int )" ), self.saveSelection )

    QObject.connect( self.btnSearch, SIGNAL( "clicked()" ), self.searchServer )
    QObject.connect( self.btnSrvInfo, SIGNAL( "clicked()" ), self.serverInfo )
    QObject.connect( self.btnDefault, SIGNAL( "clicked()" ), self.addDefaultServers )
    QObject.connect( self.btnShowCapabilities, SIGNAL( "clicked()" ), self.showCapabilities )

    QObject.connect( self.btnNew, SIGNAL( "clicked()" ), self.newServer )
    QObject.connect( self.btnEdit, SIGNAL( "clicked()" ), self.editServer )
    QObject.connect( self.btnDelete, SIGNAL( "clicked()" ), self.deleteServer )
    QObject.connect( self.btnLoad, SIGNAL( "clicked()" ), self.loadServers )
    QObject.connect( self.btnSave, SIGNAL( "clicked()" ), self.saveServers )

    self.manageGui()

  def manageGui( self ):
    self.populateConnectionList()

    self.btnShowCapabilities.setEnabled( False )

  def populateConnectionList( self ):
    settings = QSettings()

    settings.beginGroup( "/CSWClient/" )
    self.cmbConnections.clear()
    self.cmbConnections.addItems( settings.childGroups() )
    settings.endGroup()

    self.setConnectionListPosition()

    if self.cmbConnections.count() == 0:
      # no connections - disable various buttons
      self.btnSrvInfo.setEnabled( False )
      self.btnEdit.setEnabled( False )
      self.btnDelete.setEnabled( False )
      self.btnSave.setEnabled( False )
    else:
      # connections - enable various buttons
      self.btnSrvInfo.setEnabled( True )
      self.btnEdit.setEnabled( True )
      self.btnDelete.setEnabled( True )

  def setConnectionListPosition( self ):
    settings = QSettings()
    toSelect = settings.value( "/CSWClient/selected", QVariant("") ).toString()

    # does toSelect exist in cmbConnections?
    exists = False
    for i in range( self.cmbConnections.count() ):
      if self.cmbConnections.itemText( i ) == toSelect:
        self.cmbConnections.setCurrentIndex( i )
        exists = True
        break

    # If we couldn't find the stored item, but there are some, default
    # to the last item (this makes some sense when deleting items as it
    # allows the user to repeatidly click on delete to remove a whole
    # lot of items)
    if not exists and self.cmbConnections.count() > 0:
      # If toSelect is null, then the selected connection wasn't found
      # by QSettings, which probably means that this is the first time
      # the user has used qgis with database connections, so default to
      # the first in the list of connetions. Otherwise default to the last.
      if toSelect.isEmpty():
        self.cmbConnections.setCurrentIndex( 0 )
      else:
        self.cmbConnections.setCurrentIndex( self.cmbConnections.count() - 1 )

  def saveSelection( self ):
    settings = QSettings()
    settings.setValue( "/CSWClient/selected", self.cmbConnections.currentText() )

  def serverInfo( self ):
    settings = QSettings()
    key = "/CSWClient/" + self.cmbConnections.currentText()
    url = str( settings.value( key + "/url" ).toString() )

    # TODO: setup proxy server

    try:
      QApplication.setOverrideCursor( QCursor( Qt.WaitCursor ) )
      self.catalog = csw( url )
    except (HTTPError, AttributeError, ExpatError ):
      QApplication.restoreOverrideCursor()
      print "CSWClient unexpected error:", sys.exc_info()[ 0 ], sys.exc_info()[ 1 ], sys.exc_info()[ 2 ]
      QMessageBox.warning( self, self.tr( "Connection error" ),
                           self.tr( "Error connecting to server %1:\n%2" )
                           .arg( self.cmbConnections.currentText() )
                           .arg( str( sys.exc_info()[ 1 ] ) ) )
      return

    QApplication.restoreOverrideCursor()

    if self.catalog.exceptionreport:
      print self.catalog.exceptionreport.exceptions
      QMessageBox.warning( self, self.tr( "Connection error" ),
                           self.tr( "Error connecting to server %1:\n%2: %3" )
                           .arg( self.cmbConnections.currentText() )
                           .arg( self.catalog.exceptionreport.exceptions[ 0 ][ "exceptionCode" ])
                           .arg( self.catalog.exceptionreport.exceptions[ 0 ][ "ExceptionText" ] ) )


    if self.catalog:
      self.btnShowCapabilities.setEnabled( True )
      self.btnSearch.setEnabled( True )

      metadata = utils.serverMetadata( self.catalog )
      self.textCapabilities.setText( metadata )

  def newServer( self ):
    dlgNew = NewCSWConnectionDialog()
    dlgNew.setWindowTitle( self.tr( "New CSW server" ) )
    if dlgNew.exec_() == QDialog.Accepted:
      self.populateConnectionList()

  def editServer( self ):
    settings = QSettings()
    url = settings.value( "/CSWClient/" + self.cmbConnections.currentText() + "/url" ).toString()

    dlgEdit = NewCSWConnectionDialog( self.cmbConnections.currentText() )
    dlgEdit.setWindowTitle( self.tr( "Edit CSW server" ) )
    dlgEdit.leName.setText( self.cmbConnections.currentText() )
    dlgEdit.leURL.setText( url )
    if dlgEdit.exec_() == QDialog.Accepted:
      self.populateConnectionList()

  def deleteServer( self ):
    settings = QSettings()
    key = "/CSWClient/" + self.cmbConnections.currentText()
    msg = self.tr( "Are you sure you want to remove the %1 connection and all associated settings?" ).arg( self.cmbConnections.currentText() )
    result = QMessageBox.information( self, self.tr( "Confirm delete" ), msg, QMessageBox.Ok | QMessageBox.Cancel )
    if result == QMessageBox.Ok:
      settings.remove( key )
      self.cmbConnections.removeItem( self.cmbConnections.currentIndex() )
      self.setConnectionListPosition()

  def loadServers( self ):
    dlg = ManageCSWConnectionsDialog( 1 )
    dlg.exec_()
    self.populateConnectionList()

  def saveServers( self ):
    dlg = ManageCSWConnectionsDialog( 0 )
    dlg.exec_()

  def addDefaultServers( self ):
    filePath = QDir.toNativeSeparators( os.path.join( currentPath, "default.xml" ) )
    file = QFile( filePath )
    if not file.open( QIODevice.ReadOnly | QIODevice.Text ):
      QMessageBox.warning( self, self.tr( "Loading connections" ),
                           self.tr( "Cannot read file with default connections:\n%1." )
                           .arg( file.errorString() ) )
      return

    doc = QDomDocument( "connections" )
    errorStr = QString()
    errorLine = 0
    errorColumn = 0

    ( success, errorStr, errorLine, errorColumn ) = doc.setContent( file, True )
    if not success:
      QMessageBox.warning( self, self.tr( "Loading connections" ),
                           self.tr( "Parse error at line %1, column %2:\n%3" )
                           .arg( errorLine )
                           .arg( errorColumn )
                           .arg( errorStr ) )
      return

    root = doc.documentElement()
    if root.tagName() != "qgsCSWConnections":
      QMessageBox.information( self, self.tr( "Loading connections" ),
                               self.tr( "The file is not an CSW connections exchange file." ) )
      return

    settings = QSettings()
    settings.beginGroup( "/CSWClient/" )
    keys = settings.childGroups()
    settings.endGroup()

    child = root.firstChildElement()
    while not child.isNull():
      connectionName = child.attribute( "name" )
      # check for duplicates
      if keys.contains( connectionName ):
        res = QMessageBox.warning( self, self.tr( "Loading connections" ),
                                   self.tr( "Connection with name %1 already exists. Overwrite?" )
                                   .arg( connectionName ),
                                   QMessageBox.Yes | QMessageBox.No )
        if res != QMessageBox.Yes:
          child = child.nextSiblingElement()
          continue

      # no dups detected or overwrite is allowed
      key = "/CSWClient/" + connectionName
      settings.setValue( key + "/url", child.attribute( "url" ) )
      child = child.nextSiblingElement()

    self.populateConnectionList()
    QMessageBox.information( self, self.tr( "CSW servers" ),
                             self.tr( "Several CSW servers have been added to the server list." ) )

  def showCapabilities( self ):
    dlg = CSWResponseDialog()
    dlg.textXML.setText( self.catalog.response )
    dlg.exec_()

  def searchServer( self ):
    settings = QSettings()
    url = settings.value( "/CSWClient/" + self.cmbConnections.currentText() + "/url" ).toString()

    dlgSearch = CSWSearchDialog( self.iface, url )
    dlgSearch.exec_()
