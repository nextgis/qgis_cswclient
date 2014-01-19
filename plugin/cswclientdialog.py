# -*- coding: utf-8 -*-

#******************************************************************************
#
# CSW Client
# ---------------------------------------------------------
# QGIS Catalogue Service client.
#
# Copyright (C) 2010 NextGIS (http://nextgis.org),
#                    Alexander Bruy (alexander.bruy@gmail.com),
#                    Maxim Dubinin (sim@gis-lab.info)
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

import sys, os.path, urllib2

from xml.parsers.expat import ExpatError

# Set up current path, so that we know where to look for modules
currentPath = os.path.abspath( os.path.dirname( __file__ ) )
#sys.path.append( os.path.abspath( os.path.dirname( __file__ ) ) )\
sys.path.insert( 0, currentPath )

from owslib.csw import CatalogueServiceWeb as csw

import cswclient_utils as utils

from cswresponsedialog import CSWResponseDialog
from newcswconnectiondialog import NewCSWConnectionDialog
from managecswconnectionsdialog import ManageCSWConnectionsDialog
from xmlhighlighter import XmlHighlighter

from ui.ui_cswclientdialogbase import Ui_CSWClientDialog

class CSWClientDialog( QDialog, Ui_CSWClientDialog ):
  def __init__( self, iface ):
    QDialog.__init__( self )
    self.setupUi( self )

    self.iface = iface
    self.catalog = None
    self.catalogUrl = None

    # Servers tab
    QObject.connect( self.cmbConnections, SIGNAL( "activated( int )" ), self.saveSelection )

    QObject.connect( self.btnServerInfo, SIGNAL( "clicked()" ), self.serverInfo )
    QObject.connect( self.btnAddDefault, SIGNAL( "clicked()" ), self.addDefaultServers )
    QObject.connect( self.btnCapabilities, SIGNAL( "clicked()" ), self.showServerResponse )

    # server management buttons
    QObject.connect( self.btnNew, SIGNAL( "clicked()" ), self.newServer )
    QObject.connect( self.btnEdit, SIGNAL( "clicked()" ), self.editServer )
    QObject.connect( self.btnDelete, SIGNAL( "clicked()" ), self.deleteServer )
    QObject.connect( self.btnLoad, SIGNAL( "clicked()" ), self.loadServers )
    QObject.connect( self.btnSave, SIGNAL( "clicked()" ), self.saveServers )

    # Search tab
    QObject.connect( self.treeRecords, SIGNAL( "itemSelectionChanged()" ), self.recordClicked )

    QObject.connect( self.btnSearch, SIGNAL( "clicked()" ), self.startSearch )
    QObject.connect( self.btnCanvasBbox, SIGNAL( "clicked()" ), self.setCanvasBbox )
    QObject.connect( self.btnGlobalBbox, SIGNAL( "clicked()" ), self.setGlobalBbox )

    # navigation buttons
    QObject.connect( self.btnFirst, SIGNAL( "clicked()" ), self.navigate )
    QObject.connect( self.btnPrev, SIGNAL( "clicked()" ), self.navigate )
    QObject.connect( self.btnNext, SIGNAL( "clicked()" ), self.navigate )
    QObject.connect( self.btnLast, SIGNAL( "clicked()" ), self.navigate )

    QObject.connect( self.btnAddToWms, SIGNAL( "clicked()" ), self.addToWms )
    QObject.connect( self.btnOpenUrl, SIGNAL( "clicked()" ), self.openUrl )
    QObject.connect( self.btnMetadata, SIGNAL( "clicked()" ), self.showMetadata )
    QObject.connect( self.btnShowXml, SIGNAL( "clicked()" ), self.showServerResponse )

    self.manageGui()

  def manageGui( self ):
    self.tabWidget.setCurrentIndex( 0 )

    self.populateConnectionList()
    self.btnCapabilities.setEnabled( False )

    settings = QSettings()
    self.spnRecords.setValue( settings.value( "/CSWClient/returnRecords", QVariant("10") ).toInt()[ 0 ] )

    key = "/CSWClient/" + self.cmbConnections.currentText()
    self.catalogUrl = str( settings.value( key + "/url" ).toString() )

    self.setCanvasBbox()

    self.btnAddToWms.setEnabled( False )
    self.btnOpenUrl.setEnabled( False )
    self.btnMetadata.setEnabled( False )
    self.btnShowXml.setEnabled( False )

    self.btnFirst.setEnabled( False )
    self.btnPrev.setEnabled( False )
    self.btnNext.setEnabled( False )
    self.btnLast.setEnabled( False )

  def populateConnectionList( self ):
    settings = QSettings()

    settings.beginGroup( "/CSWClient/" )
    self.cmbConnections.clear()
    self.cmbConnections.addItems( settings.childGroups() )
    settings.endGroup()

    self.setConnectionListPosition()

    if self.cmbConnections.count() == 0:
      # no connections - disable various buttons
      self.btnServerInfo.setEnabled( False )
      self.btnEdit.setEnabled( False )
      self.btnDelete.setEnabled( False )
      self.btnSave.setEnabled( False )
      self.tabWidget.setTabEnabled( 1, False )
    else:
      # connections - enable various buttons
      self.btnServerInfo.setEnabled( True )
      self.btnEdit.setEnabled( True )
      self.btnDelete.setEnabled( True )
      self.tabWidget.setTabEnabled( 1, True )

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
      # the user has used CSWClient, so default to the first in the list
      # of connetions. Otherwise default to the last.
      if toSelect.isEmpty():
        self.cmbConnections.setCurrentIndex( 0 )
      else:
        self.cmbConnections.setCurrentIndex( self.cmbConnections.count() - 1 )

  def saveSelection( self ):
    settings = QSettings()
    settings.setValue( "/CSWClient/selected", self.cmbConnections.currentText() )
    key = "/CSWClient/" + self.cmbConnections.currentText()
    self.catalogUrl = str( settings.value( key + "/url" ).toString() )
    # clear server metadata
    self.textMetadata.clear()

  def serverInfo( self ):
    settings = QSettings()
    key = "/CSWClient/" + self.cmbConnections.currentText()
    self.catalogUrl = str( settings.value( key + "/url" ).toString() )

    try:
      QApplication.setOverrideCursor( QCursor( Qt.WaitCursor ) )
      self.catalog = csw( self.catalogUrl )
      QApplication.restoreOverrideCursor()
    except urllib2.HTTPError:
      QApplication.restoreOverrideCursor()
      print "CSWClient HTTP error:", sys.exc_info()[ 0 ], sys.exc_info()[ 1 ], sys.exc_info()[ 2 ]
      QMessageBox.warning( self, self.tr( "Connection error" ),
                           self.tr( "Error connecting to server %1:\n%2" )
                           .arg( self.cmbConnections.currentText() )
                           .arg( str( sys.exc_info()[ 1 ] ) ) )
      return
    except ExpatError:
      QApplication.restoreOverrideCursor()
      print "CSWClient parse error:", sys.exc_info()[ 0 ], sys.exc_info()[ 1 ], sys.exc_info()[ 2 ]
      QMessageBox.warning( self, self.tr( "Parse error" ),
                           self.tr( "Error parsing server response:\n%1" )
                           .arg( str( sys.exc_info()[ 1 ] ) ) )
      return
    except:
      QApplication.restoreOverrideCursor()
      print "CSWClient unexpected error:", sys.exc_info()[ 0 ], sys.exc_info()[ 1 ], sys.exc_info()[ 2 ]
      QMessageBox.warning( self, self.tr( "Error" ),
                           self.tr( "Error connecting to server %1:\n%2" )
                           .arg( self.cmbConnections.currentText() )
                           .arg( str( sys.exc_info()[ 1 ] ) ) )
      return

    if self.catalog.exceptionreport:
      print self.catalog.exceptionreport.exceptions
      QMessageBox.warning( self, self.tr( "Connection error" ),
                           self.tr( "Error connecting to server %1:\n%2: %3" )
                           .arg( self.cmbConnections.currentText() )
                           .arg( self.catalog.exceptionreport.exceptions[ 0 ][ "exceptionCode" ])
                           .arg( self.catalog.exceptionreport.exceptions[ 0 ][ "ExceptionText" ] ) )
      return

    if self.catalog:
      self.btnCapabilities.setEnabled( True )

      metadata = utils.serverMetadata( self.catalog )
      myStyle = QgsApplication.reportStyleSheet()
      self.textMetadata.clear()
      self.textMetadata.document().setDefaultStyleSheet( myStyle )
      self.textMetadata.setHtml( metadata )

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

# ************* Search tab *********************************************

  def setCanvasBbox( self ):
    extent = self.iface.mapCanvas().extent()
    self.leNorth.setText( str( extent.yMaximum() ) )
    self.leSouth.setText( str( extent.yMinimum() ) )
    self.leWest.setText( str( extent.xMinimum() ) )
    self.leEast.setText( str( extent.xMaximum() ) )

  def setGlobalBbox( self ):
    self.leNorth.setText( "90" )
    self.leSouth.setText( "-90" )
    self.leWest.setText( "-180" )
    self.leEast.setText( "180" )

  def startSearch( self ):
    self.catalog = None
    self.bbox = None
    self.keywords = None

    # clear all fields and disable buttons
    self.lblResults.setText( self.tr( "" ) )
    self.treeRecords.clear()
    self.textAbstract.clear()
    self.leDataUrl.clear()

    self.btnAddToWms.setEnabled( False )
    self.btnOpenUrl.setEnabled( False )
    self.btnMetadata.setEnabled( False )
    self.btnShowXml.setEnabled( False )

    self.btnFirst.setEnabled( False )
    self.btnPrev.setEnabled( False )
    self.btnNext.setEnabled( False )
    self.btnLast.setEnabled( False )

    # save some settings
    settings = QSettings()
    settings.setValue( "/CSWClient/returnRecords", self.spnRecords.cleanText() )

    # start position and number of records to return
    self.startFrom = 0
    self.maxRecords = self.spnRecords.value()

    # bbox
    minX = self.leWest.text()
    minY = self.leSouth.text()
    maxX = self.leEast.text()
    maxY = self.leNorth.text()
    self.bbox = [ minX, minY, maxX, maxY ]

    # keywords
    if self.leKeywords.text().isEmpty():
      self.keywords = []
    else:
      self.keywords = self.leKeywords.text().split( "," )

    # build request
    try:
      QApplication.setOverrideCursor( QCursor( Qt.WaitCursor ) )
      self.catalog = csw( self.catalogUrl )
    except urllib2.HTTPError:
      QApplication.restoreOverrideCursor()
      print "CSWClient HTTP error:", sys.exc_info()[ 0 ], sys.exc_info()[ 1 ], sys.exc_info()[ 2 ]
      QMessageBox.warning( self, self.tr( "Connection error" ),
                           self.tr( "Error connecting to server:\n%1" )
                           .arg( str( sys.exc_info()[ 1 ] ) ) )
      return
    except ExpatError:
      QApplication.restoreOverrideCursor()
      print "CSWClient parse error:", sys.exc_info()[ 0 ], sys.exc_info()[ 1 ], sys.exc_info()[ 2 ]
      QMessageBox.warning( self, self.tr( "Parse error" ),
                           self.tr( "Error parsing server response:\n%1" )
                           .arg( str( sys.exc_info()[ 1 ] ) ) )
      return
    except:
      QApplication.restoreOverrideCursor()
      print "CSWClient unexpected error:", sys.exc_info()[ 0 ], sys.exc_info()[ 1 ], sys.exc_info()[ 2 ]
      QMessageBox.warning( self, self.tr( "Error" ),
                           self.tr( "Error connecting to server:\n%1" )
                           .arg( str( sys.exc_info()[ 1 ] ) ) )
      return

    # TODO: allow users to select resources types to find. qtype = "service", "dataset"...
    try:
      self.catalog.getrecords( qtype = None, keywords = self.keywords, bbox = self.bbox, sortby = None, maxrecords = self.maxRecords )
    except:
      QApplication.restoreOverrideCursor()
      print "CSWClient unexpected error:", sys.exc_info()[ 0 ], sys.exc_info()[ 1 ], sys.exc_info()[ 2 ]
      QMessageBox.warning( self, self.tr( "GetRecords error" ),
                           self.tr( "Error getting server response:\n%1" )
                           .arg( str( sys.exc_info()[ 1 ] ) ) )
      return

    QApplication.restoreOverrideCursor()

    if self.catalog.exceptionreport:
      print self.catalog.exceptionreport.exceptions
      QMessageBox.warning( self, self.tr( "Error" ),
                           self.tr( "CSW exception %1:\n%2" )
                           .arg( self.catalog.exceptionreport.exceptions[ 0 ][ "exceptionCode" ])
                           .arg( self.catalog.exceptionreport.exceptions[ 0 ][ "ExceptionText" ] ) )
      return

    if not self.catalog.results:
      print "There are no results"
      QMessageBox.information( self, self.tr( "Search" ),
                               self.tr( "There are no records in server response." ) )
      return

    if self.catalog.results[ "matches" ] == 0:
      QMessageBox.information( self, self.tr( "Search" ),
                               self.tr( "There are no records matching your criteria." ) )
      self.lblResults.setText( self.tr( "Nothing found" ) )
      return

    self.displayResults()

#    if self.catalog.results[ "matches" ] < self.maxRecords:
#      self.btnFirst.setEnabled( False )
#      self.btnPrev.setEnabled( False )
#      self.btnNext.setEnabled( False )
#      self.btnLast.setEnabled( False )

  def displayResults( self ):
    self.treeRecords.clear()
    self.leDataUrl.clear()

    position = self.catalog.results[ "returned" ] + self.startFrom

    self.lblResults.setText( self.tr( "Show: %1 from %2" )
                             .arg( position )
                             .arg( self.catalog.results[ "matches" ] ) )

    for rec in self.catalog.records:
      item = QTreeWidgetItem( self.treeRecords )
      if self.catalog.records[ rec ].type:
        item.setText( 0, self.catalog.records[ rec ].type )
      else:
        item.setText( 0, "unknow" )
      if self.catalog.records[ rec ].title:
        item.setText( 1, self.catalog.records[ rec ].title )
      if self.catalog.records[ rec ].identifier:
        item.setText( 2, self.catalog.records[ rec ].identifier )

      #if self.catalog.records[ rec ].identifiers and len ( self.catalog.records[ rec ].identifiers ) > 1:
      #  for id in self.catalog.records[ rec ].identifiers:
      #    if id.sheme == "urn:x-esri:specification:ServiceType:ArcIMS:Metadata:DocID":
      #      item.setText( 2, id.identifier )
      #else:
      #  item.setText( 2, self.catalog.records[ rec ].identifier )

    self.btnShowXml.setEnabled( True )

    if self.catalog.results[ "matches" ] < self.maxRecords:
      self.btnFirst.setEnabled( False )
      self.btnPrev.setEnabled( False )
      self.btnNext.setEnabled( False )
      self.btnLast.setEnabled( False )
    else:
      self.btnFirst.setEnabled( True )
      self.btnPrev.setEnabled( True )
      self.btnNext.setEnabled( True )
      self.btnLast.setEnabled( True )

  def recordClicked( self ):
    # disable previosly enabled buttons
    self.btnAddToWms.setEnabled( False )
    self.btnOpenUrl.setEnabled( False )
    self.btnMetadata.setEnabled( True )

    # clear URL
    self.leDataUrl.clear()

    if not self.treeRecords.selectedItems():
      return

    item = self.treeRecords.currentItem()
    if not item:
      return

    recordId = str( item.text( 2 ) )
    abstract = self.catalog.records[ recordId ].abstract
    if abstract:
      self.textAbstract.setText( QString( abstract ).simplified() )
    else:
      self.textAbstract.setText( self.tr( "There is no abstract for this record" ) )

    if item.text( 0 ) == "liveData" or item.text( 0 ) == "downloadableData":
      #dataUrl = self.extractUrl( self.catalog.response, item.text( 2 ) )
      dataUrl = utils.extractUrl( self, self.catalog.response, item.text( 2 ) )
      #print "DATA URL", dataUrl
      if not dataUrl.isEmpty():
        self.leDataUrl.setText( dataUrl )
        if item.text( 0 ) == "liveData":
          self.btnAddToWms.setEnabled( True )
        elif item.text( 0 ) == "downloadableData":
          self.btnOpenUrl.setEnabled( True )

  def navigate( self ):
    senderName = self.sender().objectName()
    if senderName == "btnFirst":
      self.startFrom = 0
    elif senderName == "btnLast":
      self.startFrom = self.catalog.results[ "matches" ] - self.maxRecords
    elif senderName == "btnNext":
      self.startFrom += self.maxRecords
      if self.startFrom >= self.catalog.results[ "matches" ]:
        res = QMessageBox.information( self, self.tr( "Navigation" ),
                                       self.tr( "This is a last page. Go to the first page?" ),
                                       QMessageBox.Ok | QMessageBox.Cancel )
        if res == QMessageBox.Ok:
          self.startFrom = 0
        else:
          return
    elif senderName == "btnPrev":
      self.startFrom -= self.maxRecords
      if self.startFrom <= 0:
        res = QMessageBox.information( self, self.tr( "Navigation" ),
                                       self.tr( "This is a first page. Go to the last page?" ),
                                       QMessageBox.Ok | QMessageBox.Cancel )
        if res == QMessageBox.Ok:
          self.startFrom = self.catalog.results[ "matches" ] - self.maxRecords
        else:
          return

    QApplication.setOverrideCursor( QCursor( Qt.WaitCursor ) )

    self.catalog.getrecords( qtype = None, keywords = self.keywords, bbox = self.bbox,
                             sortby = None, maxrecords = self.maxRecords,
                             startposition = self.startFrom )

    QApplication.restoreOverrideCursor()

    self.displayResults()

  def openUrl( self ):
    QDesktopServices.openUrl( QUrl( self.leDataUrl.text(), QUrl.TolerantMode ) )

  def addToWms( self ):
    url = QUrl( self.leDataUrl.text(), QUrl.TolerantMode )
    dataUrl = str( url.toString( QUrl.RemoveQuery ) )
    #print "Trimmed URL", dataUrl

    # test if URL is valid WMS server
    from owslib.wms import WebMapService

    try:
      QApplication.setOverrideCursor( QCursor( Qt.WaitCursor ) )
      wms = WebMapService( dataUrl )
    except urllib2.HTTPError:
      QApplication.restoreOverrideCursor()
      print "CSWClient HTTP error:", sys.exc_info()[ 0 ], sys.exc_info()[ 1 ], sys.exc_info()[ 2 ]
      QMessageBox.warning( self, self.tr( "Connection error" ),
                           self.tr( "Error connecting to server:\n%1" )
                           .arg( str( sys.exc_info()[ 1 ] ) ) )
      return
    except ExpatError:
      QApplication.restoreOverrideCursor()
      print "CSWClient parse error:", sys.exc_info()[ 0 ], sys.exc_info()[ 1 ], sys.exc_info()[ 2 ]
      QMessageBox.warning( self, self.tr( "Parsing error" ),
                           self.tr( "Error parsing server response:\n%1\n\n%2" )
                           .arg( str( sys.exc_info()[ 1 ] ) )
                           .arg( self.tr( "May be URL is not valid or there is no WMS service on this server." ) ) )
      return
    except:
      QApplication.restoreOverrideCursor()
      print "CSWClient unknow error:", sys.exc_info()[ 0 ], sys.exc_info()[ 1 ], sys.exc_info()[ 2 ]
      QMessageBox.warning( self, self.tr( "Error" ),
                           self.tr( "Error:\n%1" )
                           .arg( str( sys.exc_info()[ 1 ] ) ) )
      return

    QApplication.restoreOverrideCursor()

#    dlgNew = NewCSWConnectionDialog()
#    dlgNew.setWindowTitle( self.tr( "New CSW server" ) )
#    if dlgNew.exec_() == QDialog.Accepted:
#      self.populateConnectionList()

    serverName, isOk = QInputDialog.getText( self, self.tr( "Enter name for WMS server" ),
                                             self.tr( "Server name" ) )

    # store connection
    if isOk and not serverName.isEmpty():
      # check if there is a connection with same name
      settings = QSettings()
      settings.beginGroup( "/Qgis/connections-wms" );
      keys = settings.childGroups();
      settings.endGroup();

      # check for duplicates
      if keys.contains( serverName ):
        res = QMessageBox.warning( self, self.tr( "Saving server" ),
                                   self.tr( "Connection with name %1 already exists. Overwrite?" )
                                   .arg( connectionName ),
                                   QMessageBox.Yes | QMessageBox.No )
        if res != QMessageBox.Yes:
          return

      # no dups detected or overwrite is allowed
      settings.beginGroup( "/Qgis/connections-wms" )
      settings.setValue( "/" + serverName + "/url", dataUrl )
      settings.endGroup()

  def showMetadata( self ):
    if not self.treeRecords.selectedItems():
      return

    item = self.treeRecords.currentItem()
    if not item:
      return

    recordId = str( item.text( 2 ) )

    try:
      QApplication.setOverrideCursor( QCursor( Qt.WaitCursor ) )
      cat = csw( self.catalogUrl )
    except urllib2.HTTPError:
      QApplication.restoreOverrideCursor()
      print "CSWClient HTTP error:", sys.exc_info()[ 0 ], sys.exc_info()[ 1 ], sys.exc_info()[ 2 ]
      QMessageBox.warning( self, self.tr( "Connection error" ),
                           self.tr( "Error connecting to server:\n%1" )
                           .arg( str( sys.exc_info()[ 1 ] ) ) )
      return
    except ExpatError:
      QApplication.restoreOverrideCursor()
      print "CSWClient parse error:", sys.exc_info()[ 0 ], sys.exc_info()[ 1 ], sys.exc_info()[ 2 ]
      QMessageBox.warning( self, self.tr( "Parse error" ),
                           self.tr( "Error parsing server response:\n%1" )
                           .arg( str( sys.exc_info()[ 1 ] ) ) )
      return
    except:
      QApplication.restoreOverrideCursor()
      print "CSWClient unexpected error:", sys.exc_info()[ 0 ], sys.exc_info()[ 1 ], sys.exc_info()[ 2 ]
      QMessageBox.warning( self, self.tr( "Error" ),
                           self.tr( "Error connecting to server:\n%1" )
                           .arg( str( sys.exc_info()[ 1 ] ) ) )
      return

    try:
      cat.getrecordbyid( [ self.catalog.records[ recordId ].identifier ] )
    except:
      QApplication.restoreOverrideCursor()
      print "CSWClient unexpected error:", sys.exc_info()[ 0 ], sys.exc_info()[ 1 ], sys.exc_info()[ 2 ]
      QMessageBox.warning( self, self.tr( "GetRecords error" ),
                           self.tr( "Error getting server response:\n%1" )
                           .arg( str( sys.exc_info()[ 1 ] ) ) )
      return

    QApplication.restoreOverrideCursor()

    if cat.exceptionreport:
      print cat.exceptionreport.exceptions
      QMessageBox.warning( self, self.tr( "Metadata request error" ),
                           self.tr( "Can't get metadata for record %1:\n%2: %3" )
                           .arg( recordId )
                           .arg( cat.exceptionreport.exceptions[ 0 ][ "exceptionCode" ])
                           .arg( cat.exceptionreport.exceptions[ 0 ][ "ExceptionText" ] ) )
      return

    metadata = utils.recordMetadata( cat.records[ recordId ] )

    myStyle = QgsApplication.reportStyleSheet()
    dlg = CSWResponseDialog()
    dlg.textXml.document().setDefaultStyleSheet( myStyle )
    dlg.textXml.setHtml( metadata )
    dlg.exec_()

# ************* Common stuff *******************************************

  def setupProxy( self ):
    # if there is proxy server in QGIS settings - use it
    settings.beginGroup( "proxy" )
    if settings.value( "/proxyEnabled" ).toBool():
      proxyType = settings.value( "/proxyType", QVariant( 0 ) ).toString()
      if proxyType == "HttpProxy":
        proxyHost = settings.value( "/proxyHost" ).toString()
        proxyPost = settings.value( "/proxyPort" ).toUInt()[ 0 ]
        proxyUser = settings.value( "/proxyUser" ).toString()
        proxyPass = settings.value( "/proxyPassword" ).toString()

        # setup urllib2 proxy handler
        connectionString = "http://%s:%s@%s:%s" % ( proxyUser, proxyPass,
                                                    proxyHost, proxyPort )
        #authHandler = urllib2.ProxyBasicAuthHandler()
        #authHandler.add_password( None, None, user, password )
        proxyHandler = urllib2.ProxyHandler( { "http" : connectionString } )
        opener = urllib2.build_opener( proxyHandler )
        urllib2.install_opener( opener )
    settings.endGroup()

  def showServerResponse( self ):
    dlg = CSWResponseDialog()
    highlighter = XmlHighlighter( dlg.textXml )
    dlg.textXml.setText( self.catalog.response )
    dlg.exec_()

  def extractUrl( self, response, id ):
    doc = QDomDocument()
    errorStr = QString()
    errorLine = 0
    errorColumn = 0

    ( success, errorStr, errorLine, errorColumn ) = doc.setContent( response, True )
    if not success:
      QMessageBox.warning( self, self.tr( "Parsing error" ),
                           self.tr( "Parse error at line %1, column %2:\n%3" )
                           .arg( errorLine )
                           .arg( errorColumn )
                           .arg( errorStr ) )
      return

    root = doc.documentElement().firstChildElement( "SearchResults" )
    child = root.firstChildElement( "Record" )
    found = False
    while not child.isNull() and not found:
      elem = child.firstChildElement()
      while not elem.isNull():
        e = elem.toElement()
        if e.tagName() == "identifier" and e.attribute( "scheme" ).endsWith( "DocID" ) and e.text() == id:
          print "ID", e.text()
          found = True
          break
        elem = elem.nextSiblingElement()

      if not found:
        child = child.nextSiblingElement()

    # now in child we have selected record and can extract URL
    found = False
    elem = child.firstChildElement()
    while not elem.isNull():
      e = elem.toElement()
      if e.tagName() == "identifier" and e.attribute( "scheme" ).endsWith( "DocID" ):
        print "ID after search", e.text()
      if e.tagName() == "references" and e.attribute( "scheme" ).endsWith( "Onlink" ):
        found = True
        print "URL", e.text()
        break
      elem = elem.nextSiblingElement()

    if found:
      return e.text()

    return QString()
