#ifndef UTILS_H
#define UTILS_H

#include <cstddef>
#include <algorithm>
#include <sstream>
#include <iostream>
#include <vector>
#include <cmath>
/**
# include <R.h>
# include <Rinternals.h>
# include <Rdefines.h>
# include <Rmath.h>
**/
using namespace std;

//
// Convert an R matrix to a CPP matrix (by col)
//
//vector< vector<double> > Rmatrix_to_CPP_matrix(SEXP);


//put data from data into xmat
void vector_to_matrix( vector<double> & data, vector< vector<double> > & xmat);

double compute_pair_score(vector< vector<double> > &, vector<int> &, int, int);
double compute_triple_score(vector< vector<double> > &, vector<int> &, int, int, int);
double compute_triple_secondary_score(vector< vector<double> > &, vector<int> &, int, int, int);
//
// Compute the probability table for a pair.
//
vector< vector<double> > compute_pair_ptable(vector< vector<double> > &, vector<int> &, int,int);
//
// Compute the probability table for a triple.
//
vector< vector<double> > compute_triple_ptable(vector< vector<double> > &, vector<int> &, int,int, int);

//
// Given a 2-tuple prob table compute the sum of absolute diff's of probs
//
double compute_score_from_pair_ptable(vector< vector<double> > &);
//
// Given a 3-tuple prob table compute the sum of absolute diff's of probs
//
double compute_score_from_triple_ptable(vector< vector<double> > &);

#endif
