#ifndef DIRAC_PYWRAPPER_H
#define DIRAC_PYWRAPPER_H

#include <vector>
#include "kfold.h"
//using std::vector;
void runDirac(std::vector<double> & data, int dsSize, std::vector<int> & classSizes,
            std::vector<int> & geneNet, std::vector<int> & geneNetSize,
            std::vector<bool> & returnRankMat, std::vector<double> & returnRMS,
            std::vector<double> & returnRankConservation );

int classify( std::vector<bool> & rankMatrix, int class1Size, int class2size,
            std::vector<double> & unclassifiedVector, std::vector<int> & geneNet,
            int geneNetRankStart, int geneNetRankSize, int geneNetStart,
            int geneNetSize, std::vector<double> & score);

double crossValidate(std::vector<double> & data, int dsSize,
        std::vector<int> & classSizes,std::vector<int> & geneNet,
        std::vector<int> & geneNetSize,
        int numTopNetworks, int k);
#endif
 
