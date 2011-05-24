#ifndef KTSP_H
#define KTSP_H
#include <vector>
#include <queue>
#include <map>
using std::vector;
using std::priority_queue;
using std::map;


class Ktsp{
    public:
    Ktsp( vector<double> & data, int nGenes, vector<int> & classSizes,vector<int> filter, int maxK,int n,int m);
    ~Ktsp();
    // the delta scores (nGenesxnGenes) P(i<j|C1) - P(i<j|C2)
    vector< vector<int> > delta;
    // keep track of the cumulative ranks of each gene rs[i] = sum i>j for all j
    //used by gamma |nGenes|
    vector<int> rankSum1;
    vector<int> rankSum2;
    vector<int> filters;
    vector<double> wilcoxon_scores;
    vector<int> map_to_data;
    int nGenes, nSamples, cSize1, cSize2,vcSize1, vcSize2, maxK, n, m, ourK;
    //the pair inner class is used to keep track of top pairs
    class pair{
        public:
        pair():i(NULL),j(NULL),outer(NULL){};
        pair(int i, int j, Ktsp * outer):i(i),j(j), outer(outer){};
        int i;
        int j;
        Ktsp * outer;//need this to access delta and gamma
        bool operator<(const pair & rhs) const;
        bool operator>(const pair & rhs) const;
    };
    priority_queue<pair> * pq;

    //returns a vector containing the indices of the top K pairs
    void getTopK(vector<int> & topKPairs);
 
   //for debugging
    void printTest();
   //returns the average rank difference
    int getGamma(int i, int j);//needs to be public because pair needs access
    private:
    int abs(int a);
    long abs(long a);
    double abs(double a);
    //calculates the delta matrix
    //void buildDelta();
    //resizes if necessary and zeroes out the class_one_rank, class_two_rank,
    //delta, rankSum1 and rankSum2 vectors
    void initVectors();
    //builds the rank matrix for the given class
    void rankClass(vector<double> & data, int classStart, int ClassEnd, map<int,int> & skip);
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
    void buildO();
    void swapPair(pair & currPair);
    void printDelta();
    void buildWilcoxonRanking(vector<double> & data);
    int gcd(int a, int b);   
};
#endif
