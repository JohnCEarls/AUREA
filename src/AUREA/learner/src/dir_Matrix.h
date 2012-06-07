#ifndef MATRIX_H
#define MATRIX_H
#include <cstddef>
#include <vector>
using std::vector;
template <class T>
class Matrix{
    public:
        Matrix(int x);//square matrix
        Matrix(int nCols, int nRows);
        Matrix(vector<T> * raw,int nCols,int nRows);
        ~Matrix();
        Matrix(const Matrix<T> & orig);
        const Matrix<T> & operator=(const Matrix<T> & rhs);
        void transpose();
        T &  operator()(int col, int row);
        void allVal(T val);
        int nCols();
        int nRows();
        void print();
       void assignsm(int col, int row,T val, int colOffset, int rowOffset);
        T getValsm(int col, int row, int colOffset, int rowOffset); 
        //because of the annoyance of boolean vectors, you need
        //to use these functions to read and write from T = bool
        void assign(int x, int y, T val);
        T getVal(int x, int y);
        void printBool();
   private:
        vector<T> * data;
        bool myVector;
        bool trans;
        int nCol, nRow;
        int colRowToIndex( int col, int row);
        void checkTrans(int & x, int & y);

};

#endif
