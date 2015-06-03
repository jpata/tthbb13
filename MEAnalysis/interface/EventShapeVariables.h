#include "TMatrixDSym.h"
#include "TVectorD.h"
#include "TLorentzVector.h"

#include <vector>

class EventShapeVariables {

 public:
  EventShapeVariables(const std::vector<TLorentzVector>&);

  const double isotropy(unsigned int numberOfSteps = 1000) const;
  const double circularity(unsigned int numberOfSteps = 1000) const;

  const double sphericity(const TVectorD& )  const;
  const double aplanarity(const TVectorD& )  const;
  const double C(const TVectorD& ) const;
  const double D(const TVectorD& ) const;
  
  const TMatrixDSym compMomentumTensor(double = 2.) const;
  const TVectorD compEigenValues(double = 2.) const;

  const std::vector<TLorentzVector> inputVectors_;
};
