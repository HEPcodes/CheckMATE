#ifndef DelphesClasses_h
#define DelphesClasses_h

/**
 *
 *  Definition of classes to be stored in the root tree.
 *  Function CompareXYZ sorts objects by the variable XYZ that MUST be
 *  present in the data members of the root tree class of the branch.
 *
 *  $Date: 2008-06-04 13:57:24 $
 *  $Revision: 1.1 $
 *
 *
 *  \author P. Demin - UCL, Louvain-la-Neuve
 *
 */

// Dependencies (#includes)

#include "TRef.h"
#include "TObject.h"
#include "TRefArray.h"
#include "TLorentzVector.h"

#include "classes/SortableObject.h"

class DelphesFactory;

//---------------------------------------------------------------------------

class Event: public TObject
{
public:

  Long64_t Number; // event number

  Float_t ReadTime;
  Float_t ProcTime;  

  ClassDef(Event, 1)
};

//---------------------------------------------------------------------------

class LHCOEvent: public Event
{
public:

  Int_t Trigger; // trigger word

  ClassDef(LHCOEvent, 1)
};

//---------------------------------------------------------------------------

class LHEFEvent: public Event
{
public:

  Int_t ProcessID; // subprocess code for the event | hepup.IDPRUP

  Float_t Weight; // weight for the event | hepup.XWGTUP
  Float_t ScalePDF; // scale in GeV used in the calculation of the PDFs in the event | hepup.SCALUP
  Float_t AlphaQED; // value of the QED coupling used in the event | hepup.AQEDUP
  Float_t AlphaQCD; // value of the QCD coupling used in the event | hepup.AQCDUP

  ClassDef(LHEFEvent, 2)
};

//---------------------------------------------------------------------------

class HepMCEvent: public Event
{
public:

  Int_t ProcessID; // unique signal process id | signal_process_id()
  Int_t MPI; // number of multi parton interactions | mpi () 

  Float_t Weight; // weight for the event

  Float_t Scale; // energy scale, see hep-ph/0109068 | event_scale()
  Float_t AlphaQED; // QED coupling, see hep-ph/0109068 | alphaQED()
  Float_t AlphaQCD; // QCD coupling, see hep-ph/0109068 | alphaQCD()

  Int_t ID1; // flavour code of first parton | pdf_info()->id1()
  Int_t ID2; // flavour code of second parton | pdf_info()->id2()     

  Float_t X1; // fraction of beam momentum carried by first parton ("beam side") | pdf_info()->x1()
  Float_t X2; // fraction of beam momentum carried by second parton ("target side") | pdf_info()->x2()

  Float_t ScalePDF; // Q-scale used in evaluation of PDF's (in GeV) | pdf_info()->scalePDF()

  Float_t PDF1; // PDF (id1, x1, Q) | pdf_info()->pdf1()
  Float_t PDF2; // PDF (id2, x2, Q) | pdf_info()->pdf2()

  ClassDef(HepMCEvent, 2)
};

//---------------------------------------------------------------------------

class GenParticle: public SortableObject
{
public:
  Int_t PID; // particle HEP ID number | hepevt.idhep[number]

  Int_t Status; // particle status | hepevt.isthep[number]
  Int_t IsPU; // 0 or 1 for particles from pile-up interactions
  

  Int_t M1; // particle 1st mother | hepevt.jmohep[number][0] - 1
  Int_t M2; // particle 2nd mother | hepevt.jmohep[number][1] - 1

  Int_t D1; // particle 1st daughter | hepevt.jdahep[number][0] - 1
  Int_t D2; // particle last daughter | hepevt.jdahep[number][1] - 1

  Int_t Charge; // particle charge

  Float_t Mass; // particle mass

  Float_t E; // particle energy | hepevt.phep[number][3]
  Float_t Px; // particle momentum vector (x component) | hepevt.phep[number][0]
  Float_t Py; // particle momentum vector (y component) | hepevt.phep[number][1]
  Float_t Pz; // particle momentum vector (z component) | hepevt.phep[number][2]

  Float_t PT; // particle transverse momentum
  Float_t Eta; // particle pseudorapidity
  Float_t Phi; // particle azimuthal angle

  Float_t Rapidity; // particle rapidity

  Float_t T; // particle vertex position (t component) | hepevt.vhep[number][3]
  Float_t X; // particle vertex position (x component) | hepevt.vhep[number][0]
  Float_t Y; // particle vertex position (y component) | hepevt.vhep[number][1]
  Float_t Z; // particle vertex position (z component) | hepevt.vhep[number][2]

  static CompBase *fgCompare; //!
  const CompBase *GetCompare() const { return fgCompare; }
  
  TLorentzVector P4();

  ClassDef(GenParticle, 1)
};

//---------------------------------------------------------------------------

class MissingET: public TObject
{
public:
  Float_t MET; // mising transverse energy
  Float_t Phi; // mising energy azimuthal angle

  ClassDef(MissingET, 1)
};

//---------------------------------------------------------------------------

class ScalarHT: public TObject
{
public:
  Float_t HT; // scalar sum of transverse momenta

  ClassDef(ScalarHT, 1)
};

//---------------------------------------------------------------------------

class Rho: public TObject
{
public:
  Float_t Rho; // rho energy density

  ClassDef(Rho, 1)
};

//---------------------------------------------------------------------------

class Weight: public TObject
{
public:
  Float_t Weight; // weight for the event

  ClassDef(Weight, 1)
};

//---------------------------------------------------------------------------

class Photon: public SortableObject
{
public:

  Float_t PT; // photon transverse momentum
  Float_t Eta; // photon pseudorapidity
  Float_t Phi; // photon azimuthal angle

  Float_t E; // photon energy
  
  Float_t EhadOverEem; // ratio of the hadronic versus electromagnetic energy deposited in the calorimeter

  TRefArray Particles; // references to generated particles

  Int_t EfficiencyFlags; // Saves possible identification or reconstruction efficiency flags
  Int_t IsolationFlags; // Saves possible isolation flags
  Int_t MiscellaneousFlags; // Saves possible other flags

  static CompBase *fgCompare; //!
  const CompBase *GetCompare() const { return fgCompare; }

  TLorentzVector P4();

  ClassDef(Photon, 2)
};

//---------------------------------------------------------------------------

class Electron: public SortableObject
{
public:

  Float_t PT; // electron transverse momentum
  Float_t Eta; // electron pseudorapidity
  Float_t Phi; // electron azimuthal angle

  Int_t Charge; // electron charge

  Float_t EhadOverEem; // ratio of the hadronic versus electromagnetic energy deposited in the calorimeter

  TRef Particle; // reference to generated particle

  Int_t EfficiencyFlags; // Saves possible identification or reconstruction efficiency flags
  Int_t IsolationFlags; // Saves possible isolation flags
  Int_t MiscellaneousFlags; // Saves possible other flags

  static CompBase *fgCompare; //!
  const CompBase *GetCompare() const { return fgCompare; }

  TLorentzVector P4();

  ClassDef(Electron, 2)
};

//---------------------------------------------------------------------------

class Muon: public SortableObject
{
public:

  Float_t PT; // muon transverse momentum
  Float_t Eta; // muon pseudorapidity
  Float_t Phi; // muon azimuthal angle

  Int_t Charge; // muon charge

  TRef Particle; // reference to generated particle

  Int_t EfficiencyFlags; // Saves possible identification or reconstruction efficiency flags
  Int_t IsolationFlags; // Saves possible isolation flags
  Int_t MiscellaneousFlags; // Saves possible other flags

  static CompBase *fgCompare; //!
  const CompBase *GetCompare() const { return fgCompare; }

  TLorentzVector P4();

  ClassDef(Muon, 2)
};

//---------------------------------------------------------------------------

class Jet: public SortableObject
{
public:

  Float_t PT; // jet transverse momentum
  Float_t Eta; // jet pseudorapidity
  Float_t Phi; // jet azimuthal angle

  Float_t Mass; // jet invariant mass

  Float_t DeltaEta;  // jet radius in pseudorapidity
  Float_t DeltaPhi;  // jet radius in azimuthal angle

  Int_t EfficiencyFlags; // Saves possible identification or reconstruction efficiency flags
  Int_t IsolationFlags; // Saves possible isolation flags
  Int_t MiscellaneousFlags; // Saves possible other flags
  
  Int_t BFlags; // Saves possible BJetFlags
  Float_t BFlagProb; // Saves the random number that is checked against different BFlag probabilities
  Int_t TauFlags; // Saves possible TauJetFlags
  Float_t TauFlagProb; // Saves the random number that is checked against different TauFlag probabilities

  Int_t Charge; // tau charge

  Float_t EhadOverEem; // ratio of the hadronic versus electromagnetic energy deposited in the calorimeter

  TRefArray Constituents; // references to constituents
  TRefArray Particles; // references to generated particles

  static CompBase *fgCompare; //!
  const CompBase *GetCompare() const { return fgCompare; }

  TLorentzVector P4();

  ClassDef(Jet, 2)
};

//---------------------------------------------------------------------------

class Track: public SortableObject 
{
public:  
  Int_t PID; // HEP ID number

  Int_t Charge; // track charge

  Float_t PT; // track transverse momentum

  Float_t Eta; // track pseudorapidity
  Float_t Phi; // track azimuthal angle

  Float_t EtaOuter; // track pseudorapidity at the tracker edge
  Float_t PhiOuter; // track azimuthal angle at the tracker edge

  Float_t X; // track vertex position (x component)
  Float_t Y; // track vertex position (y component)
  Float_t Z; // track vertex position (z component)

  Float_t XOuter; // track position (x component) at the tracker edge
  Float_t YOuter; // track position (y component) at the tracker edge
  Float_t ZOuter; // track position (z component) at the tracker edge

  TRef Particle; // reference to generated particle

  static CompBase *fgCompare; //!
  const CompBase *GetCompare() const { return fgCompare; }

  TLorentzVector P4();

  ClassDef(Track, 1)
};

//---------------------------------------------------------------------------

class Tower: public SortableObject 
{
public:
  Float_t ET; // calorimeter tower transverse energy
  Float_t Eta; // calorimeter tower pseudorapidity
  Float_t Phi; // calorimeter tower azimuthal angle

  Float_t E; // calorimeter tower energy

  Float_t Eem; // calorimeter tower electromagnetic energy
  Float_t Ehad; // calorimeter tower hadronic energy

  Float_t Edges[4]; // calorimeter tower edges

  TRefArray Particles; // references to generated particles

  static CompBase *fgCompare; //!
  const CompBase *GetCompare() const { return fgCompare; }

  TLorentzVector P4();

  ClassDef(Tower, 1)
};

//---------------------------------------------------------------------------

class Candidate: public SortableObject 
{
  friend class DelphesFactory;

public:
  Candidate();

  Int_t PID;

  Int_t Status;
  Int_t M1, M2, D1, D2;

  Int_t Charge;

  Float_t Mass;
  
  Int_t IsPU;
  Int_t IsConstituent;

  Int_t EfficiencyFlags; // Saves possible identification or reconstruction efficiency flags
  Int_t IsolationFlags; // Saves possible isolation flags
  Int_t MiscellaneousFlags; // Saves possible other flags
  
  Int_t BFlags; // Saves possible BJetFlags
  Float_t BFlagProb; // Saves the random number that is checked against different BFlag probabilities
  Int_t TauFlags; // Saves possible TauJetFlags
  Float_t TauFlagProb; // Saves the random number that is checked against different TauFlag probabilities        

  Float_t Eem;
  Float_t Ehad;

  Float_t Edges[4];
  Float_t DeltaEta;
  Float_t DeltaPhi;

  TLorentzVector Momentum, Position, Area;

  static CompBase *fgCompare; //!
  const CompBase *GetCompare() const { return fgCompare; }

  void AddCandidate(Candidate *object);
  TObjArray *GetCandidates();

  Bool_t Overlaps(const Candidate *object) const;

  virtual void Copy(TObject &object) const;
  virtual TObject *Clone(const char *newname = "") const;
  virtual void Clear(Option_t* option = ""); 

private:
  DelphesFactory *fFactory; //!
  TObjArray *fArray; //!
  
  void SetFactory(DelphesFactory *factory) { fFactory = factory; }

  ClassDef(Candidate, 1)
};

#endif // DelphesClasses_h


