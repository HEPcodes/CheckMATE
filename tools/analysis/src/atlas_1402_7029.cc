#include "atlas_1402_7029.h"

std::string Atlas_1402_7029::cf_index[7] = {"0","1","2","3","4","5","6"};
std::string Atlas_1402_7029::sr_index[20] = {"01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20"};

void Atlas_1402_7029::initialize() {
  setAnalysisName("atlas_1402_7029");          
  setInformation(""
    "@#ATLAS\n"
     "@#arXiv:1402.7029\n"
     "@#3 leptons and etmiss\n"
     "@#sqrt(s) = 8 Tev\n"
     "@#int(L) = 20.3 fb^-1\n"
  "");
  setLuminosity(20.3*units::INVFB);      
  ignore("towers"); // These won't read tower or track information from the
  ignore("tracks"); //  Delphes output branches to save computing time.

  bookSignalRegions("SR0taua01;SR0taua02;SR0taua03;SR0taua04;SR0taua05;SR0taua06;SR0taua07;SR0taua08;SR0taua09;SR0taua10;SR0taua11;SR0taua12;SR0taua13;SR0taua14;SR0taua15;SR0taua16;SR0taua17;SR0taua18;SR0taua19;SR0taua20;SR0taub");
 
  
  // You should initialize any declared variables here
  deltaphi = 0.;
  
  cutSingleTriggerElectronPT = 25.;

  cutSymTriggerElectronPT = 14.;

  cutAsymTriggerElectronPT1 = 25.;
  cutAsymTriggerElectronPT2 = 10.;

  cutMixedTrigger1ElectronPT = 14.;
  cutMixedTrigger2ElectronPT = 10.;
  
  cutSingleTriggerMuonPT = 25.;

  cutSymTriggerMuonPT = 14.0;

  cutAsymTriggerMuonPT1 = 18.0;
  cutAsymTriggerMuonPT2 = 10.;

  cutMixedTrigger1MuonPT = 10.;
  cutMixedTrigger2MuonPT = 18.;
}

void Atlas_1402_7029::analyze() {
  // Object selection
  missingET->addMuons(muonsCombined);  
  
  electronsMedium = filterPhaseSpace(electronsMedium, 10., -2.47, 2.47, false);
  electronsTight = filterPhaseSpace(electronsTight, 10., -2.47, 2.47, false);
  muonsCombined = filterPhaseSpace(muonsCombined, 10., -2.4, 2.4);
  jets = filterPhaseSpace(jets, 20., -2.5, 2.5);
  
  countCutflowEvent("00CR_All");
  
  // Overlap Removal
  electronsMedium = overlapRemoval(electronsMedium, 0.1);
  electronsTight = overlapRemoval(electronsTight, 0.1);
  jets = overlapRemoval(jets, electronsMedium, 0.2);
  electronsMedium = overlapRemoval(electronsMedium, jets, 0.4);
  electronsTight = overlapRemoval(electronsTight, jets, 0.4);
  muonsCombined = overlapRemoval(muonsCombined, jets, 0.4);

  // Low resonance check
  std::vector<Electron*> noResonanceElecs;
  for (int t = 0; t < electronsTight.size(); t++) {
      bool valid = true;
      for (int m = 0; m < electronsMedium.size(); m++) {
	  if (electronsMedium[m]->Charge*electronsTight[t]->Charge > 0)
	      continue;  // This also prevents an electron to be tested against itself
	  if ( (electronsMedium[m]->P4() + electronsTight[t]->P4()).M() < 12)
	      valid = false;
      }
      if (valid)
	  noResonanceElecs.push_back(electronsTight[t]);
  }
  std::vector<Muon*> noResonanceMuons;
  for (int t = 0; t < muonsCombined.size(); t++) {
      bool valid = true;
      for (int m = 0; m < muonsCombined.size(); m++) {
	  if (muonsCombined[m]->Charge*muonsCombined[t]->Charge > 0)
	      continue;  // This also prevents a muon to be tested against itself
	  if ( (muonsCombined[m]->P4() + muonsCombined[t]->P4()).M() < 12)
	      valid = false;
      }
      if (valid)
	  noResonanceMuons.push_back(muonsCombined[t]);
  }
  electronsTight = noResonanceElecs;
  muonsCombined = noResonanceMuons;

  // Apply Isolaton
  electronsTight=filterIsolation(electronsTight);
  muonsCombined=filterIsolation(muonsCombined);
  
  //    Trigger Cuts
  trigger = false;
  // single electron trigger
  if( electronsTight.size() > 0 && electronsTight[0]->PT > cutSingleTriggerElectronPT )
    trigger = true;
  // single muon trigger
  else if( muonsCombined.size() > 0 && muonsCombined[0]->PT > cutSingleTriggerMuonPT  ) 
    trigger = true;
  //symmetric dielectron trigger
  else if( electronsTight.size() > 1 && electronsTight[0]->PT > cutSymTriggerElectronPT && electronsTight[1]->PT > cutSymTriggerElectronPT  )
    trigger = true;
  //asymmetric dielectron trigger
  else if( electronsTight.size() > 1 && electronsTight[0]->PT > cutAsymTriggerElectronPT1 && electronsTight[1]->PT > cutAsymTriggerElectronPT2 )
    trigger = true;
  //symmetric dimuon trigger
  else if( muonsCombined.size() > 1 && muonsCombined[0]->PT > cutSymTriggerMuonPT && muonsCombined[1]->PT > cutSymTriggerMuonPT )
    trigger = true;
  
  //asymmetric dimuon trigger
  else if( muonsCombined.size() > 1 && muonsCombined[0]->PT > cutAsymTriggerMuonPT1 && muonsCombined[1]->PT > cutAsymTriggerMuonPT2 )
    trigger=true;
  //mixed electron-muon trigger
  else if( electronsTight.size() > 0 && muonsCombined.size() > 0 && electronsTight[0]->PT > cutMixedTrigger1ElectronPT && muonsCombined[0]->PT > cutMixedTrigger1MuonPT  )
    trigger = true;
  //mixed electron-muon trigger
  else if( electronsTight.size() > 0 && muonsCombined.size() > 0 && electronsTight[0]->PT > cutMixedTrigger2ElectronPT && muonsCombined[0]->PT > cutMixedTrigger2MuonPT)
      trigger = true;

  if( !trigger )
      return;
  countCutflowEvent("00CR_1Trigger");

  //object removal is applied
  //--------------------------
  //------Signal Regions------
  //--------------------------

  // Nleptons
  std::vector<Jet*> tauJets;
  for(int j = 0; j < jets.size(); j++) {
      if( checkTauTag(jets[j], "medium")  and fabs(jets[j]->Charge) == 1) 
	  tauJets.push_back(jets[j]);      
  }
  if( ( electronsTight.size() + muonsCombined.size() + tauJets.size() ) != 3 )
        return;  

  // Test that objects are separated by 0.3
  // MISSING BUT PROBABLY UNIMPORTANT DUE TO ISOLATION
    
  countCutflowEvent("00CR_2ThreeLeptons");

  if(  electronsTight.size() + muonsCombined.size() == 0 )
      return;  

  countCutflowEvent("00CR_3EorMu");

  //SFOS invariant mass calculation  
  mmin = 100000.;
  SFOS = false;
  thirdleptonpt = 10000.;
  double thirdleptoneta = 3;

  int ei,ej;
  ei=10;
  ej=10;
  
  if(electronsTight.size() > 1){
    for (int i = 0; i < electronsTight.size(); i++) {
	if( electronsTight[i]->PT < thirdleptonpt ) {
	    thirdleptonpt = electronsTight[i]->PT;
	    thirdleptoneta = electronsTight[i]->Eta;
	}
      for (int j = i+1; j < electronsTight.size(); j++) {
	  if(electronsTight[i]->Charge*electronsTight[j]->Charge > 0) 
	      continue;
	  mtest = (electronsTight[i]->P4() + electronsTight[j]->P4()).M();
	  
	  SFOS = true;
	  if (fabs(mtest-91.2) < mmin) {
	      mSFOS = mtest;
	      mmin = fabs(mtest-91.2);
	      ei=i;
	      ej=j;
	  }
      }
    }
  }
  
  int mi,mj;
  mi = 10;
  mj = 10;

  if(muonsCombined.size() > 1){
    for (int i = 0; i < muonsCombined.size(); i++) {
	if ( muonsCombined[i]->PT < thirdleptonpt ) {
	thirdleptonpt = muonsCombined[i]->PT;
	thirdleptoneta = muonsCombined[i]->Eta;
	}
      for(int j = i+1; j < muonsCombined.size(); j++) {
	if (muonsCombined[i]->Charge*muonsCombined[j]->Charge > 0)
	  continue;
	mtest = (muonsCombined[i]->P4() + muonsCombined[j]->P4()).M();

	SFOS = true;
	if (fabs(mtest-91.2)<mmin) {
	  mSFOS = mtest;
	  mmin = fabs(mtest-91.2);
	  mi = i;
	  mj = j;
	}
      }
    }
  }

  // Check universal bVeto condition
  bool bVeto = false;
  for (int i = 0; i < jets.size(); i++) {
      if( checkBTag(jets[i]))
	  bVeto = true;
  }
  
  // Check SR with taus
  switch (tauJets.size()) {
  case 2: {  // ===============================================Two Tau SR
      countCutflowEvent("CR2__0TwoTaus");
      do { // Check taua
	  if(bVeto)
	      break; // NO RETURN as this region is not orthogonal to taub
	  countCutflowEvent("CR2a_1BVeto");
	  if (missingET->P4().Et() < 50.)
	      break;
	  countCutflowEvent("CR2a_2Etmiss");   
	  // get lorentzvector of third lepton for mt2
	  TLorentzVector leptonP4 = (electronsTight.size() == 0 ? muonsCombined[0]->P4() : electronsTight[0]->P4());
	  double mT2_1 = mT2(leptonP4, tauJets[0]->P4(), 0.);
	  double mT2_2 = mT2(leptonP4, tauJets[1]->P4(), 0.);
	  double mT2_3 = mT2(tauJets[0]->P4(), tauJets[1]->P4(), 0.);
	  // Probe the largest of the three
	  double max_mT2 = std::max(std::max(mT2_1, mT2_2), mT2_3); // > mT2_2 ? (mT2_1 > mT2_3 ? mT2_1 : mT2_3) : (mT2_2 > mT2_3 ? mT2_2 : mT2_3));

	  if (max_mT2 < 100.)
	      break;
	  countCutflowEvent("CR2a_3mT2"); 
	  break;
      }
      while (true); // End pseudloop

      do { // Check taub
	  if (tauJets[0]->Charge*tauJets[1]->Charge > 0)
	      break;
	  countCutflowEvent("CR2b_1OSTaus");
	  if (bVeto)
	      break;
	  countCutflowEvent("CR2b_2BVeto");
	  if (missingET->P4().Et() < 60.)
	      break;
	  countCutflowEvent("CR2b_3Etmiss");      
	  double mtautau = (tauJets[0]->P4()+tauJets[1]->P4()).M();
	  double sumpt = tauJets[0]->PT + tauJets[1]->PT;

	  if(  mtautau < 70. or 120. < mtautau)
	      break;
	  countCutflowEvent("CR2b_4mtautau");
	  if(sumpt < 110.)
	      break;
	  countCutflowEvent("CR2b_5TauPT");
	  break;
      }
      while (true); // End pseudoloop
      break;
  }
  case 1: { // ===============================================One Tau SR
      countCutflowEvent("CR1_0OneTau");
      std::vector<TLorentzVector> leptonVectors;
      std::vector<double> leptonCharges;	  	  
      double mee = 0;
      // Create a common "lepton" vector
      switch(electronsTight.size()-muonsCombined.size()) {
      case 2:
	  leptonVectors.push_back(electronsTight[0]->P4());
	  leptonCharges.push_back(electronsTight[0]->Charge);
	  leptonVectors.push_back(electronsTight[1]->P4());
	  leptonCharges.push_back(electronsTight[1]->Charge);
	  mee = (electronsTight[0]->P4()+electronsTight[1]->P4()).M();
	  break;
      case 0:
	  // Make sure that the lepton vector has proper pt ordering
	  if( electronsTight[0]->PT > muonsCombined[0]->PT) {
	      leptonVectors.push_back(electronsTight[0]->P4());
	      leptonCharges.push_back(electronsTight[0]->Charge);
	      
	      leptonVectors.push_back(muonsCombined[0]->P4());
	      leptonCharges.push_back(muonsCombined[0]->Charge);
	  }
	  else {
	      leptonVectors.push_back(muonsCombined[0]->P4());
	      leptonCharges.push_back(muonsCombined[0]->Charge);

	      leptonVectors.push_back(electronsTight[0]->P4());
	      leptonCharges.push_back(electronsTight[0]->Charge);
	  }
	  break;
      case -2:
	  leptonVectors.push_back(muonsCombined[0]->P4());
	  leptonCharges.push_back(muonsCombined[0]->Charge);
	  leptonVectors.push_back(muonsCombined[1]->P4());
	  leptonCharges.push_back(muonsCombined[1]->Charge);
	  break;
      }

      if (leptonVectors.size() != 2) {
	  std::cerr << "ERROR: SOMETHING WENT WRONG IN THE LEPTON COUNTING!" << std::endl;
	  exit(1);
      }

      // Check Sign combination
      if (leptonCharges[0]*leptonCharges[1] < 0)
	  return;
      countCutflowEvent("CR1_1SSLeptons");

      if (tauJets[0]->Charge*leptonCharges[0] > 0)
	  return;
      countCutflowEvent("CR1_2OSTau");

      if(81.2 <= mee and mee <= 101.2)
	  return;
      countCutflowEvent("CR1_3Zeeveto"); 

      // Veto bs
      if (bVeto)
	  return;
      countCutflowEvent("CR1_4BVeto");

      // ETmiss
      double ptlep = leptonVectors[0].Pt() + leptonVectors[1].Pt();

      double ldeltaphi1 = fabs(leptonVectors[0].DeltaPhi(tauJets[0]->P4()));
      double lmT1 = sqrt(2.*leptonVectors[0].Pt()*tauJets[0]->PT*(1.-cos(ldeltaphi1)));
      double ldeltaphi2 = fabs(leptonVectors[1].DeltaPhi(tauJets[0]->P4()));
      double lmT2 = sqrt(2.*leptonVectors[1].Pt()*tauJets[0]->PT*(1.-cos(ldeltaphi2)));
      double lmT = fabs(125.-lmT1) < fabs(125.-lmT2) ? lmT1 : lmT2;

      if (missingET->P4().Et() < 50.)
	  return;
      countCutflowEvent("CR1_5Etmiss");      

      if (ptlep < 70.)
	  return;
      countCutflowEvent("CR1_6SumLeptonPT");      

      if (leptonVectors[1].Pt() < 30.)
	  return;
      countCutflowEvent("CR1_7SecondLeptonPT");      


      if(lmT > 120.)
	  return;
      countCutflowEvent("CR1_8LeptonMT");     
      break;
  }
  case 0: { // ===============================================No Tau SR
      countCutflowEvent("CR01NoTau");

      // First, let's check the SFOS-veto signal regions, because these have a shorter code
      if (!SFOS) {
	  countCutflowEvent("CR0taub_0");
	  // We explicitly have to require that there are not three leptons of one kind
	  if ((muonsCombined.size() == 3) or (electronsTight.size() == 3))
	      return;
	  countCutflowEvent("CR0taub_1OF");
	  if (bVeto) // No bs, please
	      return;
	  countCutflowEvent("CR0taub_2BVeto");
	  if (missingET->P4().Et() < 50.)
	      return;
	  countCutflowEvent("CR0taub_3Etmiss");
	  double delta1 = 0, delta2 = 0;
	  if (muonsCombined.size() == 2) {
	      if (thirdleptonpt < 20.) // Forbid third lepton to have pt < 20
		  return;
	      countCutflowEvent("CR0taub_4pt3");
	      delta1 = fabs(electronsTight[0]->P4().DeltaPhi(muonsCombined[0]->P4())); 
	      delta2 = fabs(electronsTight[0]->P4().DeltaPhi(muonsCombined[1]->P4()));
	  }
	  else if ( electronsTight.size() == 2)  {
	      if (thirdleptonpt < 20.) // Forbid third lepton to have pt < 20
		  return;
	      countCutflowEvent("CR0taub_4pt3");
	      delta1 = fabs(muonsCombined[0]->P4().DeltaPhi(electronsTight[0]->P4())); 
	      delta2 = fabs(muonsCombined[0]->P4().DeltaPhi(electronsTight[1]->P4()));
	  }    
	  
	  if (std::min(delta1, delta2) > 1.0)
	      return;

	  countCutflowEvent("CR0taub_5dPhi");
	  countSignalEvent("SR0taub");
      }
      else {
	  for (int j = 0; j < 20; j++)
	      countCutflowEvent("CR0taua"+sr_index[j]+"_0SFOS");
  
	  if ( 12. < mSFOS && mSFOS < 40.) {
	      for (int j=0; j<4; j++) {
		  countCutflowEvent("CR0taua"+sr_index[j]+"_1msfos");
		  if (!bVeto)
		      countCutflowEvent("CR0taua"+sr_index[j]+"_2bveto");
	      }
	  }
	      
	  if ( 40. < mSFOS && mSFOS < 60.) {
	      for (int j=4; j<8; j++){
		  countCutflowEvent("CR0taua"+sr_index[j]+"_1msfos");
		  if (!bVeto)
		      countCutflowEvent("CR0taua"+sr_index[j]+"_2bveto");
	      }
	  }
	  if ( 60. < mSFOS && mSFOS < 81.2) {
	      for (int j=8; j<12; j++){
		  countCutflowEvent("CR0taua"+sr_index[j]+"_1msfos");
		  if (!bVeto)
		      countCutflowEvent("CR0taua"+sr_index[j]+"_2bveto");
	      }
	  }
	  if ( 81.2 < mSFOS && mSFOS < 101.2) {
	      for (int j=12; j<16; j++){
		  countCutflowEvent("CR0taua"+sr_index[j]+"_1msfos");
		  if (!bVeto)
		      countCutflowEvent("CR0taua"+sr_index[j]+"_2bveto");
	      }
	  }
	  if ( mSFOS > 101.2) {
	      for (int j=16; j<20; j++){
		  countCutflowEvent("CR0taua"+sr_index[j]+"_1msfos");
		  if (!bVeto)
		      countCutflowEvent("CR0taua"+sr_index[j]+"_2bveto");
	      }
	  }
  
  
	  if( bVeto)
	      return;
  
	  TLorentzVector tot_mom;
  
	  for (int i = 0; i < electronsTight.size(); i++) {    
	      tot_mom += electronsTight[i]->P4();
	      if ( i != ei && i != ej ){
		  deltaphi = fabs(electronsTight[i]->P4().DeltaPhi(missingET->P4()));
		  mT = sqrt(2.*electronsTight[i]->PT*missingET->P4().Et()*(1.-cos(deltaphi)));
	      }
	  }
  
	  for (int i = 0; i < muonsCombined.size(); i++) {
	      tot_mom += muonsCombined[i]->P4();
	      if (i != mi && i != mj ) {
		  deltaphi = fabs(muonsCombined[i]->P4().DeltaPhi(missingET->P4()));
		  mT = sqrt(2.*muonsCombined[i]->PT*missingET->P4().Et()*(1.-cos(deltaphi)));
	      }
	  }
  
    
	  //Signal Regions
	  if ( 12. < mSFOS && mSFOS < 40.) 
	      {
		  if ( 50. < missingET->P4().Et() && missingET->P4().Et() < 90.) 
		      {
			  countCutflowEvent("CR0taua01_4etmiss");
			  if ( mT < 80. )
			      {
				  countCutflowEvent("CR0taua01_5mT");
				  countCutflowEvent("CR0taua01_6Zveto");
				  countSignalEvent("SR0taua01");
			      }
		      }	
		  if ( 90. <  missingET->P4().Et() ) 
		      {
			  countCutflowEvent("CR0taua02_4etmiss");
			  if ( mT < 80. )
			      {
				  countCutflowEvent("CR0taua02_5mT");
				  countCutflowEvent("CR0taua02_6Zveto");
				  countSignalEvent("SR0taua02");
			      }
		      }	    
		  if ( 50. < missingET->P4().Et() && missingET->P4().Et() < 75.) 
		      {
			  countCutflowEvent("CR0taua03_4etmiss");
			  if ( mT > 80. )
			      {
				  countCutflowEvent("CR0taua03_5mT");
				  countCutflowEvent("CR0taua03_6Zveto");
				  countSignalEvent("SR0taua03");
			      }
		      }	
		  if ( 75. <  missingET->P4().Et() ) 
		      {
			  countCutflowEvent("CR0taua04_4etmiss");
			  if ( mT > 80. )
			      {
				  countCutflowEvent("CR0taua04_5mT");
				  countCutflowEvent("CR0taua04_6Zveto");
				  countSignalEvent("SR0taua04");
			      }
		      }
	      }  
  
	  if ( 40. < mSFOS && mSFOS < 60.)
	      {
		  if ( 50. < missingET->P4().Et() && missingET->P4().Et() < 75.) 
		      {
			  countCutflowEvent("CR0taua05_4etmiss");
			  if ( mT < 80. )
			      {
				  countCutflowEvent("CR0taua05_5mT");
				  if ( fabs( tot_mom.M() - 91.2) > 10. )
				      {
					  countCutflowEvent("CR0taua05_6Zveto");
					  countSignalEvent("SR0taua05"); 
				      }
			      }
		      }	
		  if ( 75. <  missingET->P4().Et() ) 
		      {
			  countCutflowEvent("CR0taua06_4etmiss");
			  if ( mT < 80. )
			      {
				  countCutflowEvent("CR0taua06_5mT");
				  countCutflowEvent("CR0taua06_6Zveto");
				  countSignalEvent("SR0taua06");
			      }
		      }	    
		  if ( 50. < missingET->P4().Et() && missingET->P4().Et() < 135.) 
		      {
			  countCutflowEvent("CR0taua07_4etmiss");
			  if ( mT > 80. )
			      {
				  countCutflowEvent("CR0taua07_5mT");
				  countCutflowEvent("CR0taua07_6Zveto");
				  countSignalEvent("SR0taua07");
			      }
		      }	
		  if ( 135. <  missingET->P4().Et() ) 
		      {
			  countCutflowEvent("CR0taua08_4etmiss");
			  if ( mT > 80. )
			      {
				  countCutflowEvent("CR0taua08_5mT");
				  countCutflowEvent("CR0taua08_6Zveto");
				  countSignalEvent("SR0taua08");
			      }
		      }	   
	      }
  
	  if ( 60. < mSFOS && mSFOS < 81.2 )
	      {
		  if ( 50. < missingET->P4().Et() && missingET->P4().Et() < 75.) 
		      {
			  countCutflowEvent("CR0taua09_4etmiss");
			  if ( mT < 80. )
			      {
				  countCutflowEvent("CR0taua09_5mT");
				  if ( fabs( tot_mom.M() - 91.2) > 10. )
				      {
					  countCutflowEvent("CR0taua09_6Zveto");
					  countSignalEvent("SR0taua09"); 
				      }
			      }
		      }	
		  if ( 50. < missingET->P4().Et() && missingET->P4().Et() < 75. ) 
		      {
			  countCutflowEvent("CR0taua10_4etmiss");
			  if ( mT > 80. )
			      {
				  countCutflowEvent("CR0taua10_5mT");
				  countCutflowEvent("CR0taua10_6Zveto");
				  countSignalEvent("SR0taua10");
			      }
		      }	    
		  if ( 75. < missingET->P4().Et() ) 
		      {
			  countCutflowEvent("CR0taua11_4etmiss");
			  if ( mT < 110. )
			      {
				  countCutflowEvent("CR0taua11_5mT");
				  countCutflowEvent("CR0taua11_6Zveto");
				  countSignalEvent("SR0taua11");
			      }
		      }	
		  if ( 75. <  missingET->P4().Et() ) 
		      {
			  countCutflowEvent("CR0taua12_4etmiss");
			  if ( mT > 110. )
			      {
				  countCutflowEvent("CR0taua12_5mT");
				  countCutflowEvent("CR0taua12_6Zveto");
				  countSignalEvent("SR0taua12");
			      }
		      }	     
	      }

	  if ( 81.2 < mSFOS && mSFOS < 101.2)
	      {
		  if ( 50. < missingET->P4().Et() && missingET->P4().Et() < 90.) 
		      {
			  countCutflowEvent("CR0taua13_4etmiss");
			  if ( mT < 110. )
			      {
				  countCutflowEvent("CR0taua13_5mT");
				  if ( fabs( tot_mom.M() - 91.2) > 10. )
				      {
					  countCutflowEvent("CR0taua13_6Zveto");
					  countSignalEvent("SR0taua13"); 
				      }
			      }
		      }	
		  if ( 90. <  missingET->P4().Et() ) 
		      {
			  countCutflowEvent("CR0taua14_4etmiss");
			  if ( mT < 110. )
			      {
				  countCutflowEvent("CR0taua14_5mT");
				  countCutflowEvent("CR0taua14_6Zveto");
				  countSignalEvent("SR0taua14");
			      }
		      }	    
		  if ( 50. < missingET->P4().Et() && missingET->P4().Et() < 135.) 
		      {
			  countCutflowEvent("CR0taua15_4etmiss");
			  if ( mT > 110. )
			      {
				  countCutflowEvent("CR0taua15_5mT");
				  countCutflowEvent("CR0taua15_6Zveto");
				  countSignalEvent("SR0taua15");
			      }
		      }	
		  if ( 135. <  missingET->P4().Et() ) 
		      {
			  countCutflowEvent("CR0taua16_4etmiss");
			  if ( mT > 110. )
			      {
				  countCutflowEvent("CR0taua16_5mT");
				  countCutflowEvent("CR0taua16_6Zveto");
				  countSignalEvent("SR0taua16");
			      }
		      }	        
	      }
     
	  if ( 101.2 < mSFOS  ) 
	      {
		  if ( 50. < missingET->P4().Et() && missingET->P4().Et() < 210.) 
		      {
			  countCutflowEvent("CR0taua17_4etmiss");
			  if ( mT < 180. )
			      {
				  countCutflowEvent("CR0taua17_5mT");
				  countCutflowEvent("CR0taua17_6Zveto");
				  countSignalEvent("SR0taua17"); 
			      }
		      }	
		  if ( 50. < missingET->P4().Et() && missingET->P4().Et() < 210. ) 
		      {
			  countCutflowEvent("CR0taua18_4etmiss");
			  if ( mT > 180. )
			      {
				  countCutflowEvent("CR0taua18_5mT");
				  countCutflowEvent("CR0taua18_6Zveto");
				  countSignalEvent("SR0taua18");
			      }
		      }	    
		  if ( 210. < missingET->P4().Et() ) 
		      {
			  countCutflowEvent("CR0taua19_4etmiss");
			  if ( mT < 120. )
			      {
				  countCutflowEvent("CR0taua19_5mT");
				  countCutflowEvent("CR0taua19_6Zveto");
				  countSignalEvent("SR0taua19");
			      }
		      }	
		  if ( 210. <  missingET->P4().Et() ) 
		      {
			  countCutflowEvent("CR0taua20_4etmiss");
			  if ( mT > 120. )
			      {
				  countCutflowEvent("CR0taua20_5mT");
				  countCutflowEvent("CR0taua20_6Zveto");
				  countSignalEvent("SR0taua20");
			      }
		      }	
	      }
      }  
      break;
  }
  }
  
}

void Atlas_1402_7029::finalize() {
    // Whatever should be done after the run goes here
}       
