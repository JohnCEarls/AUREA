/**
Copyright (C) 2011  N.D. Price Lab

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
**/
#include "Ktsp.h"
#include "wilcoxon_test.cpp"
#include "order.h"
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


Ktsp::Ktsp( vector<double> & data, int numGenes, vector<int> & classSizes,vector<int> filters, int maxK, int n, int m){

    this->nGenes = numGenes;
    this->nSamples = classSizes[0] + classSizes[1];
    this->maxK = maxK;
    this->n = n;// this is the number of samples to remove during cross validation
    this->m = m;//how many times to run cross validation
    this->cSize1 = classSizes[0];
    this->cSize2 = classSizes[1];
    this->pq = NULL;
    this->filters = filters;
    
    buildWilcoxonRanking(data);
    if(this->m == 0){
        this->ourK = maxK;
    }else if(maxK>1){
        this->ourK = crossValidation(data); 
    } else {
        this->ourK = 1;
    }
    
   
    initVectors();
    
    
    map<int,int> empty;
    
    rankClass(data, 0, classSizes[0], empty);
    
    rankClass(data, classSizes[0], nSamples, empty);
    
    buildO();
    
}

Ktsp::~Ktsp(){
   delete pq;
}
/**
Takes in an empty int vector for returning the top k pairs
returns (i1,j1,i2,j2, ... ik,jk)
**/
void Ktsp::getTopK(vector<int> & topKPairs){
        map<int,int> ignore;    
        topKPairs.resize(ourK*2);
        for(int i = 0; i<  ourK; i++){
            
            pair curr = pq->top();
            while(ignore.find(curr.i) != ignore.end()
            || ignore.find(curr.j) != ignore.end()){
                curr = pq->top();
                pq->pop();
            }
           
            swapPair(curr);
           topKPairs[2*i] = map_to_data[curr.i];
            topKPairs[2*i + 1] = map_to_data[curr.j];
            ignore[curr.i] = 1;
            ignore[curr.j] = 1;
       }
    
}

/**
 Generates a rankMatrix and its associated rankSums.
 It takes a map skip to allow the cross validation. 
 skip should contain the indices of any samples you wish to ignore.
**/
void Ktsp::rankClass(vector<double> & data, int classStart, int classEnd, map<int,int> & skip){
    vector<int> * rSum;
    
    int opposite_size_factor;
    int scaledSize1, scaledSize2;
    //this factor scales the rank value
    scaledSize1 = cSize1;
    scaledSize2 = cSize2;
    
    map<int,int>::iterator it;
    for( it=skip.begin();it != skip.end(); it++){
        int skipped_samp = (*it).first;
        if(skipped_samp < cSize1){
            //we are skipping a sample in class1
            //so reduce factor
            scaledSize1--;
        } else {
            //we are skipping a sample in class1
            //so reduce factor
            scaledSize2--;
        }
    }
    vcSize1 = scaledSize1;
    vcSize2 = scaledSize2;
    if(classStart == 0){//set param for class 1
        rSum = &rankSum1;
        //this factor scales the rank value
        opposite_size_factor = (int)scaledSize2/gcd(scaledSize1, scaledSize2);
        //dividing by gcd in order to avoid overflows in delta
       
    }else{//set param for class2
        rSum = &rankSum2;
        //this factor scales the rank value
        opposite_size_factor = scaledSize1/gcd(scaledSize1, scaledSize2);
        //dividing by gcd in order to avoid overflows in delta
        opposite_size_factor = (int)-1*opposite_size_factor;        
    }
    int off;

    for(int classOffset = classStart; classOffset < classEnd; classOffset++){
         off = classOffset * nGenes;//data is 1-d so offset 
         if(skip.find(classOffset) == skip.end()){
            //for every class not in skip
            for(int i = 0; i< filters[0];i++){
                for(int j = 0; j<filters[1]; j++){
                    if(data[off + map_to_data[i]] < data[off + map_to_data[j]]){
                        delta[i][j] += opposite_size_factor;
                    }
                }
            
            }

        }
    } 
    int maxfilter;
    if( filters[0] > filters[1]){
        maxfilter = filters[0];
    } else {
        maxfilter = filters[1];
    }
     
     for(int classOffset = classStart; classOffset < classEnd; classOffset++){
         off = classOffset * nGenes;//data is 1-d so offset 
         if(skip.find(classOffset) == skip.end()){
            //for every class not in skip
            for(int i = 0; i< maxfilter;i++){
                for(int j = 0; j<maxfilter; j++){
                    if(data[off + map_to_data[i]] < data[off + map_to_data[j]]){
                        (*rSum)[j]++;
                    }else if (data[off + map_to_data[i]] > data[off + map_to_data[j]]){
                        (*rSum)[i]++;
                    }//otherwise equal
                }
                
            }

        }
    } 


}

void Ktsp::buildWilcoxonRanking(vector<double> & data){
    //map_to_data and wilcoxon_scores are member variables
    for(int i=0;i<nGenes;i++) map_to_data.push_back(i);
    //run test
    wilcoxon_test(data, nGenes, cSize1, cSize2, wilcoxon_scores);
    //sort and map
    sort_along<int>(wilcoxon_scores, map_to_data);
    //desc order
    reverse(map_to_data.begin(), map_to_data.end());
    reverse(wilcoxon_scores.begin(), wilcoxon_scores.end());
    //adjust filters
    int wilc_index;
    for(int i=0;i<2;i++){
        wilc_index = filters[i];
        while((wilc_index + 1) < nGenes && 
                wilcoxon_scores[wilc_index+1] == wilcoxon_scores[filters[i]]){
            wilc_index++;
        }
        filters[i] = wilc_index;
    }
    
}


void Ktsp::printDelta(){
    for( int i = 0 ; i < filters[0] ; i++){
        
      for(int j = 0; j < filters[1]; j++){
        cout << delta[i][j] << " ";

      } 
    cout << endl; 
    }
}

/**
Performs the internal crossvalidation to determine the best value for k
**/
int Ktsp::crossValidation(vector<double> & data){
    //cout << "in cv" << endl;
    //time_t start, end;
    srand( time(NULL) );
    vector<int> myerror;
    for(int i=0;i<maxK;i++){
        myerror.push_back(0);
    }
    //time(&start);
    for(int i = 0; i<m;i++){
        //randomly choose n samples to ignore
        map<int,int> skip;
        for(int j = 0; j<n;j++){
            int random_number = rand() % nSamples;
            if(skip.find(random_number) == skip.end()){
                skip[random_number] = 1;
            }
        }
        
        initVectors();
        rankClass(data, 0, cSize1, skip);
        rankClass(data, cSize1, nSamples, skip);    
        buildO();
        
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

        swapPair(curr);
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
Check if delta is negative, if so swap order
**/

void Ktsp::swapPair(Ktsp::pair & currPair){

    if (delta[currPair.i][currPair.j] < 0.0){
        int temp = currPair.i;
        currPair.i = currPair.j;
        currPair.j = temp;
    }
    
 
}
/**
Greatest common denominator
Euclidean Alg.
**/
int Ktsp::gcd(int a, int b){
    if(b == 0){
            return a;
    }else{
        return gcd(b, a % b);
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
           
           if (data[i*nGenes + map_to_data[currPair.i]] > data[i*nGenes + map_to_data[currPair.j]])
                suberrors += 1;
        }
        if (2*suberrors > topK.size()){
            errors +=1;
        }
    }
    //errors in class 2
    for(int i = cSize1; i<nSamples;i++){
        unsigned int suberrors = 0; 
        for(unsigned int j=0;j< topK.size(); j++){
           pair currPair = topK[j];
           if (data[i*nGenes +map_to_data[currPair.i]] < data[i*nGenes + map_to_data[currPair.j]])
                suberrors += 1;
        }    
        if (2*suberrors > topK.size()){
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
    bool resize = (int)delta.size() < filters[0];
    //rankSums will be the size of maxfilter;
    int maxfilter;
    if( filters[0] > filters[1]){
        maxfilter = filters[0];
    } else {
        maxfilter = filters[1];
    }
    if (resize){
        delta.resize(filters[0]);
        rankSum1.resize(maxfilter);
        rankSum2.resize(maxfilter);
        for(int i =0;i<filters[0];i++){delta[i].resize(filters[1]);}
    }
    for(int i=0; i<maxfilter;i++){
       rankSum1[i] = 0;
       rankSum2[i] = 0;
    }
    for( int i=0;i<filters[0];i++){
        for(int j=0;j<filters[1];j++){
            delta[i][j] = 0;
        }
    }
    
}

int Ktsp::getGamma(int indexi, int indexj ){
   return abs(vcSize2*(rankSum1[indexi] - rankSum1[indexj]) -  
   vcSize1*(rankSum2[indexi] - rankSum2[indexj]));
}


void Ktsp::buildO(){
    //k this gets tricky cause I'm trying to save space
    delete pq;
    pq = NULL;
    pq = new priority_queue<pair>;
    priority_queue<pair, vector<pair>, std::greater<pair> > temp_pq;
    //temp_pq is a min priority queue and I am going to restrict its
    //size to maxK*nGenes
    //When I go to add a pair, if the current pair is greater than the min
    // element in the queue, pop it off and insert the current element
    int maxFilter = filters[0];
    if(filters[0] < filters[1]) maxFilter = filters[0];
    unsigned int pq_size = maxK * 2 * maxFilter;
    for(int i=0;i<filters[0]; i++){
        for(int j=0;j<filters[1];j++){ 
                pair curr_pair(i,j, this);
                
                if(temp_pq.size() < pq_size){
                    temp_pq.push(curr_pair);
                } else if (curr_pair > temp_pq.top()){
                    temp_pq.pop();
                    temp_pq.push(pair(i,j,this));
                }
        }
    }
    while(!temp_pq.empty()){
        pq->push(temp_pq.top());
        temp_pq.pop();
    }

}

double Ktsp::abs(double a){
    if (a < 0.0)return -1.0 * a;
    return a;

}
int Ktsp::abs(int a){
    if (a < 0) return -1 * a;
    return a;
}

long Ktsp::abs(long a){
    if (a < 0) return -1 * a;
    return a;
}

void Ktsp::printTest(){
    for(int i = 0; i< nGenes; i++){
        for(int j = 0; j<nGenes; j++){
            //cout << (*class_one_rank)[i][j] << " " ;
        }
        cout << endl;
    }
    for(int i = 0; i< nGenes; i++){
        for(int j = 0; j<nGenes; j++){
            //cout << (*class_two_rank)[i][j] << " " ;
        }
        cout << endl;
    }
    for(int i = 0; i< nGenes; i++){
        for(int j = 0; j<nGenes; j++){
            cout << delta[i][j] << " " ;
        }
        cout << endl;

    }

}

bool Ktsp::pair::operator<( const Ktsp::pair & rhs)const{
            //using at so we know if something stupid is happening
            int deltaLeft = outer->abs(outer->delta.at(this->i).at(this->j));
            int deltaRight = outer->abs(outer->delta.at(rhs.i).at(rhs.j));
            if(deltaLeft == deltaRight){
                return outer->getGamma(this->i,this->j) < outer->getGamma(rhs.i, rhs.j);
            }else{
                return deltaLeft < deltaRight;
            }
}
bool Ktsp::pair::operator>( const Ktsp::pair & rhs)const{
            return rhs < (*this);
}
#ifdef DEBUG
/**int main(){
   int nGenes = 10000;
    vector<double> test;
    cout << "before" << std::endl;
    test.resize(20*nGenes);
    double oldVal;
    double val = 1.0;
    for(int i = 0; i<10*nGenes;i++){
        if( i%nGenes == 0) val = 1.0;
        test[i] = (float)(rand()%100) / ((float)(rand()%88) + 1.1);
    }
    val = 1.0;
    for(int i = 10*nGenes; i<20*nGenes;i++){
        if( i%nGenes == 0) val = 1.0;
            
        val += .0001;
        test[i] = (float)(rand()%100) / ((float)(rand()%88) + 1.1);
    }
     vector<int> cs(2);
    for (int i=0; i< 10 ; i++){
       //if(rand()%2) 
        test[nGenes*i+ 10] = 100000.00;
       if(rand()%2) 
        test[nGenes*i + 3] = .0000001;



    }
    for (int i=10; i< 20 ; i++){
       test[nGenes*i + 10] = .0000001;
       test[nGenes*i + 3] = 1000000.00;

    }

    cs[0] = 10;
    cs[1] = 10;
    cout << "here"<<endl;
    vector<int> filters;
    filters.push_back(10);
    filters.push_back(10);
    Ktsp a(test, nGenes, cs,filters, 6, 0, 1);
    vector<int> topK;
    a.getTopK(topK);
    cout << "getting top k"<<endl;
    for (int i=0; i<topK.size(); i++){
        cout << topK[i] << " ";
        if (i%2 == 1)
            cout << endl;
   }
    cout << "done" << endl;
    //a.printTest();
}**/
#endif
