#ifndef Isolation_h
#define Isolation_h

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

#include "classes/DelphesModule.h"

class TObjArray;

class ExRootFilter;
class IsolationClassifier;

class Isolation: public DelphesModule
{
public:

  Isolation();
  ~Isolation();

  void Init();
  void Process();
  void Finish();

private:

  Double_t fDeltaRMax;

  Double_t fPTRatioMax;

  Double_t fPTSumMax;

  Bool_t fUsePTSum;

  // NEW: flag if limit is evaluated as absolute (1) or relative (0) maximum momentum
  Int_t fAbsoluteLimit;
  
  Int_t fFlagValue; // Candidate's flag is set to this number if efficiency cut is passed

  Bool_t fAddFlag; // If true, FlagNumber is added to the candidate's current flag value.
                  // If false, it will replace any old value.

  Bool_t fKillUponFail; // If true, only flagged candidates will be written to outputs
  
  IsolationClassifier *fClassifier; //!

  ExRootFilter *fFilter;

  TIterator *fItIsolationInputArray; //!

  TIterator *fItCandidateInputArray; //!

  const TObjArray *fIsolationInputArray; //!

  const TObjArray *fCandidateInputArray; //!

  const TObjArray *fRhoInputArray; //!
  
  TObjArray *fOutputArray; //!

  ClassDef(Isolation, 1)
};

#endif
