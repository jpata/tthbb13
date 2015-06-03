#include "TTH/MEAnalysis/interface/EventShapeVariables.h"

EventShapeVariables::EventShapeVariables(const std::vector<TLorentzVector>& inputVecs) :
inputVectors_(inputVecs) {

}

const double EventShapeVariables::isotropy(unsigned int numberOfSteps) const { 
  const double deltaPhi=2*TMath::Pi()/numberOfSteps;
  double phi = 0, eIn =-1., eOut=-1.;
  for(unsigned int i=0; i<numberOfSteps; ++i){
    phi+=deltaPhi;
    double sum=0;
    for(unsigned int j=0; j<inputVectors_.size(); ++j){
      // sum over inner product of unit vectors and momenta
      sum+=TMath::Abs(TMath::Cos(phi)*inputVectors_[j].X()+TMath::Sin(phi)*inputVectors_[j].Y());
    }
    if( eOut<0. || sum<eOut ) eOut=sum;
    if( eIn <0. || sum>eIn  ) eIn =sum;
  }
  return (eIn-eOut)/eIn;
}

const double EventShapeVariables::circularity(unsigned int numberOfSteps) const
{
  const double deltaPhi=2*TMath::Pi()/numberOfSteps;
  double circularity=-1, phi=0, area = 0;
  for(unsigned int i=0;i<inputVectors_.size();i++) {
    area+=TMath::Sqrt(inputVectors_[i].X()*inputVectors_[i].X()+inputVectors_[i].Y()*inputVectors_[i].Y());
  }
  for(unsigned int i=0; i<numberOfSteps; ++i){
    phi+=deltaPhi;
    double sum=0, tmp=0.;
    for(unsigned int j=0; j<inputVectors_.size(); ++j){
      sum+=TMath::Abs(TMath::Cos(phi)*inputVectors_[j].X()+TMath::Sin(phi)*inputVectors_[j].Y());
    }
    tmp=TMath::Pi()/2*sum/area;
    if( circularity<0 || tmp<circularity ){
      circularity=tmp;
    }
  }
  return circularity;
}

const TMatrixDSym EventShapeVariables::compMomentumTensor(double r) const
{
  TMatrixDSym momentumTensor(3);
  momentumTensor.Zero();

  if ( inputVectors_.size() < 2 ){
    return momentumTensor;
  }

  // fill momentumTensor from inputVectors
  double norm = 1.;
  for ( int i = 0; i < (int)inputVectors_.size(); ++i ){
    double p2 = inputVectors_[i].Dot(inputVectors_[i]);
    double pR = ( r == 2. ) ? p2 : TMath::Power(p2, 0.5*r);
    norm += pR;
    double pRminus2 = ( r == 2. ) ? 1. : TMath::Power(p2, 0.5*r - 1.);
    momentumTensor(0,0) += pRminus2*inputVectors_[i].X()*inputVectors_[i].X();
    momentumTensor(0,1) += pRminus2*inputVectors_[i].X()*inputVectors_[i].Y();
    momentumTensor(0,2) += pRminus2*inputVectors_[i].X()*inputVectors_[i].Z();
    momentumTensor(1,0) += pRminus2*inputVectors_[i].Y()*inputVectors_[i].X();
    momentumTensor(1,1) += pRminus2*inputVectors_[i].Y()*inputVectors_[i].Y();
    momentumTensor(1,2) += pRminus2*inputVectors_[i].Y()*inputVectors_[i].Z();
    momentumTensor(2,0) += pRminus2*inputVectors_[i].Z()*inputVectors_[i].X();
    momentumTensor(2,1) += pRminus2*inputVectors_[i].Z()*inputVectors_[i].Y();
    momentumTensor(2,2) += pRminus2*inputVectors_[i].Z()*inputVectors_[i].Z();
  }

  // return momentumTensor normalized to determinant 1
  return (1./norm)*momentumTensor;
}

const TVectorD EventShapeVariables::compEigenValues(double r) const
{
  TVectorD eigenValues(3);
  TMatrixDSym myTensor = compMomentumTensor(r);
  if( myTensor.IsSymmetric() ){
    if( myTensor.NonZeros() != 0 ) myTensor.EigenVectors(eigenValues);
  }

  // CV: TMatrixDSym::EigenVectors returns eigen-values and eigen-vectors
  //     ordered by descending eigen-values, so no need to do any sorting here...
  //std::cout << "eigenValues(0) = " << eigenValues(0) << ","
  //          << " eigenValues(1) = " << eigenValues(1) << ","
  //          << " eigenValues(2) = " << eigenValues(2) << std::endl;

  return eigenValues;
}

const double EventShapeVariables::sphericity(const TVectorD& eigenValues) const
{
  return 1.5*(eigenValues(1) + eigenValues(2));
}

const double EventShapeVariables::aplanarity(const TVectorD& eigenValues) const
{
  return 1.5*eigenValues(2);
}

const double EventShapeVariables::C(const TVectorD& eigenValues) const
{
  return 3.*(eigenValues(0)*eigenValues(1) + eigenValues(0)*eigenValues(2) + eigenValues(1)*eigenValues(2));
}

const double EventShapeVariables::D(const TVectorD& eigenValues) const
{
  return 27.*eigenValues(0)*eigenValues(1)*eigenValues(2);
}
