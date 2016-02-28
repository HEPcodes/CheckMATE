#include "atlas_1407_0583.h"

void Atlas_1407_0583::initialize() {
  setAnalysisName("atlas_1407_0583");          
  setInformation(""
    "@#ATLAS\n"
     "@#arXiv:1407.0583\n"
     "@#1-lepton + (b-)jets + etmiss\n"
     "@#sqrt(s) = 8 TeV\n"
     "@#int(L) = 20.3 fb^-1\n"
  "");
  setLuminosity(20.3*units::INVFB);      
  ignore("towers"); // These won't read tower or track information from the
  ignore("tracks"); //  Delphes output branches to save computing time.
  bookSignalRegions("tN_med;tN_high;tN_boost;bCa_low;bCa_med;bCb_med1;bCb_high;bCc_diag;bCd_high1;bCd_high2;tNbC_mix;tN_diag_a;tN_diag_b;tN_diag_c;tN_diag_d;bCb_med2_a;bCb_med2_b;bCb_med2_c;bCb_med2_d;bCd_bulk_a;bCd_bulk_b;bCd_bulk_c;bCd_bulk_d;3body_a;3body_b;3body_c;3body_d;");
  // You should initialize any declared variables here
}

void Atlas_1407_0583::analyze() {
  missingET->addMuons(muonsCombined);
  electronsLoose = filterPhaseSpace(electronsLoose, 7., -2.47, 2.47);
  int nElectronsLoose = electronsLoose.size();            
  muonsCombined = filterPhaseSpace(muonsCombined, 6., -2.4, 2.4);
  int nMuonsCombined = muonsCombined.size();            
  jets = filterPhaseSpace(jets, 15., -2.5, 2.5);
  int nJets = jets.size();            
  countCutflowEvent("a");

  //-----------------------------------------------------
  // Begin with Trigger
  bool triggerFlag=false;
  
  // Electron trigger (pt > 24 GeV, Iso: dR=0.2, tracks < 10%)
  std::vector<Electron*> electronsTrigger = filterPhaseSpace(electronsLoose, 24., -2.47, 2.47);
  electronsTrigger = filterIsolation(electronsTrigger,0);
  if( (electronsTrigger.size() > 0) || ((electronsLoose.size() >0) && (electronsLoose[0]->PT > 60)) ){
    triggerFlag=true;
  }
  
  // Muon trigger (pt > 25 GeV, Iso: dR=0.2, tracks < 10%)
  std::vector<Muon*> muonsTrigger = filterPhaseSpace(muonsCombined, 24., -2.47, 2.47);
  muonsTrigger = filterIsolation(muonsTrigger,0);
  if(muonsTrigger.size() > 0){
    triggerFlag=true;
  }
  
  
  
  
}

void Atlas_1407_0583::finalize() {
  // Whatever should be done after the run goes here
}       
