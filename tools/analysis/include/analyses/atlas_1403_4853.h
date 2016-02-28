#ifndef _ATLAS_1403_4853
#define _ATLAS_1403_4853

#include "AnalysisBase.h"

class Atlas_1403_4853 : public AnalysisBase {
  public:
    Atlas_1403_4853(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_1403_4853() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
    static std::string cf_index[12];
    double cutSingleTriggerElectronPT,cutSingleTriggerMuonPT,cutDoubleTriggerElectronPT,cutDoubleTriggerMuonPT,cutMixedTriggerMuonPT,cutMixedTriggerElectronPT;
	
    double leadingleptonpt;
    
    TLorentzVector pllTb;
    double mtest;
    
    double deltamin,deltatemp;
    int i_closestjet;

    bool trigger;
    

};


#endif
