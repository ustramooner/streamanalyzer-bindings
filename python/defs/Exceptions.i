%feature("director:except") {
    if ($error != NULL) throw Swig::DirectorMethodException();
}
%{
	//we need to fool the swig preprocessor, otherwise it expands these directives
	 #define ___FILE___ __FILE__
	 #define ___LINE___ __LINE__

	  //TODO: use approperiate error
	  
	 	#define _CATCHALL() \
  	  catch (std::exception& e) { \
			  char buf[250]; \
			  snprintf(buf,250,"std exception %s in %s at %d", e.what(), ___FILE___,___LINE___); \
        PyErr_SetString(PyExc_RuntimeError,buf); \
			  return NULL; \
	    } catch (Swig::DirectorException &e) { \
        SWIG_fail; \
      }
%}

//the exception handler...
%exception {
  try {
		$function
  }_CATCHALL();
}

