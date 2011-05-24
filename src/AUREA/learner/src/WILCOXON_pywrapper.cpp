#include "learn_classifiers.h"

void runWilcoxonTest(std::vector<double> & data, int numGenes, int size_c1, int size_c2, std::vector<double> & scores){
    wilcoxon_test( data, numGenes, size_c1, size_c2, scores); 

}

