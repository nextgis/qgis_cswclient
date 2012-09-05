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

import sys, os.path

from urllib2 import HTTPError
from xml.parsers.expat import ExpatError

# Set up current path, so that we know where to look for modules
#sys.path.append( os.path.abspath( os.path.dirname( __file__ ) ) )
sys.path.insert( 0, os.path.abspath( os.path.dirname( __file__ ) ) )

from owslib.csw import CatalogueServiceWeb as csw

import cswclient_utils as utils

from cswresponsedialog import CSWResponseDialog

from ui_cswsearchdialogbase import Ui_CSWSearchDialog

class CSWSearchDialog( QDialog, Ui_CSWSearchDialog ):
  def __init__( self, iface, url ):
    QDialog.__init__( self )
    self.setupUi( self )

    self.iface = iface
    self.catalogUrl = str( url )
    self.catalog = None

    QObject.connect( self.treeRecords, SIGNAL( "itemSelectionChanged()" ), self.recordClicked )

    QObject.connect( self.btnSearch, SIGNAL( "clicked()" ), self.startSearch )
    QObject.connect( self.btnCanvasBbox, SIGNAL( "clicked()" ), self.setBboxFromCanvas )
    QObject.connect( self.btnDefaultBbox, SIGNAL( "clicked()" ), self.setDefaultBbox )
    QObject.connect( self.btnAddToMap, SIGNAL( "clicked()" ), self.addDataToCanvas )
    QObject.connect( self.btnDownload, SIGNAL( "clicked()" ), self.downloadData )
    QObject.connect( self.btnMetadata, SIGNAL( "clicked()" ), self.showMetadata )
    QObject.connect( self.btnShowXML, SIGNAL( "clicked()" ), self.showResponse )

    # navigation buttons
    QObject.connect( self.btnFirst, SIGNAL( "clicked()" ), self.navigate )
    QObject.connect( self.btnPrev, SIGNAL( "clicked()" ), self.navigate )
    QObject.connect( self.btnNext, SIGNAL( "clicked()" ), self.navigate )
    QObject.connect( self.btnLast, SIGNAL( "clicked()" ), self.navigate )

    self.manageGui()

  def manageGui( self ):
    settings = QSettings()
    self.spnRecords.setValue( settings.value( "/CSWClient/returnRecords", QVariant("10") ).toInt()[ 0 ] )

    self.setBboxFromCanvas()

    self.btnAddToMap.setEnabled( False )
    self.btnDownload.setEnabled( False )
    self.btnMetadata.setEnabled( False )
    self.btnShowXML.setEnabled( False )

    self.btnFirst.setEnabled( False )
    self.btnPrev.setEnabled( False )
    self.btnNext.setEnabled( False )
    self.btnLast.setEnabled( False )

  def setBboxFromCanvas( self ):
    extent = self.iface.mapCanvas().extent()
    self.leNorth.setText( str( extent.yMaximum() ) )
    self.leSouth.setText( str( extent.yMinimum() ) )
    self.leWest.setText( str( extent.xMinimum() ) )
    self.leEast.setText( str( extent.xMaximum() ) )

  def setDefaultBbox( self ):
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
    self.txtAbstract.clear()

    self.btnAddToMap.setEnabled( False )
    self.btnDownload.setEnabled( False )
    self.btnMetadata.setEnabled( False )
    self.btnShowXML.setEnabled( False )

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

    # TODO: setup proxy server ?


    # build request
    try:
      QApplication.setOverrideCursor( QCursor( Qt.WaitCursor ) )
      self.catalog = csw( self.catalogUrl )
    except HTTPError:
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

    if self.catalog.results[ "matches" ] < self.maxRecords:
      self.btnFirst.setEnabled( False )
      self.btnPrev.setEnabled( False )
      self.btnNext.setEnabled( False )
      self.btnLast.setEnabled( False )

    self.displayResults()

  def addDataToCanvas( self ):
    url = QUrl( self.leDataUrl.text(), QUrl.TolerantMode )
    dataUrl = str( url.toString( QUrl.RemoveQuery ) )
    print "Trimmed URL", dataUrl

    # test if URL is valid WMS server
    from owslib.wms import WebMapService

    try:
      QApplication.setOverrideCursor( QCursor( Qt.WaitCursor ) )
      wms = WebMapService( dataUrl )
    except HTTPError:
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
    #if wms.identification and wms.identification.type == "OGC:WMS":
      # store connection in WMS list
    QMessageBox.information( self, self.tr( "Info" ), self.tr( "Valid WMS Server" ) )
    print "Valid WMS server"
    print wms.identification.type

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

  def downloadData( self ):
    QDesktopServices.openUrl( QUrl( self.leDataUrl.text(), QUrl.TolerantMode ) )

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
    except HTTPError:
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
    dlg.textXML.document().setDefaultStyleSheet( myStyle )
    dlg.textXML.setHtml( metadata )
    dlg.exec_()

  def showResponse( self ):
    dlg = CSWResponseDialog()
    dlg.textXML.setText( self.catalog.response )
    dlg.exec_()

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
      item.setText( 1, self.catalog.records[ rec ].title )
      item.setText( 2, self.catalog.records[ rec ].identifier )

    self.btnShowXML.setEnabled( True )
    self.btnMetadata.setEnabled( True )

    self.btnFirst.setEnabled( True )
    self.btnPrev.setEnabled( True )
    self.btnNext.setEnabled( True )
    self.btnLast.setEnabled( True )

  def recordClicked( self ):
    # disable previosly enabled buttons
    self.btnAddToMap.setEnabled( False )
    self.btnDownload.setEnabled( False )

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
      self.txtAbstract.setText( QString( abstract ).simplified() )
    else:
      self.txtAbstract.setText( self.tr( "There is no abstract for this record" ) )

    if item.text( 0 ) == "liveData" or item.text( 0 ) == "downloadableData":
      dataUrl = self.extractUrl( self.catalog.response, item.text( 2 ) )
      print "DATA URL", dataUrl
      if not dataUrl.isEmpty():
        self.leDataUrl.setText( dataUrl )
        if item.text( 0 ) == "liveData":
          self.btnAddToMap.setEnabled( True )
        elif item.text( 0 ) == "downloadableData":
          self.btnDownload.setEnabled( True )

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

      child = child.nextSiblingElement()

    # now in child we have selected record and can extract URL
    found = False
    elem = child.firstChildElement()
    while not elem.isNull():
      e = elem.toElement()
      if e.tagName() == "references" and e.attribute( "scheme" ).endsWith( "Onlink" ):
        found = True
        print "URL", e.text()
        break
      elem = elem.nextSiblingElement()

    if found:
      return e.text()

    return QString()
