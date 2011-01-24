%{
  #include "strigi/analyzerconfiguration.h"
  #include "strigi/analysisresult.h"
  #include "strigi/streamanalyzer.h"
  #include "strigi/indexwriter.h"
  #include "strigi/pythonindexwriter.h"
  #include "strigi/indexmanager.h"
  #include "strigi/pythonindexmanager.h"
%}


//make swig work...
#define STREAMANALYZER_EXPORT

%ignore Strigi::FieldProperties::FieldProperties;
%ignore Strigi::FieldProperties::Localized;
%ignore Strigi::FieldProperties::operator=(const FieldProperties&);
%ignore Strigi::FieldRegister::fields;
%ignore Strigi::RegisteredField::writerData;
%ignore Strigi::RegisteredField::setWriterData;
%ignore Strigi::FieldProperties::locales; //TODO: causes segfault
%ignore Strigi::FieldProperties::localizedName; //TODO: causes segfault
%ignore Strigi::FieldProperties::localizedDescription; //TODO: causes segfault
%include "strigi/fieldproperties.h"
%include "strigi/fieldtypes.h"
%template (RegisteredFieldVector) std::vector<const Strigi::RegisteredField*>;


#############################
# StreamAnalyzer stuff
#############################
%ignore Strigi::StreamAnalyzer::indexFile;
%ignore Strigi::StreamAnalyzer::analyze;
%ignore Strigi::StreamAnalyzer::configuration;
%ignore Strigi::StreamAnalyzer::setIndexWriter(IndexWriter& writer);

//TODO: testme:
%ignore Strigi::StreamEndAnalyzerFactory::analyzesSubStreams;

%extend Strigi::StreamAnalyzer {
  void setIndexWriter(PythonIndexWriter& writer){
    $self->setIndexWriter((IndexWriter&)writer);
  }
}

%define DEFINE_ANALYZER(type)
  ADD_DOWNCAST_METHODS(type ## Factory)
  %feature("director") type ## Factory;
  %feature("director") type;
  %newobject type ## Factory::newInstance;
%enddef
DEFINE_ANALYZER(StreamEndAnalyzer)
DEFINE_ANALYZER(StreamEventAnalyzer)
DEFINE_ANALYZER(StreamLineAnalyzer)
DEFINE_ANALYZER(StreamSaxAnalyzer)
DEFINE_ANALYZER(StreamThroughAnalyzer)

%typemap(directorin) (const char* header, int32_t headersize) %{
  $input = Py_BuildValue("s#", $1_name, $2_name);
%}
%typemap(directorin) (const char* data, uint32_t length) %{
  $input = Py_BuildValue("s#", $1_name, $2_name);
%}
%typemap(directorin) (int nb_namespaces, const char** namespaces) %{
  $input = PyTuple_New($1_name);
  for ( int i=0;i<$1_name;i++ ) PyTuple_SetItem($input,i,Py_BuildValue("{s:s}", $2_name[i*2], $2_name[i*2+1]));
%}
%typemap(directorin) (int nb_attributes,int nb_defaulted, const char** attributes) %{
  $input = PyTuple_New($1_name);
  for ( int i=0;i<$1_name;i++ ){
    PyObject* $input_tmp = PyDict_New();
    
    PyDict_SetItemString($input_tmp, "localName", Py_BuildValue("s", $3_name[i * 5 + 0]));
    PyDict_SetItemString($input_tmp, "prefix", Py_BuildValue("s", $3_name[i * 5 + 1]));
    PyDict_SetItemString($input_tmp, "uri", Py_BuildValue("s", $3_name[i * 5 + 2]));
    PyDict_SetItemString($input_tmp, "value", Py_BuildValue("s#", $3_name[i * 5 + 3], $3_name[i * 5 + 4]-$3_name[i * 5 + 3]));

    PyTuple_SetItem($input,i, $input_tmp);
    //Py_DECREF($input_tmp);
  }
  //printf("DEFAULTED: %d ATTRIBS: %d\n", $2_name, $1_name);
%}


%include "strigi/streamanalyzer.h"
%include "strigi/streamanalyzerfactory.h"
%include "strigi/streamendanalyzer.h"
%include "strigi/streameventanalyzer.h"
%include "strigi/streamlineanalyzer.h"
%include "strigi/streamsaxanalyzer.h"
%include "strigi/streamthroughanalyzer.h"

##########################################################
# A cut down version of AnalysisResult
# The client will implement their own IndexWriter version
# which can do all of this...
##########################################################
//this shouldn't be necessary:
%ignore Strigi::AnalysisResult::indexChild;
%ignore Strigi::AnalysisResult::endAnalyzer;
%ignore Strigi::AnalysisResult::writerData;
%ignore Strigi::AnalysisResult::setWriterData;
%ignore Strigi::AnalysisResult::setId;
%ignore Strigi::AnalysisResult::id;
%ignore Strigi::AnalysisResult::parent;
%ignore Strigi::AnalysisResult::config;
%ignore Strigi::AnalysisResult::addValue(RegisteredField*field, const std::string& name, const std::string& value);
%ignore Strigi::AnalysisResult::addValue(const RegisteredField* field, const char* data, uint32_t length);
%ignore Strigi::AnalysisResult::addValue(const RegisteredField* field, uint32_t value);

//use PythonIndexWriter:
%extend Strigi::AnalysisResult{
  AnalysisResult(const std::string& p, time_t mt, PythonIndexWriter& w, Strigi::StreamAnalyzer& analyzer, const std::string& parent){
    return new AnalysisResult(p, mt, w, analyzer, parent);
  }
  void addText(const std::string& text){
    $self->addText(text.c_str(), text.length());
  }
}
%ignore Strigi::AnalysisResult::addText;
%ignore Strigi::AnalysisResult::AnalysisResult;
%include "strigi/analysisresult.h"

#############################
# The index config director
#############################
#TODO: this is confusing, PythonAnalyzerConfiguration already exists...
%feature("director") Strigi::AnalyzerConfiguration;
%ignore Strigi::AnalyzerConfiguration::FieldType;
%ignore Strigi::AnalyzerConfiguration::setFilters;
%ignore Strigi::AnalyzerConfiguration::indexType;
%ignore Strigi::AnalyzerConfiguration::setFilters;
%ignore Strigi::AnalyzerConfiguration::filters;
%ignore Strigi::AnalyzerConfiguration::fieldRegister;
%ignore Strigi::AnalyzerConfiguration::maximalStreamReadLength;
%include "strigi/analyzerconfiguration.h"

#############################
# The index writer director
#############################
%include "strigi/pythonindexwriter.h"

#############################
# The index manager director
#############################
%include "strigi/pythonindexmanager.h"

