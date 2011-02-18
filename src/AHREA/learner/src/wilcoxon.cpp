#include "wilcoxon.h"

double wilcoxon_test_statistic(const vector<double> &x, const vector<double> &y)
{
  // compute the wilcoxon test statistic
  // i.e. the sum of ranks of the y's in the combined sample
  // notation is as in Rice p.408
  int i,j;
  int m,n;
  vector<double> z, zr;
  n=(int)x.size();
  m=(int)y.size();
  for (i=0;i<n;i++)
    {
      z.push_back(x[i]);
    }
  for (j=0;j<m;j++)
    {
      z.push_back(y[j]);	    
    }
  compute_ranks(z,zr);
  double sum=0;
  for (i=n;i<n+m;i++)
    {
      sum+=zr[i];
    }
  return sum;
}
//
// Version of wilcoxon two-sided test that uses two input samples.
//
double wilcoxon_two_sided_test_statistic(const vector<double> &x, const vector<double> &y)
{
  double n=(double)x.size();
  double m=(double)y.size();
  double W=wilcoxon_test_statistic(x,y);
  double mu=(m)*(m+n+1.)/2.;
  double sd=sqrt(m*n*(m+n+1)/12.);
  double c=fabs((W-mu)/sd);
  return c;
}
//
// Version of wilcoxon that uses as input a vector of data values (xdata)
// and a binary vector (group) telling which sample is which.
//
double wilcoxon_two_sided_test_statistic(const vector<double> &xdata,
					 const vector<int> &group)
{
  vector<double> x,y;
  int n=xdata.size();
  for (int i=0;i<n;i++)
    {
      if (group[i]==0)
	{
	  x.push_back(xdata[i]);
	}
      else
	{
	  y.push_back(xdata[i]);
	}
    }
  return wilcoxon_two_sided_test_statistic(x,y);
}
