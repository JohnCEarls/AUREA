#include "learn_classifiers.h"
#include "kfold.h"
#include <math.h>
#include <iostream>

void runTST(std::vector<double> & data, int dsSize, std::vector<int> & classSizes, std::vector<int> & nvec, std::vector<int> & I1LIST, std::vector<int> & I2LIST, std::vector<int> & I3LIST ){
    bool hard_limit = false;
    if(classSizes[0] + classSizes[1] < 20){
        hard_limit = true;
    }
    
    learn_tst_classifier( data, dsSize,  classSizes,  nvec,I1LIST,I2LIST,I3LIST, hard_limit );
}

//build the scores on a single sample
std::vector<double> sample_ptable(std::vector<double> &xmat, int i1, int i2, int i3){
    int icount = 0;
    //mostly copied from utils
    std::vector<double> tcolct(6);
    for(int i=0;i<6;i++) tcolct[i]=0;
    if ((xmat[i1]<=xmat[i2])&&(xmat[i2]<=xmat[i3]))
    {
      tcolct[0]=1;
      icount++;
    }
      if ((xmat[i1]<=xmat[i3])&&(xmat[i3]<=xmat[i2]))
    {
      tcolct[1]=1;
      icount++;
    }
      if ((xmat[i2]<=xmat[i1])&&(xmat[i1]<=xmat[i3]))
    {
      tcolct[2]=1;
      icount++;
    }
      if ((xmat[i2]<=xmat[i3])&&(xmat[i3]<=xmat[i1]))
    {
      tcolct[3]=1;
      icount++;
    }
      if ((xmat[i3]<=xmat[i1])&&(xmat[i1]<=xmat[i2]))
    {
      tcolct[4]=1;
      icount++;
    }
      if ((xmat[i3]<=xmat[i2])&&(xmat[i2]<=xmat[i1]))
    {
      tcolct[5]=1;
      icount++;
    }
     for (int i=0;i<6;i++)
    {
      tcolct[i]/=(double)icount;
    }
    return tcolct;

}




double crossValidate(std::vector<double> & data, int dsSize, std::vector<int> & classSizes, std::vector<int> & nvec, int k,std::vector<int> & truth_table, bool use_accuracy){
    kfold kfGen(data, dsSize, classSizes, k);
    
    vector<double> * ts;
    vector<double> * ls;
    //let class 1 be positive [0]
    int truePositive = 0;
    int falsePositive = 0;
    //let class 2 be negative [1]
    int trueNegative = 0;
    int falseNegative = 0;

    //  int numCorrect = 0;
    ts = kfGen.getNextTrainingSet();
    while(ts!=NULL){//for each training set
        std::vector<int> I1List;
        std::vector<int> I2List;
        std::vector<int> I3List;
        std::vector<int> tsCs = kfGen.getClassSizes();

        vector<int> y;
        for(int i=0;i<tsCs[0];i++) y.push_back(0);
        for(int i=0;i<tsCs[1];i++) y.push_back(1);
        std::vector< std::vector<double> > xmat = learn_tst_classifier( (*ts), dsSize,  tsCs,  nvec,I1List,I2List,I3List, true);    
        ls = kfGen.getNextTestVector();
        while(ls != NULL){//for each learned vector
            double sum = 0.0;
            for(int i=0;i<I1List.size();i++){
                int i1=I1List[i];
                int i2=I2List[i];
                int i3=I3List[i];
                //probability table for each ordering
                std::vector< std::vector<double> > ftab=compute_triple_ptable(xmat,y,i1,i2,i3);
                //weight vector for observed ordering
                //mainly necessary to deal with ties,  if you have a tie
                //you give a uniform proportion of the probability to
                //each valid ordering
                std::vector<double> stab = sample_ptable((*ls), i1, i2, i3);
                double d1 = 0.0;
                double d2 = 0.0;
                for(int j=0;j<6;j++){
                    d1 +=  (stab[j] * ftab[0][j]);
                    d2 +=  (stab[j] * ftab[1][j]);
                }
                if(d1<d2){
                    sum += 1.0;
                } else if (d1==d2){
                    sum += .5;//tie
                }
            }
            int classifyAs = 0;
            if(2*sum > I1List.size()){
                classifyAs = 1;
            }
            int actual_class = kfGen.getTestVectorClass();
            //could put directly in truth_table but this is clearer
            if (actual_class == 0 && classifyAs == 0) truePositive++;
            if (actual_class == 0 && classifyAs == 1) falseNegative++;
            if (actual_class == 1 && classifyAs == 0) falsePositive++;
            if (actual_class == 1 && classifyAs == 1) trueNegative++;

            ls = kfGen.getNextTestVector();
        }
        ts = kfGen.getNextTrainingSet();
    }//for each training set

    double numerator, denominator;
    if(use_accuracy){
        //return accuracy not MCC
        numerator = truePositive + trueNegative;
        denominator = truePositive + trueNegative + falsePositive + falseNegative;
    } else{

        numerator =  ((truePositive*trueNegative) - (falsePositive*falseNegative));
        denominator = sqrt((double)
        ((truePositive+falsePositive )* (truePositive+falseNegative) *
        (trueNegative+falsePositive ) * (trueNegative+falseNegative))
        );
    }
    truth_table[0] =  truePositive;
    truth_table[1] = trueNegative;
    truth_table[2] = falsePositive;
    truth_table[3] = falseNegative;
    if (denominator == 0.0) denominator = 1;
    return numerator/denominator; 
     //return (double)numCorrect/(double)(classSizes[0] + classSizes[1]);   
}
