#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
from urllib import request

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.description = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True
            
    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.description = self.theContent + "</a>"
                # To avoid Unicode trouble
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                line = "<li><a href='" + self.theContent + "'>" + self.description
                print(line)
                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars
            
# --- Main prog
    
# Load parser and driver

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!

xmlFile = request.urlopen("http://barrapunto.com/index.rss")
theParser.parse(xmlFile)



print("Parse complete")
