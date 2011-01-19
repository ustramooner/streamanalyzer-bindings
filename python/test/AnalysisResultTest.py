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

filesAnalyzed = 0
triplets = {}

class DummyWriter(IndexWriter):
  def __init__(self):
    IndexWriter.__init__(self)

  def addValue(self, result, field, value): 
    #print "%s: %s = %s" % (result.path(), field.key(), value)

    print "####################################"
    print "Registered Field:"
    print "Field Key: %s" % field.key()
    print "####################################"
    
    parent = field.parent()
    if parent != None:
      print "Parent Key: %s" % parent.key()

    print "-----------------"
    print "Field Properties:"
    print "-----------------"
    props = field.properties()
    print "valid: %s" % props.valid()
    print "binary: %s" % props.binary()
    print "minCardinality: %s" % props.minCardinality()
    print "maxCardinality: %s" % props.maxCardinality()
    print "uri %s" % props.uri()
    print "name: %s" % props.name()
    print "typeUri: %s" % props.typeUri()
    print "description: %s" % props.description()
    print "parentUris: %s" % `props.parentUris()`
    print "childUris: %s" % `props.childUris()`
    print "applicableClasses: %s" % `props.applicableClasses()`
    print "compressed: %s" % props.compressed()
    print "indexed: %s" % props.indexed()
    print "stored: %s" % props.stored()
    print "tokenized: %s" % props.tokenized()
    
    
    print "---------------"
    print "AnalysisResult:"
    print "---------------"
    print "child: %s" % result.child()
    print "fileNames: %s" % result.fileName()
    print "path: %s" % result.path()
    print "parentPath: %s" % result.parentPath()
    print "mTime: %s" % result.mTime()
    print "depth: %s" % result.depth()
    print "encoding: %s" % result.encoding()
    print "mimeType: %s" % result.mimeType()
    print "extension: %s" % result.extension()
    print "config: %s" % result.config()
    
  def addTriplet(self, s, p, o):
    global triplets 
    if not s in triplets:
      triplets[s] = {}
    triplets[s][p] = o
    
  def finishAnalysis(self, r, *args):
    global filesAnalyzed
    filesAnalyzed += 1
  

class DummyManager(IndexManager):
  def __init__(self):
    IndexManager.__init__(self)
    self.writers = []
  def createIndexWriter(self):
    return DummyWriter()

class DummyConfig(AnalyzerConfiguration):
  def __init__(self):
    super(DummyConfig, self).__init__()
    self.factories = {}
  def useFactory(self, factory):
    return True

  def indexDir(self, path, dirName):
    if dirName.starswith(".svn"):
      return False
    if dirName == "unichtm":
      return False
      
    return True

class ThreadRunner(Thread):
   def __init__ (self, p, dir):
      Thread.__init__(self)
      self.p = p
      self.dir = dir
      
   def run(self):
      try:
        #TODO: using > 1 threads is faulty still..
        self.p['analyzer'].analyzeDir(self.dir, 1)
      except Exception as e:
        print e

class AnalyzersTestCase(TestCase):
    def prep(self):
      conf = DummyConfig()
      manager = DummyManager()
      analyzer = DirAnalyzer(manager, conf)
      return {'analyzer': analyzer,
              'manager': manager,
              'conf': conf,
              'writer': manager.indexWriter()
             }

    def testDirAnalyzerMultiThreaded(self):
      global filesAnalyzed
      filesAnalyzed = 0
      p = self.prep()
      tr = ThreadRunner(self.prep(), self.TESTDATA + "/a/file2")
      tr.start()
      tr.join()

if __name__ == "__main__":
    import sys
    dbg = False
    
    if '-dbg' in sys.argv:
      sys.argv.remove('-dbg')
      dbg = True
      import gc
      gc.set_debug(gc.DEBUG_LEAK)

    if '-loop' in sys.argv:
        sys.argv.remove('-loop')
        while True:
            try:
                main()
            except:
                pass
    else:
         main()
    
    if dbg:
      gc.collect()
      for o in gc.get_objects():
        print o
