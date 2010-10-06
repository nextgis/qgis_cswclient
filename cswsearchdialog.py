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

from cswresponsedialog import CSWResponseDialog

from cswsearchdialogbase import Ui_CSWSearchDialog

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

    # also disable spinbox ?
    #self.spnRecords.setEnabled( False )

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

    QApplication.setOverrideCursor( QCursor( Qt.WaitCursor ) )

    # build request
    try:
      self.catalog = csw( self.catalogUrl )
    except (HTTPError, AttributeError, ExpatError ):
      QApplication.restoreOverrideCursor()
      print "CSWClient unexpected error:", sys.exc_info()[ 0 ], sys.exc_info()[ 1 ], sys.exc_info()[ 2 ]
      QMessageBox.warning( self, self.tr( "Connection error" ),
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

    if self.catalog.results[ "matches" ] == 0:
      QMessageBox.information( self, self.tr( "Search" ),
                               self.tr( "There are no records matching your criteria." ) )
      self.lblResults.setText( self.tr( "Nothing found" ) )
      # TODO: enable some controls
      return

    self.displayResults()

  def addDataToCanvas( self ):
    pass

  def downloadData( self ):
    pass

  def showMetadata( self ):
    if not self.treeRecords.selectedItems():
      return

    item = self.treeRecords.currentItem()
    if not item:
      return

    recordId = str( item.text( 2 ) )

    QApplication.setOverrideCursor( QCursor( Qt.WaitCursor ) )

    cat = csw( self.catalogUrl )
    cat.getrecordbyid( [ self.catalog.records[ recordId ].identifier ] )
    #print cat.request

    QApplication.restoreOverrideCursor()

    if cat.exceptionreport:
      print cat.exceptionreport.exceptions
      QMessageBox.warning( self, self.tr( "Metadata request error" ),
                           self.tr( "Can't get metadata for record %1:\n%2: %3" )
                           .arg( recordId )
                           .arg( cat.exceptionreport.exceptions[ 0 ][ "exceptionCode" ])
                           .arg( cat.exceptionreport.exceptions[ 0 ][ "ExceptionText" ] ) )
      return

    dlg = CSWResponseDialog()
    dlg.textXML.setText( cat.response )
    dlg.exec_()

  def showResponse( self ):
    dlg = CSWResponseDialog()
    dlg.textXML.setText( self.catalog.response )
    dlg.exec_()

  def displayResults( self ):
    self.treeRecords.clear()

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

    # TODO: enable Add to canvas and Download buttons for appropriated
    # records types
