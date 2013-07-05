# -*- coding: utf-8 -*-

#******************************************************************************
#
# CSW Client
# ---------------------------------------------------------
# QGIS Catalogue Service client.
#
# Copyright (C) 2010 NextGIS (http://nextgis.org),
#                    Alexander Bruy (alexander.bruy@gmail.com),
#                    Maxim Dubinin (sim@gis-lab.info),
#                    Tom Kralidis (tomkralidis@hotmail.com)
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

import ConfigParser
import os

curpath = os.path.dirname(os.path.abspath(__file__))

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.join(curpath, 'metadata.txt')))

__version__ = config.get('general', 'version')

def getmdval(option):
  """Convenience function"""
  return config.get('general', option)

def name():
  return getmdval('name')

def description():
  return getmdval('description')

def category():
  return getmdval('category')

def version():
  return __version__

def qgisMinimumVersion():
  return getmdval('qgisMinimumVersion')

def author():
  return getmdval('author')

def email():
  return getmdval('email')

def icon():
  return getmdval('icon')

def classFactory( iface ):
  from cswclient import CSWClientPlugin
  return CSWClientPlugin( iface )

