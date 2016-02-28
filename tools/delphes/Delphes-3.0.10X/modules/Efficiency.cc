
/** \class Efficiency
 *
 *  Selects candidates from the InputArray according to the efficiency formula.
 *
 *  $Date: 2013-02-12 14:57:44 +0100 (Tue, 12 Feb 2013) $
 *  $Revision: 905 $
 *
 *
 *  \author P. Demin - UCL, Louvain-la-Neuve
 *
 */

#include "modules/Efficiency.h"

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

Efficiency::Efficiency() :
  fFormula(0), fItInputArray(0)
{
  fFormula = new DelphesFormula;
}

//------------------------------------------------------------------------------

Efficiency::~Efficiency()
{
  if(fFormula) delete fFormula;
}

//------------------------------------------------------------------------------

void Efficiency::Init()
{
  // read efficiency formula

  fFormula->SetMaxima(1000000);
  fFormula->Compile(GetString("EfficiencyFormula", "1.0"));

  // import input array

  fInputArray = ImportArray(GetString("InputArray", "ParticlePropagator/stableParticles"));
  fItInputArray = fInputArray->MakeIterator();

  fOutputArray = ExportArray(GetString("OutputArray", "stableParticles"));
  
  fFlagValue = GetInt("FlagValue", 0);
  
  fAddFlag = GetBool("AddFlag", false);
  
  fKillUponFail = GetBool("KillUponFail", true);
}

//------------------------------------------------------------------------------

void Efficiency::Finish()
{
  if(fItInputArray) delete fItInputArray;
}

//------------------------------------------------------------------------------

void Efficiency::Process()
{ 
  Candidate *candidate;
  Double_t pt, eta, phi;

  fItInputArray->Reset();
  while((candidate = static_cast<Candidate*>(fItInputArray->Next())))
  {
    const TLorentzVector &candidatePosition = candidate->Position;
    const TLorentzVector &candidateMomentum = candidate->Momentum;
    eta = candidatePosition.Eta();
    phi = candidatePosition.Phi();
    pt = candidateMomentum.Pt();

    // apply an efficency formula
    if(gRandom->Uniform() < fFormula->Eval(pt, eta)) {      
      fOutputArray->Add(candidate);
      if(fAddFlag) {
        Int_t oldFlagValue = candidate->EfficiencyFlags;
        candidate->EfficiencyFlags = oldFlagValue + fFlagValue;
      }
      else
	    candidate->EfficiencyFlags = fFlagValue;
    }
    else if (!fKillUponFail) {
      fOutputArray->Add(candidate);
    }
  }
}

//------------------------------------------------------------------------------
