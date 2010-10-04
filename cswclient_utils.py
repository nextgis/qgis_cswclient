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

def serverMetadata( srv ):
  myMetadata = "<html><body>"
  myMetadata += "<table width=\"100%\" border=\"1\">"
  myMetadata += "<tr><td>"
  myMetadata += QCoreApplication.translate( "CSWClient", "Server properties" )
  myMetadata += "</td></tr>"

  # server identification
  if srv.identification:
    # start nested table
    myMetadata += "<table width=\"100%\" border=\"1\">"

    # table header
    myMetadata += "<tr><th>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Property" )
    myMetadata += "</th>"
    myMetadata += "<th>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Value" )
    myMetadata += "</th></tr>"

    myMetadata += "<tr><td>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Title" )
    myMetadata += "</td>"
    myMetadata += "<td>"
    if srv.identification.title:
      myMetadata += srv.identification.title
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Type" )
    myMetadata += "</td>"
    myMetadata += "<td>"
    if srv.identification.type:
      myMetadata += srv.identification.type
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Version" )
    myMetadata += "</td>"
    myMetadata += "<td>"
    if srv.identification.version:
      myMetadata += srv.identification.version
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Keywords" )
    myMetadata += "</td>"
    myMetadata += "<td>"
    if len( srv.identification.keywords ) > 0:
      myMetadata += QStringList( srv.identification.keywords ).join( ", " )
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Fees" )
    myMetadata += "</td>"
    myMetadata += "<td>"
    if srv.identification.fees:
      myMetadata += srv.identification.fees
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Access constraints" )
    myMetadata += "</td>"
    myMetadata += "<td>"
    if srv.identification.accessconstraints:
      myMetadata += srv.identification.accessconstraints
    myMetadata += "</td></tr>"

    # close the nested table
    myMetadata += "</table>"

  # provider info
  myMetadata += "<tr><td>"
  myMetadata += "Provider information"
  myMetadata += "</td></tr>"


  if srv.provider:
    # start nested table
    myMetadata += "<table width=\"100%\" border=\"1\">"

    # table header
    myMetadata += "<tr><th>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Property" )
    myMetadata += "</th>"
    myMetadata += "<th>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Value" )
    myMetadata += "</th></tr>"

    myMetadata += "<tr><td>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Provider name" )
    myMetadata += "</td>"
    myMetadata += "<td>"
    if srv.provider.name:
      myMetadata += srv.provider.name
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Provider URL" )
    myMetadata += "</td>"
    myMetadata += "<td>"
    if srv.provider.url:
      myMetadata += srv.provider.url
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Contact name" )
    myMetadata += "</td>"
    myMetadata += "<td>"
    if srv.provider.contact.name:
      myMetadata += srv.provider.contact.name
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Contact organization" )
    myMetadata += "</td>"
    myMetadata += "<td>"
    if srv.provider.contact.organization:
      myMetadata += srv.provider.contact.organization
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Contact address" )
    myMetadata += "</td>"
    myMetadata += "<td>"
    if srv.provider.contact.address:
      myMetadata += srv.provider.contact.address
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Contact city" )
    myMetadata += "</td>"
    myMetadata += "<td>"
    if srv.provider.contact.city:
      myMetadata += srv.provider.contact.city
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Contact region" )
    myMetadata += "</td>"
    myMetadata += "<td>"
    if srv.provider.contact.region:
      myMetadata += srv.provider.contact.region
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Contact postcode" )
    myMetadata += "</td>"
    myMetadata += "<td>"
    if srv.provider.contact.postcode:
      myMetadata += srv.provider.contact.postcode
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Contact country" )
    myMetadata += "</td>"
    myMetadata += "<td>"
    if srv.provider.contact.country:
      myMetadata += srv.provider.contact.country
    myMetadata += "</td></tr>"

    myMetadata += "<tr><td>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Contact email" )
    myMetadata += "</td>"
    myMetadata += "<td>"
    if srv.provider.contact.email:
      myMetadata += srv.provider.contact.email
    myMetadata += "</td></tr>"

    #myMetadata += "<tr><td>"
    #myMetadata += QCoreApplication.translate( "CSWClient", "Contact hoursofservice" )
    #myMetadata += "</td>"
    #myMetadata += "<td>"
    #if srv.provider.contact.hoursofservice:
    #  myMetadata += srv.provider.contact.hoursofservice
    #myMetadata += "</td></tr>"

    myMetadata += "<tr><td>"
    myMetadata += QCoreApplication.translate( "CSWClient", "Contact role" )
    myMetadata += "</td>"
    myMetadata += "<td>"
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
  pass
