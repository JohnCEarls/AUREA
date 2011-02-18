#include "order.h"


double pair_double_with_int::getx()
{
  return x;
}
int pair_double_with_int::geti()
{
  return i;
}




// compute ranks with ties dealt with by averaging
void compute_ranks(const vector<double> &v, vector<double> &r)
{

  // load a vector of pairs of the form (v[0],0), (v[1],1), ...
  int count=0;

  vector<pair_double_with_int> vector_of_pairs;
  vector<double>::const_iterator it;
  it=v.begin();
  while(it!=v.end())
    {     
      pair_double_with_int newpair(*it,count);
      count++;
      vector_of_pairs.push_back(newpair);
      it++;
    }

  // sort vector of pairs
  sort(vector_of_pairs.begin(), vector_of_pairs.end());

  // compute the integer version of ranks (nothing to do with ties here)
  int n=v.size();
  vector<double> s(n); // vector of sorted values 
  vector<int> perm(n); // sorting permutation 
  vector<pair_double_with_int>::iterator it2;

  it2=vector_of_pairs.begin();
  count=0;
  while(it2!=vector_of_pairs.end())
    {
      int i=it2->geti();
      double x=it2->getx();

      perm[count]=i;
      s[count]=x ;

      it2++;
      count++;
    }


  // make a vector with the number of values tied in each 
  // clump of ties
  vector<int> count_vector;
  double value=s[0];
  int tied_count=1;
  int total_counted=0;
  int m=0;
  for (int i=1;i<n;i++)
    {
      if (s[i]==s[i-1])
	{
	  tied_count++;
	}
      else
	{
	  count_vector.push_back(tied_count);
	  m++;
	  total_counted+=tied_count;
	  value=s[i];
	  tied_count=1;
	}
    }
  if (total_counted<n)
    {
      count_vector.push_back(n-total_counted);
      m++;
    }

  // make a vector of ranks 
  vector<double> rk(n);
  double sum=0;
  double rval;
  int k;
  int pos=0;
  for (int i=0;i<m;i++)
    {
      k=count_vector[i];
      rval=sum+.5*((double)k+1.);
      for (int j=0;j<k;j++)
	{
	  rk[pos]=rval;
	  pos++;
	}
      sum+=(double)k;
    }

  r.resize(n);
  for (int i=0;i<n;i++)
    {
      r[perm[i]]=rk[i];
    }


  return;
  
}


void sort_along(vector<double> &v, vector<double> &w)
{
  // create space to load all pairs
  int n=v.size();
  vector<pair_double_with_double> V;
  pair_double_with_double p;

  for (int i=0;i<n;i++)
    {
      p.setx(v[i]);
      p.sety(w[i]);
      V.push_back(p);
    }
  
  sort(V.begin(), V.end());

  for (int i=0;i<n;i++)
    {
      v[i]=V[i].getx();
      w[i]=V[i].gety();
      
      //cout << v[i] << " " << w[i] << "\n";

    }

  return;

}






