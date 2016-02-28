#ifndef _ANALYSISBASE
#define _ANALYSISBASE

#include <iostream>
#include <fstream>
#include <stdio.h>
#include <map>
#include <math.h>

#include <TCanvas.h>
#include <TChain.h>
#include <TClonesArray.h>
#include <TH1.h>
#include <TObject.h>
#include <TROOT.h>
#include <TStyle.h>
#include <TSystem.h>

#include "classes/DelphesClasses.h"
#include "external/ExRootAnalysis/ExRootTreeReader.h"
#include "external/ExRootAnalysis/ExRootResult.h"

#include "mt2_bisect.h"
#include "mctlib.h"
#include "mt2bl_bisect.h"

// This class serves as an intrinsic parametrisation of the missingET
// vector, which is defined such that it has the same properties as there
// other final state objects, like jet->ET or electron->Ex. Furthermore,
// the user can decide which class of muons he wants to take into account
// for the total missing energy vector.
class ETMiss {
 public:
    ETMiss(MissingET* x) {
	double missingET_ET = x->MET;
	double missingET_Phi = x->Phi;
	double missingET_Ex = missingET_ET*cos(missingET_Phi);
	double missingET_Ey = missingET_ET*sin(missingET_Phi);

	content.SetPxPyPzE(missingET_Ex, missingET_Ey, 0., missingET_ET);
	PT = content.Pt();
	Eta = content.Eta();
	Phi = content.Phi();
    }
    
    // Muons have to be added manually to missingET. With this general function,
    //  one can decide which muon set(s) one wants to add.
    void addMuons(std::vector<Muon*> muons) {
	TLorentzVector sum = TLorentzVector(0,0,0,0);
      for(int i = 0; i < muons.size(); i++)
        sum += muons[i]->P4();
      
      double new_ET = sqrt(pow(content.Px()-sum.Px(), 2)+pow(content.Py()-sum.Py(), 2));
      content.SetPxPyPzE(content.Px()-sum.Px(), content.Py()-sum.Py(), 0, new_ET);
      PT = content.Pt();
      Eta = content.Eta();
      Phi = content.Phi();
    }
    
    Float_t PT; 
    Float_t Eta; 
    Float_t Phi;
    TLorentzVector P4() { return content; }

 private:
    TLorentzVector content;
};

// This is the base class for all analyses.
class AnalysisBase {
 public:
    AnalysisBase(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr, std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags);
    ~AnalysisBase(); 

    void loopOverEvents();

 protected:
    // File streams for generalized output files
    std::vector<std::ofstream*> fStreams;
    std::vector<std::string> fNames;
                
    // Containers for each event's particles
    std::vector<Electron*> electrons;
    std::vector<Electron*> electronsLoose;
    std::vector<Electron*> electronsMedium;
    std::vector<Electron*> electronsTight;
    std::vector<Muon*> muons;
    std::vector<Muon*> muonsCombined;
    std::vector<Muon*> muonsCombinedPlus;
    std::vector<Jet*> jets;
    std::vector<Jet*> jets2;
    std::vector<Photon*> photons;
    std::vector<Track*> tracks;
    std::vector<Tower*> towers;
        
    // MissingET vector
    ETMiss* missingET;
    
    // Monte Carlo weight of the event
    double weight;
                
    // Virtual functions that have to be properly defined by each individual analysis
    virtual void initialize() {}; // Runs once before the event loop
    virtual void analyze() {}; // Runs for each event separately
    virtual void finalize() {}; // Runs once after the event loop
    
    // Creates a file at the output path with specific prefix dictated by CheckMATE.
    // Textfiles start with a standardized header
    int bookFile(std::string name); 
    
    // Defines all used SR/CR/Cutflow maps
    // Multiple regions are given as one string, separated by ;
    void bookSignalRegions(std::string listOfRegions);
    void bookControlRegions(std::string listOfRegions);
    void bookCutflowRegions(std::string listOfRegions);

    // Registers the current event for given regions
    inline void countSignalEvent(std::string region) {      
      signalRegions[region] += weight;
      signalRegions2[region] += weight*weight;
    }
    inline void countControlEvent(std::string region) {      
      controlRegions[region] += weight;
      controlRegions2[region] += weight*weight;
    }
    inline void countCutflowEvent(std::string region) {
      cutflowRegions[region] += weight;
      cutflowRegions2[region] += weight*weight;
    }
    
    // Sets 'ignore' flags in order to prevent current analysis to 
    // set particle containers it does not need
    void ignore(std::string ignore_what);
    
    // A given set of objects (electrons, jets, ...) can be filtered w.r.t minimum pt and a given eta range
    // the overlap region 1.37 <= |eta| <= 1.52 is common for many objects and hence it has a seperate parameter.
    template <class T>
    std::vector<T*> filterPhaseSpace(std::vector<T*> unfiltered, double pTmin = 0., double etamin = -100, double etamax = 100, bool exclude_overlap = false) {
	std::vector<T*> filtered;
	for (int i = 0; i < unfiltered.size(); i++) {
	    T* cand = unfiltered[i];
	    if((cand->PT > pTmin) && (cand->Eta > etamin) && (cand->Eta < etamax)) {
              if(!exclude_overlap)
		filtered.push_back(cand);
              else if( (fabs(cand->Eta) < 1.37) || (fabs(cand->Eta) > 1.52) )
                filtered.push_back(cand);
            }
	}
	return filtered;
    }       

    // Returns all members of the list 'candidates', that do not overlap with any of the 'neighbours'
    // with respect to the given maximum distance dR
    template <class X, class Y>
    std::vector<X*> overlapRemoval(std::vector<X*> candidates, std::vector<Y*> neighbours, double dR) {
      // If neighbours are empty, return candidates
      if(neighbours.size() == 0)
        return candidates;
      std::vector<X*> passed_candidates;
      // Loop over candidates
      for(int i = 0; i < candidates.size(); i++) {
        bool overlap = false;
        // If a neighbour is too close, declare overlap, break and don't save candidate
        for(int j = 0; j < neighbours.size(); j++) {
          if (candidates[i]->P4().DeltaR(neighbours[j]->P4()) < dR) {
            overlap = true;
            break;
          }
        }
        if (!overlap)
          passed_candidates.push_back(candidates[i]);
      }
      return passed_candidates;
    }

    // Same as above, but candidates = neighbours, which only needs to check half the possible 
    // combinations. In case of overlaps, the one with fewer energy is removed.
    template <class X>
    std::vector<X*> overlapRemoval(std::vector<X*> candidates, double dR) {
      // Same as above for the special case that candidates = neighbours. In that case, the removal 
      // can be formulated more effectively as the sum only has to run half as many times
      if(candidates.size() == 0)
        return candidates;
      std::vector<X*> passed_candidates;
      // Loop over candidates
      for(int i = 0; i < candidates.size(); i++) {
        bool overlap = false;
        // If one of the other, still untested, candidates is too close: remove
        // Since the list is order w.r.t pt, this will always remove the softer object
        for(int j = 0; j < i; j++) {
          if (candidates[i]->P4().DeltaR(candidates[j]->P4()) < dR) {
            overlap = true;
            break;
          }
        }
        if (!overlap)
          passed_candidates.push_back(candidates[i]);
      }
      return passed_candidates;
    }
    
    // Checks whether the given list of electrons have passed the considered isolation criteron/criteria given in the list.
    // Note: The first isolation criterion defined by the user in CheckMATE is tested with relative flag 0!
    std::vector<Electron*> filterIsolation(std::vector<Electron*> unfiltered, std::vector<int> relative_flags = std::vector<int>()) {
      // Translate the relative isolation number of the analysis in the absolute number within all analyses
        std::vector<int> absolute_flags;
        for(int i = 0; i < relative_flags.size(); i++) {
          if (relative_flags[i] >= electronIsolationFlags.size()) {
            std::cerr << "Error: There is no electron isolation " << relative_flags[i] << std::endl;
            std::cerr << "Exiting... "<< std::endl;
            exit(1);
          }
          absolute_flags.push_back(electronIsolationFlags[relative_flags[i]]);
        }
        // if no flags are given, use all
        if (absolute_flags.size() == 0)          
          absolute_flags = electronIsolationFlags;
          
        return filterFlags(unfiltered, "isolation", absolute_flags);
    }
    
    // Same as above, for a single flag.
    std::vector<Electron*> filterIsolation(std::vector<Electron*> unfiltered, int relative_flag) {
      std::vector<int> absolute_flags;
      if (relative_flag >= electronIsolationFlags.size()) {
          std::cerr << "Error: There is no electron isolation " << relative_flag << std::endl;
          std::cerr << "Exiting... "<< std::endl;
          exit(1);
        }
        absolute_flags.push_back(electronIsolationFlags[relative_flag]);        
        return filterFlags(unfiltered, "isolation", absolute_flags);
    }    
    
    // Same as above, for muons
    std::vector<Muon*> filterIsolation(std::vector<Muon*> unfiltered, std::vector<int> relative_flags = std::vector<int>()) {
      // Translate the relative isolation number of the analysis in the absolute number within all analyses
        std::vector<int> absolute_flags;
        for(int i = 0; i < relative_flags.size(); i++) {
          if (relative_flags[i] >= muonIsolationFlags.size()) {
            std::cerr << "Error: There is no muon isolation " << relative_flags[i] << std::endl;
            std::cerr << "Exiting... "<< std::endl;
            exit(1);
          }
          absolute_flags.push_back(muonIsolationFlags[relative_flags[i]]);
        }
        // if no flags are given, use all
        if (absolute_flags.size() == 0)          
          absolute_flags = muonIsolationFlags;
          
        return filterFlags(unfiltered, "isolation", absolute_flags);
    }
    
    std::vector<Muon*> filterIsolation(std::vector<Muon*> unfiltered, int relative_flag) {
        std::vector<int> absolute_flags;
        if (relative_flag >= muonIsolationFlags.size()) {
            std::cerr << "Error: There is no muon isolation " << relative_flag << std::endl;
            std::cerr << "Exiting... "<< std::endl;
            exit(1);
          }
          absolute_flags.push_back(muonIsolationFlags[relative_flag]);
        
        
        return filterFlags(unfiltered, "isolation", absolute_flags);
    }    
    
    std::vector<Photon*> filterIsolation(std::vector<Photon*> unfiltered, std::vector<int> relative_flags = std::vector<int>()) {
      // Translate the relative isolation number of the analysis in the absolute number within all analyses
        std::vector<int> absolute_flags;
        for(int i = 0; i < relative_flags.size(); i++) {
          if (relative_flags[i] >= photonIsolationFlags.size()) {
            std::cerr << "Error: There is no photon isolation " << relative_flags[i] << std::endl;
            std::cerr << "Exiting... "<< std::endl;
            exit(1);
          }
          absolute_flags.push_back(photonIsolationFlags[relative_flags[i]]);
        }
        // if no flags are given, use all
        if (absolute_flags.size() == 0)          
          absolute_flags = photonIsolationFlags;
          
        return filterFlags(unfiltered, "isolation", absolute_flags);
    }
    
    std::vector<Photon*> filterIsolation(std::vector<Photon*> unfiltered, int relative_flag) {
        std::vector<int> absolute_flags;
        if (relative_flag >= photonIsolationFlags.size()) {
            std::cerr << "Error: There is no photon isolation " << relative_flag << std::endl;
            std::cerr << "Exiting... "<< std::endl;
            exit(1);
          }
          absolute_flags.push_back(photonIsolationFlags[relative_flag]);
        
        
        return filterFlags(unfiltered, "isolation", absolute_flags);
    }    
    
    // Checks if candidate jet fulfills given tau identification cut ('loose', 'medium', 'tight')
    bool checkTauTag(Jet* candidate, std::string efficiency);
    
    // Checks if candidate jet fulfills given b-jet identification 
    // The first b-efficiency defined in CheckMATE is tested with relative_flag = 0.
    // If the candidate belongs to the 'second jet' type, the user has to give the option
    // 'secondJet', since the internal numbering of the flags is different.
    bool checkBTag(Jet* candidate, int relative_flag = 0, std::string option = "");
    
    inline void setInformation(std::string s) {
	information = s;
    };
    
    inline void setLuminosity(double l) {
      luminosity = l;
    };
    
    inline void setAnalysisName(std::string name) {
      analysis = name;
    };
        
    // Normalises number to the given luminosity of the analysis and the nominal cross section of the data
    inline double normalize(double x) {
	return x*xsect*luminosity/sumOfWeights;
    };

    // Evaluates mT 
    double mT(const TLorentzVector & vis, const TLorentzVector & invis);
    
    // Evaluates mT2 (arXiv:0810.5178)
    double mT2(const TLorentzVector & vis1, const TLorentzVector & vis2, double m_inv, const TLorentzVector & invis = TLorentzVector(0., 0., 0., 0.));

    // Evaluates 'normal' MCT (JHEP 0804:034,2008, arXiv:0802.2879 [hep-ph])
    double mCT(const TLorentzVector & v1, const TLorentzVector & v2);
    
    // Evaluates boost corrected MCT (JHEP 0804:034,2008, arXiv:0802.2879 [hep-ph])
    double mCTcorr(const TLorentzVector & v1, const TLorentzVector & v2, const TLorentzVector & vds, const TLorentzVector & invis, const double ecm = 8000.0, const double mxlo = 0.0);
    
    // Evaluates MCT transverse (arXiv:0910.1584 [hep-ph])
    double mCTy(const TLorentzVector & v1, const TLorentzVector & v2, const TLorentzVector & vds, const TLorentzVector & invis);        
    
    // Evaluates mT2_bl (arXiv:1203.4813), Also known as asymmetric mT2 in atlas_conf_2013_037
    double mT2_bl(const TLorentzVector & pl_in, const TLorentzVector & pb1_in, const TLorentzVector & pb2_in, const TLorentzVector & invis = TLorentzVector(0., 0., 0., 0.));    


    // For using ExRootAnalysis
    ExRootResult *result;

 private:
    // Overall reader of the ROOT tree
    ExRootTreeReader *treeReader;	
    TChain *chain;
    
    // Objects for all the branches in the ROOT file
    TClonesArray *branchElectron;
    TClonesArray *branchMuon;
    TClonesArray *branchJet;
    TClonesArray *branchJet2;
    TClonesArray *branchPhoton;
    TClonesArray *branchMissingET;
    TClonesArray *branchEvent;
    TClonesArray *branchTrack;
    TClonesArray *branchTower;    
        
    // Information on files
    std::string outputFolder;
    std::string outputPrefix;
    std::string inputFile;

    // Information about the analysis to be printed at the start of each output file
    std::string analysis;
    std::string information;
    
    // Global parameters
    Long64_t nEvents;
    double sumOfWeights;
    double sumOfWeights2;
    double xsect;
    double xsecterr;
    double luminosity;
        
    // Sums up weights (and weights^2) that fall into control, signal or cutflow regions 
    std::map<std::string, double> controlRegions;
    std::map<std::string, double> signalRegions;    
    std::map<std::string, double> cutflowRegions;
    std::map<std::string, double> controlRegions2;
    std::map<std::string, double> signalRegions2;    
    std::map<std::string, double> cutflowRegions2;
    
    // Absolute flag values for the isolation criteria of the individual analysis
    // [e.g. if there are 2 analyses with 2 isolation criteria each, analysis 1 gets (1, 2)
    //  whereas analysis 2 gets (3, 4) ]
    std::vector<int> electronIsolationFlags;
    std::vector<int> muonIsolationFlags;
    std::vector<int> photonIsolationFlags;
    std::vector<int> jetBTagFlags;
    std::vector<int> jet2BTagFlags;    
    
    // If these flags are set, the corresponding containers won't be set up (to save computing time)
    bool ignoreElectrons;
    bool ignoreElectrons_LooseIsolation;
    bool ignoreElectrons_MediumEfficiency;
    bool ignoreElectrons_TightEfficiency;
    bool ignoreMuons;
    bool ignoreMuons_LooseIsolation;
    bool ignoreMuons_CombinedPlusEfficiency;
    bool ignoreMuons_CombinedEfficiency;
    bool ignorePhotons;
    bool ignorePhotons_LooseIsolation;
    bool ignoreTracks;
    bool ignoreTowers;

    // A given set of objects (Electrons, Jets, ...) can be filtered w.r.t given flag values
    template <class T>
    std::vector<T*> filterFlags(std::vector<T*> unfiltered, std::string whichFlag, std::vector<int> flags) {
      std::vector<T*> filtered;
      for (int i = 0; i < unfiltered.size(); i++) {
        T* cand = unfiltered[i];
        // First, decode the member's isoflag into a vector of valid flags
        int code = 0;
        if(whichFlag == "isolation") {
          code = cand->IsolationFlags;
        }        
        else if(whichFlag == "efficiency")
          code = cand->EfficiencyFlags;
        
        std::vector<int> candidates_flags = code_to_flags(code);
        
        // Then, check if iso_flags are all within the member's flags        
        bool passes = true;
        for (int iso = 0; iso < flags.size(); iso++) {
          if(std::find(candidates_flags.begin(), candidates_flags.end(), flags[iso]) == candidates_flags.end()) {
            passes = false;
            break;
          }
        }
        
        // Only if memebr passed it should be saved in filtered list
        if(passes)
          filtered.push_back(cand);
      }
      return filtered;
    }
    
    // The flagnumber, read in binary, tells which flags have been set to true
    std::vector<int> code_to_flags(int code) {
      std::vector<int> flags;
      int flag = 0;
      while(code > 0) {
        if(code % 2 == 1)
          flags.push_back(flag);
          code -= code % 2;
        code /= 2;
        flag++;
      }
      return flags;
    }
};

// Numerical implementation of cross section and luminosity units
namespace units {
    const double KB = 1.E18, B = 1.E15, MB = 1.E12, MUB = 1.E9, NB = 1.E6, PB = 1.E3, FB = 1.0, AB = 1.E-3, ZB = 1.E-6; 
    const double INVKB = 1./KB, INVB = 1./B, INVMB = 1./MB, INVMUB = 1./MUB, INVNB = 1./NB, INVPB = 1./PB, INVFB = 1./FB, INVAB = 1./AB, INVZB = 1./ZB;
    inline double strToUnit(std::string unit) {
	if (unit == "KB") return KB;
	else if (unit == "B") return B;
	else if (unit == "MB") return MB;
	else if (unit == "MUB") return MUB;
	else if (unit == "NB") return NB;
	else if (unit == "PB") return PB;
	else if (unit == "FB") return FB;
	else if (unit == "AB") return AB;
	else if (unit == "ZB") return ZB;
	else if (unit == "INVKB") return INVKB;
	else if (unit == "INVB") return INVB;
	else if (unit == "INVMB") return INVMB;
	else if (unit == "INVMUB") return INVMUB;
	else if (unit == "INVNB") return INVNB;
	else if (unit == "INVPB") return INVPB;
	else if (unit == "INVFB") return INVFB;
	else if (unit == "INVAB") return INVAB;
	else if (unit == "INVZB") return INVZB;
	else {std::cerr << "Unit unknown!" << std::endl; exit(1);}
    }
}


#endif
