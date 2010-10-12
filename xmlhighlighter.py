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

nameStartCharList = ":A-Z_a-z\\x00C0-\\x00D6\\x00D8-\\x00F6\\x00F8-\\x02FF\\x0370-\\x037D\\x037F-\\x1FFF\\x200C-\\x200D\\x2070-\\x218F\\x2C00-\\x2FEF\\x3001-\\xD7FF\\xF900-\\xFDCF\\xFDF0-\\xFFFD"
nameCharList = nameStartCharList + "\\-\\.0-9\\x00B7\\x0300-\\x036F\\x203F-\\x2040"
nameStart = "[" + nameStartCharList + "]"
nameChar = "[" + nameCharList + "]"
xmlName = nameStart + "(" + nameChar + ")*"

class XmlHighlighter( QSyntaxHighlighter ):
  def __init__( self, parent ):
    QSyntaxHighlighter.__init__( self, parent )

    self.parent = parent
    self.highlightingRules = []

    xmlOpenTag = QTextCharFormat()
    xmlCloseTag = QTextCharFormat()
    xmlComment = QTextCharFormat()
    xmlDoctype = QTextCharFormat()
    xmlAttribute = QTextCharFormat()
    xmlAtttibuteValue = QTextCharFormat()

    # open tags
    pattern = QRegExp( "\\b<" + xmlName + "\\b" + ">?$" )
    xmlOpenTag.setForeground( Qt.darkBlue )
    xmlOpenTag.setFontWeight( QFont.Bold )
    rule = HighlightingRule( pattern, xmlOpenTag )
    self.highlightingRules.append( rule )

    # close tags
    pattern = QRegExp("\\b</" + xmlName + ">" + "|/>|>$" )
    xmlCloseTag.setForeground( Qt.darkBlue )
    xmlCloseTag.setFontWeight( QFont.Bold )
    rule = HighlightingRule( pattern, xmlCloseTag )
    self.highlightingRules.append( rule )

    # comments
    #pattern = QRegExp("^<!\\-\\-$.*^\\-\\->$")
    #xmlComment.setForeground( Qt.gray )
    #xmlComment.setFontItalic( True )
    #rule = HighlightingRule( pattern, xmlComment )
    #self.highlightingRules.append( rule )

    # doctype
    #pattern = QRegExp("^<!DOCTYPE.*>$")
    #xmlDoctype.setForeground( Qt.red )
    #xmlDoctype.setFontWeight( QFont.Bold )
    #rule = HighlightingRule( pattern, xmlDoctype )
    #self.highlightingRules.append( rule )

    # attributes
    #pattern = QRegExp("\s" + xmlName + "\b")
    #xmlAttribute.setForeground( Qt.darkYellow )
    #rule = HighlightingRule( pattern, xmlAttribute )
    #self.highlightingRules.append( rule )

    # attribute values
    #pattern = QRegExp("\".*\"" )
    #pattern.setMinimal( True )
    #xmlCloseTag.setForeground( Qt.darkGreen )
    #xmlCloseTag.setFontWeight( QFont.Bold )
    #rule = HighlightingRule( pattern, xmlCloseTag )
    #self.highlightingRules.append( rule )

  def highlightBlock( self, text ):
    for rule in self.highlightingRules:
      expression = QRegExp( rule.pattern )
      index = expression.indexIn( text )
      while index >= 0:
        length = expression.matchedLength()
        self.setFormat( index, length, rule.format )
        index = text.indexOf( expression, index + length )
    self.setCurrentBlockState( 0 )

class HighlightingRule():
  def __init__( self, pattern, format ):
    self.pattern = pattern
    self.format = format
