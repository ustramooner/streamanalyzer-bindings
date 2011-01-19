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
    self.factories[factory.name()] = []

    for f in factory.registeredFields():
      self.factories[factory.name()].append(f.key())
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
      tr = ThreadRunner(self.prep(), self.TESTDATA)
      tr.start()
      tr.join()
      
    def testDirAnalyzerMultiThreadedStop(self):
      global filesAnalyzed
      filesAnalyzed = 0
      
      #fetch ALL documents count...
      t1 = time.time()
      p = self.prep()
      tr = ThreadRunner(self.prep(), self.TESTDATA)
      tr.start()
      tr.join()
      tt = time.time() - t1
      allFilesAnalyzed = filesAnalyzed
      	
      filesAnalyzed = 0
      p = self.prep()
      tr = ThreadRunner(p, self.TESTDATA)
      tr.start()
      time.sleep( tt / 2.0 )
      p['analyzer'].stop()
      tr.join()
      self.assertLess(filesAnalyzed, allFilesAnalyzed)

    
    def testDirAnalyzer1(self):
      global triplets
      triplets = {}

      p = self.prep()
      p['analyzer'].analyzeDir(os.path.join(self.TESTDATA, 'mail'), 1)
      
      expected = {
        ':bmqbh': 
          {
          'http://www.semanticdesktop.org/ontologies/2007/03/22/nco#hasEmailAddress': 
            'mailto:j@v.info', 
          'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': 
            'http://www.semanticdesktop.org/ontologies/2007/03/22/nco#Contact'
          }, 
        'mailto:DianeHolleymlr@trinityvalleyservices.net': 
          {
          'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': 
            'http://www.semanticdesktop.org/ontologies/2007/03/22/nco#EmailAddress', 
          'http://www.semanticdesktop.org/ontologies/2007/03/22/nco#emailAddress': 
            'DianeHolleymlr@trinityvalleyservices.net'
          }, 
        'mailto:j@v.info': 
          {
          'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': 
            'http://www.semanticdesktop.org/ontologies/2007/03/22/nco#EmailAddress', 
          'http://www.semanticdesktop.org/ontologies/2007/03/22/nco#emailAddress': 
            'j@v.info'
          },
        ':nwlrb': 
          {
          'http://www.semanticdesktop.org/ontologies/2007/03/22/nco#fullname': 
            '"June Klein" ', 
          'http://www.semanticdesktop.org/ontologies/2007/03/22/nco#hasEmailAddress': 
            'mailto:DianeHolleymlr@trinityvalleyservices.net', 
          'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': 
            'http://www.semanticdesktop.org/ontologies/2007/03/22/nco#Contact'
          }
      };
      
      expectedAnons = [ x for x in expected.keys() if x.startswith(":") ]
      actualAnons = [ x for x in triplets.keys() if x.startswith(":") ]
      
      if len(expected[expectedAnons[0]]) == len(triplets[actualAnons[0]]):
        expected[actualAnons[0]] = expected[expectedAnons[0]]
        expected[actualAnons[1]] = expected[expectedAnons[1]]
        del expected[expectedAnons[0]]
        del expected[expectedAnons[1]]
      else:
        expected[actualAnons[1]] = expected[expectedAnons[0]]
        expected[actualAnons[0]] = expected[expectedAnons[1]]
        del expected[expectedAnons[0]]
        del expected[expectedAnons[1]]
      
      #do a unsorted comparison
      for e in expected:
        self.assertEquals(len(expected[e]), len(triplets[e]), "checking len of key %s with values: %s == %s" % (e, str(expected[e]), str(triplets[e])) )
        for x in expected[e]:
          self.assertEquals(expected[e][x], triplets[e][x])
      
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
