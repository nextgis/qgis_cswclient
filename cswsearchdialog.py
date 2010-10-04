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

    self.manageGui()

  def manageGui( self ):
    #settings = QSettings()
    #res = settings.value( "/CSWClient/results", QVariant( "10" ) )
    #print "*****DEBUG*******", res
    #self.spnRecords.setValue( settings.value( "/CSWClient/results", "10" ).toInt() [ 0 ] )

    self.setBboxFromCanvas()

    self.btnAddToMap.setEnabled( False )
    self.btnDownload.setEnabled( False )
    self.btnMetadata.setEnabled( False )
    self.btnShowXML.setEnabled( False )

  def setBboxFromCanvas( self ):
    extent = self.iface.mapCanvas().extent()
    self.leNorth.setText( str( extent.yMaximum() ) )
    self.leSouth.setText( str( extent.yMinimum() ) )
    self.leWest.setText( str( extent.xMaximum() ) )
    self.leEast.setText( str( extent.xMinimum() ) )

  def setDefaultBbox( self ):
    self.leNorth.setText( "90" )
    self.leSouth.setText( "-90" )
    self.leWest.setText( "-180" )
    self.leEast.setText( "180" )

  def startSearch( self ):
    # clear all fields
    self.treeRecords.clear()
    self.txtAbstract.clear()

    # save some settings
    settings = QSettings()
    settings.setValue( "/CSWClient/results", self.spnRecords.value() )

    # bbox
    minX = self.leWest.text()
    minY = self.leSouth.text()
    maxX = self.leEast.text()
    maxY = self.leNorth.text()
    bbox = [ minX, minY, maxX, maxY ]

    # keywords
    if self.leKeywords.text().isEmpty():
      keywords = []
    else:
      keywords = self.leKeywords.text().split( "," )

    # records to return
    maxRecords = self.spnRecords.value()

    # build request
    self.catalog = csw( self.catalogUrl )

    self.catalog.getrecords( qtype = None, keywords = keywords, bbox = bbox, sortby = None, maxrecords = maxRecords )

    self.lblResults.setText( self.tr( "Returned: %1 from %2" ).arg( self.catalog.results[ "returned" ] ).arg( self.catalog.results[ "matches" ] ) )

    self.displayResults()

    self.btnShowXML.setEnabled( True )
    self.btnMetadata.setEnabled( True )

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

    cat = csw( self.catalogUrl )
    cat.getrecordbyid( [ self.catalog.records[ recordId ].identifier ] )
    print cat.request

    dlg = CSWResponseDialog()
    dlg.textXML.setText( cat.response )
    dlg.exec_()

  def showResponse( self ):
    dlg = CSWResponseDialog()
    dlg.textXML.setText( self.catalog.response )
    dlg.exec_()

  def displayResults( self ):
    for rec in self.catalog.records:
      item = QTreeWidgetItem( self.treeRecords )
      item.setText( 0, self.catalog.records[ rec ].type )
      item.setText( 1, self.catalog.records[ rec ].title )
      print "*** DEBUG ***", self.catalog.records[ rec ].identifier
      item.setText( 2, self.catalog.records[ rec ].identifier )

  def recordClicked( self ):
    if not self.treeRecords.selectedItems():
      return

    item = self.treeRecords.currentItem()
    if not item:
      return

    recordId = str( item.text( 2 ) )
    abstract = self.catalog.records[ recordId ].abstract
    self.txtAbstract.setText( QString( abstract ).simplified() )
