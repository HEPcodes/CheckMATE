#ifndef Efficiency_h
#define Efficiency_h

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

#include "classes/DelphesModule.h"

class TIterator;
class TObjArray;
class DelphesFormula;

class Efficiency: public DelphesModule
{
public:

  Efficiency();
  ~Efficiency();

  void Init();
  void Process();
  void Finish();

private:

  DelphesFormula *fFormula; //!

  Int_t fFlagValue; // Candidate's flag is set to this number if efficiency cut is passed
  Bool_t fAddFlag; // If true, FlagNumber is added to the candidate's current flag value.
                  // If false, it will replace any old value.
  Bool_t fKillUponFail; // If true, only flagged candidates will be written to output

  TIterator *fItInputArray; //!

  const TObjArray *fInputArray; //!
  
  TObjArray *fOutputArray; //!

  ClassDef(Efficiency, 1)
};

#endif
