#include "learn_classifiers.h"
//
// TSP with tie-breaking (possible muliple pairs)
//
#include <stdio.h>



extern "C" {
    // replace dmat with double vector
    // add nGenes
    // blah is the class size so in blabptr create mask
    //
  void learn_utsp_classifier(vector<double> & data,int dsSize, vector<int> & classSizes, vector<int> & nvec, vector<int> & I1LIST, vector<int> & I2LIST )
{

  //
  // Extract the expression matrix & dimensions
  //
  
  vector< vector<double> > xmat(data.size()/dsSize, vector<double>(dsSize));
  //puts values in data matrix int xmat
  vector_to_matrix(data, xmat);
  int nsamples=xmat.size(); 
  int ngenes=xmat[0].size();

  //
  // Extract the labels (0/1-vector)
  //
  //int *blabptr=INTEGER(blab);
  vector<int> y(nsamples);
  double n0=classSizes[0], n1=classSizes[1];
  for (int i=0;i < nsamples;i++)
  {
      if(i<classSizes[0]){
        y[i] = 0;
      } else {
        y[i] = 1; 
      }
  }

  //
  // Extract the filter condition (single integer)
  //
  //int *nvecptr=INTEGER(nvec);
  int filternumber1=nvec[0];
  int filternumber2=nvec[1];



  //
  // Replace columns of expression matrix by ranks in columns.
  //
  vector< vector<double> > rmat(nsamples);
  for (int i=0;i<nsamples;i++)
    {
      compute_ranks(xmat[i],rmat[i]);
    }
  //
  // Compute average ranks within classes for each gene.
  //
  vector<double> arank0(ngenes);
  vector<double> arank1(ngenes);
  for (int i=0;i<ngenes;i++)
    {
      double s0=0;
      double s1=0;
      for (int k=0;k<nsamples;k++)
	{
	  if (y[k]==0)
	    {
	      s0+=rmat[k][i];
	    }
	  else
	    {
	      s1+=rmat[k][i];
	    }
	}
      arank0[i]=s0/n0;
      arank1[i]=s1/n1;
    }
  //
  // Transpose rmat so we can do operations by gene
  //
  vector< vector<double> > r=transpose(rmat);

  //
  // Compute Wilcoxon test statistic for each gene.
  //
  vector<double> w(ngenes);
  for (int i=0;i<ngenes;i++) {
      vector<double> u0;
      vector<double> u1;
      for (int j=0;j<nsamples;j++)	{
	    if (y[j]==0)	    {
	      u0.push_back(rmat[j][i]);
	    } else  {
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
  double SCORE1, MAXSCORE1=0, SCORE2, MAXSCORE2=0;
  //vector<int> I1LIST, I2LIST;
  int ind1, ind2;
  for (int i1=0;i1<filternumber1;i1++)
    {
      for (int i2=i1+1;i2<filternumber2;i2++)
        {
          ind1=is[i1];
          ind2=is[i2];
          SCORE1=compute_pair_score(xmat,y,ind1,ind2);
          if (SCORE1==MAXSCORE1)
            {
              SCORE2=fabs((arank0[ind1]-arank0[ind2])-(arank1[ind1]-arank1[ind2]));
              if (SCORE2==MAXSCORE2)
            {
              I1LIST.push_back(ind1);
              I2LIST.push_back(ind2);
            }
              if (SCORE2>MAXSCORE2)
            {
              SCORE2=MAXSCORE2;
              I1LIST.clear();
              I2LIST.clear();
              I1LIST.push_back(ind1);
              I2LIST.push_back(ind2);
            }
            }
          if (SCORE1>MAXSCORE1)
            {
              MAXSCORE1=SCORE1;
              MAXSCORE2=fabs((arank0[ind1]-arank0[ind2])-(arank1[ind1]-arank1[ind2]));
              I1LIST.clear();
              I2LIST.clear();
              I1LIST.push_back(ind1);
              I2LIST.push_back(ind2);
            }
        }
    }
    //now lets put them in the right order j.e.
    for( int i=0; i< I1LIST.size(); i++){
        vector< vector<double> > ftab=compute_pair_ptable(xmat,y,I1LIST[i],I2LIST[i]);

     double score_sum =ftab[0][0]-ftab[0][1] + ftab[1][1] - ftab[1][0];

        if (score_sum > 0){//order is backwards
            //swap
            int temp = I1LIST[i];
            I1LIST[i] = I2LIST[i];
            I2LIST[i] = temp;
        }
    }



}
}
