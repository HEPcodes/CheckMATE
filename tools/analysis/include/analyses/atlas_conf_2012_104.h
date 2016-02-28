#ifndef _ATLAS_CONF_2012_104
#define _ATLAS_CONF_2012_104

#include "AnalysisBase.h"

class Atlas_conf_2012_104 : public AnalysisBase {
  public:
    Atlas_conf_2012_104(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_conf_2012_104() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
    double signal_el,signal_mu;
    double cutTriggerElectronPT_comb,cutTriggerElectron_ETmiss_comb,cutTriggerElectronPT;
    double cutTriggerMuonPT,cutTriggerMuon_JetPT,cutTriggerMuon_ETmiss;
    double mEff,mEff_inc,sumjetpt,sumjetpt_4,mT,deltaphi;
    bool trigger;
};


class Atlas_conf_2012_104_CR : public AnalysisBase {
  public:
    Atlas_conf_2012_104_CR(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr, std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_conf_2012_104_CR() {}
    
    void initialize();
    void analyze();        
    void finalize();

  private:
};

#endif
