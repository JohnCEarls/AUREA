%module tsp
#define PySwigIterator tsp_PySwigIterator

%{
    #include "TSP_pywrapper.h"
%}

%include stl.i
namespace std {
    %template(IntVector) vector<int>;
    %template(DoubleVector) vector<double>;
}

%include "TSP_pywrapper.h"

%include tsp_supp.py
