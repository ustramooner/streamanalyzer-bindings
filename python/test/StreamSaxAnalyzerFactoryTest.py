# ====================================================================
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ====================================================================

from BaseTestCase import TestCase, main
from streamanalyzer import *
import os, signal
from threading import Thread
import time
import struct

Fields = {}

class TestStreamSaxAnalyzer(StreamSaxAnalyzer):
  def __init__(self, factory):
    super(TestStreamSaxAnalyzer, self).__init__()
    self.factory = weakref.proxy(factory)
  
  def name(self): return "TestStreamSaxAnalyzer"
  def startAnalysis(self, result):
    self.result = result
    pass
  def endAnalysis(self, *args):
    pass
  def startElement(self, localname, prefix, uri, namespaces, attributes):
    if localname.lower() == "title":
      self.inTitle = True
      self.title = ""
    else:
      self.inTitle = False
      
    #print "localname: %s" % localname
    #print "prefix: %s" % prefix
    #print "uri: %s" % uri
    #print "namespaces: %s" % str(namespaces)
    #print "attributes: %s" % str(attributes)

  def endElement(self, localname, prefix, uri):
    if self.inTitle: self.result.addValue(self.factory.title, self.title.strip())
    pass
  def characters(self, string):
    if self.inTitle: self.title += string
  def isReadyWithStream(self):
    return True

class TestStreamSaxAnalyzerFactory(StreamSaxAnalyzerFactory):
  def __init__(self):
    super(TestStreamSaxAnalyzerFactory, self).__init__()
  def registerFields(self, reg):
    self.title = reg.registerField("http://www.villagechief.com/ontologies#title")
  def newInstance(self):
    return TestStreamSaxAnalyzer(self)
  def name(self):
    return "TestStreamSaxAnalyzer"


class DummySaxWriter(IndexWriter):
  def __init__(self):
    super(DummySaxWriter, self).__init__()

  def addValue(self, result, field, value): 
    if field.key().startswith("http://www.villagechief.com/"):
      global Fields
      Fields[field.key()] = value
  def addTriplet(self, s, p, o):
    pass
  def addText(self, result, string):
    pass
  def finishAnalysis(self, r, *args):
    pass  

class DummySaxManager(IndexManager):
  def __init__(self):
    super(DummySaxManager, self).__init__()
    IndexManager.addFactory(TestStreamSaxAnalyzerFactory())
  def createIndexWriter(self):
    return DummySaxWriter()

class DummySaxConfig(AnalyzerConfiguration):
  def __init__(self):
    super(DummySaxConfig, self).__init__()
  def useFactory(self, factory):
    return True if factory.name() != "HtmlSaxAnalyzer" else False

  def indexDir(self, path, dirName):
    if dirName.starswith(".svn"):
      return False
    if dirName == "unichtm":
      return False
      
    return True

class StreamSaxAnalyzersTestCase(TestCase):
    def prep(self):
      conf = DummySaxConfig()
      manager = DummySaxManager()
      analyzer = DirAnalyzer(manager, conf)
      return {'analyzer': analyzer,
              'manager': manager,
              'conf': conf,
              'writer': manager.indexWriter()
             }
    def tearDown(self):
      IndexManager.clearFactories()
      global Fields
      Fields = {}

    def testSaxAnalyzer(self):
      p = self.prep()
      p['analyzer'].analyzeDir(self.TESTDATA + "/home.de.html")
      
      global Fields
      self.assertEquals({
          'http://www.villagechief.com/ontologies#title': "GNU Operating System - Free Software Foundation (FSF)"
        }, 
        Fields)
      
if __name__ == "__main__":
    import sys
    
    if '-loop' in sys.argv:
        sys.argv.remove('-loop')
        while True:
            try:
                main()
            except:
                pass
    elif '-dbg' in sys.argv:
      sys.argv.remove('-dbg')
      from BaseTestCase import LeakFind
      with (LeakFind()):
        main()
    else:
         main()
    
