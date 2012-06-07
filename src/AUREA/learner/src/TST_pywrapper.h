#ifndef TST_PYWRAPPER_H
#define TST_PYWRAPPER_H

#include <cstddef>
#include "learn_classifiers.h"
#include <vector>
void runTST(std::vector<double> & data, int dsSize, std::vector<int> & classSizes, std::vector<int> & nvec, std::vector<int> & I1LIST, std::vector<int> & I2LIST, std::vector<int> & I3LIST );
double crossValidate(std::vector<double> & data, int dsSize, std::vector<int> & classSizes, std::vector<int> & nvec, int k );

#endif
