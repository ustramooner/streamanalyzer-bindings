%{
  #include "strigi/analyzerconfiguration.h"
  #include "strigi/analysisresult.h"
  #include "strigi/streamanalyzer.h"
  #include "strigi/indexwriter.h"
  #include "strigi/pythonindexwriter.h"
  #include "strigi/indexmanager.h"
  #include "strigi/pythonindexmanager.h"
  #include "strigi/diranalyzer.h"
  #include "strigi/pythondiranalyzer.h"
%}


//make swig work...
#define STREAMANALYZER_EXPORT

%ignore Strigi::FieldProperties::FieldProperties;
%ignore Strigi::FieldProperties::Localized;
%ignore Strigi::FieldProperties::operator=(const FieldProperties&);
%ignore Strigi::FieldRegister::fields;
//%ignore Strigi::FieldProperties::compressed;
//%ignore Strigi::FieldProperties::indexed;
//%ignore Strigi::FieldProperties::stored;
//%ignore Strigi::FieldProperties::tokenized;
%ignore Strigi::RegisteredField::writerData;
%ignore Strigi::RegisteredField::setWriterData;
%ignore Strigi::FieldRegister;
%ignore Strigi::FieldProperties::locales; //TODO: causes segfault
%ignore Strigi::FieldProperties::localizedName; //TODO: causes segfault
%ignore Strigi::FieldProperties::localizedDescription; //TODO: causes segfault
%include "strigi/fieldproperties.h"
%include "strigi/fieldtypes.h"
%template (RegisteredFieldVector) std::vector<const Strigi::RegisteredField*>;


%ignore Strigi::StreamAnalyzerFactory::registerFields;
%ignore Strigi::StreamAnalyzerFactory::addField;
%ignore Strigi::StreamAnalyzer;
%ignore Strigi::StreamEndAnalyzer;
%ignore Strigi::StreamEventAnalyzer;
%ignore Strigi::StreamLineAnalyzer;
%ignore Strigi::StreamSaxAnalyzer;
%ignore Strigi::StreamThroughAnalyzer;
%ignore Strigi::StreamAnalyzerFactory::newInstance;
%ignore Strigi::StreamEndAnalyzerFactory::newInstance;
%ignore Strigi::StreamEventAnalyzerFactory::newInstance;
%ignore Strigi::StreamLineAnalyzerFactory::newInstance;
%ignore Strigi::StreamSaxAnalyzerFactory::newInstance;
%ignore Strigi::StreamThroughAnalyzerFactory::newInstance;
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
%ignore Strigi::AnalysisResult::index;
%ignore Strigi::AnalysisResult::indexChild;
%ignore Strigi::AnalysisResult::addText;
%ignore Strigi::AnalysisResult::addValue;
%ignore Strigi::AnalysisResult::addTriplet;
%ignore Strigi::AnalysisResult::setEncoding;
%ignore Strigi::AnalysisResult::setMimeType;
%ignore Strigi::AnalysisResult::newAnonymousUri;
%ignore Strigi::AnalysisResult::endAnalyzer;
%ignore Strigi::AnalysisResult::AnalysisResult;
%ignore Strigi::AnalysisResult::writerData;
%ignore Strigi::AnalysisResult::setWriterData;
%ignore Strigi::AnalysisResult::setId;
%ignore Strigi::AnalysisResult::id;
%ignore Strigi::AnalysisResult::parent;
%include "strigi/analysisresult.h"


#############################
# The index config director
#############################
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


################################
# A dir analyzer which can stop
################################
%include "strigi/pythondiranalyzer.h"

