#ifndef KTSP_H
#define KTSP_H
#include <vector>
#include <queue>
#include <map>
using std::vector;
using std::priority_queue;
using std::map;

/**
Uses a linear amount of memory with high probability, but it is 3 times slower
**/
class Ktsp{
    public:
    Ktsp( vector<double> & data, int nGenes, vector<int> & classSizes, int maxK,int n,int m);
    ~Ktsp();
    //the rank matrices (nGenesxnGenes)
    //vector< vector<int> > * class_one_rank;
    //vector< vector<int> > * class_two_rank;
    // the delta scores (nGenesxnGenes) P(i<j|C1) - P(i<j|C2)
   // keep track of the cumulative ranks of each gene rs[i] = sum i>j for all j
    //used by gamma |nGenes|
    vector<int> rankSum1;
    vector<int> rankSum2;
    
    int nGenes, nSamples, cSize1, cSize2,vcSize1, vcSize2, maxK, n, m, ourK;
    unsigned int MAX_PQ_SIZE;
    //the pair inner class is used to keep track of top pairs
    class pair{
        public:
        pair():i(NULL),j(NULL),delta(NULL), gamma(NULL){};
        pair(int i, int j, int delta, int gamma):i(i),j(j), delta(delta), gamma(gamma){};
        int i;
        int j;
        //Ktsp * outer;//need this to access delta and gamma
        int delta;
        int gamma;
        bool operator<(const pair & rhs) const;
        bool operator>(const pair & rhs) const;
        bool operator==(const pair & rhs) const;
    };
    priority_queue<pair> * pq;

    //returns a vector containing the indices of the top K pairs
    void getTopK(vector<int> & topKPairs);
 
   //returns the average rank difference
    int getGamma(int i, int j);//needs to be public because pair needs access
    private:
    int abs(int a);
    double abs(double a);
   //delta, rankSum1 and rankSum2 vectors
    void initVectors();
    //builds the rank matrix for the given class
   //performs the crossvalidation from which we determine the best k
    //returns the best K
    int crossValidation(vector<double> & data);
    //this finds the number of errors for each k value within
    //each subset of samples (nSamples - n)
    void findKError(vector<double> & data, vector<int> & errors);
    //takes the given top pairs and returns the number of samples that are
    //misclassified
    int misclassify(vector<double> & data, vector<pair> & topK);
    //clears and fills the priority queue

    //NEW FUNCS MUST DOCUMENT
    void buildO(  priority_queue<Ktsp::pair, vector<Ktsp::pair>, std::greater<Ktsp::pair> > & scratch_pq);
    void addPairToScratch(Ktsp::pair & curr_pair, priority_queue<Ktsp::pair, vector<Ktsp::pair>, std::greater<Ktsp::pair> > & scratch_pq, unsigned int & max_pq_size);
    void train(vector<double> & data, map<int, int> & skip);
    int adjustClassSize(int & adj_class_1, int & adj_class_2 , map<int, int> & skip);
};
#endif
