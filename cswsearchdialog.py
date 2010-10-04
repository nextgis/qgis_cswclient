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
  def __init__( self, iface ):
    QDialog.__init__( self )
    self.setupUi( self )

    self.iface = iface
    self.catUrl = None
    self.catalog = None

    QObject.connect( self.cmbCatalogs, SIGNAL( "activated( int )" ), self.saveSelection )

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

    self.populateCatalogList()

    self.setBboxFromCanvas()

    self.btnAddToMap.setEnabled( False )
    self.btnDownload.setEnabled( False )
    self.btnMetadata.setEnabled( False )
    self.btnShowXML.setEnabled( False )

  def populateCatalogList( self ):
    settings = QSettings()

    settings.beginGroup( "/CSWClient/" )
    self.cmbCatalogs.clear()
    self.cmbCatalogs.addItems( settings.childGroups() )
    settings.endGroup()

    self.setCatalogListPosition()

  def setCatalogListPosition( self ):
    settings = QSettings()

    toSelect = settings.value( "/CSWClient/search" ).toString()
    # does toSelect exist in cmbConnections?
    exists = False
    for i in range( self.cmbCatalogs.count() ):
      if self.cmbCatalogs.itemText( i + 1 ) == toSelect:
        self.cmbCatalogs.setCurrentIndex( i + 1 )
        exists = True
        break

    # If we couldn't find the stored item, but there are some, default
    # to the last item (this makes some sense when deleting items as it
    # allows the user to repeatidly click on delete to remove a whole
    # lot of items)
    if not exists and self.cmbCatalogs.count() > 0:
      # If toSelect is null, then the selected connection wasn't found
      # by QSettings, which probably means that this is the first time
      # the user has used qgis with database connections, so default to
      # the first in the list of connetions. Otherwise default to the last.
      if toSelect.isEmpty():
        self.cmbCatalogs.setCurrentIndex( 0 )
      else:
        self.cmbCatalogs.setCurrentIndex( self.cmbCatalogs.count() - 1 )

  def saveSelection( self, index ):
    settings = QSettings()
    settings.setValue( "/CSWClient/search", self.cmbCatalogs.currentText() )

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

    # catalog URL
    key = "/CSWClient/" + self.cmbCatalogs.currentText()
    url = str( settings.value( key + "/url" ).toString() )
    self.catUrl = url

    # build request
    self.catalog = csw( url )

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

    cat = csw( self.catUrl )
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
      item.setText( 2, self.catalog.records[ rec ].identifier )
      #print self.catalog.records[ rec ].uri
      #print self.catalog.records[ rec ].source
      #print self.catalog.records[ rec ].format

  def recordClicked( self ):
    if not self.treeRecords.selectedItems():
      return

    item = self.treeRecords.currentItem()
    if not item:
      return

    recordId = str( item.text( 2 ) )
    abstract = self.catalog.records[ recordId ].abstract
    self.txtAbstract.setText( QString( abstract ).simplified() )
