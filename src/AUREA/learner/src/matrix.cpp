#include "matrix.h"


vector< vector<double> > transpose(vector< vector<double> > &X)
{
  int i,j;
  
  int nrows=X.size();
  int ncols=X[0].size();

  vector< vector<double> > XT(ncols);
  for (i=0;i<ncols;i++)
    {
      XT[i].resize(nrows);
    }
  for (i=0;i<nrows;i++)
    {
      for (j=0;j<ncols;j++)
	{
	  XT[j][i]=X[i][j];
	}
    }
  return XT;


}
