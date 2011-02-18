#include "learn_classifiers.h"
#include <stdio.h>
#include <iostream>
using std::cout;
using std::endl;
//extern "C" {
vector< vector<double> > learn_tst_classifier(vector<double> & data,int dsSize, vector<int> & classSizes, vector<int> & nvec, vector<int> & I1LIST, vector<int> & I2LIST, vector<int> & I3LIST)
{

 
    vector< vector<double> > xmat(data.size()/dsSize, vector<double>(dsSize));
  //puts values in data matrix int xmat

  vector_to_matrix(data, xmat);
  int nsamples=xmat.size();
  int ngenes=xmat[0].size();

  //
  // Extract the labels (0/1-vector)
  //
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
  int filternumber1=nvec[0];
  int filternumber2=nvec[1];
  int filternumber3=nvec[2];  


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
	  if (y[j]==0)//class1
	    {
	      u0.push_back(rmat[j][i]);
	    }
	  else //class2
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

    sort_along<int>(w,is);
  
  //
  // Go from biggest wilcoxon to smallest.
  //

  reverse(is.begin(),is.end());
  reverse(w.begin(),w.end());
/**for(int i=0;i<is.size();i++){
    cout << is.at(i)<< ", " << w.at(i) << endl;
}**/

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
  for (f=filternumber3+1;f<ngenes;f++)
    {
      if (w[f]<wmax) break;
    }
  filternumber3=f;
  if (filternumber3>ngenes)
    {
      filternumber3--;
    }  


  //
  // For each 3-tuple, compute counts and maintain a list of 3-tuples 
  // with maximum score. 
  //

  double SCORE1, MAXSCORE1=0, SCORE2, MAXSCORE2=0;
  //vector<int> I1LIST, I2LIST, I3LIST;
  int ind1, ind2, ind3;
//    cout << "filternumber1" << filternumber1 << endl;
// cout << "filternumber2" << filternumber2 << endl;
// cout << "filternumber3" << filternumber3 << endl;
  for (int i1=0;i1<filternumber1;i1++)
    {
      for (int i2=i1+1;i2<filternumber2;i2++)
	{
	  for (int i3=i2+1;i3<filternumber3;i3++)
	    {
	      ind1=is[i1];
	      ind2=is[i2];
	      ind3=is[i3];

	      SCORE1=compute_triple_score(xmat,y,ind1,ind2,ind3);
	      if (SCORE1==MAXSCORE1)
		{
		  // check secondary score
		  SCORE2=compute_triple_secondary_score(xmat,y,ind1,ind2,ind3);
		  {
		    if (SCORE2==MAXSCORE2)
		      {
			I1LIST.push_back(ind1);
			I2LIST.push_back(ind2);
			I3LIST.push_back(ind3);
		      }
		    if (SCORE2>MAXSCORE2)
		      {
			// new secondary max score
			MAXSCORE2=SCORE2;
			I1LIST.clear();
			I2LIST.clear();
			I3LIST.clear();
			I1LIST.push_back(ind1);
			I2LIST.push_back(ind2);
			I3LIST.push_back(ind3);
		      }
		  }
		}
	      if (SCORE1>MAXSCORE1)
		{
		  // new primary max score
		  MAXSCORE1=SCORE1;
		  MAXSCORE2=compute_triple_secondary_score(xmat,y,ind1,ind2,ind3);
		  I1LIST.clear();
		  I2LIST.clear();
		  I3LIST.clear();
		  I1LIST.push_back(ind1);
		  I2LIST.push_back(ind2);
		  I3LIST.push_back(ind3);
		}
	    }
	}
    }
    return xmat;
  
}
//}
