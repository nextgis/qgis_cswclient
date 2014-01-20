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
from config import StaticContext
 
class MetaSearchPlugin(object):
    """base plugin"""
    def __init__(self, iface):
        """init"""
        self.iface = iface
        self.context = StaticContext()

    def initGui(self):
        """startup"""

    def unload(self):
        """teardown"""
        self.menu.deleteLater()

    def help(self):
        """open help in user's default web browser"""
        webbrowser.open(self.context.metadata.get('general', 'homepage'))
