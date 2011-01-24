%include <std_common.i>
%include <std_vector.i>
%include <std_map.i>
%include <std_except.i>
%include <std_string.i>
%include <stl.i>

typedef signed char int8_t;
typedef unsigned char uint8_t;
typedef short int16_t;
typedef unsigned short uint16_t;
typedef int int32_t;
typedef unsigned int uint32_t;
typedef long int64_t;
typedef unsigned long uint64_t;
%apply long long {long};
typedef unsigned long time_t;
%template (StringList) std::vector<std::string>;

//definitions for Char stuff...
%include "Chars.i"
%include "Exceptions.i"
%include "StreamsChar.i"
%include "StreamsWChar.i"

%include "libstreams.i"
%include "libstreamanalyzer.i"

