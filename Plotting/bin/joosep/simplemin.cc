//
//  simplemin.cpp
//  MEStudiesJP
//
//  Created by Joosep Pata on 27/11/14.
//  Copyright (c) 2014 Joosep Pata. All rights reserved.
//

#include <iostream>
#include "Minuit2/Minuit2Minimizer.h"
#include "Math/Functor.h"

using namespace std;

int ncalls = 0;
double RosenBrock(const double *xx )
{
	const double x = xx[0];
	const double y = xx[1];
	const double tmp1 = y-x*x;
	const double tmp2 = 1-x;
	ncalls += 1;
	return 100*tmp1*tmp1+tmp2*tmp2;
}

int NumericalMinimization()
{
	// Choose method upon creation between:
	// kMigrad, kSimplex, kCombined,
	// kScan, kFumili
	ROOT::Minuit2::Minuit2Minimizer min ( ROOT::Minuit2::kMigrad );
 
	min.SetMaxFunctionCalls(10000000);
	min.SetMaxIterations(1000000);
	min.SetTolerance(0.000001);
 
	ROOT::Math::Functor f(&RosenBrock,2);
	double step[2] = {0.0001,0.0001};
	double variable[2] = { -1.,1.2};
 
	min.SetFunction(f);
 
	// Set the free variables to be minimized!
	min.SetVariable(0,"x",variable[0], step[0]);
	min.SetVariable(1,"y",variable[1], step[1]);
 
	min.Minimize();
 
	const double *xs = min.X();
	cout << "Minimum: f(" << xs[0] << "," << xs[1] << "): "
	<< RosenBrock(xs) << endl;
	
	cout << "ncalls: " << ncalls << endl;
	
	return 0;
}

int main() {
	NumericalMinimization();
	return 0;
}