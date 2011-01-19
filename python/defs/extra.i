%pythoncode %{

import threading

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

%}

