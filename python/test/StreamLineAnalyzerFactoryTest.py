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
import weakref

Fields = {}
Triplets = {}
Text = ""

class TestStreamLineAnalyzer(StreamLineAnalyzer):
  def __init__(self, factory):
    super(TestStreamLineAnalyzer, self).__init__()
    self.factory = weakref.proxy(factory)
    
  def startAnalysis(self, result):
    self.result = result
    self.ready = False
    self.lines = 0
    
  def handleLine(self, *args):
    self.lines += 1

  def endAnalysis(self, complete):
    if not self.ready and complete:
      self.result.addValue(self.factory.strField, self.result.path())
      self.result.addValue(self.factory.intField, 123)
      self.result.addValue(self.factory.doubleField, 1.23)
      self.result.addText("XXX")
      self.result.addTriplet("s", "p", "o")
      {'s': {'p': 'o'}}
  def isReadyWithStream(self):
    return self.ready
    
class TestStreamLineAnalyzerFactory(StreamLineAnalyzerFactory):
  def __init__(self):
    super(TestStreamLineAnalyzerFactory, self).__init__()
  def registerFields(self, reg):
    self.strField = reg.registerField("http://www.villagechief.com/ontologies/#str");
    self.intField = reg.registerField("http://www.villagechief.com/ontologies/#int");
    self.doubleField = reg.registerField("http://www.villagechief.com/ontologies/#double");
    self.addField(self.strField)
    self.addField(self.intField)
    self.addField(self.doubleField)
    
  def newInstance(self):
    return TestStreamLineAnalyzer(self)
  def name(self):
    return "TestStreamLineAnalyzer"

class DummyLineWriter(IndexWriter):
  def __init__(self):
    super(DummyLineWriter, self).__init__()

  def addValue(self, result, field, value): 
    if field.key().startswith("http://www.villagechief.com/"):
      global Fields
      Fields[field.key()] = value

  def addTriplet(self, s, p, o):
    global Triplets 
    if not s in Triplets:
      Triplets[s] = {}
    Triplets[s][p] = o
  
  def addText(self, result, string):
    global Text
    Text += string
    
  def finishAnalysis(self, r, *args):
    pass  

class DummyLineManager(IndexManager):
  def __init__(self):
    super(DummyLineManager, self).__init__()
    IndexManager.addFactory(TestStreamLineAnalyzerFactory())
  def createIndexWriter(self):
    return DummyLineWriter()

class DummyLineConfig(AnalyzerConfiguration):
  def __init__(self):
    super(DummyLineConfig, self).__init__()
  def useFactory(self, factory):
    return True

  def indexDir(self, path, dirName):
    if dirName.starswith(".svn"):
      return False
    if dirName == "unichtm":
      return False
      
    return True

class StreamLineAnalyzersTestCase(TestCase):
    def prep(self):
      conf = DummyLineConfig()
      manager = DummyLineManager()
      analyzer = DirAnalyzer(manager, conf)
      return {'analyzer': analyzer,
              'manager': manager,
              'conf': conf,
              'writer': manager.indexWriter()
             }
    def tearDown(self):
      IndexManager.clearFactories()
      global Fields
      global Triplets
      global Text
      Fields = {}
      Triplets = {}
      Text = ""

    def testLineAnalyzer(self):
      p = self.prep()
      p['analyzer'].analyzeDir(self.TESTDATA + "/a/file1")
      
      global Fields
      self.assertEquals({
          'http://www.villagechief.com/ontologies/#str': self.TESTDATA + '/a/file1',
          'http://www.villagechief.com/ontologies/#int': 123,
          'http://www.villagechief.com/ontologies/#double': 1.23
        }, 
        Fields)
      global Text
      self.assertEquals("XXXhallo\n", Text)

      global Triplets
      self.assertEquals({'s': {'p': 'o'}}, Triplets)

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
    
