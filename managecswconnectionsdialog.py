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

from managecswconnectionsdialogbase import Ui_ManageCSWConnectionsDialog

class ManageCSWConnectionsDialog( QDialog, Ui_ManageCSWConnectionsDialog ):
  def __init__( self, mode ):
    QDialog.__init__( self )
    self.setupUi( self )

    # 0 - save, 1 - load
    self.dialogMode = mode

    QObject.connect( self.btnBrowse, SIGNAL( "clicked()" ), self.selectFile )

    self.manageGui()

  def manageGui( self ):
    if self.dialogMode == 1:
      self.label.setText( self.tr( "Load from file" ) )
      self.buttonBox.button( QDialogButtonBox.Ok ).setText( self.tr( "Load" ) )
    else:
      self.label.setText( self.tr( "Save to file" ) )
      self.buttonBox.button( QDialogButtonBox.Ok ).setText( self.tr( "Save" ) )
      self.populateConnections()

    self.buttonBox.button( QDialogButtonBox.Ok ).setEnabled( False )

  def selectFile( self ):
    if self.dialogMode == 0:
      self.fileName = QFileDialog.getSaveFileName( self, self.tr( "Save connections" ), ".", self.tr( "Extensible Markup Language (*.xml *.XML)" ) )
    else:
      self.fileName = QFileDialog.getOpenFileName( self, self.tr( "Load connections" ), ".", self.tr( "Extensible Markup Language (*.xml *XML)" ) )

    if self.fileName.isEmpty():
      return

    # ensure the user never ommited the extension from the file name
    if not self.fileName.toLower().endsWith( ".xml" ) :
      self.fileName += ".xml"

    self.leFileName.setText( self.fileName )

    if self.dialogMode == 1:
      self.populateConnections()

    self.buttonBox.button( QDialogButtonBox.Ok ).setEnabled( True )

  def populateConnections( self ):
    # Save mode. Populate connections list from settings
    if self.dialogMode == 0:
      settings = QSettings()
      settings.beginGroup( "/CSWClient/" )
      keys = settings.childGroups()
      for key in keys:
        item = QListWidgetItem( self.listConnections )
        item.setText( key )
      settings.endGroup()
    # Load mode. Populate connections list from file
    else:
      file = QFile( self.fileName )
      if not file.open( QIODevice.ReadOnly | QIODevice.Text ):
        QMessageBox.warning( self, self.tr( "Loading connections" ),
                             self.tr( "Cannot read file %1:\n%2." )
                             .arg( mFileName )
                             .arg( file.errorString() ) )
        return

      doc = QDomDocument()
      (success, errorStr, errorLine, errorColumn) = doc.setContent( file, True )
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
        self.fileName = ""
        self.leFileName.clear()
        self.listConnections.clear()
        return

      child = root.firstChildElement()
      while not child.isNull():
        item = QListWidgetItem( self.listConnections )
        item.setText( child.attribute( "name" ) )
        child = child.nextSiblingElement()

  def saveCSWConnections( self, connections ):
    doc = QDomDocument( "connections" )
    root = doc.createElement( "qgsCSWConnections" )
    root.setAttribute( "version", "1.0" )
    doc.appendChild( root )

    settings = QSettings()
    key = "/CSWClient/"
    for conn in connections:
      el = doc.createElement( "csw" )
      el.setAttribute( "name", conn )
      el.setAttribute( "url", settings.value( key + conn + "/url", "" ).toString() )
      root.appendChild( el )

    return doc

  def loadCSWConnections( self, doc, items ):
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

      # process only selected connections
      if not items.contains( connectionName ):
        child = child.nextSiblingElement()
        continue

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

  def accept( self ):
    selection = self.listConnections.selectedItems()
    if len( selection ) == 0:
      return

    items = QStringList()
    for sel in selection:
      items.append( sel.text() )

    if self.dialogMode == 0: # save
      doc = self.saveCSWConnections( items )

      file = QFile( self.fileName )
      if not file.open( QIODevice.WriteOnly | QIODevice.Text ):
        QMessageBox.warning( self, self.tr( "Saving connections" ),
                             self.tr( "Cannot write file %1:\n%2." )
                             .arg( self.fileName )
                             .arg( file.errorString() ) )
        return

      out = QTextStream( file )
      doc.save( out, 4 )
    else: #load
      file = QFile( self.fileName )
      if not file.open( QIODevice.ReadOnly | QIODevice.Text ):
        QMessageBox.warning( self, self.tr( "Loading connections" ),
                             self.tr( "Cannot write file %1:\n%2." )
                             .arg( self.fileName )
                             .arg( file.errorString() ) )
        return

      doc = QDomDocument()
      (success, errorStr, errorLine, errorColumn) = doc.setContent( file, True )
      if not success:
        QMessageBox.warning( self, self.tr( "Loading connections" ),
                             self.tr( "Parse error at line %1, column %2:\n%3" )
                             .arg( errorLine )
                             .arg( errorColumn )
                             .arg( errorStr ) )
        return

      self.loadCSWConnections( doc, items )

    self.fileName = ""
    self.leFileName.clear()
    self.listConnections.clear()
    self.buttonBox.button( QDialogButtonBox.Ok ).setEnabled( False )

  @pyqtSignature("reject()")
  def reject( self ):
    QDialog.reject( self )
