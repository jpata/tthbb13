#ifndef MECOMBINATION_H // header guards
#define MECOMBINATION_H

#include <map>
#include <cmath>
#include <vector>
#include <map>

//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////


// permutations for SL(4,2) events with six jets matched to six quarks

extern const int permutations_TYPE0_S[12];
extern const int permutations_TYPE0_B[12];

// permutations for SL(4,>=3) events with five jets matched to five quarks

extern const int permutations_TYPE0_5EXTRA_S[60];

extern const int permutations_TYPE0_5EXTRA_B[60];

//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////

// permutations for SL(4,1) events with five jets matched to five quarks,
// and one q from W->qq' lost

extern const int permutations_TYPE2_S[12];
extern const int permutations_TYPE2_B[12];


//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////

// permutations for SL(4,2) events with five jets matched to five quarks,
// and one q from W->qq' lost

extern const int permutations_TYPE1_S[24];
extern const int permutations_TYPE1_B[24];

//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////

// permutations for DL(4) events with all four jets matched to four quarks

extern const int permutations_TYPE6_S[12];
extern const int permutations_TYPE6_B[12];

//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////

// permutations for inequivalent flavor 4b 2q assigments to 6 jets

extern const int permutations_6J_S[15];

// permutations for inequivalent flavor 4q 2b assigments to 6 jets

extern const int permutations_6J_B[15];

//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////

/*
int permutations_6j_FULL[720];
int myCounter=0;
for(int i = 2; i <8 ; i++ ){
  for(int j = 2; j<8 ; j++){
    if(j==i) continue;
    for(int k = 2; k<8 ; k++){	
      if(k==i || k==j) continue;
      for(int l = 2; l<8 ; l++){
	if(l==i || l==j || l==k) continue;
	for(int m = 2; m<8 ; m++){
	  if(m==i || m==j || m==k || m==l) continue;
	  for(int n = 2; n<8 ; n++){
	    if(n==i || n==j || n==k || n==l || n==m) continue;
	    permutations_6j_FULL[myCounter] = i*100000 + j*10000 + k*1000 + l*100 + m*10 + n*1;
	    myCounter++;
	  }
	}	  
      }
    }
  }
 }
*/

//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////

// permutations for inequivalent flavor 4b 1q assigment to 5 jets

extern const int permutations_5J_S[5];

// permutations for inequivalent flavor 2b 3q assigment to 5 jets

extern const int permutations_5J_B[10];

//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////

// permutations for inequivalent flavor 4b assigment to 4 jets

extern const int permutations_4J_S[1];

// permutations for inequivalent flavor 2b 2q assigment to 4 jets

extern const int permutations_4J_B[6];

//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////

namespace perm_maps {

  using namespace std;
//map1 -> i => xxxxxx
//map2 -> xxxxxx => i
//where xxxxxx is a 6-digit int consisting of 1-s and 0-s signifiying the perm_to_gen matching
	extern const map<int, int> map1;
	extern const map<int, int> map2;
	extern const char* positions[6];

  extern int get_n(int x, int n);
  extern vector<int> comb_as_vector(int x, int length);
	extern bool has_n(int x, int n);
	extern bool higgs_b_missed(int x);
	extern bool top_b_missed(int x);
  extern bool w_q1_missed(int x);
  extern bool w_q2_missed(int x);
  extern bool w_qq_missed(int x);
	extern int count_matched(int x);
	
}

#endif
