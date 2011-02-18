#include "learn_classifiers.h"
//
// filtered TSP with no tie-breaking
//
extern "C" {
  SEXP learn_mtsp_classifier(SEXP dmat, SEXP blab, SEXP nvec)
{

  //
  // Extract the expression matrix & dimensions
  //
  vector< vector<double> > xmat=Rmatrix_to_CPP_matrix(dmat);
  int nsamples=xmat.size(); 
  int ngenes=xmat[0].size();

  //
  // Extract the labels (0/1-vector)
  //
  int *blabptr=INTEGER(blab);
  vector<int> y(nsamples);
  for (int i=0;i<nsamples;i++)
    {
      y[i]=blabptr[i];
    }

  //
  // Extract the filter condition (single integer)
  //
  int *nvecptr=INTEGER(nvec);
  int filternumber1=nvecptr[0];
  int filternumber2=nvecptr[1];

  //
  // Replace columns of expression matrix by ranks in columns.
  //
  vector< vector<double> > rmat(nsamples);
  for (int i=0;i<nsamples;i++)
    {
      compute_ranks(xmat[i],rmat[i]);
    }
  
  //
  // Transpose rmat so we can do operations by gene
  //
  vector< vector<double> > r=transpose(rmat);

  //
  // Compute Wilcoxon test statistic for each gene.
  //
  vector<double> w(ngenes);
  for (int i=0;i<ngenes;i++)
    {
      vector<double> u0;
      vector<double> u1;
      for (int j=0;j<nsamples;j++)
	{
	  if (y[j]==0)
	    {
	      u0.push_back(rmat[j][i]);
	    }
	  else
	    {
	      u1.push_back(rmat[j][i]);
	    }
	}
      w[i]=wilcoxon_two_sided_test_statistic(u0,u1);
    }
  //
  // Make a list of indices 0-th corresponds to highest wilcoxon,
  // 1-th corresponds to second highest wilcoxon, etc.
  //
  vector<int> is(ngenes);
  for (int i=0;i<ngenes;i++)
    {
      is[i]=i;
    }
  
  //for (int i=0;i<ngenes;i++)
  //  {
  //    Rprintf("%d %f \n", i,  w[i]);
  //  }
  sort_along<int>(w,is);
  
  //
  // Go from biggest wilcoxon to smallest.
  //
  reverse(is.begin(),is.end());
  reverse(w.begin(),w.end());

  //
  // Some wilcoxon stats could be tied, so extent the search range as necessary.
  //
  int f;
  double wmax=w[filternumber1];
  for (f=filternumber1+1;f<ngenes;f++)
    {
      if (w[f]<wmax) break;
    }
  filternumber1=f;
  if (filternumber1>ngenes)
    {
      filternumber1--;
    }  
  for (f=filternumber2+1;f<ngenes;f++)
    {
      if (w[f]<wmax) break;
    }
  filternumber2=f;
  if (filternumber2>ngenes)
    {
      filternumber2--;
    }  

  //
  // For each 2-tuple, compute counts and maintain a list of 2-tuples 
  // with maximum score. 
  //
  double SCORE, MAXSCORE=0;
  vector<int> I1LIST, I2LIST;
  for (int i1=0;i1<filternumber1;i1++)
    {
      for (int i2=i1+1;i2<filternumber2;i2++)
	{
	  int ind1=is[i1];
	  int ind2=is[i2];
	  SCORE=compute_pair_score(xmat,y,ind1,ind2);
	  if (SCORE==MAXSCORE)
	    {
	      I1LIST.push_back(ind1);
	      I2LIST.push_back(ind2);
	    }
	  if (SCORE>MAXSCORE)
	    {
	      MAXSCORE=SCORE;
	      I1LIST.clear();
	      I2LIST.clear();
	      I1LIST.push_back(ind1);
	      I2LIST.push_back(ind2);
	    }
	}
    }
  int NMAX=I1LIST.size();
  Rprintf("maximum score achieved = %f \n", MAXSCORE);
  Rprintf("number of best pairs = %d \n", I1LIST.size());
  for (int i=0;i<NMAX;i++)
    {
      Rprintf("%3d %3d \n", I1LIST[i],I2LIST[i]);
    }
    //
  // Prepare output to R calling program.
  //

  // allocate space for a list of pointers of size listsize.
  SEXP outvec;
  int listsize=2;
  PROTECT(outvec=allocVector(VECSXP, listsize));
  vector<SEXP> tmp(listsize);
  
  // 
  // output the pairs as two lists of integers
  // note that R indices get incremented by 1
  //
  PROTECT(tmp[0]=NEW_INTEGER(NMAX)); 
  for (int i=0;i<NMAX;i++)
    {
      INTEGER_POINTER(tmp[0])[i]=I1LIST[i]+1;
    }
  SET_VECTOR_ELT(outvec,0,tmp[0]);

  PROTECT(tmp[1]=NEW_INTEGER(NMAX)); 
  for (int i=0;i<NMAX;i++)
    {
      INTEGER_POINTER(tmp[1])[i]=I2LIST[i]+1;
    }
  SET_VECTOR_ELT(outvec,1,tmp[1]);

  UNPROTECT(3);
  return outvec;
  
  
}
}
