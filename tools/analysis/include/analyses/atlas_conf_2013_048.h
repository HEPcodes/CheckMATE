#ifndef _ATLAS_CONF_2013_048
#define _ATLAS_CONF_2013_048

#include "AnalysisBase.h"

class Atlas_conf_2013_048 : public AnalysisBase {
  public:
    Atlas_conf_2013_048(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_conf_2013_048() {}
  
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
