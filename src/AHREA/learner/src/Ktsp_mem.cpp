#include "Ktsp_mem.h"
#include <vector>
#include <iostream>
#include <string>
#include <map>
#include <stdlib.h>
#include <time.h>
#define DEBUG
using std::map;
using std::cout;
using std::endl;
using std::vector;


Ktsp::Ktsp( vector<double> & data, int numGenes, vector<int> & classSizes, int maxK, int n, int m){
    //time_t start, end;
    //cout << "init" << endl;
    //init class vars
    this->nGenes = numGenes;
    this->nSamples = classSizes[0] + classSizes[1];
    this->maxK = maxK;
    this->n = n;// this is the number of samples to remove during cross validation
    this->m = m;//how many times to run cross validation
    this->cSize1 = classSizes[0];
    this->cSize2 = classSizes[1];
    //this->class_one_rank = new vector< vector<int> >;
    //this->class_two_rank = new vector< vector<int> >;
    this->pq = NULL;
    MAX_PQ_SIZE = (unsigned int)(maxK * 2 * nGenes);
    //cout << "Finding K" << endl;
    //time(&start);
    //run the cross validation routine and return the optimum k
    this->ourK = crossValidation(data); 
    //now using this k we set up to run on the whole matrix
    //cout << "found K" << endl;
    //time(&end);
    //double diff = difftime(end, start);
    //cout << "cross validation took : ";
    //cout << diff << endl;
    
    initVectors();
    //time(&start);
    //diff = difftime(start, end);
    //cout << "init vectors took : ";
    //cout << diff << endl;
    map<int,int> empty;
    //time(&start);
    //  cout << "rank class 1" << endl;
    train( data, empty );
    //rankClass(data, 0, cSize1, empty);
   // cout << "rank class 1" << endl;
    //rankClass(data, cSize2, nSamples, empty);
    //time(&end);
    //diff = difftime(end, start);
    //cout << "rank class took : ";
    //cout << diff << endl;
//    cout << "build Delta" << endl;
    //    buildDelta();
    //time(&start);
    //diff = difftime(start, end);
    //cout << "build delta took : ";
    //cout << diff << endl;
//    cout << "build O" << endl;
    //buildO();
    //time(&end);
    //diff = difftime(end, start);
    //cout << "build O took : ";
    //cout << diff << endl;
//    cout << "done w/ ktsp" << endl;

    
}

Ktsp::~Ktsp(){
//    cout << "in destructor" << endl;
    //delete class_one_rank;
    //delete class_two_rank;
    delete pq;
//    cout << "leaving destructor" << endl;

}
/**
Takes in an empty int vector for returning the top k pairs
returns (i1,j1,i2,j2, ... ik,jk)
**/
void Ktsp::getTopK(vector<int> & topKPairs){
        map<int,int> ignore;    
        for(int i = 0; i<  ourK; i++){
            pair curr = pq->top();
            while(ignore.find(curr.i) != ignore.end()
            || ignore.find(curr.j) != ignore.end()){
                curr = pq->top();
                pq->pop();
            }
            topKPairs.push_back(curr.i);
            topKPairs.push_back(curr.j);
            ignore[curr.i] = 1;
            ignore[curr.j] = 1;
       }
    
}



/**
Performs the crossvalidation to determine the best value for k
**/
int Ktsp::crossValidation(vector<double> & data){
    srand( time(NULL) );
    vector<int> myerror;
    for(int i=0;i<maxK;i++){
        myerror.push_back(0);
    }
    //time(&start);
    for(int i = 0; i<m;i++){
        map<int,int> skip;
        for(int j = 0; j<n;j++){
            int random_number = rand() % nSamples;
            if(skip.find(random_number) == skip.end()){
                skip[random_number] = 1;
            }
        }
        initVectors();
        train(data, skip );
        findKError(data, myerror );
     
    }
    int bestKrate = (nSamples + 1)*m;//worst possible
    int bestK = 0;
    for(int i = 0;i<maxK;i++){
        if(i%2 == 0){
            if(myerror[i] < bestKrate){
                bestK = i+1;
                bestKrate = myerror[i];
            }
        }
    }
    return bestK;
}


/**
Returns the errors vector which is of size maxK and contains
the sum of misclassified samples for each k
**/
void Ktsp::findKError(vector<double> & data, vector<int> & errors){
    vector<pair> topK;
    map<int,int> ignore;
    for(int i = 0; i< maxK; i++){
            pair curr = pq->top();
            pq->pop();
            while(ignore.find(curr.i) != ignore.end() 
            || ignore.find(curr.j) != ignore.end()){
                curr = pq->top();
                pq->pop();
            }
            topK.push_back(curr);
            ignore[curr.i] = 1;
            ignore[curr.j] = 1;
        if( i% 2 == 0){

            //runs the classification anf returns the error rate for the given
            // topK
            errors[i] = misclassify(data, topK);                
        }
    }
}
/**
Given the topKScoring pairs it classifies all samples and returns the
number of misclassifications
**/
int Ktsp::misclassify(vector<double> & data, vector<pair> & topK ){
    int errors = 0;
    //errors in class 1
    for(int i = 0; i<cSize1;i++){
        unsigned int suberrors = 0;
        for(unsigned int j=0;j< topK.size(); j++){
           pair currPair = topK[j];
           
           if (data[i*nGenes + currPair.i] > data[i*nGenes + currPair.j])
                suberrors += 1;
        }
        if (suberrors > topK.size()/2){
            errors +=1;

        }
    }
    //errors in class 2
    for(int i = cSize1; i<nSamples;i++){
        unsigned int suberrors = 0; 
        for(unsigned int j=0;j< topK.size(); j++){
           pair currPair = topK[j];
           if (data[i*nGenes + currPair.i] < data[i*nGenes + currPair.j])
                suberrors += 1;
        }    
        if (suberrors > topK.size()/2){
            errors +=1;
        }
    }
    return errors;
}
/**
Resizes if necessary and initializes the rank matrices
delta matrix and rankSum vectors
**/
void Ktsp::initVectors(){
    bool resize = (int)rankSum1.size() < nGenes;
    if (resize){
        rankSum1.resize(nGenes);
        rankSum2.resize(nGenes);
    }
    for(int i=0; i<nGenes;i++){
       rankSum1[i] = 0;
        rankSum2[i] = 0;
   }
   
}

//adjusts the class size to account for skipped samples
int Ktsp::adjustClassSize(int & adj_class_1, int & adj_class_2 , map<int, int> & skip){
    adj_class_1 = cSize1;
    adj_class_2 = cSize2;
    map<int, int>::iterator it;
    for(it=skip.begin(); it != skip.end() ; it++){
        int skipped_samp = (*it).first;
        if(skipped_samp < cSize1){
            adj_class_1--;    
        } else {
            adj_class_2--;
        }
    }
 
}

void Ktsp::train(vector<double> & data, map<int, int> & skip ){
    unsigned int max_pq_size = MAX_PQ_SIZE;//save at least 2maxk n points
    priority_queue<pair, vector<pair>, std::greater<pair> >  scratch_pq;
    //adjust sizes to account for skipped samples
    int vcSize1, vcSize2;
    adjustClassSize(vcSize1, vcSize2, skip);
   
    for(int i = 0; i<nGenes; i++){
        for(int j = 0; j<nGenes; j++){
            //make delta for i,j
            int sample;
            int delta = 0;
            //for every samp in class1
            for(sample=0; sample < cSize1; sample++){
                //check that this is not a skipped sample
                if(skip.find(sample) == skip.end()){
                    if(data[sample*nGenes + i ] < data[sample*nGenes + j] )
                    {
                        delta += vcSize2;
                        rankSum1[j]++;
                    }else{
                        rankSum1[i]++;
                    }
                }
            }
            //for every samp in class2
            for(sample=cSize1; sample < cSize1+cSize2; sample++){               
                //check that this is not a skipped sample
                if(skip.find(sample) == skip.end()){
                    if( data[ sample * nGenes + i ] < data[ sample * nGenes + j] )
                    {
                        delta -= vcSize1;
                        rankSum2[j]++;
                    }else{
                        rankSum2[i]++;
                    }
                }

            } 
            
            pair curr_pair(i,j,delta,-1);
            //we can't know gamma yet so set to -1
            addPairToScratch( curr_pair, scratch_pq, max_pq_size );   
        }//j
    }//i
    //Now add Gamma and put in maxheap
    buildO(scratch_pq);
}


void Ktsp::buildO(priority_queue<Ktsp::pair, vector<Ktsp::pair>, std::greater<Ktsp::pair> > & scratch_pq){
    delete pq;
    pq = new priority_queue<pair>;
    pair curr_pair;
    while(!scratch_pq.empty()){
        curr_pair = scratch_pq.top();
        curr_pair.gamma = getGamma(curr_pair.i, curr_pair.j);
        pq->push(curr_pair);
        scratch_pq.pop(); 
    }
}
//Adds the curr_pair to the priority queue if it is within range
void Ktsp::addPairToScratch(Ktsp::pair & curr_pair,priority_queue<Ktsp::pair, vector<Ktsp::pair>, std::greater<Ktsp::pair> > & scratch_pq, unsigned int & max_pq_size){
    //this may seem a little convoluted.
    //basically, I have a min pq that can hold k*max*n elements
    //That is the maximum number of elements with ties.
    //the p-queue holds the best points we have seen so far.
    //top is the worst of the best elements we have seen
//priority_queue<Ktsp::pair, vector<Ktsp::pair>, std::greater<Ktsp::pair> >
            if(scratch_pq.size() < max_pq_size){
                scratch_pq.push( curr_pair  );
            }else if(curr_pair > scratch_pq.top()){
                while(MAX_PQ_SIZE < max_pq_size && curr_pair > scratch_pq.top()){
                    //cout << "d";
                    scratch_pq.pop();
                    max_pq_size--;
                }
                if(curr_pair > scratch_pq.top()){
                    scratch_pq.pop();
                    scratch_pq.push(curr_pair);
                }
            } else if(curr_pair == scratch_pq.top()){
                //cout << "i";
                max_pq_size++;//if its a tie we have to increase the size
                scratch_pq.push( curr_pair );
            }
}
//Gamma = the distance between the ranksum of c1 and c2
int Ktsp::getGamma(int indexi, int indexj ){
   return abs(vcSize2*(rankSum1[indexi] - rankSum1[indexj]) -  
   vcSize1*(rankSum2[indexi] - rankSum2[indexj]));
}

double Ktsp::abs(double a){
    if (a < 0.0)return -1.0 * a;
    return a;

}
int Ktsp::abs(int a){
    if (a < 0) return -1 * a;
    return a;
}


bool Ktsp::pair::operator<( const Ktsp::pair & rhs)const{
            if(this->delta == rhs.delta){
                return this->gamma < rhs.gamma;
            }else{
                return this->delta < rhs.gamma;
            }
}
bool Ktsp::pair::operator>( const Ktsp::pair & rhs)const{
            return rhs < (*this);
}

bool Ktsp::pair::operator==( const Ktsp::pair & rhs)const{
    return (this->delta == rhs.delta) && (this->gamma == rhs.gamma);
}

#ifdef DEBUG
int main(){
    int nGenes = 100;
    vector<double> test;
    cout << "before" << std::endl;
    test.resize(20*nGenes);
    double oldVal;
    double val = 1.0;
    for(int i = 0; i<10*nGenes;i++){
        val += .0001;
        test[i] = val; //(float)(rand()%100) / ((float)(rand()%88) + 1.1);
    }
    for(int i = 10*nGenes; i<20*nGenes;i++){
        val -= .0001;
        test[i] = val; //(float)(rand()%100) / ((float)(rand()%88) + 1.1);
    }
     vector<int> cs(2);
    for (int i=0; i< 10 ; i++){
       if(rand()%2) test[nGenes*i] = 100.00;
       if(rand()%2) test[nGenes*i + 3] = .0000001;



    }
    for (int i=10; i< 20 ; i++){
      if(rand()%2) test[nGenes*i] = .000001;
      if(rand()%2) test[nGenes*i + 3] = 100.00;

    }


    cs[0] = 10;
    cs[1] = 10;
    cout << "here"<<endl;
    Ktsp a(test, nGenes, cs, 10, 0, 1);
    vector<int> topK;
    a.getTopK(topK);
    cout << "getting top k"<<endl;
    for (int i=0; i<topK.size(); i++){
        cout << topK[i] << " ";
        if (i%2 == 1)
            cout << endl;
   }
    cout << "done" << endl;
}
#endif
