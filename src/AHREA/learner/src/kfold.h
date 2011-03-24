#ifndef KFOLD_H
#define KFOLD_H
#include <vector>
using std::vector;

class kfold{
    public:
        kfold(vector<double> & data, int numGenes, vector<int> & classSizes, int k);
        ~kfold();
        vector<double> * getNextTrainingSet();
        vector<double> * getNextTestVector();
        vector<int> getClassSizes();
        int getTestVectorClass();
    private:
        int nGenes, k, it, curr_class, next_fold, class1size, class2size;
        vector<double> * orig_data;
        vector<int> samp_vector;
        vector<double> * generated_data;
        vector<double> * generated_test;
        vector<int> curr_classSizes;
        vector<int> generateSampleVector();
        int getFoldSize();
        bool trainingData( int sample );
        bool checkFoldsGood( vector<int> & sample);
};
#endif
