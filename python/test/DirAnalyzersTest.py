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
import os

files = []

class DummyWriter(IndexWriter):
  def __init__(self):
    IndexWriter.__init__(self)
  def startAnalysis(self, r):
    global files
    files.append(r.path())

class DummyManager(IndexManager):
  def __init__(self):
    IndexManager.__init__(self)
    self.writer = None
  def createIndexWriter(self):
    return DummyWriter()

class DummyConfig(AnalyzerConfiguration):
  def __init__(self):
    AnalyzerConfiguration.__init__(self)
  def useFactory(self, x):
    return True

class AnalyzersTestCase(TestCase):
    def prep(self):
      conf = DummyConfig()
      manager = DummyManager()
      analyzer = DirAnalyzer(manager, conf)
      return {'analyzer': analyzer,
              'manager': manager,
              'conf': conf,
              'writer': manager.writer
             }
    
    def testDirAnalyzer1(self):
      p = self.prep()
      global files
      files = []
      p['analyzer'].analyzeDir(os.path.join(self.TESTDATA, 'a.gz'))
      self.assertEquals(
        [
          self.TESTDATA + '/a.gz', 
          self.TESTDATA + '/a.gz/a'
        ],
        files
      )
      
    def testDirAnalyzer2(self):
      p = self.prep()
      global files
      files = []
      p['analyzer'].analyzeDir(os.path.join(self.TESTDATA, 'a.bz2'))
      
      self.assertEquals(
        [
          self.TESTDATA + '/a.bz2',
          self.TESTDATA + '/a.bz2/a',
          self.TESTDATA + '/a.bz2/a/file1',
          self.TESTDATA + '/a.bz2/a/file2'
        ],
        files
      )
      
    def testDirAnalyzer3(self):
      p = self.prep()
      global files
      files = []
      p['analyzer'].analyzeDir(os.path.join(self.TESTDATA, 'unichtm'))
      self.assertEquals(132, len(files))
      
    def testDirAnalyzer4_password_zip(self):
      p = self.prep()
      global files
      files = []
      p['analyzer'].analyzeDir(os.path.join(self.TESTDATA, 'a-enc.zip'))
      self.assertEquals(
        [
          '/home/ben/dev/strigi-bindings/python/test/testdata/a-enc.zip',
          '/home/ben/dev/strigi-bindings/python/test/testdata/a-enc.zip/a'
        ],
        files
      )
        

if __name__ == "__main__":
    import sys
    if '-loop' in sys.argv:
        sys.argv.remove('-loop')
        while True:
            try:
                main()
            except:
                pass
    else:
         main()
