%{
  #include "strigi/streambase.h"
  #include "strigi/substreamprovider.h"

  #include "strigi/stringstream.h"
  #include "strigi/stringterminatedsubstream.h"
  #include "strigi/inputstreamreader.h"
  #include "strigi/fileinputstream.h"
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
%ignore Strigi::StreamBase::read(const T*& start, int32_t min, int32_t max);

//now include base files
%include "strigi/streambase.h"
%template (InputStream) Strigi::StreamBase<char>;
%template (Reader) Strigi::StreamBase<wchar_t>;

%newobject Strigi::StreamBase<char>::openFile;
%extend Strigi::StreamBase<char> {
  static InputStream* openFile(const char* path){
    return new Strigi::FileInputStream(path);
  }
  
  PyObject* read(int32_t min, int32_t max){
    const char* buf;
    int32_t read = $self->read(buf, min, max);
    return Py_BuildValue("s#", buf, read);
  }
}

