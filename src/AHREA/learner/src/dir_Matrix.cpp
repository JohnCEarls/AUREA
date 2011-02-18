#include "dir_Matrix.h"
#include <iostream>
using std::vector;
using std::cout;
using std::endl;
using std::cerr;

//#define DEBUG

template <class T>
Matrix<T>::Matrix(int x){
    trans = false;
    myVector = true;
    nCol = x;
    nRow = x;
    data = new vector<T>(x*x);
    
}

template <class T>
Matrix<T>::Matrix(int nCols, int nRows){
    trans = false;
    myVector = true;
    nCol = nCols;
    nRow = nRows;
    data = new vector<T>(nCols*nRows);
    #ifdef DEBUG
    for(int i = 0; i< nCols*nRows; i++){
        data->at(i) = i;
    }
    #endif
    
}

template <class T>
Matrix<T>::Matrix(vector<T> * raw, int nCols, int nRows){
    trans = false;
    myVector = false;
    nCol = nCols;
    nRow = nRows;
    data = raw;

    
}
template <class T>
Matrix<T>::~Matrix(){
    if (myVector) delete data;
}

template <class T>
Matrix<T>::Matrix(const Matrix<T> & orig){
    data = new vector<T>(*(orig.data));
    trans = orig.trans;
    myVector = true;
    nCol = orig.nCol;
    nRow = orig.nRow;
}

template <class T>
const Matrix<T> & Matrix<T>::operator=(const Matrix<T> &orig){
    if(this != &orig){
        //clear
        if (myVector) delete data;
        //copy
        data = new vector<T>(*(orig.data));
        trans = orig.trans;
        myVector = true;
        nCol = orig.nCol;
        nRow = orig.nRow;
         
    }
    return *this;
}

template <class T>
T & Matrix<T>::operator()(int col, int row){
    #ifdef DEBUG
    //cout << "col=" << col;
    //cout << "row=" << row;
    #endif
    return data->at(colRowToIndex(col,row));//row y, column x
}

template <class T>
void Matrix<T>::assignsm(int col, int row,T val, int colOffset, int rowOffset){
    assign(col + colOffset, row + rowOffset, val);
}
template <class T>
T Matrix<T>::getValsm(int col, int row, int colOffset, int rowOffset){
    return getVal(col + colOffset, row + rowOffset);
}


template <class T>
void Matrix<T>::assign(int col, int row, T val){
    data->at(colRowToIndex(col,row)) = val;
}

template <class T>
T Matrix<T>::getVal(int col, int row){
    return data->at(colRowToIndex(col, row));

}

template <class T>
void Matrix<T>::transpose(){
    trans = !trans;
    
    int temp = nCol;
    nCol = nRow;
    nRow = temp;
    
}
template <class T>
void Matrix<T>::print(){
    #ifdef DEBUG
    cout<<"in print" << endl;
    #endif
    for(int i=0;i<this->nRows();i++){
        for(int j = 0; j< this->nCols(); j++){
            
            cout << (*this)(j,i)<< " ";
        }
        cout << endl;
    }
     #ifdef DEBUG
    cout << "out of print" << endl;
    #endif
}
template <class T>
void Matrix<T>::printBool(){
     for(int i=0;i<nRows();i++){
        for(int j = 0; j< nCols(); j++){
            
            cout << data->at(colRowToIndex( j, i));
        }
        cout << endl;
    }
}

template <class T>
void Matrix<T>::checkTrans(int & x, int & y){
    if(trans){
        int temp = x;
        x = y;
        y = x;
    }
}

template <class T>
void Matrix<T>::allVal(T val){
    for(int i = 0; i < nRows(); i++){
        for(int j = 0; j < nCols(); j++){
            #ifdef DEBUG
            //cout << "col =" << j;
            //cout << ", row = " << i;
            #endif
            data->at(colRowToIndex(j,i)) = val;
        }
    }
}

template <class T>
int Matrix<T>::nCols(){
    return nCol;
}

template <class T>
int Matrix<T>::nRows(){
    return nRow;
}

template <class T>
int Matrix<T>::colRowToIndex(int col, int row){
    if(trans) return row*nCol + col;
    return col*nRow + row;
}



#ifdef DEBUG
int main(){
    Matrix<float> a(10,10);
    a.print();
    int colOff = 1;
    int rowOff = 0;
    int nCols = 1;
    int nRows = 10;
    for(int j = 0; j< nRows; j++){
        for(int i = 0; i<nCols;i++){
            cout <<a.getValsm(i,j,colOff,rowOff) << " ";
        }
        cout << endl;
    }
    //a.allVal(6.0);
   // a(1,0)=12.0;
   // a(0,2)=8.0;
   // a.print();
   // a.transpose();
   // a.print();
   // a.transpose();
    a.print();
}
#endif
