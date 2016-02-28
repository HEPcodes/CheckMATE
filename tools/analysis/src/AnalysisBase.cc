#include "AnalysisBase.h"

AnalysisBase::AnalysisBase(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr, std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) {
    // Setting internal parameters
    outputFolder = outFol;
    outputPrefix = outPre;
    inputFile = inFile;
    xsect = xs;
    xsecterr = xserr;    
    luminosity = 0;
    ignoreElectrons = ignoreElectrons_LooseIsolation = ignoreElectrons_MediumEfficiency = ignoreElectrons_TightEfficiency = ignoreMuons = ignoreMuons_LooseIsolation = ignoreMuons_CombinedPlusEfficiency = ignoreMuons_CombinedEfficiency = ignorePhotons = ignorePhotons_LooseIsolation = ignoreTracks  = ignoreTowers = false;


    // Reading the Delphes Tree
    chain = new TChain("Delphes");
    chain->Add(inFile.c_str());
    treeReader = new ExRootTreeReader(chain);
    result = new ExRootResult();  
    branchEvent = treeReader->UseBranch(branches["Event"].c_str());
    branchTrack = treeReader->UseBranch(branches["Track"].c_str());
    branchTower = treeReader->UseBranch(branches["Tower"].c_str());
    branchJet = treeReader->UseBranch(branches["Jet"].c_str());
    branchJet2 = treeReader->UseBranch(branches["Jet2"].c_str());
    branchElectron = treeReader->UseBranch(branches["Electron"].c_str());
    branchPhoton = treeReader->UseBranch(branches["Photon"].c_str());
    branchMuon = treeReader->UseBranch(branches["Muon"].c_str());
    branchMissingET = treeReader->UseBranch(branches["MissingET"].c_str());
  
    // Saving which flagvalues correspond to this analysis (given by CheckMATE)
    electronIsolationFlags = flags["electron_isolation"];
    muonIsolationFlags = flags["muon_isolation"];
    photonIsolationFlags = flags["photon_isolation"];
    jetBTagFlags = flags["jet_btags"];
    jet2BTagFlags = flags["jet2_btags"];
   
    // Setting the random number generator
    if (!flags["randomseed"].empty())
       srand(flags["randomseed"][0]);
    else      
       srand(time(0));    
}

AnalysisBase::~AnalysisBase() {
    // Free all pointers
    delete chain;
    delete treeReader;  
    delete result;
  
    for (int i = 0; i < fStreams.size(); i++) {
	fStreams[i]->close();
	delete fStreams[i];
    }
}

void AnalysisBase::bookSignalRegions(std::string listOfRegions) {
  std::string currKey = "";
  // Sum letter by letter and define map-key as soon as ; is reached
  for(int i = 0; i < strlen(listOfRegions.c_str()); i++) {
    char c = listOfRegions[i];
    if (c == ';') {
      signalRegions[currKey] = signalRegions2[currKey] = 0.0;
      currKey = "";
    }
    else
      currKey += c;
  }
  // The last key might not be separated by ;
  if(currKey != "")
      signalRegions[currKey] = signalRegions2[currKey] = 0.0;
}

void AnalysisBase::bookControlRegions(std::string listOfRegions) {
  std::string currKey = "";
  // Sum letter by letter and define map-key as soon as ; is reached
  for(int i = 0; i < strlen(listOfRegions.c_str()); i++) {
    char c = listOfRegions[i];
    if (c == ';') {
      controlRegions[currKey] = controlRegions2[currKey] = 0.0;
      currKey = "";
    }
    else
      currKey += c;
  }
  // The last key might not be separated by ;
  if(currKey != "")
      controlRegions[currKey] = controlRegions2[currKey] = 0.0;
}
void AnalysisBase::bookCutflowRegions(std::string listOfRegions) {
  std::string currKey = "";
  // Sum letter by letter and define map-key as soon as ; is reached
  for(int i = 0; i < strlen(listOfRegions.c_str()); i++) {
    char c = listOfRegions[i];
    if (c == ';') {
      cutflowRegions[currKey] = cutflowRegions2[currKey] = 0.0;
      currKey = "";
    }
    else
      currKey += c;
  }
  // The last key might not be separated by ;
  if(currKey != "")
      cutflowRegions[currKey] = cutflowRegions2[currKey] = 0.0;
}
    
    
void AnalysisBase::loopOverEvents() {
    // These const vectors are needed for efficiency/isolation filters
    std::vector<int> looseIsolationFlags;
    looseIsolationFlags.push_back(0);
    std::vector<int> mediumEfficiencyFlags;
    mediumEfficiencyFlags.push_back(0);
    std::vector<int> tightEfficiencyFlags;
    tightEfficiencyFlags.push_back(1);
  
    initialize();
    sumOfWeights = 0;            
    nEvents = treeReader->GetEntries();
    double missingET_ET = 0, missingET_Phi = 0, missingET_Ex = 0, missingET_Ey = 0;
    for(Int_t entry = 0; entry < nEvents; ++entry) {
	treeReader->ReadEntry(entry);
	weight = ((LHEFEvent*)branchEvent->At(0))->Weight;
        // If the events do not have any weights / the wrong weight branch is used, Delphes will save NAN in the corresponding branch
	if (weight != weight) {
	    weight = ((HepMCEvent*)branchEvent->At(0))->Weight;
   	    if (weight != weight) 
	       weight=1.;
	}


	sumOfWeights += weight;
	sumOfWeights2 += weight*weight;
    
	if(!ignoreElectrons) {
	    electrons.clear();
	    if(branchElectron) {
		for(int i = 0; i < branchElectron->GetEntries(); i++)
		    electrons.push_back((Electron*)branchElectron->At(i));
	    }
	    // All electrons need to fulfill minimum isolation criteria 
	    // (Note that this flag is not accessible by the user from within the analyses!)
	    if(!ignoreElectrons_LooseIsolation) {
		electronsLoose = filterFlags(electrons, "isolation", looseIsolationFlags);    
		if(!ignoreElectrons_MediumEfficiency) {
		    electronsMedium = filterFlags(electronsLoose, "efficiency", mediumEfficiencyFlags);
		    if(!ignoreElectrons_TightEfficiency)
			electronsTight = filterFlags(electronsMedium, "efficiency", tightEfficiencyFlags);
		}
	    }
	}
    
	if(!ignoreMuons) {
	    muons.clear();
	    if(branchMuon) {
		for(int i = 0; i < branchMuon->GetEntries(); i++) 
		    muons.push_back((Muon*)branchMuon->At(i));
	    }
	    // All muons need to fulfill minimum isolation criteria
	    if(!ignoreMuons_LooseIsolation) {
		muons = filterFlags(muons, "isolation", looseIsolationFlags);
    
		if(!ignoreMuons_CombinedPlusEfficiency) {
		    muonsCombinedPlus = filterFlags(muons, "efficiency", mediumEfficiencyFlags);
		    if(!ignoreMuons_CombinedEfficiency) 
			muonsCombined = filterFlags(muonsCombinedPlus, "efficiency", tightEfficiencyFlags);
		}
	    }
	}

	jets.clear();
	for(int i = 0; i < branchJet->GetEntries(); i++) 
	    jets.push_back((Jet*)branchJet->At(i));
    
	jets2.clear();
	if(branchJet2) {
	    for(int i = 0; i < branchJet2->GetEntries(); i++) 
		jets2.push_back((Jet*)branchJet2->At(i));
	}
    
	if(!ignorePhotons) {
	    photons.clear();
	    if(branchPhoton) {
		for(int i = 0; i < branchPhoton->GetEntries(); i++) 
		    photons.push_back((Photon*)branchPhoton->At(i));
	    }
	    // All photons need to fulfill minimum isolation criteria
	    if(!ignorePhotons_LooseIsolation)
		photons = filterFlags(photons, "isolation", looseIsolationFlags);
	}

	if(!ignoreTracks) {
	    tracks.clear();
	    if(branchTrack) {
		for(int i = 0; i < branchTrack->GetEntries(); i++) 
		    tracks.push_back((Track*)branchTrack->At(i));
	    }
	}

	if(!ignoreTowers) {
	    towers.clear();
	    if(branchTower) {
		for(int i = 0; i < branchTower->GetEntries(); i++) 
		    towers.push_back((Tower*)branchTower->At(i));
	    }
	}
    
	missingET = new ETMiss((MissingET*)branchMissingET->At(0));
    
	analyze();
    }
    finalize();
    
    // Save results of signal-, control- and/or cutflow-regions in specific files
    if(!cutflowRegions.empty()) {        
      int cutflowOutput = bookFile(analysis+"_cutflow.dat");      
      *fStreams[cutflowOutput] << "Cut  Sum_W  Sum_W2  Acc  N_Norm\n";
      for(std::map<std::string, double>::iterator cutflow_iter=cutflowRegions.begin(); cutflow_iter!=cutflowRegions.end(); ++cutflow_iter)
        *fStreams[cutflowOutput] << cutflow_iter->first << "  " << cutflow_iter->second << "  " << cutflowRegions2[cutflow_iter->first] << "  " << cutflow_iter->second/sumOfWeights << "  " << normalize(cutflow_iter->second) << "\n";
    }
    if(!signalRegions.empty()) {        
      int signalOutput = bookFile(analysis+"_signal.dat");
      *fStreams[signalOutput] << "SR  Sum_W  Sum_W2  Acc  N_Norm\n";
      for(std::map<std::string, double>::iterator signal_iter=signalRegions.begin(); signal_iter!=signalRegions.end(); ++signal_iter)
        *fStreams[signalOutput] << signal_iter->first << "  " << signal_iter->second << "  " << signalRegions2[signal_iter->first] << "  " << signal_iter->second/sumOfWeights << "  " << normalize(signal_iter->second) << "\n";
    }
    if(!controlRegions.empty()) {        
      int controlOutput = bookFile(analysis+"_control.dat");
      *fStreams[controlOutput] << "CR  Sum_W  Sum_W2  Acc  N_Norm\n";
      for(std::map<std::string, double>::iterator control_iter=controlRegions.begin(); control_iter!=controlRegions.end(); ++control_iter)
        *fStreams[controlOutput] << control_iter->first << "  " << control_iter->second << "  " << controlRegions2[control_iter->first] << "  " << control_iter->second/sumOfWeights << "  " << normalize(control_iter->second) << "\n";
    }
}               


int AnalysisBase::bookFile(std::string name) {
    // Assemble absolute filename
    std::string filename = outputFolder+"/"+outputPrefix+"_"+name;
    // Open stream
    std::ofstream* file = new ofstream(filename.c_str());
    // Write standard information
    *file << information << "\n";
    *file << "@Inputfile:       " << inputFile << "\n";
    *file << "@XSect:           " << xsect << " fb\n";
    *file << "@ Error:          " << xsecterr << " fb\n";
    *file << "@MCEvents:        " << nEvents << "\n";
    *file << "@ SumOfWeights:   " << sumOfWeights << "\n";
    *file << "@ SumOfWeights2:  " << sumOfWeights2 << "\n";
    *file << "@ NormEvents:     " << normalize(sumOfWeights) << "\n\n";
    fStreams.push_back(file);
    fNames.push_back(filename);
    // The returned number denotes the corresponding index for the fStreams vector
    return fStreams.size()-1;
}


bool AnalysisBase::checkTauTag(Jet* candidate, std::string efficiency) {
    if ((efficiency == "loose") && (candidate->TauFlags >= 1))
        return true;
    else if ((efficiency == "medium") && (candidate->TauFlags >= 2))
        return true;
    else if ((efficiency == "tight") && (candidate->TauFlags == 3))
        return true;
    return false;
}


bool AnalysisBase::checkBTag(Jet* candidate, int relative_flag, std::string option) {
    // First, decode the member's isoflag into a vector of valid flags    
    int absolute_flag = 0;
    if(option == "secondJet") {
        if (relative_flag >= jet2BTagFlags.size()) {
            std::cerr << "Error: There is no second jet b tag " << relative_flag << std::endl;
            std::cerr << "Exiting... "<< std::endl;
            exit(1);
        }      
        absolute_flag = jet2BTagFlags[relative_flag];
    }
    else {
        if (relative_flag >= jetBTagFlags.size()) {
            std::cerr << "Error: There is no b tag " << relative_flag << std::endl;
            std::cerr << "Exiting... "<< std::endl;
            exit(1);
        }      
        absolute_flag = jetBTagFlags[relative_flag];
    }      
 
    int code = candidate->BFlags;
    std::vector<int> candidate_flags = code_to_flags(code);
    // Return bool whether the flag is in the candidate's flags
    bool result = (std::find(candidate_flags.begin(), candidate_flags.end(), absolute_flag) != candidate_flags.end());
    return result;
}
 
void AnalysisBase::ignore(std::string ignore_what) {
    if(ignore_what == "electrons")
        ignoreElectrons = true;
    else if(ignore_what == "electrons_looseIsolation")
        ignoreElectrons_LooseIsolation = true;
    else if(ignore_what == "electronsMedium")
        ignoreElectrons_MediumEfficiency = true;
    else if(ignore_what == "electronsTight")
        ignoreElectrons_TightEfficiency = true;
    else if(ignore_what == "muons")
        ignoreMuons = true;
    else if(ignore_what == "muons_looseIsolation")
        ignoreMuons_LooseIsolation = true;
    else if(ignore_what == "muonsCombinedPlus")
        ignoreMuons_CombinedPlusEfficiency = true;
    else if(ignore_what == "muonsCombined")
        ignoreMuons_CombinedEfficiency = true;
    else if(ignore_what == "photons")
        ignorePhotons = true;
    else if(ignore_what == "photons_looseIsolation")
        ignorePhotons_LooseIsolation = true;
    else if(ignore_what == "tracks")
        ignoreTracks = true;
    else if(ignore_what == "towers")
        ignoreTowers = true;
    else {
        std::cerr << "Cannot ignore " << ignore_what << std::endl;
        std::cerr << "Exiting." << std::endl;
        exit(1);
    }
}

double AnalysisBase::mT(const TLorentzVector & vis, const TLorentzVector & invis, const double m_vis, const double m_invis) {
    // If no masses are given, assumed to be zero  
    return sqrt(m_vis*m_vis + m_invis*m_invis +  2.*vis.Pt()*invis.Et()*(1.-cos(fabs(vis.DeltaPhi(invis)))));
}

double AnalysisBase::mT2(const TLorentzVector & vis1, const TLorentzVector & vis2, double m_inv, const TLorentzVector & invis) {
    // Setup mt2 evaluation object.
    mt2_bisect::mt2 mt2_event;
    TLorentzVector zeroVector = TLorentzVector(0. ,0. ,0. ,0.);
    // If no invis is given, use missingET. Note that pmiss[0] is irrelvant, which is why we set it to -1.
    double pmiss[] = {-1, missingET->P4().Px(), missingET->P4().Py()};
    if (invis != zeroVector) {
        pmiss[0] = -1;
        pmiss[1] = invis.Px();
        pmiss[2] = invis.Py();
    }
 
    // Construct arrays that mt2_bisect needs as input and start evaluation
    double p1[3] = {vis1.M(), vis1.Px(), vis1.Py()};
    double p2[3] = {vis2.M(), vis2.Px(), vis2.Py()};
    mt2_event.set_momenta( p1, p2, pmiss );
    mt2_event.set_mn( m_inv );
    return mt2_event.get_mt2();  
}

double AnalysisBase::mCT(const TLorentzVector & v1,const TLorentzVector & v2)
{
    mctlib::mct mct_event;
    double v1t[4] = {v1.E(),v1.Px(),v1.Py(),v1.Pz()};
    double v2t[4] = {v2.E(),v2.Px(),v2.Py(),v2.Pz()};
    return mct_event.mctnorm(v1t,v2t);  //returns 'normal' mCT
}

double AnalysisBase::mCTcorr(const TLorentzVector & v1, const TLorentzVector & v2,const TLorentzVector & vds,const TLorentzVector & invis,const double ecm,const double mxlo)
{
    mctlib::mct mct_event;
    double v1t[4] = {v1.E(),v1.Px(),v1.Py(),v1.Pz()};
    double v2t[4] = {v2.E(),v2.Px(),v2.Py(),v2.Pz()};
    double vdst[4] = {vds.E(),vds.Px(),vds.Py(),vds.Pz()};
    double ptmt[2] = {invis.Px(),invis.Py()};
    return mct_event.mctcorr(v1t,v2t,vdst,ptmt,ecm,mxlo);
}

double AnalysisBase::mCTperp(const TLorentzVector & v1, const TLorentzVector & v2,const TLorentzVector & vds,const TLorentzVector & invis)
{
    mctlib::mct mct_event;
    double v1t[4] = {v1.E(),v1.Px(),v1.Py(),v1.Pz()};
    double v2t[4] = {v2.E(),v2.Px(),v2.Py(),v2.Pz()};
    double vdst[4] = {vds.E(),vds.Px(),vds.Py(),vds.Pz()};
    double ptmt[2] = {invis.Px(),invis.Py()};
    return mct_event.mcy(v1t,v2t,vdst,ptmt);
}

double AnalysisBase::mCTparallel(const TLorentzVector & v1, const TLorentzVector & v2,const TLorentzVector & vds,const TLorentzVector & invis)
{
    mctlib::mct mct_event;
    double v1t[4] = {v1.E(),v1.Px(),v1.Py(),v1.Pz()};
    double v2t[4] = {v2.E(),v2.Px(),v2.Py(),v2.Pz()};
    double vdst[4] = {vds.E(),vds.Px(),vds.Py(),vds.Pz()};
    double ptmt[2] = {invis.Px(),invis.Py()};
    return mct_event.mcx(v1t,v2t,vdst,ptmt);
}

double AnalysisBase::mT2_bl(const TLorentzVector & pl_in, const TLorentzVector & pb1_in, const TLorentzVector & pb2_in, const TLorentzVector & invis) {
    // Setup mt2_bl evaluation object.
    mt2bl_bisect::mt2bl mt2bl_event;
    TLorentzVector zeroVector = TLorentzVector(0. ,0. ,0. ,0.);
   
    double pl[4] = {pl_in.E(), pl_in.Px(), pl_in.Py(), pl_in.Pz()};      // El, plx, ply, plz,     (visible lepton)
    double pb1[4] = {pb1_in.E(), pb1_in.Px(), pb1_in.Py(), pb1_in.Pz()};  // Eb1, pb1x, pb1y, pb1z  (bottom on the same side as the visible lepton)
    double pb2[4] = {pb2_in.E(), pb2_in.Px(), pb2_in.Py(), pb2_in.Pz()};  // Eb2, pb2x, pb2y, pb2z  (other bottom, paired with the invisible W)
 
    // If no invis is given, use missingET. Note that pmiss[0] is irrelvant, which is why we set it to -1.
    double pmiss[] = {-1, missingET->P4().Px(), missingET->P4().Py()};
    if (invis != zeroVector) {
        pmiss[0] = -1;
        pmiss[1] = invis.Px();
        pmiss[2] = invis.Py();
    }
 
    // Construct arrays that mt2_bisect needs as input and start evaluation
    mt2bl_event.set_momenta(pl,pb1,pb2,pmiss);

    return mt2bl_event.get_mt2bl();  
}

double AnalysisBase::alphaT(const std::vector<Jet*> & jets, const double thresh_ET) {
    // alphaT code supplied by CMS
    // Need to pass jets and energy threshold of jets to be considered for variable (allows different ET to that of baseline jets)

    double HT = 0.;
    double mHTNorm = 0.;
    std::vector<Jet*> jetsThresh;
    TLorentzVector vecHT;
    for (int i = 0; i < jets.size(); i++) {
      double ET = jets[i]->P4().Et();
      if (ET > thresh_ET) {
        jetsThresh.push_back(jets[i]);
        HT += ET;
        vecHT += jets[i]->P4();
      }
    }
    double mHT = vecHT.Pt();
   
    std::vector<double> diff( 1<<(jetsThresh.size()-1) , 0. );
    for (unsigned i=0; i < diff.size(); i++) {
      for (unsigned j=0; j < jetsThresh.size(); j++) {
        diff[i] += jetsThresh[j]->P4().Et() * ( 1 - 2 * (int(i>>j)&1) ) ;
      }
    }
    double DHT = fabs( *min_element( diff.begin(), diff.end(), fabs_less() ) );
    double alphaT = 0.5 * ( HT - DHT ) / sqrt( HT*HT - mHT*mHT );
   
    return alphaT;
}

std::vector<double> AnalysisBase::razor(const std::vector<TLorentzVector> & finalStateObj, const TLorentzVector & invis) {
    // Razor code supplied by CMS (Maurizio Pierini)
    // Need to pass objects (4 vectors that could be jets or leptons) and missingET
    // Result is a 2 dimensional vector, [0] = MR, [1] = R

    TLorentzVector j1, j2;
    bool foundGood = false;
    int N_comb = 1;
    for(int i = 0; i < finalStateObj.size(); i++)
      N_comb *= 2;
 
    double M_min = 9999999999.0;
    int j_count;
    for(int i = 1; i < N_comb-1; i++) {
      TLorentzVector j_temp1, j_temp2;
      int itemp = i;
      j_count = N_comb/2;
      int count = 0;
      while(j_count > 0){
        if(itemp/j_count == 1)
          j_temp1 += finalStateObj[count];
        else
          j_temp2 += finalStateObj[count];
        itemp -= j_count*(itemp/j_count);
        j_count /= 2;
        count++;
      }
      double M_temp = j_temp1.M2()+j_temp2.M2();
      // smallest mass
      if (M_temp < M_min) {
        M_min = M_temp;
        j1 = j_temp1;
        j2 = j_temp2;
      }
    }  
    if (j2.Pt() > j1.Pt()) {
      TLorentzVector temp = j1;
      j1 = j2;
      j2 = temp;
    }  
   
    double A = j1.P();
    double B = j2.P();
    double az = j1.Pz();
    double bz = j2.Pz();
    TVector3 j1T, j2T;
    j1T.SetXYZ(j1.Px(),j1.Py(),0.0);
    j2T.SetXYZ(j2.Px(),j2.Py(),0.0);
    double ATBT = (j1T+j2T).Mag2();
    double MR = sqrt((A+B)*(A+B)-(az+bz)*(az+bz)-(j2T.Dot(j2T)-j1T.Dot(j1T))*(j2T.Dot(j2T)-j1T.Dot(j1T))/(j1T+j2T).Mag2());
    double mybeta = (j2T.Dot(j2T)-j1T.Dot(j1T))/sqrt(ATBT*((A+B)*(A+B)-(az+bz)*(az+bz)));
    double mygamma = 1./sqrt(1.-mybeta*mybeta);
    //gamma times MRstar  
    MR = MR*mygamma;
 
    double MRT = missingET->P4().Et()*(j1.Pt()+j2.Pt()) - missingET->P4().Vect().Dot(j1.Vect()+j2.Vect());
    MRT /= 2.;
    MRT = sqrt(MRT);
   
    double R = MRT/MR;
   
    std::vector<double> razor;
    razor.push_back(MR);
    razor.push_back(R);
   
    return razor;
}

