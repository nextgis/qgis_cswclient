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

from qgis.core import *
from qgis.gui import *

import cswclientdialog

from __init__ import version

import resources_rc

class CSWClientPlugin( object ):
  def __init__( self, iface ):
    self.iface = iface
    self.iface = iface
    try:
      self.QgisVersion = unicode( QGis.QGIS_VERSION_INT )
    except:
      self.QgisVersion = unicode( QGis.qgisVersion )[ 0 ]

    # For i18n support
    userPluginPath = QFileInfo( QgsApplication.qgisUserDbFilePath() ).path() + "/python/plugins/cswclient"
    systemPluginPath = QgsApplication.prefixPath() + "/python/plugins/cswclient"

    overrideLocale = QSettings().value( "locale/overrideFlag", QVariant( False ) ).toBool()
    if not overrideLocale:
      localeFullName = QLocale.system().name()
    else:
      localeFullName = QSettings().value( "locale/userLocale", QVariant( "" ) ).toString()

    if QFileInfo( userPluginPath ).exists():
      translationPath = userPluginPath + "/i18n/cswclient_" + localeFullName + ".qm"
    else:
      translationPath = systemPluginPath + "/i18n/cswclient_" + localeFullName + ".qm"

    self.localePath = translationPath
    if QFileInfo( self.localePath ).exists():
      self.translator = QTranslator()
      self.translator.load( self.localePath )
      QCoreApplication.installTranslator( self.translator )

  def initGui( self ):
    if int( self.QgisVersion ) < 1:
      QMessageBox.warning( self.iface.mainWindow(), "CSW Client",
                           QCoreApplication.translate( "CSW Client", "Quantum GIS version detected: " ) + unicode( self.QgisVersion ) + ".xx\n" +
                           QCoreApplication.translate( "CSW Client", "This version of CSW Client requires at least QGIS version 1.0.0\nPlugin will not be enabled." ) )
      return None

    self.actionRun = QAction( QIcon( ":/cswclient.png" ), "CSW Client", self.iface.mainWindow() )
    self.actionRun.setStatusTip( QCoreApplication.translate( "CSW Client", "Perform search in Catalogue Services" ) )
    self.actionAbout = QAction( QIcon( ":/about.png" ), "About", self.iface.mainWindow() )

    QObject.connect( self.actionRun, SIGNAL( "triggered()" ), self.run )
    QObject.connect( self.actionAbout, SIGNAL( "triggered()" ), self.about )

    if hasattr( self.iface, "addPluginToWebMenu" ):
      self.iface.addPluginToWebMenu( QCoreApplication.translate( "CSW Client", "CSW Client" ), self.actionRun )
      self.iface.addPluginToWebMenu( QCoreApplication.translate( "CSW Client", "CSW Client" ), self.actionAbout )
      self.iface.addWebToolBarIcon( self.actionRun )
    else:
      self.iface.addPluginToMenu( QCoreApplication.translate( "CSW Client", "CSW Client" ), self.actionRun )
      self.iface.addPluginToMenu( QCoreApplication.translate( "CSW Client", "CSW Client" ), self.actionAbout )
      self.iface.addToolBarIcon( self.actionRun )

  def unload( self ):
    if hasattr( self.iface, "addPluginToWebMenu" ):
      self.iface.removePluginWebMenu( QCoreApplication.translate( "CSW Client", "CSW Client" ), self.actionRun )
      self.iface.removePluginWebMenu( QCoreApplication.translate( "CSW Client", "CSW Client" ), self.actionAbout )
      self.iface.removeWebToolBarIcon( self.actionRun )
    else:
      self.iface.removePluginMenu( QCoreApplication.translate( "CSW Client", "CSW Client" ), self.actionRun )
      self.iface.removePluginMenu( QCoreApplication.translate( "CSW Client", "CSW Client" ), self.actionAbout )
      self.iface.removeToolBarIcon( self.actionRun )

  def about( self ):
    dlgAbout = QDialog()
    dlgAbout.setWindowTitle( QApplication.translate( "CSW Client", "About CSW Client", "Window title" ) )
    lines = QVBoxLayout( dlgAbout )
    title = QLabel( QApplication.translate( "CSW Client", "<b>CSW Client</b>" ) )
    title.setAlignment( Qt.AlignHCenter | Qt.AlignVCenter )
    lines.addWidget( title )
    version = QLabel( QApplication.translate( "CSW Client", "Version: %1" ).arg( version() ) )
    version.setAlignment( Qt.AlignHCenter | Qt.AlignVCenter )
    lines.addWidget( version )
    lines.addWidget( QLabel( QApplication.translate( "CSW Client", "Catalogue Services browser. Provide\ninterface for discovering and retrieval\nof spatial data and services metadata." ) ) )
    lines.addWidget( QLabel( QApplication.translate( "CSW Client", "<b>Developers:</b>" ) ) )
    lines.addWidget( QLabel( "&nbsp;&nbsp;<a href=\"http://nextgis.ru\">NextGIS</a>" ) )
    lines.addWidget( QLabel( "  Alexander Bruy" ) )
    lines.addWidget( QLabel( "  Maxim Dubinin" ) )
    lines.addWidget( QLabel( QApplication.translate( "CSW Client", "<b>Homepage:</b>") ) )

    overrideLocale = QSettings().value( "locale/overrideFlag", QVariant( False ) ).toBool()
    if not overrideLocale:
      localeFullName = QLocale.system().name()
    else:
      localeFullName = QSettings().value( "locale/userLocale", QVariant( "" ) ).toString()

    localeShortName = localeFullName[ 0:2 ]
    if localeShortName in [ "ru", "uk" ]:
      link = QLabel( "<a href=\"http://gis-lab.info/qa/cswclient.html\">http://gis-lab.info/qa/cswclient.html</a>" )
    else:
      link = QLabel( "<a href=\"http://gis-lab.info/qa/cswclient-eng.html\">http://gis-lab.info/qa/cswclient-eng.html</a>" )

    link.setOpenExternalLinks( True )
    lines.addWidget( link )

    btnClose = QPushButton( QApplication.translate( "CSW Client", "Close" ) )
    lines.addWidget( btnClose )
    QObject.connect( btnClose, SIGNAL( "clicked()" ), dlgAbout, SLOT( "close()" ) )

    dlgAbout.exec_()

  def run( self ):
    dlg = cswclientdialog.CSWClientDialog( self.iface )
    dlg.exec_()

