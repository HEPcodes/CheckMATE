#ifndef BTagging_h
#define BTagging_h

/** \class BTagging
 *
 *  Determines origin of jet,
 *  applies b-tagging efficiency (miss identification rate) formulas
 *  and sets b-tagging flags 
 *
 *  $Date: 2013-04-26 12:39:14 +0200 (Fri, 26 Apr 2013) $
 *  $Revision: 1099 $
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
class BTaggingPartonClassifier;

class BTagging: public DelphesModule
{
public:

  BTagging();
  ~BTagging();

  void Init();
  void Process();
  void Finish();

private:

  Int_t fFlagValue; // Candidate's flag is set to this number if efficiency cut is passed
  Bool_t fAddFlag; // If true, FlagNumber is added to the candidate's current flag value.
                  // If false, it will replace any old value.
  
  Double_t fDeltaR;

  std::map< Int_t, DelphesFormula * > fEfficiencyMap; //!
  
  BTaggingPartonClassifier *fClassifier; //!
  
  ExRootFilter *fFilter;

  TIterator *fItPartonInputArray; //!
  
  TIterator *fItJetInputArray; //!

  const TObjArray *fPartonInputArray; //!
  
  const TObjArray *fJetInputArray; //!

  ClassDef(BTagging, 1)
};

#endif
