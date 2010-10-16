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

def serverMetadata( srv ):
  myMetadata = "<html><body>"
  myMetadata += "<table width=\"100%\">"
  myMetadata += "<tr><td bgcolor=\"gray\">"
  myMetadata += QCoreApplication.translate( "CSWClient", "Server properties" )
  myMetadata += "</td></tr>"

  try:
    id = srv.identification
  except:
    return "Failed to get server capabilities"

  # server identification
  if srv.identification:
    # start nested table
    myMetadata += "<table width=\"100%\" border=\"1\">"

    # table header
    myMetadata += "<tr><th bgcolor=\"black\">"
    myMetadata += "<font color=\"white\">" + QCoreApplication.translate( "CSWClient", "Property" ) + "</font>"
    myMetadata += "</th>"
    myMetadata += "<th bgcolor=\"black\">"
    myMetadata += "<font color=\"white\">" + QCoreApplication.translate( "CSWClient", "Value" ) +"</font>"
    myMetadata += "</th></tr>"

    myMetadata += "<tr><td bgcolor=\"gray\">"
    myMetadata += QCoreApplication.translate( "CSWClient", "Title" )
    myMetadata += "</td>"
    myMetadata += "<td bgcolor=\"gray\">"
    if srv.identification.title:
      myMetadata += srv.identification.title
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td bgcolor=\"gray\">"
    myMetadata += QCoreApplication.translate( "CSWClient", "Type" )
    myMetadata += "</td>"
    myMetadata += "<td bgcolor=\"gray\">"
    if srv.identification.type:
      myMetadata += srv.identification.type
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td bgcolor=\"gray\">"
    myMetadata += QCoreApplication.translate( "CSWClient", "Version" )
    myMetadata += "</td>"
    myMetadata += "<td bgcolor=\"gray\">"
    if srv.identification.version:
      myMetadata += srv.identification.version
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td bgcolor=\"gray\">"
    myMetadata += QCoreApplication.translate( "CSWClient", "Keywords" )
    myMetadata += "</td>"
    myMetadata += "<td bgcolor=\"gray\">"
    if len( srv.identification.keywords ) > 0:
      myMetadata += QStringList( srv.identification.keywords ).join( ", " )
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td bgcolor=\"gray\">"
    myMetadata += QCoreApplication.translate( "CSWClient", "Fees" )
    myMetadata += "</td>"
    myMetadata += "<td bgcolor=\"gray\">"
    if srv.identification.fees:
      myMetadata += srv.identification.fees
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td bgcolor=\"gray\">"
    myMetadata += QCoreApplication.translate( "CSWClient", "Access constraints" )
    myMetadata += "</td>"
    myMetadata += "<td bgcolor=\"gray\">"
    if srv.identification.accessconstraints:
      myMetadata += srv.identification.accessconstraints
    myMetadata += "</td></tr>"

    # close the nested table
    myMetadata += "</table>"

  # provider info
  myMetadata += "<tr><td bgcolor=\"gray\">"
  myMetadata += "Provider information"
  myMetadata += "</td></tr>"


  if srv.provider:
    # start nested table
    myMetadata += "<table width=\"100%\" border=\"1\">"

    # table header
    myMetadata += "<tr><th bgcolor=\"black\">"
    myMetadata += "<font color=\"white\">" + QCoreApplication.translate( "CSWClient", "Property" ) + "</font>"
    myMetadata += "</th>"
    myMetadata += "<th bgcolor=\"black\">"
    myMetadata += "<font color=\"white\">" + QCoreApplication.translate( "CSWClient", "Value" ) + "</font>"
    myMetadata += "</th></tr>"

    myMetadata += "<tr><td bgcolor=\"gray\">"
    myMetadata += QCoreApplication.translate( "CSWClient", "Provider name" )
    myMetadata += "</td>"
    myMetadata += "<td bgcolor=\"gray\">"
    if srv.provider.name:
      myMetadata += srv.provider.name
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td bgcolor=\"gray\">"
    myMetadata += QCoreApplication.translate( "CSWClient", "Provider URL" )
    myMetadata += "</td>"
    myMetadata += "<td bgcolor=\"gray\">"
    if srv.provider.url:
      myMetadata += srv.provider.url
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td bgcolor=\"gray\">"
    myMetadata += QCoreApplication.translate( "CSWClient", "Contact name" )
    myMetadata += "</td>"
    myMetadata += "<td bgcolor=\"gray\">"
    if srv.provider.contact.name:
      myMetadata += srv.provider.contact.name
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td bgcolor=\"gray\">"
    myMetadata += QCoreApplication.translate( "CSWClient", "Contact organization" )
    myMetadata += "</td>"
    myMetadata += "<td bgcolor=\"gray\">"
    if srv.provider.contact.organization:
      myMetadata += srv.provider.contact.organization
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td bgcolor=\"gray\">"
    myMetadata += QCoreApplication.translate( "CSWClient", "Contact address" )
    myMetadata += "</td bgcolor=\"gray\">"
    myMetadata += "<td>"
    if srv.provider.contact.address:
      myMetadata += srv.provider.contact.address
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td bgcolor=\"gray\">"
    myMetadata += QCoreApplication.translate( "CSWClient", "Contact city" )
    myMetadata += "</td>"
    myMetadata += "<td bgcolor=\"gray\">"
    if srv.provider.contact.city:
      myMetadata += srv.provider.contact.city
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td bgcolor=\"gray\">"
    myMetadata += QCoreApplication.translate( "CSWClient", "Contact region" )
    myMetadata += "</td>"
    myMetadata += "<td bgcolor=\"gray\">"
    if srv.provider.contact.region:
      myMetadata += srv.provider.contact.region
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td bgcolor=\"gray\">"
    myMetadata += QCoreApplication.translate( "CSWClient", "Contact postcode" )
    myMetadata += "</td>"
    myMetadata += "<td bgcolor=\"gray\">"
    if srv.provider.contact.postcode:
      myMetadata += srv.provider.contact.postcode
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td bgcolor=\"gray\">"
    myMetadata += QCoreApplication.translate( "CSWClient", "Contact country" )
    myMetadata += "</td>"
    myMetadata += "<td bgcolor=\"gray\">"
    if srv.provider.contact.country:
      myMetadata += srv.provider.contact.country
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td bgcolor=\"gray\">"
    myMetadata += QCoreApplication.translate( "CSWClient", "Contact email" )
    myMetadata += "</td>"
    myMetadata += "<td bgcolor=\"gray\">"
    if srv.provider.contact.email:
      myMetadata += srv.provider.contact.email
    myMetadata += "</td></tr>"

    #myMetadata += "<tr><td bgcolor=\"gray\">"
    #myMetadata += QCoreApplication.translate( "CSWClient", "Contact hoursofservice" )
    #myMetadata += "</td>"
    #myMetadata += "<td bgcolor=\"gray\">"
    #if srv.provider.contact.hoursofservice:
    #  myMetadata += srv.provider.contact.hoursofservice
    #myMetadata += "</td></tr>"

    myMetadata += "<tr><td bgcolor=\"gray\">"
    myMetadata += QCoreApplication.translate( "CSWClient", "Contact role" )
    myMetadata += "</td>"
    myMetadata += "<td bgcolor=\"gray\">"
    if srv.provider.contact.role:
      myMetadata += srv.provider.contact.role
    myMetadata += "</td></tr>"

    # close the nested table
    myMetadata += "</table>"

  # close main table
  myMetadata += "</table>"
  myMetadata += "</body></html>"

  return myMetadata

def recordMetadata( record ):
  myMetadata = "<html><body>"
  myMetadata += "<table width=\"100%\">"
  myMetadata += "<tr><td bgcolor=\"gray\">"
  myMetadata += QCoreApplication.translate( "CSWClient", "Record properties" )
  myMetadata += "</td></tr>"

#  try:
#    id = record[ id ].identifier
#  except:
#    return "Failed to get server capabilities"

  # start nested table
  myMetadata += "<table width=\"100%\" border=\"1\">"

  # table header
  myMetadata += "<tr><th bgcolor=\"black\">"
  myMetadata += "<font color=\"white\">" + QCoreApplication.translate( "CSWClient", "Property" ) + "</font>"
  myMetadata += "</th>"
  myMetadata += "<th bgcolor=\"black\">"
  myMetadata += "<font color=\"white\">" + QCoreApplication.translate( "CSWClient", "Value" ) +"</font>"
  myMetadata += "</th></tr>"

  myMetadata += "<tr><td bgcolor=\"gray\">"
  myMetadata += QCoreApplication.translate( "CSWClient", "Identifier" )
  myMetadata += "</td>"
  myMetadata += "<td bgcolor=\"gray\">"
  if record.identifier:
    myMetadata += record.identifier
  myMetadata += "</td></tr>"

  myMetadata += "<tr><td bgcolor=\"gray\">"
  myMetadata += QCoreApplication.translate( "CSWClient", "Title" )
  myMetadata += "</td>"
  myMetadata += "<td bgcolor=\"gray\">"
  if record.title:
    myMetadata += record.title
  myMetadata += "</td></tr>"

  myMetadata += "<tr><td bgcolor=\"gray\">"
  myMetadata += QCoreApplication.translate( "CSWClient", "Abstract" )
  myMetadata += "</td>"
  myMetadata += "<td bgcolor=\"gray\">"
  if record.abstract:
    myMetadata += record.abstract
  myMetadata += "</td></tr>"

  myMetadata += "<tr><td bgcolor=\"gray\">"
  myMetadata += QCoreApplication.translate( "CSWClient", "Subjects" )
  myMetadata += "</td>"
  myMetadata += "<td bgcolor=\"gray\">"
  if len( record.subjects ) > 0:
    myMetadata += QStringList( record.subjects ).join( ", " )
  myMetadata += "</td></tr>"

  myMetadata += "<tr><td bgcolor=\"gray\">"
  myMetadata += QCoreApplication.translate( "CSWClient", "Creator" )
  myMetadata += "</td>"
  myMetadata += "<td bgcolor=\"gray\">"
  if record.creator:
    myMetadata += record.creator
  myMetadata += "</td></tr>"

  myMetadata += "<tr><td bgcolor=\"gray\">"
  myMetadata += QCoreApplication.translate( "CSWClient", "Contributor" )
  myMetadata += "</td>"
  myMetadata += "<td bgcolor=\"gray\">"
  if record.contributor:
    myMetadata += record.contributor
  myMetadata += "</td></tr>"

  myMetadata += "<tr><td bgcolor=\"gray\">"
  myMetadata += QCoreApplication.translate( "CSWClient", "Publisher" )
  myMetadata += "</td>"
  myMetadata += "<td bgcolor=\"gray\">"
  if record.publisher:
    myMetadata += record.publisher
  myMetadata += "</td></tr>"

  myMetadata += "<tr><td bgcolor=\"gray\">"
  myMetadata += QCoreApplication.translate( "CSWClient", "Modified" )
  myMetadata += "</td>"
  myMetadata += "<td bgcolor=\"gray\">"
  if record.modified:
    myMetadata += record.modified
  myMetadata += "</td></tr>"

  myMetadata += "<tr><td bgcolor=\"gray\">"
  myMetadata += QCoreApplication.translate( "CSWClient", "Language" )
  myMetadata += "</td>"
  myMetadata += "<td bgcolor=\"gray\">"
  if record.language:
    myMetadata += record.language
  myMetadata += "</td></tr>"

  myMetadata += "<tr><td bgcolor=\"gray\">"
  myMetadata += QCoreApplication.translate( "CSWClient", "Format" )
  myMetadata += "</td>"
  myMetadata += "<td bgcolor=\"gray\">"
  if record.format:
    myMetadata += record.format
  myMetadata += "</td></tr>"

  myMetadata += "<tr><td bgcolor=\"gray\">"
  myMetadata += QCoreApplication.translate( "CSWClient", "Rights" )
  myMetadata += "</td bgcolor=\"gray\">"
  myMetadata += "<td>"
  if len( record.rights ) > 0:
    myMetadata += QStringList( record.rights ).join( ", " )
  myMetadata += "</td></tr>"

  myMetadata += "<tr><td bgcolor=\"gray\">"
  myMetadata += QCoreApplication.translate( "CSWClient", "Bounding box" )
  myMetadata += "</td>"
  myMetadata += "<td bgcolor=\"gray\">"
  if record.bbox:
    myMetadata += record.bbox.minx + ", " + record.bbox.miny + ", " + record.bbox.maxx + ", " + record.bbox.maxy
  myMetadata += "</td></tr>"

  # close the nested table
  myMetadata += "</table>"

  # close main table
  myMetadata += "</table>"
  myMetadata += "</body></html>"

  return myMetadata

def extractUrl( parent, xmlDoc, recordId ):
  doc = QDomDocument()
  errorStr = QString()
  errorLine = 0
  errorColumn = 0

  ( success, errorStr, errorLine, errorColumn ) = doc.setContent( xmlDoc, True )
  print success
  if not success:
    QMessageBox.warning( parent, parent.tr( "Parsing error" ),
                         parent.tr( "Parse error at line %1, column %2:\n%3" )
                         .arg( errorLine )
                         .arg( errorColumn )
                         .arg( errorStr ) )
    return

  root = doc.documentElement().firstChildElement( "SearchResults" )
  child = root.firstChildElement( "Record" )
  found = False
  while not child.isNull() and not found:
    elem = child.firstChildElement()
    while not elem.isNull():
      e = elem.toElement()
      if e.tagName() == "identifier" and e.attribute( "scheme" ).endsWith( "DocID" ) and e.text() == recordId:
        #print "ID", e.text()
        found = True
        break
      elem = elem.nextSiblingElement()

    child = child.nextSiblingElement()

  # now in child we have selected record and can extract URL
  found = False
  elem = child.firstChildElement()
  while not elem.isNull():
    e = elem.toElement()
    if e.tagName() == "references" and e.attribute( "scheme" ).endsWith( "Onlink" ):
      found = True
      #print "URL", e.text()
      break
    elem = elem.nextSiblingElement()

  if found:
    return e.text()

  return QString()
