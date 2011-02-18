#ifndef TSP_PYWRAPPER_H
#define TSP_PYWRAPPER_H

#include "learn_classifiers.h"
#include <vector>

void runTSP(std::vector<double> & data, int dsSize, std::vector<int> & classSizes, std::vector<int> & nvec , std::vector<int> & I1LIST, std::vector<int> & I2LIST );

double crossValidate(std::vector<double> & data, int dsSize, std::vector<int> & classSizes, std::vector<int> & nvec, int k);
#endif
