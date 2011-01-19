%{
  #include "strigi/streambase.h"
  #include "strigi/substreamprovider.h"

  #include "strigi/stringstream.h"
  #include "strigi/stringterminatedsubstream.h"
  #include "strigi/inputstreamreader.h"
  #include "strigi/stringterminatedsubstream.h"

  #include "strigi/substreamproviderprovider.h"
  #include "strigi/archivereader.h"
%}

%{
	//stuff that goes in the wrapper
%}

//make swig work...
#define STREAMS_EXPORT

//non-templated base class
%rename (StreamsBase) Strigi::StreamBaseBase;
//now include base files
%include "strigi/streambase.h"
%template (InputStream) Strigi::StreamBase<char>;
%template (Reader) Strigi::StreamBase<wchar_t>;

