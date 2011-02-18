%module wilcoxon 
#define PySwigIterator wilcoxon_PySwigIterator

%{
    #include "WILCOXON_pywrapper.h"
%}

%include stl.i
namespace std {
    %template(IntVector) vector<int>;
    %template(DoubleVector) vector<double>;
}

%include "WILCOXON_pywrapper.h"

%include wilcoxon_supp.py
