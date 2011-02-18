%module tst
#define PySwigIterator tst_PySwigIterator

%{
    #include "TST_pywrapper.h"
%}

%include stl.i
namespace std {
    %template(IntVector) vector<int>;
    %template(DoubleVector) vector<double>;
}

%include "TST_pywrapper.h"

%include tst_supp.py
