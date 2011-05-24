#include "learn_classifiers.h"
#include "wilcoxon_test.h"
#include <vector>
using std::vector;
/**
*
* This method returns via the parameter scores the vector of wilcoxon scores.
* This goes through the data and returns a vector of scores saying how differentially
* expressed each gene is.
*
* Heavily ripped off from learn_tst_classifier.cpp
*
**/
void wilcoxon_test(vector<double>& data,int numGenes, int size_c1, int size_c2, vector<double> & scores){
    if (scores.size() < numGenes){
        scores.resize(numGenes);
    }
    int nsamples = size_c1 + size_c2;
    vector< vector<double> > xmat(nsamples, vector<double>(numGenes));
    vector_to_matrix(data, xmat);
 
    //make rank matrix
    vector< vector<double> > rank_mat(nsamples);
    for(int i=0;i<nsamples;i++){
        compute_ranks(xmat[i], rank_mat[i]);
    }
    
    for(int i=0;i<numGenes;i++){
        vector<double> u0;
        vector<double> u1;
        //class 1 gene i goes in u0
        for(int j=0;j<size_c1;j++) u0.push_back(rank_mat[j][i]);
        //class 2 gene i goes in u1
        for(int j=size_c1;j<nsamples;j++) u1.push_back(rank_mat[j][i]);
        //now see if gene i from c1 and c2 are differentially expressed
        scores[i] = wilcoxon_two_sided_test_statistic(u0, u1);
    }
    //score is returned via paramerters
}
