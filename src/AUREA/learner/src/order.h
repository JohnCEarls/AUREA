#ifndef ORDER_H
#define ORDER_H
#include <cstddef>
#include <vector>
#include <iostream>
#include <algorithm>


using namespace std;

void compute_ranks(const vector<double> &, vector<double> &);


class pair_double_with_int
{
 private:
  double x;
  int i;
 public:
  pair_double_with_int()
    {
    }
  pair_double_with_int(double y, int j)
    {
      x=y;   
      i=j;
    }
  double getx();
  int geti();
  friend bool operator<(pair_double_with_int p1, pair_double_with_int p2)
    {
      return (p1.x<p2.x);
    }
};

class pair_double_with_double
{
 private:
  double x;
  double y;
 public:

  pair_double_with_double()
    {
    }
  pair_double_with_double(double xt, double yt)
    {
      x=xt;
      y=yt;
    }
  void setx(double xt)
    {
      x=xt;
    }
  void sety(double yt)
    {
      y=yt;
    }
  double getx()
    {
      return x;
    }
  double gety()
    {
      return y;
    }
  friend bool operator<(pair_double_with_double p1, pair_double_with_double p2)
    {
      return (p1.x<p2.x);
    }
};

void sort_along(vector<double> &,vector<double> &);

template<class T>
class pair_double_with_T
{
 private:
  double x;
  T y;
 public:

  pair_double_with_T()
    {
    }
  pair_double_with_T(double xt, T yt)
    {
      x=xt;
      y=yt;
    }
  void setx(double xt)
    {
      x=xt;
    }
  void sety(T yt)
    {
      y=yt;
    }
  double getx()
    {
      return x;
    }
  T gety()
    {
      return y;
    }
  friend bool operator<(pair_double_with_T p1, pair_double_with_T p2)
    {
      return (p1.x<p2.x);
    }
};


//
// sort a double vector v and apply the same 
// sorting permutation to a vector w
//
// example of usage: if w has type vector<double>
// 
// 
//    sort_along<double>(v,w)
//
//
//
template<class T>
void sort_along(vector<double> &v, vector<T> &w)
{
  // create space to load all pairs
  int n=v.size();
  vector< pair_double_with_T<T> > V;
  pair_double_with_T<T> p;

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
    }

  return;

}



#endif
