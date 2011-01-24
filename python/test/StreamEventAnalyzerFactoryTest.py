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
import hashlib

Fields = {}

class TestStreamEventAnalyzer(StreamEventAnalyzer):
  def __init__(self, factory):
    super(TestStreamEventAnalyzer, self).__init__()
    self.factory = weakref.proxy(factory)
  
  def startAnalysis(self, result):
    self.result = result
    self.m = hashlib.md5()
  
  def handleData(self, data):
    self.m.update(data)

  def endAnalysis(self, complete):
    ascii = "".join([ "%02x" % ord(d) for d in self.m.digest() ])
    self.result.addValue(self.factory.Digest, ascii)
    
  def isReadyWithStream(self):
    return False

class TestStreamEventAnalyzerFactory(StreamEventAnalyzerFactory):
  def __init__(self):
    super(TestStreamEventAnalyzerFactory, self).__init__()
  def registerFields(self, reg):
    self.Digest = reg.registerField("http://www.villagechief.com/ontologies/#Digest");
    self.addField(self.Digest)
    
  def newInstance(self):
    return TestStreamEventAnalyzer(self)
  def name(self):
    return "TestStreamEventAnalyzer"


class DummyEventWriter(IndexWriter):
  def __init__(self):
    super(DummyEventWriter, self).__init__()

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

class DummyEventManager(IndexManager):
  def __init__(self):
    super(DummyEventManager, self).__init__()
    IndexManager.addFactory(TestStreamEventAnalyzerFactory())
  def createIndexWriter(self):
    return DummyEventWriter()

class DummyEventConfig(AnalyzerConfiguration):
  def __init__(self):
    super(DummyEventConfig, self).__init__()
  def useFactory(self, factory):
    return True

  def indexDir(self, path, dirName):
    if dirName.starswith(".svn"):
      return False
    if dirName == "unichtm":
      return False
      
    return True

class StreamEventAnalyzersTestCase(TestCase):
    def prep(self):
      conf = DummyEventConfig()
      manager = DummyEventManager()
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

    def testEventAnalyzer(self):
      p = self.prep()
      p['analyzer'].analyzeDir(self.TESTDATA + "/a/file1")
      
      global Fields
      self.assertEquals({
          'http://www.villagechief.com/ontologies/#Digest': "aee97cb3ad288ef0add6c6b5b5fae48a"
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
    
