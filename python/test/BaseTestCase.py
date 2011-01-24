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

from unittest2 import TestCase as UnitTestCase, main, TestLoader
import os
import gc, weakref
from collections import defaultdict
import types

class TestCase(UnitTestCase):
  "Test base class"
  
  #def cleanup(*args):
  #  print "done..."

  def __init__(self, *args, **kwds):
    super(TestCase, self).__init__(*args, **kwds)
    #import inspect
    #this_file = inspect.currentframe().f_code.co_filename
    self.TESTDATA = os.path.join(os.path.dirname(__file__), 'testdata')
    #self.addCleanup(self.cleanup)

def load_tests(loader, standard_tests, pattern):
  # top level directory cached on loader instance
  this_dir = os.path.dirname(__file__)
  package_tests = loader.discover(start_dir=this_dir, pattern='*Test.py')
  standard_tests.addTests(package_tests)
  return standard_tests
    
if __name__ == "__main__":
  import sys
  if '-dbg' in sys.argv:
    sys.argv.remove('-dbg')
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

class LeakFind():
  def __init__(self):
    self.before=defaultdict(int)
    
    
  def __enter__(self):
    gc.collect()
    for i in gc.get_objects():
      if type(i) == types.InstanceType:
        self.before[i.__class__]+=1
      elif str(type(i)) == "<type 'instancemethod'>":
        self.before[str(i)]+=1
      else:
        self.before[type(i)]+=1
  
  def __exit__(self, *args):
    gc.collect()
    after=defaultdict(int)
    for i in gc.get_objects(): 
      if type(i) == types.InstanceType:
        after[i.__class__]+=1
      elif str(type(i)) == "<type 'instancemethod'>":
        after[str(i)]+=1
      else:
        after[type(i)]+=1
    
    #remove references in this class
    after[defaultdict]-=1
    
    print "MEMORY LEAKS:"
    print "============="
    i = 1
    for k in after:
      if after[k]-self.before[k]:
        print "%d. %s = %d" % (i, k, after[k]-self.before[k]) 
        i += 1
        
