#include "learn_classifiers.h"
#include "kfold.h"
void runTSP(std::vector<double> & data, int dsSize, vector<int> & classSizes, vector<int> & nvec, std::vector<int> & I1LIST, std::vector<int> & I2LIST ){
    learn_utsp_classifier( data, dsSize,  classSizes,  nvec, I1LIST, I2LIST);
}
/**
Returns the percent correct using k-fold crossvalidation (given k)
**/
double crossValidate(std::vector<double> & data, int dsSize, std::vector<int> & classSizes, std::vector<int> & nvec, int k){
    kfold kfGen(data, dsSize, classSizes, k);
    vector<double> * ts;
    vector<double> * ls;
    int numCorrect = 0;
    ts = kfGen.getNextTrainingSet();
    while(ts!=NULL){//for each training set
        vector<int> I1List;
        vector<int> I2List;
        vector<int> tsCs = kfGen.getClassSizes();
        runTSP( (*ts),dsSize,tsCs,nvec,I1List, I2List);
        ls = kfGen.getNextTestVector();
        while(ls != NULL){//for each learned vector
            double sum = 0.0;
            for(int i=0;i<I1List.size();i++){
                if(ls->at(I1List[i]) < ls->at(I2List[i])){
                    sum += 1.0;
                } else if (ls->at(I1List[i]) == ls->at(I2List[i])){
                    sum += 0.5;//tie, Hulk sad :(
                }
            }
            int classifyAs = 0;
            if(2*sum > I1List.size()){
                classifyAs = 1; 
            }
            if (kfGen.getTestVectorClass() == classifyAs){
                numCorrect++;
            }
            ls = kfGen.getNextTestVector();


        }
        ts = kfGen.getNextTrainingSet();
    }
    return (double)numCorrect/(double)(classSizes[0] + classSizes[1]);
    
}

