#include "KTSP_pywrapper.h"
#include "kfold.h"
#include "iostream"
#include <math.h>
using std::cout;
using std::endl;

void runKTSP(std::vector<double> & data, int nGenes, std::vector<int> & classSizes,vector<int> filters, int maxK, int n, int m, std::vector<int> & topKPairs){
    Ktsp ourKtsp( data, nGenes, classSizes,filters,maxK, n, m);
    ourKtsp.getTopK( topKPairs );
}

double crossValidate( std::vector<double> & data, int nGenes, std::vector<int> & classSizes,vector<int> filters, int maxK, int n, int m, int kFoldk, bool use_accuracy){
    kfold kfGen(data, nGenes, classSizes, kFoldk);
    vector<double> * ts;
    vector<double> * ls;
    //moving to a Matthews correlation coefficient
    //let class 1 be positive [0]
    int truePositive = 0;
    int falsePositive = 0;
    //let class 2 be negative [1]
    int trueNegative = 0;
    int falseNegative = 0;

   int numCorrect = 0;
    ts = kfGen.getNextTrainingSet();
    while(ts!=NULL){//for each training set
        vector<int> topKPairs;
        vector<int> tsCs = kfGen.getClassSizes();
        runKTSP( (*ts),nGenes,tsCs,filters, maxK,n,m,topKPairs);
        ls = kfGen.getNextTestVector();
        while(ls != NULL){//for each learned vector
            double sum = 0.0;
            for(int i=1;i<(int)topKPairs.size();i+=2){
                int index1, index2;
                if (i%2 == 1){
                    index1 = topKPairs[i-1];
                    index2 = topKPairs[i];
                    if(ls->at(index1) > ls->at(index2)){
                        sum += 1.0;
                    } else if (ls->at(index1) == ls->at(index2)){
                        sum += 0.5;//tie, Hulk sad :(
                    }
                }
            }
            int classifyAs = 0;
            if(2*sum > topKPairs.size()/2){
                classifyAs = 1; 
            }
            int actual_class = kfGen.getTestVectorClass();
            if (actual_class == 0 && classifyAs == 0) truePositive++;
            if (actual_class == 0 && classifyAs == 1) falseNegative++;
            if (actual_class == 1 && classifyAs == 0) falsePositive++;
            if (actual_class == 1 && classifyAs == 1) trueNegative++;
            /**
          if (kfGen.getTestVectorClass() == classifyAs){
                numCorrect++;
            }**/
            ls = kfGen.getNextTestVector();


        }
        ts = kfGen.getNextTrainingSet();
    }
    double numerator, denominator;
    if(use_accuracy){
        //return accuracy not MCC
        numerator = truePositive + trueNegative;
        denominator = truePositive + trueNegative + falsePositive + falseNegative;

    } else {
        numerator =  ((truePositive*trueNegative) - (falsePositive*falseNegative));
        denominator = sqrt((double)
        ((truePositive+falsePositive )* (truePositive+falseNegative) *
        (trueNegative+falsePositive ) * (trueNegative+falseNegative))
    );
    }
    if (denominator == 0.0) denominator = 1;
    
    return numerator/denominator; 

    //return (double)numCorrect/(double)(classSizes[0] + classSizes[1]);
}
