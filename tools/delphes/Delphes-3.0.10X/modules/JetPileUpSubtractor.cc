
/** \class JetPileUpSubtractor
 *
 *  Subtract pile-up contribution from jets using the fastjet area method
 *
 *  $Date: 2012-11-18 15:57:08 +0100 (Sun, 18 Nov 2012) $
 *  $Revision: 814 $
 *
 *  \author M. Selvaggi - UCL, Louvain-la-Neuve
 *
 */

#include "modules/JetPileUpSubtractor.h"

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

JetPileUpSubtractor::JetPileUpSubtractor() :
  fItJetInputArray(0)
{

}

//------------------------------------------------------------------------------

JetPileUpSubtractor::~JetPileUpSubtractor()
{

}

//------------------------------------------------------------------------------

void JetPileUpSubtractor::Init()
{
  fJetPTMin = GetDouble("JetPTMin", 20.0);

  // import input array(s)

  fJetInputArray = ImportArray(GetString("JetInputArray", "FastJetFinder/jets"));
  fItJetInputArray = fJetInputArray->MakeIterator();

  fRhoInputArray = ImportArray(GetString("RhoInputArray", "Rho/rho"));

  // create output array(s)

  fOutputArray = ExportArray(GetString("OutputArray", "jets"));

}

//------------------------------------------------------------------------------

void JetPileUpSubtractor::Finish()
{
  if(fItJetInputArray) delete fItJetInputArray;
}

//------------------------------------------------------------------------------

void JetPileUpSubtractor::Process()
{
  Candidate *candidate;
  TLorentzVector momentum, area;
  Double_t rho = 0.0;

  if(fRhoInputArray && fRhoInputArray->GetEntriesFast() > 0)
  {
    candidate = static_cast<Candidate*>(fRhoInputArray->At(0));
    rho = candidate->Momentum.Pt();
  }

  // loop over all input candidates
  fItJetInputArray->Reset();
  while((candidate = static_cast<Candidate*>(fItJetInputArray->Next())))
  {
    momentum = candidate->Momentum;
    area = candidate->Area;

    // apply pile-up correction
    if(momentum.Pt() <= rho * area.Pt()) continue;

    momentum -= rho * area;
  
    if(momentum.Pt() <= fJetPTMin) continue;

    candidate = static_cast<Candidate*>(candidate->Clone());
    candidate->Momentum = momentum;

    fOutputArray->Add(candidate);
  }
}

//------------------------------------------------------------------------------
