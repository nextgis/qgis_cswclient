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

from newcswconnectiondialogbase import Ui_NewCSWConnectionDialog

class NewCSWConnectionDialog( QDialog, Ui_NewCSWConnectionDialog ):
  def __init__( self, connectionName = QString( "" ) ):
    QDialog.__init__( self )
    self.setupUi( self )

    self.origName = connectionName

  def accept( self ):
    settings = QSettings()

    connName = self.leName.text()

    if not connName.isEmpty():
      key = "/CSWClient/" + connName

      # warn if entry was renamed to an existing connection
      if self.origName != connName and settings.contains( key + "/url" ):
        res = QMessageBox.warning( self, self.tr( "Save connection" ),
                               self.tr( "Should the existing connection %1 be overwritten?" )
                               .arg( connName ),
                               QMessageBox.Ok | QMessageBox.Cancel )
        if res == QMessageBox.Cancel:
          return

      # on rename delete original entry first
      if not self.origName.isEmpty() and self.origName != connName:
        settings.remove( "/CSWClient/" + self.origName )

      settings.setValue( key + "/url", self.leURL.text().trimmed() );

      QDialog.accept( self )

  @pyqtSignature("reject()")
  def reject( self ):
    QDialog.reject( self )
