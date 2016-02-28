#include "atlas_1308_2631.h"

void Atlas_1308_2631::initialize() {
  setAnalysisName("atlas_1308_2631");          
  setInformation(""
    "@# ATLAS \n"
    "@# ATLAS arXiv:1308.2631 \n"
    "@#0 leptons + 2 b-jets + Etmiss [Sbottom/stop]\n"
    "@# Energy: 8 TeV \n"
    "@# Luminosity: 20.1 fb^-1 \n"  
    "@# UNVALIDATED!!!!!!!!!!!!!!!!!!!!!!!!! \n\n"
    "");
  setLuminosity(20.1*units::INVFB);      
//  ignore("towers"); // These won't read tower or track information from the
  ignore("tracks"); //  Delphes output branches to save computing time.
  bookSignalRegions("SRA1;SRA2;SRA3;SRA4;SRA5;SRB;");
  bookCutflowRegions("0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16");

}

void Atlas_1308_2631::analyze() {
    ///UNVALIDATED
    missingET->addMuons(muonsCombined);
    jets = filterPhaseSpace(jets, 20., -4.9, 4.9);
    int nJets = jets.size();   
    photons = filterPhaseSpace(photons, 100., -2.0, 2.0);
    int nPhotons = photons.size();
    electronsMedium = filterPhaseSpace(electronsMedium, 7., -2.47, 2.47);
    int nElectronsMedium = electronsMedium.size();    
    muonsCombined = filterPhaseSpace(muonsCombined, 6., -2.4, 2.4);
    int nMuonsCombined = muonsCombined.size();  
    countCutflowEvent("0");
    
    // Veto events with photons > 100 GeV
    // B-tagging algorithm set at 60%, |eta| < 2.5
    // Electron candidates are 'medium', pT > 7 GeV, 
    // Electrons for control regions are 'tight', pT > 20 GeV, <10% charged pT in dR 0.2
    // Muon candidates pT > 6
    // Muons for control regions pT > 20, < 1.8 GeV in calo in dR 0.2
    
    bool flagSRA = false;
    bool flagSRB = false;
    
    //------------------------------
    //Veto events with hard photon since unlikely to pass jet quality condition
    if(nPhotons > 1)
        return;
    countCutflowEvent("1");

    //------------------------
    // Initial trigger
    // Normalised to cutflow efficiency
    // Trigger is 99% efficient for signal selection however.
    if(missingET->P4().Et() < 150.0)
	return;
    if(missingET->P4().Et() > 250.0)
	flagSRB = true;
    countCutflowEvent("2");
    
    //------------------------
    // Remove jets that overlap with electrons
    jets = overlapRemoval(jets, electronsMedium, 0.2);
    nJets = jets.size();
    //---------------------------
    // Remove any baseline muon that overlaps with a jet and veto event if muon left
    muonsCombined = overlapRemoval(muonsCombined, jets, 0.4);
    nMuonsCombined = muonsCombined.size();
    if(nMuonsCombined > 0)
	return;
    countCutflowEvent("3");
    //---------------------------
    // Remove any baseline electron that overlaps with a jet and veto event with any electron left
    electronsMedium = overlapRemoval(electronsMedium, jets, 0.4);
    nElectronsMedium = electronsMedium.size();
    if(nElectronsMedium > 0)
	return;
    countCutflowEvent("4");
    
    //------------------------------
    // Leading jet pT cut, 130 (A), 150 (B)
    
    std::vector<Jet*> jets_filt = filterPhaseSpace(jets, 20., -2.8, 2.8);
    nJets = jets_filt.size(); 
    if(nJets == 0)
        return;
    if(jets_filt[0]->PT < 130.0)
        return;
    if(jets_filt[0]->PT < 150.0)
        flagSRB = false;
    countCutflowEvent("5");
    
    //------------------------------
    // Veto event if no second jet
    if (nJets < 2)
        return;
    countCutflowEvent("6");
    
    //------------------------------
    // Second jet pT cut, 50 (A), 30 (B)
    if(jets_filt[1]->PT < 30.0)
        return;
    if(jets_filt[1]->PT > 50.0)
        flagSRA = true;
    if((flagSRA == false) && (flagSRB == false))
        return;
    countCutflowEvent("7");
    
    //------------------------------
    // Third jet pT cut, < 50 (A), > 30 (B)
    if( (nJets > 2) && (jets_filt[2]->PT > 30)){
        if (jets_filt[2]->PT > 50) flagSRA = false;
    }
    else flagSRB = false; 
    if((flagSRA == false) && (flagSRB == false))
        return;
    countCutflowEvent("8");
    
    //------------------------------
    // Large angle (2.5) between MET and jet(1) required for SRB
    if(fabs(missingET->P4().DeltaPhi(jets_filt[0]->P4())) < 2.5) flagSRB = false;    
    if((flagSRA == false) && (flagSRB == false))
        return;
    countCutflowEvent("9");
    
    //------------------------------
    // Exactly 2 b-jets required
    std::vector<Jet*> bJets, notBJets;
    for(int i=0; i < nJets; i++){
        if( (fabs(jets_filt[i]->Eta) < 2.5) && (checkBTag(jets_filt[i]) == true) ) bJets.push_back(jets_filt[i]);
	else notBJets.push_back(jets_filt[i]);
    }
    if (bJets.size() != 2)
        return;
    countCutflowEvent("10");
    
        //------------------------------
    // B-tagging, leading 2 jets for SRA, jets 2 and 3 for SRB
    if(flagSRA == true){
        if( (checkBTag(jets_filt[0]) == 0) || (checkBTag(jets_filt[1]) == 0) ) flagSRA = false;
    }
    if(flagSRB == true){
        if( (checkBTag(jets_filt[1]) == 0) || (checkBTag(jets_filt[2]) == 0) ) flagSRB = false;
    }  
    if((flagSRA == false) && (flagSRB == false))
        return;
    countCutflowEvent("11");

    //------------------------------
    // Require that the three highest pt jets do not lie collinear (0.4) with MET
    for(int i=0; i < nJets; i++){
        if((i<3) && (fabs(jets_filt[i]->P4().DeltaPhi(missingET->P4())) < 0.4) )
	    return;
    }
    countCutflowEvent("12");
    
    //------------------------------
    // Require that EtMiss/meff(k) > 0.25, k = 2 (A), 3 (B)
    double mEff = missingET->P4().Et() + jets_filt[0]->PT + jets_filt[1]->PT;
    if( (flagSRA == true) && ((missingET->P4().Et()/mEff) < 0.25) ) flagSRA = false;
    if(flagSRB == true){
        mEff += jets_filt[2]->PT;
        if((missingET->P4().Et()/mEff) < 0.25)  flagSRB = false;
    }
    if((flagSRA == false) && (flagSRB == false))
        return;
    countCutflowEvent("13");
    
    //------------------------------
    // SRB requires H_{T,3} (sum of jets_filt 4 -> n < 50)
    if(flagSRB == true){
	double HT3 = 0.;
        for(int i=3; i < nJets; i++){
            HT3 += jets_filt[i]->PT;
	}
	if(HT3 > 50.0) flagSRB = false;
    }
    if((flagSRA == false) && (flagSRB == false))
        return;
    countCutflowEvent("14");
    
    //------------------------------
    // SRA requires leading two jets m_bb > 200.0 GeV
    if(flagSRA == true){
        TLorentzVector vecBB = jets_filt[0]->P4() + jets_filt[1]->P4();
	if( vecBB.M() < 200.0) flagSRA = false;
    }
    if((flagSRA == false) && (flagSRB == false))
        return;
    countCutflowEvent("15");
    
    //--------------------------
    //------Signal Regions------
    //--------------------------
    // Signal region B is now given
    if(flagSRB == true) 
	countSignalEvent("SRB");
    
    //--------------------------
    // Signal regions A require that mCT is calculated
    if(flagSRA == true){
	
	TLorentzVector vds;
	//vds =(0.0,0.0,0.0,0.0);
/*	for(int i=0; i < towers.size(); i++){
	    if( (fabs(towers[i]->Eta)) < 4.9){
		TLorentzVector tower;
		//std::cerr << "E: tower: " << towers[i]->ET << std::endl;
		tower.SetPtEtaPhiM(towers[i]->ET,towers[i]->Eta,towers[i]->Phi,0.0);
		vds += tower;
	    }
	}
	vds = vds - jets[0]->P4() - jets[1]->P4();
	*/
	double mct_corr = mCTcorr(jets_filt[0]->P4(), jets_filt[1]->P4(), vds, missingET->P4(), 8000.0, 0.0 );
    //--------------------------
    // Signal region A1 requires mCT > 150. GeV
	if(mct_corr < 150.0)
	    return;
	countSignalEvent("SRA1");
    //--------------------------
    // Signal region A1 requires mCT > 200. GeV
	if(mct_corr < 200.0)
	    return;
	countSignalEvent("SRA2");
    //--------------------------
    // Signal region A1 requires mCT > 250. GeV
	if(mct_corr < 250.0)
	    return;
	countSignalEvent("SRA3");
    //--------------------------
    // Signal region A1 requires mCT > 300. GeV
	if(mct_corr < 300.0)
	    return;
	countSignalEvent("SRA4");
    //--------------------------
    // Signal region A1 requires mCT > 350. GeV
	if(mct_corr < 350.0)
	    return;
	countSignalEvent("SRA5");
    }
    
}

void Atlas_1308_2631::finalize() {
}       
