#ifndef _ATLAS_1402_7029
#define _ATLAS_1402_7029

#include "AnalysisBase.h"

class Atlas_1402_7029 : public AnalysisBase {
  public:
    Atlas_1402_7029(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_1402_7029() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
    double cutSingleTriggerElectronPT, cutSymTriggerElectronPT, cutAsymTriggerElectronPT1, cutAsymTriggerElectronPT2;
    double cutSingleTriggerMuonPT, cutSymTriggerMuonPT, cutAsymTriggerMuonPT1, cutAsymTriggerMuonPT2;
    double cutMixedTrigger1ElectronPT, cutMixedTrigger2ElectronPT, cutMixedTrigger1MuonPT, cutMixedTrigger2MuonPT;
};


#endif
