
/** \class Isolation
 *
 *  Sums transverse momenta of isolation objects (tracks, calorimeter towers, etc)
 *  within a DeltaR cone around a candidate and calculates fraction of this sum
 *  to the candidate's transverse momentum. outputs candidates that have
 *  the transverse momenta fraction within (PTRatioMin, PTRatioMax].
 *
 *  $Date: 2013-08-19 15:40:54 +0200 (Mon, 19 Aug 2013) $
 *  $Revision: 1267 $
 *
 *
 *  \author P. Demin - UCL, Louvain-la-Neuve
 *
 */

#include "modules/Isolation.h"

#include "classes/DelphesClasses.h"
#include "classes/DelphesFactory.h"
#include "classes/DelphesFormula.h"

#include "ExRootAnalysis/ExRootResult.h"
#include "ExRootAnalysis/ExRootFilter.h"
#include "ExRootAnalysis/ExRootClassifier.h"

#include "TMath.h"
#include "TString.h"
#include "TFormula.h"
#include "TRandom3.h"
#include "TObjArray.h"
#include "TDatabasePDG.h"
#include "TLorentzVector.h"

#include <algorithm>
#include <stdexcept>
#include <iostream>
#include <sstream>

using namespace std;

//------------------------------------------------------------------------------

class IsolationClassifier : public ExRootClassifier
{
public:

  IsolationClassifier() {}

  Int_t GetCategory(TObject *object);

  Double_t fPTMin;
};

//------------------------------------------------------------------------------

Int_t IsolationClassifier::GetCategory(TObject *object)
{
  Candidate *track = static_cast<Candidate*>(object);
  const TLorentzVector &momentum = track->Momentum;

  if(momentum.Pt() < fPTMin) return -1;

  return 0;
}

//------------------------------------------------------------------------------

Isolation::Isolation() :
  fClassifier(0), fFilter(0),
  fItIsolationInputArray(0), fItCandidateInputArray(0)
{
  fClassifier = new IsolationClassifier;
}

//------------------------------------------------------------------------------

Isolation::~Isolation()
{
}

//------------------------------------------------------------------------------

void Isolation::Init()
{
  const char *rhoInputArrayName;

  fDeltaRMax = GetDouble("DeltaRMax", 0.5);

  fPTRatioMax = GetDouble("PTRatioMax", 0.1);

  fPTSumMax = GetDouble("PTSumMax", 5.0);

  fFlagValue = GetInt("FlagValue", 1);
  
  fAddFlag = GetBool("AddFlag", false);
  
  fKillUponFail = GetBool("KillUponFail", true);
  
  fUsePTSum = GetBool("UsePTSum", false);

  fClassifier->fPTMin = GetDouble("PTMin", 0.5);

  // import input array(s)

  fIsolationInputArray = ImportArray(GetString("IsolationInputArray", "Delphes/partons"));
  fItIsolationInputArray = fIsolationInputArray->MakeIterator();

  fFilter = new ExRootFilter(fIsolationInputArray);

  fCandidateInputArray = ImportArray(GetString("CandidateInputArray", "Calorimeter/electrons"));
  fItCandidateInputArray = fCandidateInputArray->MakeIterator();

  fOutputArray = ExportArray(GetString("OutputArray", "stableParticles"));
  
  rhoInputArrayName = GetString("RhoInputArray", "");
  if(rhoInputArrayName[0] != '\0')
  {
    fRhoInputArray = ImportArray(rhoInputArrayName);
  }
  else
  {
    fRhoInputArray = 0;
  }

}

//------------------------------------------------------------------------------

void Isolation::Finish()
{
  if(fFilter) delete fFilter;
  if(fItCandidateInputArray) delete fItCandidateInputArray;
  if(fItIsolationInputArray) delete fItIsolationInputArray;
}

//------------------------------------------------------------------------------

void Isolation::Process()
{
  Candidate *candidate, *isolation;
  TObjArray *isolationArray;
  Double_t sum, ratio;
  Int_t counter;
  Double_t rho = 0.0;

  if(fRhoInputArray && fRhoInputArray->GetEntriesFast() > 0)
  {
    candidate = static_cast<Candidate*>(fRhoInputArray->At(0));
    rho = candidate->Momentum.Pt();
  }

  // select isolation objects
  fFilter->Reset();
  isolationArray = fFilter->GetSubArray(fClassifier, 0);

  if(isolationArray == 0) return;

  TIter itIsolationArray(isolationArray);

  // loop over all input jets
  fItCandidateInputArray->Reset();
  while((candidate = static_cast<Candidate*>(fItCandidateInputArray->Next())))
  {
    const TLorentzVector &candidateMomentum = candidate->Momentum;

    // loop over all input tracks
    sum = 0.0;
    counter = 0;
    itIsolationArray.Reset();
    while((isolation = static_cast<Candidate*>(itIsolationArray.Next())))
    {
      const TLorentzVector &isolationMomentum = isolation->Momentum;

      if(candidateMomentum.DeltaR(isolationMomentum) <= fDeltaRMax &&
         !candidate->Overlaps(isolation))
      {
        sum += isolationMomentum.Pt();
        ++counter;
      }
    }

    // correct sum for pile-up contamination
    sum = sum - rho*fDeltaRMax*fDeltaRMax*TMath::Pi();  
    ratio = sum/candidateMomentum.Pt();    
    
    if((fUsePTSum)&&(sum < fPTSumMax)) {
      fOutputArray->Add(candidate);
      if(fAddFlag) {
        Int_t oldFlagValue = candidate->IsolationFlags;
        candidate->IsolationFlags = oldFlagValue + fFlagValue;
      }
      else
        candidate->IsolationFlags = fFlagValue;
    }
    else if((!fUsePTSum) && (ratio < fPTRatioMax)) {
      fOutputArray->Add(candidate);
      if(fAddFlag) {
        Int_t oldFlagValue = candidate->IsolationFlags;
        candidate->IsolationFlags = oldFlagValue + fFlagValue;
      }
      else
        candidate->IsolationFlags = fFlagValue;
    }
    else if (!fKillUponFail)
      fOutputArray->Add(candidate);

  }
}

//------------------------------------------------------------------------------
