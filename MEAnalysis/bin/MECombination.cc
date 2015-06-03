#include "TTH/MEAnalysis/interface/MECombination.h"

//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////


// permutations for SL(4,2) events with six jets matched to six quarks

const int permutations_TYPE0_S[12] =  
  {234567, 534267,     
   634725, 734625,     
   534762, 734562,     
   234765, 734265,     
   634572, 534672,     
   234675, 634275      
  };
const int permutations_TYPE0_B[12] =  
  {234567, 534267,     
   634725, 734625,     
   534762, 734562,     
   234765, 734265,     
   634572, 534672,     
   234675, 634275      
  };

// permutations for SL(4,>=3) events with five jets matched to five quarks

const int permutations_TYPE0_5EXTRA_S[60] =  
  {234567, 534267,     
   634725, 734625,     
   534762, 734562,     
   234765, 734265,     
   634572, 534672,     
   234675, 634275,     
   234567, 534267, // restart...    
   634725, 734625,     
   534762, 734562,     
   234765, 734265,     
   634572, 534672,     
   234675, 634275,
   234567, 534267, // restart...        
   634725, 734625,     
   534762, 734562,     
   234765, 734265,     
   634572, 534672,     
   234675, 634275,
   234567, 534267, // restart...        
   634725, 734625,     
   534762, 734562,     
   234765, 734265,     
   634572, 534672,     
   234675, 634275,
   234567, 534267, // restart...        
   634725, 734625,     
   534762, 734562,     
   234765, 734265,     
   634572, 534672,     
   234675, 634275
  };

const int permutations_TYPE0_5EXTRA_B[60] =  
  {234567, 534267,     
   634725, 734625,     
   534762, 734562,     
   234765, 734265,     
   634572, 534672,     
   234675, 634275,     
   234567, 534267, // restart...    
   634725, 734625,     
   534762, 734562,     
   234765, 734265,     
   634572, 534672,     
   234675, 634275,
   234567, 534267, // restart...        
   634725, 734625,     
   534762, 734562,     
   234765, 734265,     
   634572, 534672,     
   234675, 634275,
   234567, 534267, // restart...        
   634725, 734625,     
   534762, 734562,     
   234765, 734265,     
   634572, 534672,     
   234675, 634275,
   234567, 534267, // restart...        
   634725, 734625,     
   534762, 734562,     
   234765, 734265,     
   634572, 534672,     
   234675, 634275
  };

  

//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////


// permutations for SL(4,1) events with five jets matched to five quarks,
// and one q from W->qq' lost

const int permutations_TYPE2_S[12] =  
  {234567, 534267,     
   634725, 734625,     
   534762, 734562,     
   234765, 734265,     
   634572, 534672,     
   234675, 634275      
  };
const int permutations_TYPE2_B[12] =  
  {234567, 534267,     
   634725, 734625,     
   534762, 734562,     
   234765, 734265,     
   634572, 534672,     
   234675, 634275      
  };


//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////


// permutations for SL(4,2) events with five jets matched to five quarks,
// and one q from W->qq' lost

const int permutations_TYPE1_S[24] =  
  {234567, 534267,     
   634725, 734625,     
   534762, 734562,     
   234765, 734265,     
   634572, 534672,     
   234675, 634275,     
   243567, 543267,     
   643725, 743625,     
   543762, 743562,     
   243765, 743265,     
   643572, 543672,     
   243675, 643275      
  };

const int permutations_TYPE1_B[24] =  
  {234567, 534267,     
   634725, 734625,     
   534762, 734562,     
   234765, 734265,     
   634572, 534672,     
   234675, 634275,     
   243567, 543267,     
   643725, 743625,     
   543762, 743562,     
   243765, 743265,     
   643572, 543672,     
   243675, 643275      
  };


//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////


// permutations for DL(4) events with all four jets matched to four quarks

const int permutations_TYPE6_S[12] =  
  {234567, 534267,     
   634725, 734625,     
   534762, 734562,     
   234765, 734265,     
   634572, 534672,     
   234675, 634275      
  };

const int permutations_TYPE6_B[12] =  
  {234567, 534267,     
   634725, 734625,     
   534762, 734562,     
   234765, 734265,     
   634572, 534672,     
   234675, 634275      
  };


//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////


// permutations for inequivalent flavor 4b 2q assigments to 6 jets

const int permutations_6J_S[15] =      
  { 267345,
    257346,
    256347, 
    247356,
    246357, 
    245367,
    237456,
    236457,
    235467,
    234567,
    327456,
    326457,
    325467,
    324567,
    423567
  };

// permutations for inequivalent flavor 4q 2b assigments to 6 jets

const int permutations_6J_B[15] =      
  { 623745,
    523746,
    523647,
    423756,
    423657,
    423567,
    324756,
    324657,
    324567,
    325467,
    234756,
    234657,
    234567,
    235467,
    245367
  };


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

const int permutations_5J_S[5] =      
  { 274356,
    264357,
    254367,
    234567,
    324567
  };

// permutations for inequivalent flavor 2b 3q assigment to 5 jets

const int permutations_5J_B[10] =      
  { 624735,
    524736,
    524637,
    324756,
    324657,
    324567,
    234756,
    234657,
    234567,
    254367
  };


//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////


// permutations for inequivalent flavor 4b assigment to 4 jets

const int permutations_4J_S[1] =      
  { 234567 };

// permutations for inequivalent flavor 2b 2q assigment to 4 jets

const int permutations_4J_B[6] =      
  { 234567,
    234657,
    234756,
    534627,
    534726,
    634725
  };

//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////

namespace perm_maps {

  using namespace std;
//map1 -> i => xxxxxx
//map2 -> xxxxxx => i
//where xxxxxx is a 6-digit int consisting of 1-s and 0-s signifiying the perm_to_gen matching
	const map<int, int> map1 = {
		{0, 0},
		{1, 1},
		{2, 10},
		{3, 11},
		{4, 100},
		{5, 101},
		{6, 110},
		{7, 111},
		{8, 1000},
		{9, 1001},
		{10, 1010},
		{11, 1011},
		{12, 1100},
		{13, 1101},
		{14, 1110},
		{15, 1111},
		{16, 10000},
		{17, 10001},
		{18, 10010},
		{19, 10011},
		{20, 10100},
		{21, 10101},
		{22, 10110},
		{23, 10111},
		{24, 11000},
		{25, 11001},
		{26, 11010},
		{27, 11011},
		{28, 11100},
		{29, 11101},
		{30, 11110},
		{31, 11111},
		{32, 100000},
		{33, 100001},
		{34, 100010},
		{35, 100011},
		{36, 100100},
		{37, 100101},
		{38, 100110},
		{39, 100111},
		{40, 101000},
		{41, 101001},
		{42, 101010},
		{43, 101011},
		{44, 101100},
		{45, 101101},
		{46, 101110},
		{47, 101111},
		{48, 110000},
		{49, 110001},
		{50, 110010},
		{51, 110011},
		{52, 110100},
		{53, 110101},
		{54, 110110},
		{55, 110111},
		{56, 111000},
		{57, 111001},
		{58, 111010},
		{59, 111011},
		{60, 111100},
		{61, 111101},
		{62, 111110},
		{63, 111111},
	};
	
	const map<int, int> map2 = {
		{0, 0},
		{1, 1},
		{10, 2},
		{11, 3},
		{100, 4},
		{101, 5},
		{110, 6},
		{111, 7},
		{1000, 8},
		{1001, 9},
		{1010, 10},
		{1011, 11},
		{1100, 12},
		{1101, 13},
		{1110, 14},
		{1111, 15},
		{10000, 16},
		{10001, 17},
		{10010, 18},
		{10011, 19},
		{10100, 20},
		{10101, 21},
		{10110, 22},
		{10111, 23},
		{11000, 24},
		{11001, 25},
		{11010, 26},
		{11011, 27},
		{11100, 28},
		{11101, 29},
		{11110, 30},
		{11111, 31},
		{100000, 32},
		{100001, 33},
		{100010, 34},
		{100011, 35},
		{100100, 36},
		{100101, 37},
		{100110, 38},
		{100111, 39},
		{101000, 40},
		{101001, 41},
		{101010, 42},
		{101011, 43},
		{101100, 44},
		{101101, 45},
		{101110, 46},
		{101111, 47},
		{110000, 48},
		{110001, 49},
		{110010, 50},
		{110011, 51},
		{110100, 52},
		{110101, 53},
		{110110, 54},
		{110111, 55},
		{111000, 56},
		{111001, 57},
		{111010, 58},
		{111011, 59},
		{111100, 60},
		{111101, 61},
		{111110, 62},
		{111111, 63},
	};
	
  int get_n(int x, int n) {
    if (n <= 0) {
      throw exception();
    }
    return (int)((x % (int)std::pow(10, n)) / (int)std::pow(10, n-1));
  }

  vector<int> comb_as_vector(int x, int length) {
      vector<int> ret;
      for (int i=length; i > 0; i--) {
          ret.push_back(get_n(x, i));
      }
      return ret;
  }

	bool has_n(int x, int n) {
		return (bool)get_n(x, n);
	}
	
	const char* positions[] = {"bl", "w1", "w2", "bh", "b1", "b2"};
	
	bool higgs_b_missed(int x) {
		return !(has_n(x, 2) && has_n(x, 1));
	}
	
	bool top_b_missed(int x) {
		return !(has_n(x, 6) && has_n(x, 3));
	}

  bool w_q1_missed(int x) {
    return !(has_n(x, 4));
  }

  bool w_q2_missed(int x) {
    return !(has_n(x, 5));
  }

  bool w_qq_missed(int x) {
    return !(has_n(x, 4) && has_n(x, 5));
  }
	
	int count_matched(int x) {
		int n = 0;
		for (int i=1;i<=6;i++) {
			n += (int)has_n(x, i);
		}
		return n;
	}
	
}