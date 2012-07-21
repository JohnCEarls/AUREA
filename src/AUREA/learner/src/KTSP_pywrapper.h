#ifndef KTSP_PYWRAPPER_H
#define KTSP_PYWRAPPER_H
#include "Ktsp.h"
#include <vector>
#include <cstddef>
void runKTSP(std::vector<double> & data, int nGenes, std::vector<int> & classSizes,std::vector<int> filters, int maxK, int n, int m, std::vector<int> & topKPairs);

double crossValidate( std::vector<double> & data, int nGenes, std::vector<int> & classSizes, std::vector<int> filters, int maxK, int n, int m, int kFoldk,std::vector<int> & truth_table, bool use_accuracy = false);

#endif
