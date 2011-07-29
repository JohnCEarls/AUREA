#include  <string>
#include <vector>
#include "/home/earls3/Price/AUREA/src/AUREA/learner/src/kfold.h"
#include <iostream>
using namespace std;
//g++ testKfold.cpp /home/earls3/Price/AUREA/src/AUREA/learner/src/kfold.cpp

vector<double> generateData(int numGenes, int class1, int class2){
    //create vector with doubles where number before decimal is sample number
    //and after is the gene number
    cout << "generating data vector" << endl;
    vector<double> data(numGenes*(class1+class2));
    for(unsigned int samp = 0; samp< class1+class2;samp++){
        for(unsigned int gene = 0; gene<numGenes; gene++){
            data.at(samp*numGenes + gene) = (double)samp + (double)gene/(double)numGenes;
        }
        
    }
    return data;

}
bool allThere(vector<double> training, vector<double> test, int numsamples, int numgenes){
    bool allthere = true;
    if (training.size() + test.size() != numsamples * numgenes){
        cout << "Error: wrong sized test or training"<<endl;
        allthere = false;
    }

    int * samples = new int[numsamples];
    for(int i=0;i<numsamples;i++) samples[i] = 0;
    for(unsigned int samp = 0; samp < training.size()/numgenes;samp++) samples[(int)training.at(samp*numgenes)] = 1;
    for(unsigned int samp = 0; samp < test.size()/numgenes;samp++) samples[(int)test.at(samp*numgenes)] = 1;
    for(int i = 0;i<numsamples; i++) allthere = allthere && samples[i];
    delete samples;
    return allthere;

}

bool checkClasses(vector<double> training, int numgenes, int class1, int class2){
    bool has1 = false;
    bool has2 = false;
    for(unsigned int samp = 0; samp < training.size();samp++)
        if ((int)training.at(samp) < class1)
           has1 = true;
        else
           has2 = true;


    return has1 && has2;

}

void printMatrix(vector<double> data, int numgenes){
    for (int i = 0; i<data.size(); i++){
        cout << data.at(i) << " ";
        if (! (i%numgenes))
            cout << endl;
    }
    cout << endl <<endl;
}

void appendVector(vector<double> & builtvector,vector<double> toAppend){
    for (int i=0;i<toAppend.size();i++){
        builtvector.push_back(toAppend[i]);
    }
}

bool testOne(int class1, int class2, int numgenes, int k){
    bool passed = true;
    cout << "init kfold tests" << endl;

    cout << "class1 = " << class1 << endl;
    cout << "class2 = " << class2 << endl;
    cout << "numgenes = " << numgenes << endl;
    cout << "k = " << k << endl;
    cout << endl;
    vector<double> data = generateData(numgenes, class1, class2);
    //printMatrix(data, numgenes);
    vector<double> * temp;
    vector<int> cSizes;
    cSizes.push_back(class1); cSizes.push_back( class2);
    //cout << "generating classes" << endl;
    kfold myk(data, numgenes, cSizes, 10);
    //cout << "making sets" << endl;
    int round = 0;
    while( temp = myk.getNextTrainingSet()){
        
        vector<double> train;
        vector<double> test;
        train = (*temp);
        while(temp = myk.getNextTestVector())
            appendVector(test,(*temp));

        //cout << "Checking if all there" << endl;
        
       if (! allThere(train, test, class1 + class2, numgenes)){
            cout<< "Error: Samples are missing from round: " << round << endl;
            passed = false;}
       if (! checkClasses(train, numgenes, class1, class2) ){
            cout << "Error: training set only contains 1 class from round: "  << round << endl;
            passed = false;}





       round++;

    }
     if (passed)
        cout << "This config passed" << endl;
    else
        cout << "This config did not pass" << endl;
    cout << "*********************************************" << endl<<endl;
    return passed;
}

int main(){
    bool passed = true;
    //bool testOne(int class1, int class2, int numgenes, int k){
    passed = testOne(1000, 1000, 10000, 10);
    passed = passed && testOne(10, 10000, 400, 10);
    passed = testOne(10, 10, 10000, 10);
    passed = passed && testOne(9, 10000, 400, 10);



    if (passed)
        cout << "***All tests passed" << endl;
    else
        cout << "---Not all tests passed" << endl;
}




