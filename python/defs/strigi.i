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

