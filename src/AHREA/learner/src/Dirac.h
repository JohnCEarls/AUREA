#ifndef DIRAC_H
#define DIRAC_H

#include <vector>
#include <string>
#include "Matrix.h"

using std::vector;

class Dirac{
    public:
        Dirac();
        //this is the function called by python
        //see the .cpp file for a complete description of variables
        void enter( vector<double> & data, int dsSize, vector<int> & classSizes, 
            vector<int> & geneNet, vector<int> & geneNetSize,
            vector<bool> & returnRankMat, vector<double> & returnRMS, 
            vector<double> & returnRankConservation);
        //returns 0 for class 1, 1 for class 2
        //takes a pregenerated rankMatrix, some info describing the problem
        //and classifies the given unclassifiedVector
        int classify( vector<bool> & rankMatrix, int class1Size, int class2size,
            vector<double> & unclassifiedVector, vector<int> & geneNet,
            int geneNetRankStart, int geneNetRankSize, int geneNetStart, 
            int geneNetSize, vector<double> & score );
        //Given a network id, return the number of elements before 
        //that network in a rank vector/matrix.
        int getNetworkRankStart(int network_id, vector<int> & geneNetSize);
        //nChoose2 of gene network [network_id] size
        int getNetworkRankSize(int network_id, vector<int> & geneNetSize);
        int getNetworkStart(int network_id, vector<int> & geneNetSize);
        vector<int> getTopNetworks(int numTopNets, vector<double> & rankMatchingScores, int class1Size, int class2Size);

    private:
        void generateRankedSet(Matrix<double> & dataMat, int s, int e, 
            vector<int> & geneNet, int gs, int ge, Matrix<bool> & rankMat, 
            int rmcs, int rmrs);
        void generateRankTemplate(Matrix<bool> & rankedSet, vector<int> & classSizes);
        float generateRankConservationIndex(vector<double> & rms);
        int nChooseTwo(int n);
        Matrix<bool> * initRankMatrix(vector<bool> & returnRankMatrix, vector<int> & classSizes, 
            vector<int> & geneNetSize, Matrix<int> *& matMask);
        Matrix<double> * initDataMatrix( vector<double> & data, int dsSize, 
            vector<int> & classSizes);
        void generateRankMatchingScore(Matrix<bool> & rankedSet,Matrix<int> & matrixMask,
            int numClasses, int numsamples, int numGeneNetworks, vector<double> & R );
        void generateRankConservationIndex( Matrix<double> & rmsMat, Matrix<int> & matrixMask, 
            vector<double> & returnRankConservation);
};
#endif
