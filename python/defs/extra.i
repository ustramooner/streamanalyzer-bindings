%pythoncode %{

import threading
import os

class IndexManager(PythonIndexManager):
  def __init__(self):
    super(IndexManager, self).__init__()
    self.tls = threading.local()
  
  """ Returns an IndexWriter. Note that there are multiple IndexWriters depending on the thread which is requesting it"""
  def indexWriter(self):
    return self.pythonIndexWriter()

  """ Since IndexWriters are not thread safe, we keep and return a thread specific IndexWriter"""
  def pythonIndexWriter(self):
    if not 'writer' in self.tls.__dict__:
      self.tls.writer = self.createIndexWriter()
    return self.tls.writer
    
  """ Adds a Analyzer Factory to the indexer. Note that this is global because Strigi does not provide any other way"""
  @staticmethod
  def addFactory(factory):
    IndexManager.factories.append(factory)
    PythonIndexManager.addFactory(factory)
  """ Clears all the custom factories """
  @staticmethod
  def clearFactories():
    del IndexManager.factories[:]
    PythonIndexManager.clearFactories()
  factories = []

#add data cleanup to finishAnalysis
def IndexWriterDataHandlerfinishAnalysis(self, result):
  self._finishAnalysis(result)
  if 'datas' in self.__dict__ and result.path() in self.datas: del self.datas[result.path()]
IndexWriter._finishAnalysis = IndexWriter.finishAnalysis
IndexWriter.finishAnalysis = IndexWriterDataHandlerfinishAnalysis

class DirAnalyzer():
  def __init__(self, manager, conf):
    self.manager = manager
    self.conf = conf
    self.writer = manager.indexWriter()
    self.analyzer = StreamAnalyzer(self.conf);
    self.analyzer.setIndexWriter(self.writer);
    self.running = False
  def __del__(self): self.analyzer = None
  def stop(self):
    self.running = False
  
  def analyzeFile(self, path):
    if os.path.exists(path):
      mtime = os.path.getmtime(path)
      exists = True
    else:
      mtime = 0
      exists = False

    result = AnalysisResult(path, int(mtime), self.writer, self.analyzer, "")
    if exists and os.path.isfile(path):
      stream = InputStream.openFile(path)
      result.index(stream)
      stream = None
    else:
      result.index(None)

  def _analyze(self):
      pass
      
  def analyzeDir(self, dir):
    self.running = True
    dir = os.path.abspath(dir)

    # if the path does not point to a directory, return
    if not os.path.exists(dir) or not os.path.isdir(dir):
      self.analyzeFile(dir)
      self.writer.commit()
      return

    for root, subFolders, files in os.walk(dir):
      self.analyzeFile(root)

      for file in files:
        if self.conf.indexFile(root, file):
          self.analyzeFile(os.path.join(root, file))

      #commit after each directory
      self.writer.commit()
      if not self.running: break
      
      #remove subFolders that we don't want to index
      remove = []
      for subFolder in subFolders:
        if not self.conf.indexDir(root, subFolder): remove.append(subFolder)
      for r in remove:
        subFolders.remove(r)



#factories need to keep instances of the analyzers they create, add replacements in here... 
def StreamEndAnalyzerFactoryNewInstance(self):
  if not '_instances' in self.__dict__: self._instances = []
  ret = self._newInstance()
  self._instances.append(ret)
  return ret
def StreamEndAnalyzerFactoryInit(self):
  StreamEndAnalyzerFactory.__initOrig__(self)
  if not '_newInstance' in self.__class__.__dict__:
    #replace the newInstance function
    self.__class__._newInstance = self.__class__.newInstance
    self.__class__.newInstance =  StreamEndAnalyzerFactoryNewInstance
#replace the init
StreamEndAnalyzerFactory.__initOrig__ = StreamEndAnalyzerFactory.__init__
StreamEndAnalyzerFactory.__init__ = StreamEndAnalyzerFactoryInit 

def StreamThroughAnalyzerFactoryNewInstance(self):
  if not '_instances' in self.__dict__: self._instances = []
  ret = self._newInstance()
  self._instances.append(ret)
  return ret
def StreamThroughAnalyzerFactoryInit(self):
  StreamThroughAnalyzerFactory.__initOrig__(self)
  if not '_newInstance' in self.__class__.__dict__:
    #replace the newInstance function
    self.__class__._newInstance = self.__class__.newInstance
    self.__class__.newInstance =  StreamThroughAnalyzerFactoryNewInstance
#replace the init
StreamThroughAnalyzerFactory.__initOrig__ = StreamThroughAnalyzerFactory.__init__
StreamThroughAnalyzerFactory.__init__ = StreamThroughAnalyzerFactoryInit 

def StreamSaxAnalyzerFactoryNewInstance(self):
  if not '_instances' in self.__dict__: self._instances = []
  ret = self._newInstance()
  self._instances.append(ret)
  return ret
def StreamSaxAnalyzerFactoryInit(self):
  StreamSaxAnalyzerFactory.__initOrig__(self)
  if not '_newInstance' in self.__class__.__dict__:
    #replace the newInstance function
    self.__class__._newInstance = self.__class__.newInstance
    self.__class__.newInstance =  StreamSaxAnalyzerFactoryNewInstance
#replace the init
StreamSaxAnalyzerFactory.__initOrig__ = StreamSaxAnalyzerFactory.__init__
StreamSaxAnalyzerFactory.__init__ = StreamSaxAnalyzerFactoryInit 

def StreamEventAnalyzerFactoryNewInstance(self):
  if not '_instances' in self.__dict__: self._instances = []
  ret = self._newInstance()
  self._instances.append(ret)
  return ret
def StreamEventAnalyzerFactoryInit(self):
  StreamEventAnalyzerFactory.__initOrig__(self)
  if not '_newInstance' in self.__class__.__dict__:
    #replace the newInstance function
    self.__class__._newInstance = self.__class__.newInstance
    self.__class__.newInstance =  StreamEventAnalyzerFactoryNewInstance
#replace the init
StreamEventAnalyzerFactory.__initOrig__ = StreamEventAnalyzerFactory.__init__
StreamEventAnalyzerFactory.__init__ = StreamEventAnalyzerFactoryInit 

def StreamLineAnalyzerFactoryNewInstance(self):
  if not '_instances' in self.__dict__: self._instances = []
  ret = self._newInstance()
  self._instances.append(ret)
  return ret
def StreamLineAnalyzerFactoryInit(self):
  StreamLineAnalyzerFactory.__initOrig__(self)
  if not '_newInstance' in self.__class__.__dict__:
    #replace the newInstance function
    self.__class__._newInstance = self.__class__.newInstance
    self.__class__.newInstance =  StreamLineAnalyzerFactoryNewInstance
#replace the init
StreamLineAnalyzerFactory.__initOrig__ = StreamLineAnalyzerFactory.__init__
StreamLineAnalyzerFactory.__init__ = StreamLineAnalyzerFactoryInit 

%}

