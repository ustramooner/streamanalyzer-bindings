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

class TestStreamEndAnalyzer(StreamEndAnalyzer):
  def __init__(self, factory):
    super(TestStreamEndAnalyzer, self).__init__()
    self.factory = weakref.proxy(factory)
  def isReadyWithStream(self):
    return self.ready
  pngmagic = "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a"
  
  def checkHeader(self, header):
    return len(header) > 29 and header[0:8] == TestStreamEndAnalyzer.pngmagic
    
    
  def analyze(self, result, input):
    c = input.read(12, 12);
    if len(c) != 12:
        # file is too small to be a png
        return -1;

    # read chunksize and include the size of the type and crc (4 + 4)
    chunksize = struct.unpack(">L", c[8:12])[0] + 8
    if chunksize > 1048576:
        raise Exception("chunk too big: %d" %chunksize)
        return -1

    c = input.read(chunksize, chunksize)
    # the IHDR chunk should be the first
    if len(c) != chunksize or c[0:4] != "IHDR":
        raise Exception ("invalid IHDR or chunk read")
        return -1;

    # read the png dimensions
    result.addValue(self.factory.ImageWidth, struct.unpack(">I", c[4:8])[0])
    result.addValue(self.factory.ImageHeight, struct.unpack(">I", c[8:12])[0])

    input.reset(0)
    return 0

class TestStreamEndAnalyzerFactory(StreamEndAnalyzerFactory):
  def __init__(self):
    super(TestStreamEndAnalyzerFactory, self).__init__()
  def registerFields(self, reg):
    self.ImageWidth = reg.registerField("http://www.villagechief.com/ontologies/#ImageWidth");
    self.addField(self.ImageWidth)
    self.ImageHeight = reg.registerField("http://www.villagechief.com/ontologies/#ImageHeight");
    self.addField(self.ImageHeight)
    
  def newInstance(self):
    return TestStreamEndAnalyzer(self)
  def name(self):
    return "TestStreamEndAnalyzer"


class DummyEndWriter(IndexWriter):
  def __init__(self):
    super(DummyEndWriter, self).__init__()
    
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

class DummyEndManager(IndexManager):
  def __init__(self):
    super(DummyEndManager, self).__init__()
    IndexManager.addFactory(TestStreamEndAnalyzerFactory())
  def createIndexWriter(self):
    return DummyEndWriter()

class DummyEndConfig(AnalyzerConfiguration):
  def __init__(self):
    super(DummyEndConfig, self).__init__()
  def useFactory(self, factory):
    return True

  def indexDir(self, path, dirName):
    if dirName.starswith(".svn"):
      return False
    if dirName == "unichtm":
      return False
      
    return True

class StreamEndAnalyzersTestCase(TestCase):
    def prep(self):
      conf = DummyEndConfig()
      manager = DummyEndManager()
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

    def testEndAnalyzer(self):
      p = self.prep()
      p['analyzer'].analyzeDir(self.TESTDATA + "/strigi.png")
      
      global Fields
      self.assertEquals({
          'http://www.villagechief.com/ontologies/#ImageWidth': 530,
          'http://www.villagechief.com/ontologies/#ImageHeight': 364
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
    
