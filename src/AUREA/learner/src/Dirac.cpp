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
#include "dir_Matrix.cpp"
#include "Dirac.h"
#include <stdlib.h>
#include <algorithm>
#include <time.h>
using std::pair;
//#define DEBUG
Dirac::Dirac(){

}


/**
    This is the big kahuna method.  It takes in all of the data and returns it via the passed in references.
    The parameters are defined as follows:
    **Input Data**
    vector<double> & data: this vector contains all of the numeric data from the microarrays.  It is one long
        vector that contains the  data for each sample appended to the sample before it.
        They should be sorted by classes.
    int dsSize - this is the total number of genes in a single sample
    vector<int> & classSize : this vector contains the number of samples for each class in the order
        they are stored in data.  It and dsSize are used to slice up the data.
    vector<int> & geneNet : this vector contains the indices for the genes in each gene network. The indices
        are relative to the size of a single sample.
    vector<int> & geneNetSize : this vector contains the number of elements in each gene network in the same
        order as they are added to geneNet.  This is used to partition geneNet.

    **Return Data**
    vector<bool> & returnRankMat:  This is the matrix that contains the binary ranking information for 
        each sample within a geneNetwork and the rank templates for each class within a geneNetwork.
        The matrix is layed out like this:
        Class 1 ordering for GN1 - class 1 rank template for GN1 - Class 2 ordering for Gn1 ...
        Class 1 ordering for GN2 - ..                           - Class 2 ordering for GN2 ...
        ....
        This is the logical ordering after put into to a Matrix.  
        Note the vector will be ordered:
        sample1 ordering GN1
        sample1 ordering GN2
        ...
        sample1 ordering GNn
        sample2 ordering GN1
        ...
        sample2 ordering GNn
        rank template for s1 and s2 (assuming they are a class(as C1) for GN1
        rt for C1 for GN1
        ...
        rt for C1 for GNn
        sample2 ordering GN1
        ...
        etc
    vector <double> & returnRMS: This contains the rank matching scores, so for each template their is a sub
        vector of how closely it matches the orderings for all samples within that geneNetwork.
        for gn1
        rms for sample1 against class 1 rt
        rms for sample2 against class 1 rt
        ...
        rms for samplen against class 1 rt
        rms for sample1 against class 2 rt
        rms for sample2 against class 2 rt
        ...
        rms for samplen against class n rt
        for gn2
        rms for sample1 against class 1 rt
        rms for sample2 against class 1 rt
        ...
        rms for samplen against class 1 rt
        rms for sample1 against class 2 rt
        rms for sample2 against class 2 rt
        ...
    vector <double> & returnRankConservation: This contains the rank conservation index, so the average of 
        rank matching within a class and geneNetwork.
        rci class 1 gn1
        rci class 2 gn1
        ...
        rci class 1 gn2
        rci class 2 gn2
        ...
        rci class n gnn

**/

void Dirac::enter( vector<double> & data, int dsSize, vector<int> & classSizes, vector<int> & geneNet, vector<int> & geneNetSize, 
    vector<bool> & returnRankMat, vector<double> & returnRMS, vector<double> & returnRankConservation ){
    #ifdef DEBUG
    cout << "in enter" << endl;
    #endif

    //this is the matrix that contains the raw data
    Matrix<double> * dataMat = initDataMatrix(data, dsSize, classSizes);
    
    //this matrix will hold the offsets for the rank matrix
    Matrix<int> * matMask;
    //this is the inititialized rank matrix
    Matrix<bool> * rankMat = initRankMatrix(returnRankMat, classSizes, geneNetSize, matMask );
    //foreach geneNetwork
   
    int gnStart = 0;
    int gnEnd = 0;
    int rmcs,rmrs;
    int matMaskIndex = 0;
    
    for(unsigned int gn = 0; gn < geneNetSize.size(); gn++){
        gnEnd += geneNetSize[gn];   //for each class
        int clst = 0;
        int clend = 0;
        for(unsigned int cl=0; cl < classSizes.size(); cl++){
            clend += classSizes[cl];
            rmcs = (*matMask)(matMaskIndex,0);
            rmrs = (*matMask)(matMaskIndex,1);
            generateRankedSet((*dataMat), clst, clend, geneNet, gnStart, gnEnd,(*rankMat),rmcs,rmrs);
            clst += clend;
            matMaskIndex += 2;
            

        }
        gnStart = gnEnd;
    }
   
     
    generateRankTemplate((*rankMat), classSizes);
    generateRankMatchingScore((*rankMat),(*matMask), classSizes.size(), dsSize, geneNetSize.size(), returnRMS );
    
    int nSamples = 0;
    for(unsigned int i=0;i<classSizes.size();i++) nSamples += classSizes[i];
    
    Matrix<double> rmsMat( &returnRMS, geneNetSize.size()*classSizes.size() ,nSamples); 
    generateRankConservationIndex(rmsMat, (*matMask), returnRankConservation);
    

    #ifdef DEBUG
    cout << "out enter" << endl;
    #endif

 
}
void Dirac::generateRankConservationIndex( Matrix<double> & rmsMat, Matrix<int> & matrixMask, vector<double> & returnRankConservation){
    #ifdef DEBUG
    cout << "in grci" << endl;
    #endif
   
    //rmsMat.printBool(); 
    
    int matIndex = 0;
    //int start = 0;
    int classOffset = 0;
    int rmsCol = 0;
    while(matIndex < matrixMask.nCols()){
        if(matrixMask(matIndex, 0) == 0){
            classOffset = 0;
        }
        int classSize = matrixMask(matIndex,2);
        float rankSum = 0.0;
        #ifdef DEBUG
        cout <<"Class Offset: " << classOffset << endl;
        cout <<"Class Size: " << classSize << endl;
        #endif
        for(int i=classOffset; i< classOffset + classSize; i++){
            //cout << rmsCol << " "<<  i << endl;
            rankSum += rmsMat( rmsCol, i );
        }        
        returnRankConservation.push_back(rankSum/classSize);
        rmsCol++;
        classOffset += classSize;
        matIndex += 2;
    }
    #ifdef DEBUG                                                                                                                                                                                                                                                                                                                                                                                                                                            
    cout << "out grci" << endl;
    #endif

}

void Dirac::generateRankedSet(Matrix<double> & dataMat, int s, int e, vector<int> & geneNet, int gs, int ge, Matrix<bool> & rankMat, int rmcs, int rmrs){
    #ifdef DEBUG
    cout << "in grs" << endl;
    cout << "rmcs = " << rmcs << endl;
    cout << "rmrs = " << rmrs << endl;
    #endif 
    //for each sample in class
    int rankMatrixCol = rmcs;
    for(int samp_i = s; samp_i < e; samp_i++){
        //for each gene in the geneNetwork
        int rankMatrixRow = rmrs;
        for(int gn = gs; gn < ge-1; gn++){
            int dmRowLoc1 = geneNet[gn];

            for(int gnc = gn + 1; gnc < ge; gnc++){
                int dmRowLoc2 = geneNet[gnc];
                #ifdef DEBUG
                //cout << "comparing " << dataMat.getVal(samp_i, dmRowLoc1) << " < "  << dataMat.getVal(samp_i, dmRowLoc2) << endl;
                #endif
                if(dataMat.getVal(samp_i, dmRowLoc1) < dataMat.getVal(samp_i, dmRowLoc2)){
        
                    rankMat.assign(rankMatrixCol, rankMatrixRow++, true);
                    #ifdef DEBUG
                    //cout << rankMatrixCol << " " << rankMatrixRow;
                    //cout << "tis true" << endl;
                    #endif                    
                }else{
                    rankMat.assign(rankMatrixCol, rankMatrixRow++, false);
                }
                //rankMat.assign(rankMatrixCol, rankMatrixRow - 1, true);
                //cout << "testing";
            }
        }
        rankMatrixCol++;
    }
    #ifdef DEBUG
    cout << "out grs" << endl;
    #endif 
 }

void Dirac::generateRankTemplate(Matrix<bool> & rankedSet, vector<int> & classSizes){    
    #ifdef DEBUG
    cout << "in grt" << endl;
    #endif 
     //create and init storage
   //storage holds the sum of true per gene
    vector<int> storage(rankedSet.nRows());
    for(unsigned int i=0;i<storage.size();i++)storage[i] = 0;

    //keep track of which column has
    int classInc = 0;
    int classStep = classSizes[0];
    int half = classSizes[0]/2;
    for(int n = 0; n < rankedSet.nCols() ; n++){
        //for each sample
        for(int g=0; g < rankedSet.nRows();g++){
            if(classStep == n){
                //cout << n;
                //in the template column
                if(storage[g] > half){
                    rankedSet.assign(n, g, true);
                } else {
                    rankedSet.assign(n, g, false);
                }
                storage[g] = 0; //reset this storage
                if((g+1) == rankedSet.nRows() && (n + 1) < rankedSet.nCols()){
                    //last row of template column
                    classStep += (classSizes[++classInc] + 1);
                    half = classSizes[classInc] / 2;
                }
            }else if(rankedSet.getVal(n,g)){//increment number of 1s
                storage[g]++;
            }            
       }
    }
    #ifdef DEBUG
    cout << "out grt" << endl;
    #endif 
 }

//Rank Matching Score
void Dirac::generateRankMatchingScore(Matrix<bool> & rankedSet,Matrix<int> & matrixMask,int numClasses, int numSamples, int numGeneNetworks, vector<double> & R ){
    #ifdef DEBUG
    cout << "in grms" << endl;
    #endif 
 
    for(int i = 0; i< numGeneNetworks; i++){
        int rM1ColStart=matrixMask(i*4,0);
        int rM1NumCol =matrixMask(i*4,2);
 
        int rM2ColStart=matrixMask(i*4 + 2, 0);
        int rM2NumCol = matrixMask(i*4 + 2, 2);
        int rT1ColStart=matrixMask(i*4 + 1, 0);
        int rT2ColStart=matrixMask(i*4 + 3, 0);
        int rowStart = matrixMask(i*4, 1);
        int numRows = matrixMask(i*4,3);
        int match;
        //rank template 1 vs rankmatrix class 1
        for(int col = rM1ColStart; col< rM1ColStart + rM1NumCol; col++){
            match = 0;
            for(int row = rowStart; row < rowStart + numRows; row++){
                   if(rankedSet.getVal(col,row) == rankedSet.getVal(rT1ColStart, row)){
                            match++;
                   }
          
            }
            R.push_back((double)match/(double)numRows);
        }
        //rank template 1 vs rankmatrix class 2
        for(int col = rM2ColStart; col< rM2ColStart + rM2NumCol; col++){
            match = 0;
            for(int row = rowStart; row < rowStart + numRows; row++){
                   if(rankedSet.getVal(col,row) == rankedSet.getVal(rT1ColStart, row)){
                            match++;
                   }
          
            }
            R.push_back((double)match/(double)numRows);
        } 
        //rank template 2 vs rankmatrix class 1
        for(int col = rM1ColStart; col< rM1ColStart + rM1NumCol; col++){
            match = 0;
            for(int row = rowStart; row < rowStart + numRows; row++){
                   if(rankedSet.getVal(col,row) == rankedSet.getVal(rT2ColStart, row)){
                            match++;
                   }
          
            }
            R.push_back((double)match/(double)numRows);
        }

        //rank template 1 vs rankmatrix class 1
        for(int col = rM2ColStart; col< rM2ColStart + rM2NumCol; col++){
            match = 0;
            for(int row = rowStart; row < rowStart + numRows; row++){
                   if(rankedSet.getVal(col,row) == rankedSet.getVal(rT2ColStart, row)){
                            match++;
                   }
          
            }
            R.push_back((double)match/(double)numRows);
        }
    }
}

int Dirac::nChooseTwo(int n){
    return (n*(n-1))/2;    
}

/**
    Returns the initialized rank matrix.  It also returns (as a param) the matrix mask (offsets) for the rank matrix
    So we can break the Matrix up into submatrices as described in the comments for enter.

**/

Matrix<bool> * Dirac::initRankMatrix(vector<bool> & returnRankMatrix, vector<int> & classSizes, vector<int> & geneNetSize, Matrix<int> *& offsets){
    #ifdef DEBUG
    cout << "irm" << endl;
    #endif
        //because of the annoyance of boolean vectors, you need
        //to use these functions to read and wr   //Number of rows is the sum of (gene network size choose 2)
    int totalRows = 0;
    for(unsigned int netSize = 0; netSize < geneNetSize.size(); netSize++){
        totalRows += nChooseTwo(geneNetSize[netSize]);
        if(nChooseTwo(geneNetSize[netSize]) == 0){
            cout << "wtf";
            cout << "gns = " << geneNetSize[netSize];
        }
        
    }
    int totalCols = 0;
    for(unsigned int classNum = 0; classNum < classSizes.size(); classNum++){
        totalCols += (classSizes[classNum] + 1);//add a column for every sample in a class + 1 for the rankTemplate for that class
    }
    #ifdef DEBUG
    cout << "changing size of rrm" << endl;
    #endif
    //now we need to resize the returnRankMatrix - it starts empty
    int totalCells = totalCols * totalRows;
    returnRankMatrix.resize(totalCells);
    //Now put on Matrix
    
    Matrix<bool> * rankMatrix = new Matrix<bool>(&returnRankMatrix, totalCols, totalRows);
        
    //now we need to generate the table of offsets for the rrm

    int numMatrices = geneNetSize.size() * (2*classSizes.size());//num genesets + numclasses + rt for each class
    
    #ifdef DEBUG
    cout << "building Matrix Mask" << endl;
    #endif
    offsets = new Matrix<int>(numMatrices,4);

    int col = 0;
    int row = 0;
    //int colOffSet = classSizes[0];
    int rowOffSet = nChooseTwo(geneNetSize[0]);
    //incrementers for geneSetSize and classSizes
    int geneSinc = 0;
    unsigned int classSinc = 0;
    
   int matindex = 0;
    while(matindex < numMatrices){
        if(classSinc == classSizes.size()){//newRow
            col = 0;
            //colOffset = classSize[0];
            row = row + nChooseTwo(geneNetSize[geneSinc++]);
            rowOffSet = nChooseTwo(geneNetSize[geneSinc]);
            classSinc = 0;
        }
        //the start coordinates
        (*offsets)(matindex, 0) = col;
        (*offsets)(matindex, 1) = row;
        (*offsets)(matindex, 2) = classSizes[classSinc];
        (*offsets)(matindex, 3) = rowOffSet;
        
        //add ranktemplate mask
        matindex++;
        col = col + classSizes[classSinc];
        (*offsets)(matindex,0) = col;
        (*offsets)(matindex,1) = row;
        (*offsets)(matindex,2) = 1;
        (*offsets)(matindex,3) = rowOffSet;
      
        col += 1;
        classSinc++;
        matindex++;
    }
    #ifdef DEBUG
    cout << "irm" << endl;
    #endif
     return rankMatrix;
}




/**
    This wraps a matrix around the data vector

**/

Matrix<double> * Dirac::initDataMatrix( vector<double> & data, int dsSize, vector<int> & classSizes){
    #ifdef DEBUG
    cout << "idm" << endl;
    #endif
     
    int totalRows = dsSize; // this is the number of genes in each sample
    //cal num of columns
    int totalCols = 0;
    for(unsigned int classNum = 0; classNum < classSizes.size(); classNum++){
        totalCols += classSizes[classNum]; //sum the class sizes to get the number of samples
    }
    #ifdef DEBUG
    cout << "idm" << endl;
    #endif
     //Now we generate the data matrix
    return new Matrix<double>(&data, totalCols, totalRows);

    

}
/**
A helper function, kinda removed from the rest of the class

takes an already computed rankMatrix, and an unclassified data vector and returns 0 if class 1, 1 if class 2
It also returns each classes score in the parameters.
**/
int Dirac::classify(vector<bool> & rankMatrix, int class1Size, int class2Size, vector<double> & unclassifiedVector, vector<int> & geneNet,int geneNetRankStart,
int geneNetRankSize, int geneNetStart, int geneNetSize, vector<double> & score ){
    //cout << rankMatrix.size() << endl;
    
    int numRows = rankMatrix.size()/((class1Size + 1) + (class2Size + 1));
    int rt1Index = class1Size*numRows + geneNetRankStart;
    int rt2Index = (class1Size+1)*numRows + class2Size*numRows + geneNetRankStart;
    //cout << numRows << endl;
    //cout << rt1Index << endl;

    //cout << rt2Index << endl;
    int match1=0;
    int match2=0;
    //loop through comparing genes in the classifying geneNet
    for (int i = geneNetStart; i < geneNetStart + geneNetSize-1; i++ ){
        for(int j = i+1; j< geneNetStart + geneNetSize; j++){
            bool val = unclassifiedVector[geneNet[i]] < unclassifiedVector[geneNet[j]];
           
            //cout << geneNet[i] << " " << geneNet[j];
            //cout << " " << rankMatrix[rt1Index] << " " << rankMatrix[rt2Index] << endl;
 
            if (val == rankMatrix[rt1Index++] )match1++;
            if (val == rankMatrix[rt2Index++] )match2++;

        }        
    }
    
    score.push_back( (double)match1/(double)(geneNetRankSize));
    score.push_back( (double)match2/(double)(geneNetRankSize) ); 
    if (score[0] > score[1]) 
        return 0;
    else
        return 1;
    //yeah, I know it could be written more compactly.  This is easier to read.
}

/**
    Given a network id, return the number of elements before that network in a
    rank vector/matrix.
**/
int Dirac::getNetworkRankStart(int network_id, vector<int> & geneNetSize){
    if (network_id == 0){
        return 0;
    } else {
        return nChooseTwo(geneNetSize[network_id-1]) + getNetworkRankStart(network_id-1, geneNetSize);
    }
}
/**
    Given a network id, return the size of that networks rank vector/matrix.
**/

int Dirac::getNetworkRankSize(int network_id, vector<int> & geneNetSize){
    return nChooseTwo(geneNetSize[0]);
}

int Dirac::getNetworkStart(int network_id, vector<int> & geneNetSize){
    if (network_id == 0){
        return 0;
    } else {
        return geneNetSize[network_id-1] + getNetworkStart(network_id-1, geneNetSize);
    }
}
bool cmp (double i,double j) { return (i>j);}
/**
Given the number of top networks you are interested in
Return a vector of the indices of the top scoring networks
**/
vector<int> Dirac::getTopNetworks(int numTopNets, vector<double> & rankMatchingScores, int class1Size, int class2Size ){
    vector<int> topNets;//a list of numTopNets, best networks
    //for each sample in 
    int numNets = rankMatchingScores.size()/(2*(class1Size+class2Size));
    vector<double> scores;
    vector<double> dist;
    for(int network=0; network<numNets; network++){
        int net_offset = 2*(class1Size+class2Size);
        int score = 0;
        double distance = 0.0;
        double v1, v2;
        //compare class1 against rt1
        int class_offset = class1Size + class2Size;
        for(int sample=0;sample < class1Size; sample++){
            v1 = rankMatchingScores.at(network*net_offset + sample);
            v2 = rankMatchingScores.at(network*net_offset + class_offset + sample);
            
            if( v1 - v2 > 0.0)score += class2Size;
            distance += class1Size*(v1-v2);           
        }
        for(int sample=class1Size;sample<class_offset; sample++){
            v1 = rankMatchingScores.at(network*net_offset + sample);
            v2 = rankMatchingScores.at(network*net_offset + class_offset + sample);
            
            if( v2 - v1 > 0.0)score += class2Size;
            distance += class1Size*(v2-v1);           
        }
        scores.push_back(score);
        dist.push_back(distance);        
    }
    //get top nets
    vector<double> scores_cp = scores;
    //partition scores
   std::partial_sort(scores_cp.begin(), scores_cp.begin() + numTopNets, scores_cp.end(), cmp );
    double part_score = scores_cp[numTopNets-1];//score of last top net
    vector<int> ties;
    for(int i = 0; i<(int)scores.size();i++){
        if(scores[i] > part_score){//add top
            topNets.push_back(i);
        } else if(scores[i] == part_score){ //store ties 
            ties.push_back(i);
        }
    }
    if (ties.size()){
        //cout << endl;
        //manage ties
        vector<double> dist_cp;
        
        for(int i = 0; i < (int)ties.size();i++){
            dist_cp.push_back(dist[ties[i]]);
        }
        //partition ties on distance
        std::partial_sort(dist_cp.begin(), dist_cp.begin()+(numTopNets-topNets.size()), dist_cp.end(), cmp);
        //double checking that nothing funny is going on
        if((numTopNets-topNets.size())-1 < 0) cout << "Error: Dirac.cpp line: " << __LINE__ << endl;


        double dist_part_score = dist_cp[(numTopNets-topNets.size())-1];

        for(int i = 0; i< (int)ties.size();i++){
            if(dist[ties[i]] >= dist_part_score && (int)topNets.size() < numTopNets){//add top distances
                    topNets.push_back(ties[i]);
            } 
        } 
    }
    return topNets;   
}
/**
int main(){
    Dirac a;
    vector<double> data;
    //generate trivial data
    int nGenes = 500;
    int nSamples = 20;
    float fInc = .05;
    float fSum = 1.0;
    for(int i = 0; i < nSamples; i++){
        if( i > 9 ) fInc = -.05;
        for(int j=0;j<nGenes; j++){
               data.push_back(fSum += fInc);     
        }
    }
    vector<double> unclassified;
    for( int i = 0 ; i<nGenes; i++){
        unclassified.push_back(1.0);
    }
    int dsSize = nGenes;
    vector<int> classSizes(2);
    classSizes[0] = 10;
    classSizes[1] = 10;
    srand(time(NULL));

    vector<int> geneNet;
    vector<int> geneNetSize;
    int gnSize;
    for(int i = 0; i<8; i++){
        gnSize = 0;
        for(int j = i; j< 20; j++){
            gnSize++;    
             geneNet.push_back(rand() % 500);            

        }
        geneNetSize.push_back(gnSize);

    } 
    vector<bool> returnRankMat;
    vector<double> returnRMS;
   vector<double> returnRankConservation;
    vector<double> returnRankDiff;
    for(unsigned int i=0;i<geneNet.size();i++){
        cout << geneNet[i] << " ";
    }
    
    a.enter(  data,  dsSize,  classSizes,
             geneNet, geneNetSize,
             returnRankMat, returnRMS,
             returnRankConservation );

    Matrix<bool> rm(&returnRankMat, 22, returnRankMat.size()/22);
    //rm.printBool();
    Matrix<double> dm (&data,20 ,dsSize);
    //dm.print();

    Matrix<double> rms(&returnRMS,20, returnRMS.size()/20);
    //rms.print();
    cout << "RC: ";
    for(unsigned int i = 0; i<returnRankConservation.size(); i++){
        cout << returnRankConservation[i] << " ";
    } 
    cout << endl;

    int net = 5;
    int geneNetRankStart = 0;
    for(int i = 0; i<net;i++){
        geneNetRankStart += (geneNetSize[i]*geneNetSize[i]-1)/2;
    }    
    int geneNetRankSize = (geneNetSize[net]*geneNetSize[net]-1)/2;
    double score1 = 0;
    double score2 = 0;
    vector<double> score;
    int result = a.classify(returnRankMat, classSizes[0], classSizes[1], 
        unclassified, geneNet,geneNetRankStart, geneNetRankSize, 
        net, geneNetSize[net], score);
    vector<int> topNets = a.getTopNetworks(3,returnRMS, classSizes[0], classSizes[1]);
    for(int i = 0; i<topNets.size();i++){
        cout << "tn[" << i << "] = ";
        cout << topNets[i] << endl;
    }
    cout << score[0] << endl;
    cout << score[1] << endl;
    cout << result << endl;
    return 0;
}**/
