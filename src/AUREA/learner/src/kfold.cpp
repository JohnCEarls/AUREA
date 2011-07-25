#include "kfold.h"
#include <vector>
#include <stdlib.h>
#include <time.h>
#include <iostream>
using std::vector;
using std::cout;
using std::endl;
/**
Class to generate the vectors from a dataset for kfold cross validation.
data is the whole dataset
numGenes is the number of rows
classSizes is a vector containing the 2 classSizes
k is the number of folds
**/
kfold::kfold( vector<double> & data, int numGenes, vector<int> & classSizes, int k){
    this->nGenes = numGenes;
    this->orig_data = &data;
    this->class1size = classSizes[0];
    this->class2size = classSizes[1];
    this->k = k;
    this->it = 0;
    this->samp_vector = generateSampleVector();
    this->next_fold = 0;
    this->generated_data = NULL;
    this->generated_test = NULL;
    this->curr_class = -1;
    this->curr_classSizes = classSizes;
}

kfold::~kfold(){
    delete generated_data;
    delete generated_test;
    orig_data = NULL;
}
/**
Generates a vector containing [0,...,n-1] that has been shuffled.
**/
vector<int> kfold::generateSampleVector(){
    
    srand(time(NULL));
    if (k > class1size + class2size){
        k = class1size + class2size;
        //k is bigger than our sample size, so lets do loocv        
    }
    vector<int> samples(class1size+class2size);
    for(int i = 0;i<class1size+class2size;i++){
        samples[i] = i;        
    }
    for(int i=class1size+class2size-1;i>0;i--){//fisher-yates shuffle
        int j = rand() % i;
        int temp = samples[i];
        samples[i] = samples[j];
        samples[j] = temp;
    }
    
    if (checkFoldsGood(samples)){
        return samples;
    } else {
        //all our pigeons are in the same hole.
        //shuffle shuffle
        return generateSampleVector();
    } 

}
/**
Checks that we will not have a training set without any samples for a class.

**/
bool kfold::checkFoldsGood( vector<int> & sample){
    int fsize = getFoldSize();
    
    bool good = true;

    if (class1size > fsize && class2size > fsize) return good;//shortcircuit pigeon
    int class1counter, class2counter;
    for( int i = 0; i < sample.size();i++ ){
        //the only way for this to happen is if all of one class ends up in a
        //fold
        if (i%fsize == 0){//new fold
           class1counter = 0;
           class2counter = 0;
        }
        //size of class[1||2] in this fold 
        if(sample.at(i) < class1size){//class1sample
            class1counter++;
        } else {//class2sample
            class2counter++;
        }
        if ((class1counter == class1size) 
            || (class2counter == class2size)){
            //Oh noes!!!!All our eggs are in one basket.
            good = false;
            break;
        }
     }
     return good;
}
/**
Returns a vector that contains the training set for the next set of learners
Returns null if there are no more training sets to be generated.

NOTE: on each call to this function the previous training set is deleted!!
You will need to copy the vector if you want to keep it.
**/
vector<double> * kfold::getNextTrainingSet(){
    next_fold = next_fold + getFoldSize();
    curr_classSizes[0] = 0;
    curr_classSizes[1] = 0;
    if (samp_vector.size() == it){
        
        return NULL;
    }
    delete generated_data;
    generated_data = new vector<double>();
    for(int base_i = 0; base_i<class1size+class2size;base_i++){
        if(trainingData(base_i) ){
            curr_classSizes[base_i >= class1size]++;        
            for(int j=0; j<nGenes;j++){
                generated_data->push_back(orig_data->at(base_i*nGenes + j));
            }
        }
    
    }
    if (next_fold > samp_vector.size()){
        next_fold = samp_vector.size();
    }
    return generated_data;
}
/**
Returns the current test vector.
Returns null if their are no more test vectors for the current training set

NOTE: on each call to this function the previous test vector is deleted!!
You will need to copy the vector if you want to keep it.
**/
vector<double> * kfold::getNextTestVector(){    
    delete generated_test;
    if(it == next_fold){
        curr_class = -1;
        generated_test = NULL;
        return NULL;
    }
    generated_test = new vector<double>();
    int next_sample = samp_vector[it];
    if (next_sample < class1size){
        curr_class = 0;
    } else {
        curr_class = 1;
    }
    int col = nGenes*next_sample;
    
    for(int i = 0; i<nGenes; i++){
        generated_test->push_back(orig_data->at(col + i));
    }
    it++;
   return generated_test;
}
vector<int> kfold::getClassSizes(){
    return curr_classSizes;
}

int kfold::getTestVectorClass(){
    return curr_class;
}
/**
Given a sample number
return true if sample is in training set
return false is sample is to be used for crossvalidation
**/
bool kfold::trainingData(int sample){
    int ksize = getFoldSize();
    int temp_it = it;
    for(int i=it; i < next_fold;i++){
        if(samp_vector[i] == sample){
            return false;
        }
    }
    return true;
}
int kfold::getFoldSize(){
    int ksize = (class1size+class2size)/k;
    if((class1size+class2size)%k > 0){
        ksize++;
    }
    return ksize; 
}
void printVect(vector<double> a, int rows){
    for(int i=0;i<a.size();i++){
        if (i%rows == 0){cout << endl;}
        cout << a.at(i) << " ";
    }
    cout << endl;
}
/**
int main(){

    vector<double> data;
    vector<int> cs;
    
    int c1=5;
    int c2 = 5;
    int nGenes = 10;
    float base = 0.0;
    for (int i=0; i<c1;i++){
        for(int j=0;j<nGenes;j++){
                base = 0.0;
            data.push_back(i*nGenes + j + base);
        }
    
    }
    for (int i=c1; i<c1+c2;i++){
        for(int j=0;j<nGenes;j++){
                base = 0.5;
            data.push_back(i*nGenes + j + base);
        }
    
    }
    cs.push_back(c1);
    cs.push_back(c2);
    kfold k(data,nGenes, cs, 3);
    vector<double> * ts;
    vector<double> * ls;
    ts = k.getNextTrainingSet();
    int counter = 0;
    while(ts != NULL){
    counter++;
    cout <<endl<< "ts" << endl;
        printVect((*ts), nGenes);
        ls = k.getNextTestVector();
        while(ls != NULL){
            cout <<  endl<< "ls" << endl;
            printVect((*ls), nGenes);
            cout << "class=" << k.getTestVectorClass()<<endl;
            cout << "cs1=" <<k.getClassSizes()[0];
            cout << "cs2=" <<k.getClassSizes()[1];
            k.getTestVectorClass();
            ls = k.getNextTestVector();
        }
        ts = k.getNextTrainingSet();
    }

    cout << "times ran = " << counter << endl;
}**/
