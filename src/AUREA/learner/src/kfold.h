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
#ifndef KFOLD_H
#define KFOLD_H
#include <vector>
#include <cstddef>
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
