#include "cms_sus_12_019.h"

void Cms_sus_12_019::initialize() {
  setAnalysisName("cms_sus_12_019");          
  setInformation(""
    "@#2-leptons, jets and missing energy\n"
     "@#Opposite flavour leptons\n"
  "");
  setLuminosity(19.4*units::INVFB);      
  ignore("towers"); // These won't read tower or track information from the
  ignore("tracks"); //  Delphes output branches to save computing time.
  bookSignalRegions("Cen_SF;For_SF;");
  // You should initialize any declared variables here
}

void Cms_sus_12_019::analyze() {
  // Your eventwise analysis code goes here
  
  missingET->addMuons(muonsCombined);

//  if((electronsMedium.size() + muonsCombined.size()) > 1)
  //    countCutflowEvent("aa");
  
  electronsLoose = filterPhaseSpace(electronsLoose, 10., -2.4, 2.4);  
  electronsLoose = filterIsolation(electronsLoose);
  muonsCombined = filterPhaseSpace(muonsCombined, 10., -2.4, 2.4);  
  muonsCombined = filterIsolation(muonsCombined);
  
  //  if((electronsLoose.size() + muonsCombined.size()) > 1)
   //   countCutflowEvent("ab");
  
  jets = filterPhaseSpace(jets, 40., -3.0, 3.0);
  jets = overlapRemoval(jets, electronsLoose, 0.4);
  electronsLoose = overlapRemoval(electronsLoose, jets, 0.4);
  int nJets = jets.size();            
  countCutflowEvent("a_initial");
  
  //if((electronsLoose.size() + muonsCombined.size()) > 1)
    //  countCutflowEvent("ac");
  
  //Require two leptons pT >20
  electronsLoose = filterPhaseSpace(electronsLoose, 20., -2.4, 2.4);
  muonsCombined = filterPhaseSpace(muonsCombined, 20., -2.4, 2.4);
  
  // Include trigger efficiencies
  bool triggerFlag = false;
  double triggerRatio = (double) rand() / (double) (RAND_MAX + 1.);
  if((electronsLoose.size() >1) && (triggerRatio < 0.97)) triggerFlag =true;
  else if((muonsCombined.size() >1) && (triggerRatio < 0.97)) triggerFlag =true;
  else if((electronsLoose.size() == 1) && (muonsCombined.size() == 1)){ 
    if((fabs(muonsCombined[0]->Eta) < 1.4) && (fabs(electronsLoose[0]->Eta) <1.4) && (triggerRatio < 0.94)) triggerFlag =true;
    else if (triggerRatio < 0.88) triggerFlag =true;
  }
  
  if(triggerFlag == false)
    return;
  countCutflowEvent("b_trigger");
  
  //Signal leptons should not lie in transition region
  std::vector<Electron*> electronsSignal;
  std::vector<Muon*> muonsSignal;
    
  for(int i = 0; i < electronsLoose.size(); i++){
    if( (fabs(electronsLoose[i]->Eta) < 1.4) || (fabs(electronsLoose[i]->Eta) > 1.6) ) electronsSignal.push_back(electronsLoose[i]);
  }
  for(int i = 0; i < muonsCombined.size(); i++){
    if( (fabs(muonsCombined[i]->Eta) < 1.4) || (fabs(muonsCombined[i]->Eta) > 1.6) ) muonsSignal.push_back(muonsCombined[i]);
  }
  
  //Require at least two leptons
  if((electronsLoose.size() + muonsCombined.size()) < 2)
    return;
  countCutflowEvent("c_2lep");
  
  //Require two jets pT >40
  //jets = filterPhaseSpace(jets, 40., -3.0, 3.0);
  if(jets.size() < 2)
    return;
  countCutflowEvent("d_2jets");
  
  //Require either 2 jets and met > 150 or 3 jets and met > 100
  bool jetMet = false;
  if( (jets.size() > 1) && ( missingET->P4().Et() > 150.)) jetMet = true;
  else if( (jets.size() > 2) && ( missingET->P4().Et() > 100.)) jetMet = true;
  if(jetMet == false)
    return;
  countCutflowEvent("e_jetsMet");
  
  //Find if both or only one lepton is in central region, Eta < 1.4
  //Currently not used
  int numCenLep =0;
  bool cenLep = false;
  for(int i = 0; i < electronsLoose.size(); i++){
    if(fabs(electronsLoose[i]->Eta) < 1.4) numCenLep += 1;
  }
  for(int i = 0; i < muonsCombined.size(); i++){
    if(fabs(muonsCombined[i]->Eta) < 1.4) numCenLep += 1;
  }
  
  //Now split by leptons 
  if(electronsLoose.size() > 1){
    //Assume we take hardest electrons if more than 2
    int lepCharge = electronsLoose[0]->Charge * electronsLoose[1]->Charge;
    double diLepMass = (electronsLoose[0]->P4() + electronsLoose[1]->P4()).M();
    std::cout << "lepCharge: " << lepCharge << ", diLepMass: " << diLepMass << std::endl;
    if((lepCharge <0) && (diLepMass > 20.) && (diLepMass < 70.)){
      if((fabs(electronsLoose[0]->Eta) < 1.4) && (fabs(electronsLoose[1]->Eta) < 1.4)){
	countCutflowEvent("f_el_Cen_OSSF");
	countSignalEvent("Cen_SF");
      }
      else{
	countCutflowEvent("f_el_For_OSSF");
	countSignalEvent("For_SF");
      }
    }
  }
      
  if(muonsCombined.size() > 1){
    //Assume we take hardest electrons if more than 2
    int lepCharge = muonsCombined[0]->Charge * muonsCombined[1]->Charge;
    double diLepMass = (muonsCombined[0]->P4() + muonsCombined[1]->P4()).M();
    std::cout << "lepCharge: " << lepCharge << ", diLepMass: " << diLepMass << std::endl;
    if((lepCharge <0) && (diLepMass > 20.) && (diLepMass < 70.)){
      if((fabs(muonsCombined[0]->Eta) < 1.4) && (fabs(muonsCombined[1]->Eta) < 1.4)){
	countCutflowEvent("f_mu_Cen_OSSF");
	countSignalEvent("Cen_SF");
      }
      else{
	countCutflowEvent("f_mu_For_OSSF");
	countSignalEvent("For_SF");
      }
    }
  }
  
    if((muonsCombined.size() > 0) && (electronsLoose.size() > 0)){ 
    //Assume we take hardest electrons if more than 2
    int lepCharge = muonsCombined[0]->Charge * electronsLoose[0]->Charge;
    double diLepMass = (muonsCombined[0]->P4() + electronsLoose[0]->P4()).M();
    std::cout << "lepCharge: " << lepCharge << ", diLepMass: " << diLepMass << std::endl;
    if((lepCharge <0) && (diLepMass > 20.) && (diLepMass < 70.)){
      if((fabs(muonsCombined[0]->Eta) < 1.4) && (fabs(electronsLoose[0]->Eta) < 1.4)){
	countCutflowEvent("f_emu_Cen_OSOF");
	//countSignalEvent("Cen_OF");
      }
      else{
	countCutflowEvent("f_emu_For_OSOF");
	//countSignalEvent("For_OF");
      }
    }
  }

  
}

void Cms_sus_12_019::finalize() {
  // Whatever should be done after the run goes here
}       
