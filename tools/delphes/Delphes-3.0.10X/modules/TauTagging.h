#ifndef TauTagging_h
#define TauTagging_h

/** \class TauTagging
 *
 *  Determines origin of jet,
 *  applies b-tagging efficiency (miss identification rate) formulas
 *  and sets b-tagging flags 
 *
 *  $Date: 2013-02-22 01:01:36 +0100 (Fri, 22 Feb 2013) $
 *  $Revision: 926 $
 *
 *
 *  \author P. Demin - UCL, Louvain-la-Neuve
 *
 */

#include "classes/DelphesModule.h"

#include <map>

class TObjArray;
class DelphesFormula;

class ExRootFilter;
class TauTaggingPartonClassifier;

class TauTagging: public DelphesModule
{
public:

  TauTagging();
  ~TauTagging();

  void Init();
  void Process();
  void Finish();

private:

  Double_t fDeltaR;
  Double_t fDeltaRTau;
  Double_t fDeltaRTrack;

  Int_t fFlagValue; // Candidate's flag is set to this number if efficiency cut is passed
  Bool_t fAddFlag; // If true, FlagNumber is added to the candidate's current flag value.
                  // If false, it will replace any old value.

  std::map< Int_t, DelphesFormula * > fEfficiencyMap; //!
  
  TauTaggingPartonClassifier *fClassifier; //!
  
  ExRootFilter *fFilter;

  TIterator *fItPartonInputArray; //!
  
  TIterator *fItTrackInputArray; //!
  
  TIterator *fItJetInputArray; //!

  const TObjArray *fParticleInputArray; //!

  const TObjArray *fTrackInputArray; //!

  const TObjArray *fPartonInputArray; //!
  
  const TObjArray *fJetInputArray; //!

  ClassDef(TauTagging, 1)
};

#endif
