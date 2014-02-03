# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2010 NextGIS (http://nextgis.org),
#                    Alexander Bruy (alexander.bruy@gmail.com),
#                    Maxim Dubinin (sim@gis-lab.info)
#
# Copyright (C) 2014 Tom Kralidis (tomkralidis@gmail.com)
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

import ConfigParser
from gettext import gettext, ngettext
import logging
import os

from jinja2 import Environment, FileSystemLoader
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import QMessageBox

LOGGER = logging.getLogger('MetaSearch')


class StaticContext(object):
    """base configuration / scaffolding"""

    def __init__(self):
        """init"""
        self.ppath = os.path.dirname(os.path.abspath(__file__))
        self.metadata = ConfigParser.ConfigParser()
        self.metadata.readfp(open(os.path.join(self.ppath, 'metadata.txt')))

def render_template(language, context, data, template):
    """Renders HTML display of metadata XML"""

    env = Environment(extensions=['jinja2.ext.i18n'],
                      loader=FileSystemLoader(context.ppath))
    env.install_gettext_callables(gettext, ngettext, newstyle=True)

    template_file = 'resources/templates/%s' % template
    template = env.get_template(template_file)
    return template.render(language=language, obj=data)

def tr(text):
    """translates text for objects which do not inherit QObject"""

    return QCoreApplication.translate('MetaSearch', text)

def get_connections_from_file(filename):
    """load connections from connection file"""

    error = 0
    try:
        doc = etree.parse(filename).getroot()
    except etree.ParseError, err:
        error = 1
        msg = self.tr('Cannot parse XML file: %s' % err)
    except IOError, err:
        error = 1
        msg = self.tr('Cannot open file: %s' % err)

    if doc.tag != 'qgcCSWConnections':
        error = 1
        msg = self.tr('Invalid CSW connections XML.')

    if exception == 1:
        QMessageBox.information(self, self.tr('Loading Connections'), msg)
        return
    return doc


from PyQt4.QtXml import *


def extractUrl(parent, xmlDoc, recordId):
    doc = QDomDocument()
    errorStr = ''
    errorLine = 0
    errorColumn = 0

    (success, errorStr, errorLine, errorColumn) = doc.setContent(xmlDoc, True)
    print success
    if not success:
        QMessageBox.warning(parent, parent.tr("Parsing error"),
                         parent.tr("Parse error at line %1, column %2:\n%3")
                         .arg(errorLine)
                         .arg(errorColumn)
                         .arg(errorStr))
        return

    root = doc.documentElement().firstChildElement("SearchResults")
    child = root.firstChildElement("Record")
    found = False
    while not child.isNull() and not found:
        elem = child.firstChildElement()
        while not elem.isNull():
            e = elem.toElement()
            if e.tagName() == "identifier" and e.attribute("scheme").endsWith("DocID") and e.text() == recordId:
                #print "ID", e.text()
                found = True
                break
            elem = elem.nextSiblingElement()

        if not found:
            child = child.nextSiblingElement()

    # now in child we have selected record and can extract URL
    found = False
    elem = child.firstChildElement()
    while not elem.isNull():
        e = elem.toElement()
        if e.tagName() == "references" and e.attribute("scheme").endsWith("Onlink"):
            found = True
            #print "URL", e.text()
            break
        elem = elem.nextSiblingElement()

    if found:
        return e.text()

    return str()
