%module(directors="1") streamanalyzer

//fix for wrong python director typemap
%typemap(directorin) PyObject* %{
 $input = $1_name;
%}

%{
  //catch used in functions which may call a director function
  #define _CLCATCH() \
    catch ( ... ){ \
      printf("... caught\n"); \
      throw Swig::DirectorMethodException(); \
    }

//extra c++ code
%{
  #include <strigi/analyzerplugin.h>
  #include <strigi/streamendanalyzer.h>
  #include <strigi/streamthroughanalyzer.h>
  #include <strigi/streamsaxanalyzer.h>
  #include <strigi/streamlineanalyzer.h>
  #include <strigi/streameventanalyzer.h>
  #include <list>
  
  template <typename Type, typename Base>
  class StreamAnalyzerFactoryWrapper : public Base {
      Base* f;
  public:
      StreamAnalyzerFactoryWrapper(Base* f){  this->f = f; }
      ~StreamAnalyzerFactoryWrapper(){ }
      const char* name() const { 
        try{ return this->f->name(); 
        }catch(Swig::DirectorException& ex){ printf("DirectorException: %s in name\n", ex.getMessage()); }
      }
      Type* newInstance() const { 
        try{ return this->f->newInstance(); 
        }catch(Swig::DirectorException& ex){ printf("DirectorException: %s in newInstance\n", ex.getMessage()); }
      }
      void registerFields(Strigi::FieldRegister& f){ 
        try{ this->f->registerFields(f); 
        }catch(Swig::DirectorException& ex){ printf("DirectorException: %s in registerFields\n", ex.getMessage()); }
      }
  };  
  typedef StreamAnalyzerFactoryWrapper<Strigi::StreamEndAnalyzer, Strigi::StreamEndAnalyzerFactory> PythonStreamEndAnalyzerFactory;
  typedef StreamAnalyzerFactoryWrapper<Strigi::StreamThroughAnalyzer, Strigi::StreamThroughAnalyzerFactory> PythonStreamThroughAnalyzerFactory;
  typedef StreamAnalyzerFactoryWrapper<Strigi::StreamSaxAnalyzer, Strigi::StreamSaxAnalyzerFactory> PythonStreamSaxAnalyzerFactory;
  typedef StreamAnalyzerFactoryWrapper<Strigi::StreamLineAnalyzer, Strigi::StreamLineAnalyzerFactory> PythonStreamLineAnalyzerFactory;
  typedef StreamAnalyzerFactoryWrapper<Strigi::StreamEventAnalyzer, Strigi::StreamEventAnalyzerFactory> PythonStreamEventAnalyzerFactory;
  
  //Factory
  class PythonAnalyzerFactoryFactory : public Strigi::AnalyzerFactoryFactory {
  public:
      static std::list<Strigi::StreamEndAnalyzerFactory*> seaf;
      static std::list<Strigi::StreamThroughAnalyzerFactory*> staf;
      static std::list<Strigi::StreamSaxAnalyzerFactory*> ssaf;
      static std::list<Strigi::StreamLineAnalyzerFactory*> slaf;
      static std::list<Strigi::StreamEventAnalyzerFactory*> sevaf;
      
      std::list<Strigi::StreamEndAnalyzerFactory*>
      streamEndAnalyzerFactories() const {
          std::list<Strigi::StreamEndAnalyzerFactory*> ret;
          for ( std::list<Strigi::StreamEndAnalyzerFactory*>::iterator itr = seaf.begin(); itr != seaf.end(); itr ++ ){
            ret.push_back(new PythonStreamEndAnalyzerFactory(*itr));
          }
          return ret;
      }
      std::list<Strigi::StreamThroughAnalyzerFactory*>
      streamThroughAnalyzerFactories() const {
          std::list<Strigi::StreamThroughAnalyzerFactory*> ret;
          for ( std::list<Strigi::StreamThroughAnalyzerFactory*>::iterator itr = staf.begin(); itr != staf.end(); itr ++ ){
            ret.push_back(new PythonStreamThroughAnalyzerFactory(*itr));
          }
          return ret;
      }
      std::list<Strigi::StreamSaxAnalyzerFactory*>
      streamSaxAnalyzerFactories() const {
          std::list<Strigi::StreamSaxAnalyzerFactory*> ret;
          for ( std::list<Strigi::StreamSaxAnalyzerFactory*>::iterator itr = ssaf.begin(); itr != ssaf.end(); itr ++ ){
            ret.push_back(new PythonStreamSaxAnalyzerFactory(*itr));
          }
          return ret;
      }
      std::list<Strigi::StreamLineAnalyzerFactory*>
      streamLineAnalyzerFactories() const {
          std::list<Strigi::StreamLineAnalyzerFactory*> ret;
          for ( std::list<Strigi::StreamLineAnalyzerFactory*>::iterator itr = slaf.begin(); itr != slaf.end(); itr ++ ){
            ret.push_back(new PythonStreamLineAnalyzerFactory(*itr));
          }
          return ret;
      }
      std::list<Strigi::StreamEventAnalyzerFactory*>
      streamEventAnalyzerFactories() const {
          std::list<Strigi::StreamEventAnalyzerFactory*> ret;
          for ( std::list<Strigi::StreamEventAnalyzerFactory*>::iterator itr = sevaf.begin(); itr != sevaf.end(); itr ++ ){
            ret.push_back(new PythonStreamEventAnalyzerFactory(*itr));
          }
          return ret;
      }
  };
  
  std::list<Strigi::StreamEndAnalyzerFactory*> PythonAnalyzerFactoryFactory::seaf;
  std::list<Strigi::StreamThroughAnalyzerFactory*> PythonAnalyzerFactoryFactory::staf;
  std::list<Strigi::StreamSaxAnalyzerFactory*> PythonAnalyzerFactoryFactory::ssaf;
  std::list<Strigi::StreamLineAnalyzerFactory*> PythonAnalyzerFactoryFactory::slaf;
  std::list<Strigi::StreamEventAnalyzerFactory*> PythonAnalyzerFactoryFactory::sevaf;
  

  STRIGI_ANALYZER_FACTORY(PythonAnalyzerFactoryFactory)
%}



###########################################################
# include everything else
###########################################################
%include <exception.i>
%include "../../defs/common.i"

#extra python code
%include "extra.i"



###########################################################
# testing
###########################################################

