#ifndef TreeWriter_h
#define TreeWriter_h

/** \class TreeWriter
 *
 *  Fills ROOT tree branches.
 *
 *  $Date: 2013-05-26 02:00:39 +0200 (Sun, 26 May 2013) $
 *  $Revision: 1123 $
 *
 *
 *  \author P. Demin - UCL, Louvain-la-Neuve
 *
 */

#include "classes/DelphesModule.h"

#include <map>

class TClass;
class TObjArray;
class TRefArray;

class Candidate;
class ExRootTreeBranch;

class TreeWriter: public DelphesModule
{
public:

  TreeWriter();
  ~TreeWriter();

  void Init();
  void Process();
  void Finish();

private:

  void FillParticles(Candidate *candidate, TRefArray *array);

  void ProcessParticles(ExRootTreeBranch *branch, TObjArray *array);
  void ProcessTracks(ExRootTreeBranch *branch, TObjArray *array);
  void ProcessTowers(ExRootTreeBranch *branch, TObjArray *array);
  void ProcessPhotons(ExRootTreeBranch *branch, TObjArray *array);
  void ProcessElectrons(ExRootTreeBranch *branch, TObjArray *array);
  void ProcessMuons(ExRootTreeBranch *branch, TObjArray *array);
  void ProcessTauJets(ExRootTreeBranch *branch, TObjArray *array);
  void ProcessJets(ExRootTreeBranch *branch, TObjArray *array);
  void ProcessMissingET(ExRootTreeBranch *branch, TObjArray *array);
  void ProcessScalarHT(ExRootTreeBranch *branch, TObjArray *array);
  void ProcessRho(ExRootTreeBranch *branch, TObjArray *array);
  void ProcessWeight(ExRootTreeBranch *branch, TObjArray *array);

#ifndef __CINT__
  typedef void (TreeWriter::*TProcessMethod)(ExRootTreeBranch *, TObjArray *); //!

  typedef std::map< ExRootTreeBranch *, std::pair< TProcessMethod, TObjArray * > > TBranchMap; //!

  TBranchMap fBranchMap; //!

  std::map< TClass *, TProcessMethod > fClassMap; //!
#endif

  ClassDef(TreeWriter, 1)
};

#endif
