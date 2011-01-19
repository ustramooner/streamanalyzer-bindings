#ifndef STRIGI_PYTHONDIRANALYZER_H
#define STRIGI_PYTHONDIRANALYZER_H


#ifdef SWIGGING
##############################################################################
#
#  To enable a 'stop' call, we have a callback which determines whether we should continue...
#
###############################################################################
%rename (DirAnalyzer) PythonDirAnalyzer;
#endif

#ifndef SWIGGING
  class _AnalysisCaller : public Strigi::AnalysisCaller {
    bool* running;
  public:
    _AnalysisCaller(bool* _running):
      running(_running)
    {
    }
    bool continueAnalysis(){
      return *running;
    }
  };
#else
  
  %extend PythonDirAnalyzer {
    %pythoncode %{
      _traps = []
      @staticmethod
      def _handleSignal(*args):
        for t in DirAnalyzer._traps:
          t.stop()
      def installSignal(self):
        import signal
        signal.signal(signal.SIGINT, DirAnalyzer._handleSignal)
        if not self in DirAnalyzer._traps:
          DirAnalyzer._traps.append(weakref.ref(self))
      def uninstallSignal(self):
        if self in DirAnalyzer._traps:
          DirAnalyzer._traps.remove(self)
      def __del__(self):
        self.uninstallSignal()
    %}
  }
#endif

class PythonDirAnalyzer {
    bool running;
    Strigi::DirAnalyzer an;
    _AnalysisCaller analysisCaller;
public:
    PythonDirAnalyzer(PythonIndexManager& manager, Strigi::AnalyzerConfiguration& conf):
      an(manager, conf),
      analysisCaller(&running)
    {
      running = false;
    }
    virtual ~PythonDirAnalyzer(){
    }
    int analyzeDir(const std::string& dir, int nthreads = 1, const std::string& lastToSkip = std::string()){
      running = true;
      try{
        return an.analyzeDir(dir, nthreads, &analysisCaller, lastToSkip);
  	  }_CLCATCH();
    }
    void stop(){
      running = false; 
    }
};

#endif


