#ifndef FastJetFinder_h
#define FastJetFinder_h

/** \class FastJetFinder
 *
 *  Finds jets using FastJet library.
 *
 *  $Date: 2013-03-06 18:06:55 +0100 (Wed, 06 Mar 2013) $
 *  $Revision: 1031 $
 *
 *
 *  \author P. Demin - UCL, Louvain-la-Neuve
 *
 */

#include "classes/DelphesModule.h"

#include <vector>

class TObjArray;
class TIterator;

namespace fastjet {
  class JetDefinition;
  class AreaDefinition;
  class Selector;
}

class FastJetFinder: public DelphesModule
{
public:

  FastJetFinder();
  ~FastJetFinder();

  void Init();
  void Process();
  void Finish();
  
private:

  void *fPlugin; //!
  fastjet::JetDefinition *fDefinition; //!
   
  Int_t fJetAlgorithm;
  Double_t fParameterR;
  Double_t fJetPTMin;
  Double_t fConeRadius;
  Double_t fSeedThreshold;
  Double_t fConeAreaFraction;
  Int_t fMaxIterations;
  Int_t fMaxPairSize;
  Int_t fIratch;
  Double_t fAdjacencyCut;
  Double_t fOverlapThreshold;
  
  // --- FastJet Area method --------
  
  fastjet::AreaDefinition *fAreaDefinition;
  Int_t fAreaAlgorithm;  
  Bool_t  fComputeRho; 
  Double_t fRhoEtaMax;
  
  // -- ghost based areas --
  Double_t fGhostEtaMax;
  Int_t fRepeat;
  Double_t fGhostArea;
  Double_t fGridScatter;
  Double_t fPtScatter;
  Double_t fMeanGhostPt; 
  
  // -- voronoi areas --
  Double_t fEffectiveRfact;
  
  
  TIterator *fItInputArray; //!

  const TObjArray *fInputArray; //!

  TObjArray *fOutputArray; //!
  TObjArray *fRhoOutputArray; //!

  ClassDef(FastJetFinder, 1)
};

#endif
