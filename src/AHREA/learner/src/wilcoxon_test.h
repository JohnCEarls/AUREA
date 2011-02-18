#ifndef WILCOXON_TEST
#define WILCOXON_TEST
#include <vector>
extern "C"{

void wilcoxon_test(std::vector<double>& data,int numGenes, 
int size_c1, int size_c2, std::vector<double> & scores);
}
#endif

