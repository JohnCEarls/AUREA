%module dirac
#define PySwigIterator dirac_PySwigIterator
%{
    #include "Dirac_pywrapper.h"
%}

%include stl.i
namespace std {
    %template(IntVector) vector<int>;
    %template(DoubleVector) vector<double>;
    %template(BoolVector) vector<bool>;
}

%include "Dirac_pywrapper.h"

%include "dirac_supp.py"

