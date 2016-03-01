#ifndef Weighter_h
#define Weighter_h

/** \class Weighter
 *
 *  Apply a weight depending on PDG code.
 *
 *  $Date: 2013-05-27 00:36:00 +0200 (Mon, 27 May 2013) $
 *  $Revision: 1125 $
 *
 *
 *  \author P. Demin - UCL, Louvain-la-Neuve
 *
 */

#include "classes/DelphesModule.h"

#include <set>
#include <map>

class TObjArray;

class Weighter: public DelphesModule
{
public:

  Weighter();
  ~Weighter();

  void Init();
  void Process();
  void Finish();

private:
  struct TIndexStruct
  {
    Int_t codes[4];
    bool operator< (const TIndexStruct &value) const;
  };

  std::set<Int_t> fWeightSet, fCodeSet;
  std::map<TIndexStruct, Double_t> fWeightMap;

  TIterator *fItInputArray; //!

  const TObjArray *fInputArray; //!

  TObjArray *fOutputArray; //!

  ClassDef(Weighter, 1)
};

#endif
