#ifndef _ATLAS_CONF_2013_035
#define _ATLAS_CONF_2013_035

#include "AnalysisBase.h"

class Atlas_conf_2013_035 : public AnalysisBase {
  public:
    Atlas_conf_2013_035(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_conf_2013_035() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
    static std::string cf_index[9];
    double cutSingleTriggerElectronPT, cutSymTriggerElectronPT, cutAsymTriggerElectronPT1, cutAsymTriggerElectronPT2;
    double cutSingleTriggerMuonPT, cutSymTriggerMuonPT, cutAsymTriggerMuonPT1, cutAsymTriggerMuonPT2;
    double cutMixedTriggerElectronPT1, cutMixedTriggerElectronPT2, cutMixedTriggerMuonPT1, cutMixedTriggerMuonPT2;
    
    double mtest, mmin, mSFOS;
    bool SFOS;
    double mT, deltaphi;
    double thirdleptonpt;
    
    bool trigger;    

};


#endif
