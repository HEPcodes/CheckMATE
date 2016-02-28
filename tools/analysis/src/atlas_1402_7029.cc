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

  bookCutflowRegions("0;");
  bookSignalRegions("SR0taua01;SR0taua02;SR0taua03;SR0taua04;SR0taua05;SR0taua06;SR0taua07;SR0taua08;SR0taua09;SR0taua10;SR0taua11;SR0taua12;SR0taua13;SR0taua14;SR0taua15;SR0taua16;SR0taua17;SR0taua18;SR0taua19;SR0taua20;");
 
  for (int j=0; j<20; j++){
    for (int i=0; i<7; i++){
      bookCutflowRegions("CR0taua"+sr_index[j]+"_"+cf_index[i]+";");
    }
  }
  
  // You should initialize any declared variables here
  deltaphi = 0.;
  
  cutSingleTriggerElectronPT = 25.;
  cutSymTriggerElectronPT = 14.;
  cutAsymTriggerElectronPT1 = 25.;
  cutAsymTriggerElectronPT2 = 10.;
  cutMixedTriggerElectronPT1 = 14.;
  cutMixedTriggerElectronPT2 = 10.;
  
  cutSingleTriggerMuonPT = 25.;
  cutSymTriggerMuonPT = 14.0;
  cutAsymTriggerMuonPT1 = 18.0;
  cutAsymTriggerMuonPT2 = 10.;
  cutMixedTriggerMuonPT1 = 10.;
  cutMixedTriggerMuonPT2 = 18.;
}

void Atlas_1402_7029::analyze() {
  // Your eventwise analysis code goes here
  missingET->addMuons(muonsCombined);  
  electronsMedium = filterPhaseSpace(electronsMedium, 10., -2.47, 2.47, true);
  electronsTight = filterPhaseSpace(electronsTight, 10., -2.47, 2.47, true);
  muonsCombined = filterPhaseSpace(muonsCombined, 10., -2.4, 2.4);
  jets = filterPhaseSpace(jets, 20., -2.5, 2.5);
  countCutflowEvent("0");
//  countCutflowEvent("CR0taua01_1"); 
//  countSignalEvent("SR0taua01");
  
  for (int j=0; j<20; j++)
    countCutflowEvent("CR0taua"+sr_index[j]+"_"+cf_index[0]);
  
    //remove electrons within 0.1 of any reconstructed electron
  electronsMedium = overlapRemoval(electronsMedium, 0.1);
  electronsTight = overlapRemoval(electronsTight, 0.1);
  jets = overlapRemoval(jets, electronsMedium, 0.2);
  electronsMedium = overlapRemoval(electronsMedium, jets, 0.4);
  electronsTight = overlapRemoval(electronsTight, jets, 0.4);

  muonsCombined = overlapRemoval(muonsCombined, jets, 0.4);
  std::vector<Electron*> isoElecsM = overlapRemoval(electronsMedium, muonsCombined, 0.1);
  std::vector<Electron*> isoElecsT = overlapRemoval(electronsTight, muonsCombined, 0.1);
  std::vector<Muon*> isoMuons = overlapRemoval(muonsCombined, electronsMedium, 0.1);
  
  electronsMedium=isoElecsM;
  electronsTight=isoElecsT;
  muonsCombined=isoMuons;
  
  electronsMedium=filterIsolation(electronsMedium,0);
  electronsTight=filterIsolation(electronsTight,1);
  muonsCombined=filterIsolation(muonsCombined);
  
  trigger = false;
  double random_trigger = (double) rand() / (double) (RAND_MAX + 1.);
  //    Trigger Cuts
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
  else if( electronsTight.size() > 0 && muonsCombined.size() > 0 && electronsTight[0]->PT && cutMixedTriggerElectronPT1 && muons[0]->PT > cutMixedTriggerMuonPT1  )
    trigger = true;
  //mixed electron-muon trigger
  else if( electronsTight.size() > 0 && muonsCombined.size() > 0 && electronsTight[0]->PT && cutMixedTriggerElectronPT2 && muonsCombined[0]->PT > cutMixedTriggerMuonPT2)
    trigger = true;

  //object removal is applied
  //--------------------------
  //------Signal Regions------
  //--------------------------
  //std::cerr <<  "elec: " << electronsTight.size() << ", muons: " << muonsCombined.size() << std::endl;
  
    
  if( ( electronsTight.size() + muonsCombined.size() ) != 3 || !trigger )
    return;
 // if( ( electronsMedium.size() + muonsCombined.size() ) != 3 )
 //   return;

  for (int j=0; j<20; j++)
    countCutflowEvent("CR0taua"+sr_index[j]+"_"+cf_index[1]);  
  
   //SFOS invariant mass calculation  
  mmin = 100000.;
  SFOS = false;
  thirdleptonpt = 10000.;

  int ei,ej;
  ei=10;
  ej=10;
  
  if(electronsTight.size() > 1){
    for (int i = 0; i < electronsTight.size(); i++) {
      if( electronsTight[i]->PT < thirdleptonpt ) 
	thirdleptonpt = electronsTight[i]->PT;
      for (int j = i+1; j < electronsTight.size(); j++) {
	if(electronsTight[i]->Charge*electronsTight[j]->Charge > 0) 
	  continue;
	mtest = (electronsTight[i]->P4() + electronsTight[j]->P4()).M();
	SFOS = true;
	if (mtest<12.) 
	  return;
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
      if ( muonsCombined[i]->PT < thirdleptonpt ) 
	thirdleptonpt = muonsCombined[i]->PT;
      for(int j = i+1; j < muonsCombined.size(); j++) {
	if (muonsCombined[i]->Charge*muonsCombined[j]->Charge > 0)
	  continue;
	mtest = (muonsCombined[i]->P4() + muonsCombined[j]->P4()).M();
	if (mtest < 12.) 
	  return;
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

  if (!SFOS) 
    return;
  
  if ( 12. < mSFOS && mSFOS < 40.)
    for (int j=0; j<4; j++)
      countCutflowEvent("CR0taua"+sr_index[j]+"_"+cf_index[2]);
  if ( 40. < mSFOS && mSFOS < 60.)
    for (int j=4; j<8; j++)
      countCutflowEvent("CR0taua"+sr_index[j]+"_"+cf_index[2]);    
  if ( 60. < mSFOS && mSFOS < 81.2)
    for (int j=8; j<12; j++)
      countCutflowEvent("CR0taua"+sr_index[j]+"_"+cf_index[2]);       
  if ( 81.2 < mSFOS && mSFOS < 101.2)
    for (int j=12; j<16; j++)
      countCutflowEvent("CR0taua"+sr_index[j]+"_"+cf_index[2]);    
  if ( mSFOS > 101.2)
    for (int j=16; j<20; j++)
      countCutflowEvent("CR0taua"+sr_index[j]+"_"+cf_index[2]);           
  
  for (int i = 0; i < jets.size(); i++) {
    if( checkBTag(jets[i]))
      return;
  }

  for (int j=0; j<20; j++)
    countCutflowEvent("CR0taua"+sr_index[j]+"_"+cf_index[3]);      
  
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
      countCutflowEvent("CR0taua01_4");
      if ( mT < 80. )
      {
	countCutflowEvent("CR0taua01_5");
	countCutflowEvent("CR0taua01_6");
	countSignalEvent("SR0taua01");
      }
    }	
    if ( 90. <  missingET->P4().Et() ) 
    {
      countCutflowEvent("CR0taua02_4");
      if ( mT < 80. )
      {
	countCutflowEvent("CR0taua02_5");
	countCutflowEvent("CR0taua02_6");
	countSignalEvent("SR0taua02");
      }
    }	    
    if ( 50. < missingET->P4().Et() && missingET->P4().Et() < 75.) 
    {
      countCutflowEvent("CR0taua03_4");
      if ( mT > 80. )
      {
	countCutflowEvent("CR0taua03_5");
	countCutflowEvent("CR0taua03_6");
	countSignalEvent("SR0taua03");
      }
    }	
    if ( 75. <  missingET->P4().Et() ) 
    {
      countCutflowEvent("CR0taua04_4");
      if ( mT > 80. )
      {
	countCutflowEvent("CR0taua04_5");
	countCutflowEvent("CR0taua04_6");
	countSignalEvent("SR0taua04");
      }
    }
  }  
  
  if ( 40. < mSFOS && mSFOS < 60.)
  {
    if ( 50. < missingET->P4().Et() && missingET->P4().Et() < 75.) 
    {
      countCutflowEvent("CR0taua05_4");
      if ( mT < 80. )
      {
	countCutflowEvent("CR0taua05_5");
	if ( fabs( tot_mom.M() - 91.2) > 10. )
	{
	  countCutflowEvent("CR0taua05_6");
	  countSignalEvent("SR0taua05"); 
	}
      }
    }	
    if ( 75. <  missingET->P4().Et() ) 
    {
      countCutflowEvent("CR0taua06_4");
      if ( mT < 80. )
      {
	countCutflowEvent("CR0taua06_5");
	countCutflowEvent("CR0taua06_6");
	countSignalEvent("SR0taua06");
      }
    }	    
    if ( 50. < missingET->P4().Et() && missingET->P4().Et() < 135.) 
    {
      countCutflowEvent("CR0taua07_4");
      if ( mT > 80. )
      {
	countCutflowEvent("CR0taua07_5");
	countCutflowEvent("CR0taua07_6");
	countSignalEvent("SR0taua07");
      }
    }	
    if ( 135. <  missingET->P4().Et() ) 
    {
      countCutflowEvent("CR0taua08_4");
      if ( mT > 80. )
      {
	countCutflowEvent("CR0taua08_5");
	countCutflowEvent("CR0taua08_6");
	countSignalEvent("SR0taua08");
      }
    }	   
  }
  
  if ( 60. < mSFOS && mSFOS < 81.2 )
  {
    if ( 50. < missingET->P4().Et() && missingET->P4().Et() < 75.) 
    {
      countCutflowEvent("CR0taua09_4");
      if ( mT < 80. )
      {
	countCutflowEvent("CR0taua09_5");
	if ( fabs( tot_mom.M() - 91.2) > 10. )
	{
	  countCutflowEvent("CR0taua09_6");
	  countSignalEvent("SR0taua09"); 
	}
      }
    }	
    if ( 50. < missingET->P4().Et() && missingET->P4().Et() < 75. ) 
    {
      countCutflowEvent("CR0taua10_4");
      if ( mT > 80. )
      {
	countCutflowEvent("CR0taua10_5");
	countCutflowEvent("CR0taua10_6");
	countSignalEvent("SR0taua10");
      }
    }	    
    if ( 75. < missingET->P4().Et() ) 
    {
      countCutflowEvent("CR0taua11_4");
      if ( mT < 110. )
      {
	countCutflowEvent("CR0taua11_5");
	countCutflowEvent("CR0taua11_6");
	countSignalEvent("SR0taua11");
      }
    }	
    if ( 75. <  missingET->P4().Et() ) 
    {
      countCutflowEvent("CR0taua12_4");
      if ( mT > 110. )
      {
	countCutflowEvent("CR0taua12_5");
	countCutflowEvent("CR0taua12_6");
	countSignalEvent("SR0taua12");
      }
    }	     
  }

  if ( 81.2 < mSFOS && mSFOS < 101.2)
  {
    if ( 50. < missingET->P4().Et() && missingET->P4().Et() < 90.) 
    {
      countCutflowEvent("CR0taua13_4");
      if ( mT < 110. )
      {
	countCutflowEvent("CR0taua13_5");
	if ( fabs( tot_mom.M() - 91.2) > 10. )
	{
	  countCutflowEvent("CR0taua13_6");
	  countSignalEvent("SR0taua13"); 
	}
      }
    }	
    if ( 90. <  missingET->P4().Et() ) 
    {
      countCutflowEvent("CR0taua14_4");
      if ( mT < 110. )
      {
	countCutflowEvent("CR0taua14_5");
	countCutflowEvent("CR0taua14_6");
	countSignalEvent("SR0taua14");
      }
    }	    
    if ( 50. < missingET->P4().Et() && missingET->P4().Et() < 135.) 
    {
      countCutflowEvent("CR0taua15_4");
      if ( mT > 110. )
      {
	countCutflowEvent("CR0taua15_5");
	countCutflowEvent("CR0taua15_6");
	countSignalEvent("SR0taua15");
      }
    }	
    if ( 135. <  missingET->P4().Et() ) 
    {
      countCutflowEvent("CR0taua16_4");
      if ( mT > 110. )
      {
	countCutflowEvent("CR0taua16_5");
	countCutflowEvent("CR0taua16_6");
	countSignalEvent("SR0taua16");
      }
    }	        
  }
     
  if ( 101.2 < mSFOS  ) 
  {
    if ( 50. < missingET->P4().Et() && missingET->P4().Et() < 210.) 
    {
      countCutflowEvent("CR0taua17_4");
      if ( mT < 180. )
      {
	countCutflowEvent("CR0taua17_5");
	countCutflowEvent("CR0taua17_6");
	countSignalEvent("SR0taua17"); 
      }
    }	
    if ( 50. < missingET->P4().Et() && missingET->P4().Et() < 210. ) 
    {
      countCutflowEvent("CR0taua18_4");
      if ( mT > 180. )
      {
	countCutflowEvent("CR0taua18_5");
	countCutflowEvent("CR0taua18_6");
	countSignalEvent("SR0taua18");
      }
    }	    
    if ( 210. < missingET->P4().Et() ) 
    {
      countCutflowEvent("CR0taua19_4");
      if ( mT < 120. )
      {
	countCutflowEvent("CR0taua19_5");
	countCutflowEvent("CR0taua19_6");
	countSignalEvent("SR0taua19");
      }
    }	
    if ( 210. <  missingET->P4().Et() ) 
    {
      countCutflowEvent("CR0taua20_4");
      if ( mT > 120. )
      {
	countCutflowEvent("CR0taua20_5");
	countCutflowEvent("CR0taua20_6");
	countSignalEvent("SR0taua20");
      }
    }	
  }
  
  
  
}

void Atlas_1402_7029::finalize() {
  // Whatever should be done after the run goes here
}       
