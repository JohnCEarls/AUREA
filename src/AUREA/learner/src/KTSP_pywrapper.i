%module ktsp
#define PySwigIterator ktsp_PySwigIterator

%{
    #include "KTSP_pywrapper.h"
%}

%include stl.i
namespace std {
    %template(IntVector) vector<int>;
    %template(DoubleVector) vector<double>;
}

%include "KTSP_pywrapper.h"

%include "ktsp_supp.py"
