#ifndef wilcoxon_H
#define wilcoxon_H

#include <vector>
#include <cmath>
#include "order.h"

using namespace std;

double wilcoxon_test_statistic(const vector<double> &, const vector<double> &);
double wilcoxon_two_sided_test_statistic(const vector<double> &, const vector<double> &);
double wilcoxon_two_sided_test_statistic(const vector<double> &, const vector<int> &);

#endif
