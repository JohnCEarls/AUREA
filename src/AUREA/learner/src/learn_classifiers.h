#ifndef LEARN_CLASSIFIERS_H
#define LEARN_CLASSIFIERS_H
#include <cstddef>
#include "utils.h"
#include <vector>
#include <cmath>

#include <algorithm>
#include <sstream>
#include <iostream>
#include <vector>

#include "utils.h"
#include "order.h"
#include "wilcoxon.h"
#include "matrix.h"

//extern "C" {
  void learn_utsp_classifier(std::vector<double> & data,int dsSize, std::vector<int> & classSizes, std::vector<int> & nvec,  vector<int> & I1LIST, vector<int> & I2LIST );

//    SEXP learn_mtsp_classifier(SEXP,SEXP,SEXP);
  std::vector< std::vector<double> > learn_tst_classifier(std::vector<double> & data,int dsSize, std::vector<int> & classSizes, std::vector<int> & nvec, std::vector<int> & I1LIST, std::vector<int> & I2LIST, std::vector<int> & I3LIST );

  //added by j.e. in order to allow before running testing of how big
    // tsp and tst will get
  void wilcoxon_test(std::vector<double>& data,int numGenes, int size_c1, int size_c2, std::vector<double> & scores); 

//}
#endif
