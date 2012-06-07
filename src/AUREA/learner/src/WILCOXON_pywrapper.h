#ifndef WILCOXON_H
#define WILCOXON_H
#include <cstddef>
#include "learn_classifiers.h"
#include <vector>
void runWilcoxonTest(std::vector<double> & data, int numGenes, int size_c1, int size_c2, std::vector<double> & scores);
#endif
