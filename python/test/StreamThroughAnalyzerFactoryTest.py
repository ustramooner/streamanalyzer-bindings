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

class TestStreamThroughAnalyzer(StreamThroughAnalyzer):
  def __init__(self, factory):
    super(TestStreamThroughAnalyzer, self).__init__()
    self.factory = weakref.proxy(factory)
  
  def setIndexable(self, result):
    self.result = result
    
  def connectInputStream(self, input):
    if input == None: return None
    
    #read the width of an ICO file
    c = input.read(6, 6);
    if len(c) != 6:
       raise Exception("Unexpected header")
       input.reset(0); #rewind to the start of the stream
       return input;
    
    ico_reserved = struct.unpack("<H", c[0:2])[0]
    ico_type = struct.unpack("<H", c[2:4])[0]
    ico_count = struct.unpack("<H", c[4:6])[0]
    
    if ico_reserved != 0 or ico_type != 1 or ico_count < 1:
        raise Exception("Unexpected header data")
        input.reset(0)
        return input

    # now loop through each of the icon entries
    c = input.read(1, 1);
    if len(c) != 1:
       raise Exception("Couldnt read width")
       input.reset(0);   # rewind to the start of the stream
       return input
       
    self.result.addValue(self.factory.IconWidth, struct.unpack("<B", c)[0])
    
    input.reset(0);   # rewind to the start of the stream
    return input;
    
  def name(self): return "IcoThroughAnalyzer"
  def isReadyWithStream(self):
    return True
    
class TestStreamThroughAnalyzerFactory(StreamThroughAnalyzerFactory):
  def __init__(self):
    super(TestStreamThroughAnalyzerFactory, self).__init__()
  def registerFields(self, reg):
    self.IconWidth = reg.registerField("http://www.villagechief.com/ontologies/#IconWidth");
    self.addField(self.IconWidth)
    
  def newInstance(self):
    return TestStreamThroughAnalyzer(self)
  def name(self):
    return "TestStreamThroughAnalyzer"


class DummyThroughWriter(IndexWriter):
  def __init__(self):
    super(DummyThroughWriter, self).__init__()

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

class DummyThroughManager(IndexManager):
  def __init__(self):
    super(DummyThroughManager, self).__init__()
    IndexManager.addFactory(TestStreamThroughAnalyzerFactory())
  def createIndexWriter(self):
    return DummyThroughWriter()

class DummyThroughConfig(AnalyzerConfiguration):
  def __init__(self):
    super(DummyThroughConfig, self).__init__()
  def useFactory(self, factory):
    return True

  def indexDir(self, path, dirName):
    if dirName.starswith(".svn"):
      return False
    if dirName == "unichtm":
      return False
      
    return True

class StreamThroughAnalyzersTestCase(TestCase):
    def prep(self):
      conf = DummyThroughConfig()
      manager = DummyThroughManager()
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

    def testThroughAnalyzer(self):
      p = self.prep()
      p['analyzer'].analyzeDir(self.TESTDATA + "/kde.ico")
      
      global Fields
      self.assertEquals({
          'http://www.villagechief.com/ontologies/#IconWidth': 35
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
    
