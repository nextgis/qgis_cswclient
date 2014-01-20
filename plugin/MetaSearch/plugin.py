# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2010 NextGIS (http://nextgis.org),
#                    Alexander Bruy (alexander.bruy@gmail.com),
#                    Maxim Dubinin (sim@gis-lab.info),
#                    Tom Kralidis (tomkralidis@gmail.com)
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
###############################################################################

import webbrowser

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from config import StaticContext
 
class MetaSearchPlugin(object):
    """base plugin"""
    def __init__(self, iface):
        """init"""
        self.iface = iface
        self.context = StaticContext()

    def initGui(self):
        """startup"""

        icon = QIcon(self.context.curpath + "/images/cswclient.png")
        self.helpAction = QAction(icon, "Help with MetaSearch", self.iface.mainWindow())
        self.helpAction.setWhatsThis("1Configuration for test plugin")
        self.helpAction.setStatusTip("1This is status tip")
        QObject.connect(self.helpAction, SIGNAL('triggered()'), self.help)

        self.iface.addToolBarIcon(self.helpAction)
        self.iface.addPluginToWebMenu("&Test plugins", self.helpAction)


    def unload(self):
        """teardown"""
        # remove the plugin menu item and icon
        self.iface.removePluginWebMenu("&WebTest plugins",self.action)
        self.iface.removeToolBarIcon(self.action)

    def help(self):
        """open help in user's default web browser"""
        webbrowser.open(self.context.metadata.get('general', 'homepage'))
