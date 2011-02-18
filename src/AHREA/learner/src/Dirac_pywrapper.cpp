#include <vector>
#include <iostream>
#include "Dirac.h"
#include "kfold.h"
using std::cout;
using std::endl;
void runDirac(std::vector<double> & data, int dsSize, std::vector<int> & classSizes,
            std::vector<int> & geneNet, std::vector<int> & geneNetSize,
            std::vector<bool> & returnRankMat, std::vector<double> & returnRMS,
            std::vector<double> & returnRankConservation){

    Dirac d;
    d.enter( data,  dsSize,  classSizes,
            geneNet, geneNetSize,
            returnRankMat, returnRMS,
            returnRankConservation);


}

int classify( std::vector<bool> & rankMatrix, int class1Size, int class2size,
            std::vector<double> & unclassifiedVector, std::vector<int> & geneNet,
            int geneNetRankStart, int geneNetRankSize, int geneNetStart,
            int geneNetSize, vector<double> & score){
    Dirac d;
    return d.classify( rankMatrix, class1Size, class2size, unclassifiedVector, 
            geneNet, geneNetRankStart, geneNetRankSize, geneNetStart,
            geneNetSize,score);

}


double crossValidate(std::vector<double> & data, int dsSize, 
        std::vector<int> & classSizes,std::vector<int> & geneNet, 
        std::vector<int> & geneNetSize,
        int numTopNetworks, int k){
    kfold kfGen(data, dsSize, classSizes, k);
    vector<double> * ts;
    vector<double> * ls;
    int numCorrect = 0;

    ts = kfGen.getNextTrainingSet();
    while(ts!=NULL){//for each training set
        //cout << "new training set"<<endl;
        vector<int> tsCs = kfGen.getClassSizes();
      
        vector<bool>  returnRankMat;
        vector<double>  returnRMS;
        vector<double>  returnRankConservation;
        runDirac( (*ts),dsSize,tsCs, geneNet, geneNetSize,returnRankMat, returnRMS, returnRankConservation );
        Dirac d;
        vector<int> topNets = d.getTopNetworks( numTopNetworks, returnRMS, tsCs[0], tsCs[1]);
                
        ls = kfGen.getNextTestVector();
        while(ls != NULL){//for each learned vector
            //cout <<"new learning set" << endl;
            double sum = 0.0;
            for(int i = 0; i<topNets.size();i++){
                int net_id = topNets[i];
                int net_rank_start = d.getNetworkRankStart(net_id, geneNetSize);
                int net_rank_size = d.getNetworkRankSize(net_id, geneNetSize);
                int net_start = d.getNetworkStart(net_id, geneNetSize);
                int net_size = geneNetSize[net_id];
                vector<double> score;
                sum += d.classify( returnRankMat, tsCs[0], tsCs[1], (*ls),geneNet, net_rank_start, net_rank_size, net_start, net_size, score);
                //cout << sum << endl;
                //cout << kfGen.getTestVectorClass() << endl;
               //cout << net_id<<endl;// = topNets[i];
                //cout << net_rank_start<<endl;// = d.getNetworkRankStart(net_id, geneNetSize);
                //cout << net_rank_size<<endl;// = d.getNetworkRankSize(net_id, geneNetSize);
                //cout << net_start<<endl;// = d.getNetworkStart(net_id, geneNetSize);
                //cout << net_size <<endl;
 
            }    

            int classifyAs = 0;
            if(2*sum > topNets.size()){
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

