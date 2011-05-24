#include "utils.h"

//
// Convert an R matrix to a C++ matrix - note that this is by column.
//
/**
No R means no R matrix
vector< vector<double> > Rmatrix_to_CPP_matrix(SEXP dmat)
{
   
   SEXP mdim;
   PROTECT(mdim=getAttrib(dmat, R_DimSymbol));
   int mnrows=INTEGER(mdim)[0];
   int mncols=INTEGER(mdim)[1];

   double *mvec=NUMERIC_POINTER(AS_NUMERIC(dmat));
   vector< vector<double> > mat(mncols);
   int k=0;
   for (int i=0;i<mncols;i++)
   {
      mat[i].resize(mnrows);
      for (int j=0;j<mnrows;j++)
      {
         mat[i][j]=mvec[k];
         k++;
      }
   }
   UNPROTECT(1);
   return mat;  
}
**/

//Puts the data from data into xmat
void vector_to_matrix(vector<double> & data, vector< vector<double> > & xmat){

    //addData
    int numGenes = xmat[0].size();
    int samp = -1;
    
    for(int i = 0; i < data.size(); i++){
        int gene = i % numGenes;
        if (gene == 0) samp++;
        xmat[samp][gene] = data[i];        
    }//done
}

//
// Compute the probability table for a pair.
//
vector< vector<double> > compute_pair_ptable(vector< vector<double> > &xmat, vector<int> &y, int i1,int i2)
{

  int i,j;

  int ncols=xmat.size();

  vector<double> zcol(2,0);
  vector< vector< double> > ftab(2);
  ftab[0].resize(2);
  ftab[1].resize(2);
  for (j=0;j<2;j++)
    {
      ftab[0][j]=0;
      ftab[1][j]=0;
    }
  int y0count=0,y1count=0;
  for (j=0;j<ncols;j++)
    {
      if (y[j]==0) 
	{
	  y0count++;
	}
      else
	{
	  y1count++;
	}
      vector<double> tcolct(2,0); // counts for this particular chip

      // record which inequalities hold
      int icount=0;
      if (xmat[j][i1]<=xmat[j][i2])
	{
	  tcolct[0]=1;
	  icount++;
	}
      if (xmat[j][i2]<=xmat[j][i1])
	{
	  tcolct[1]=1;
	  icount++;
	}      
      for (i=0;i<2;i++)
	{
	  tcolct[i]/=(double)icount;
	  ftab[y[j]][i]+=tcolct[i];
	}
    }
  for (i=0;i<2;i++)
    {
      ftab[0][i]/=(double)y0count;
      ftab[1][i]/=(double)y1count;
    }

  return ftab;
}


vector< vector<double> > compute_triple_ptable(vector< vector<double> > &xmat, vector<int> &y, int i1,int i2, int i3)
{

  int i,j;

  int ncols=xmat.size();

  vector<double> zcol(6,0);
  vector< vector< double> > ftab(2);
  ftab[0].resize(6);
  ftab[1].resize(6);
  for (j=0;j<6;j++)
    {
      ftab[0][j]=0;
      ftab[1][j]=0;
    }
  int y0count=0,y1count=0;
  for (j=0;j<ncols;j++)
    {
      if (y[j]==0) 
	{
	  y0count++;
	}
      else
	{
	  y1count++;
	}
      vector<double> tcolct(6,0); // counts for this particular chip

      // record which inequalities hold
      int icount=0;
      if ((xmat[j][i1]<=xmat[j][i2])&&(xmat[j][i2]<=xmat[j][i3]))
	{
	  tcolct[0]=1;
	  icount++;
	}
      if ((xmat[j][i1]<=xmat[j][i3])&&(xmat[j][i3]<=xmat[j][i2]))
	{
	  tcolct[1]=1;
	  icount++;
	}      
      if ((xmat[j][i2]<=xmat[j][i1])&&(xmat[j][i1]<=xmat[j][i3]))
	{
	  tcolct[2]=1;
	  icount++;
	}
      if ((xmat[j][i2]<=xmat[j][i3])&&(xmat[j][i3]<=xmat[j][i1]))
	{
	  tcolct[3]=1;
	  icount++;
	}
      if ((xmat[j][i3]<=xmat[j][i1])&&(xmat[j][i1]<=xmat[j][i2]))
	{
	  tcolct[4]=1;
	  icount++;
	}
      if ((xmat[j][i3]<=xmat[j][i2])&&(xmat[j][i2]<=xmat[j][i1]))
	{
	  tcolct[5]=1;
	  icount++;
	}
      for (i=0;i<6;i++)
	{
	  tcolct[i]/=(double)icount;
	  ftab[y[j]][i]+=tcolct[i];
	}
    }
  for (i=0;i<6;i++)
    {
      ftab[0][i]/=(double)y0count;
      ftab[1][i]/=(double)y1count;
    }

  return ftab;
}

double compute_score_from_pair_ptable(vector< vector<double> > &ftab)
{
  double sum=0;
  for (int i=0;i<2;i++)
    {
      sum+=fabs(ftab[0][i]-ftab[1][i]);
    }
  return sum;
  
}

double compute_score_from_triple_ptable(vector< vector<double> > &ftab)
{
  double sum=0;
  for (int i=0;i<6;i++)
    {
      sum+=fabs(ftab[0][i]-ftab[1][i]);
    }
  return sum;
  
}


double compute_pair_score(vector< vector<double> > &xmat, vector<int> &y, int i1, int i2)
{
  vector< vector<double> > ftab=compute_pair_ptable(xmat,y,i1,i2);
  double score=compute_score_from_pair_ptable(ftab);
  return score;
}
double compute_triple_score(vector< vector<double> > &xmat, vector<int> &y, int i1, int i2, int i3)
{
  vector< vector<double> > ftab=compute_triple_ptable(xmat,y,i1,i2,i3);
  double score=compute_score_from_triple_ptable(ftab);
  return score;
}
double compute_triple_secondary_score(vector< vector<double> > &xmat, vector<int> &y, int i1, int i2, int i3)
{
  double score12=compute_pair_score(xmat,y,i1,i2);
  double score13=compute_pair_score(xmat,y,i1,i3);
  double score23=compute_pair_score(xmat,y,i2,i3);
  double score=score12+score13+score23;
  return score;
}
