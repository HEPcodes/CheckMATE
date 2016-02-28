#ifndef _ATLAS_1404_2500
#define _ATLAS_1404_2500

#include "AnalysisBase.h"

class Atlas_1404_2500 : public AnalysisBase {
  public:
    Atlas_1404_2500(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_1404_2500() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
    static std::string cf_index[10];
    double trigger_ETmiss, trigger_single_el_pt, trigger_single_mu_pt, trigger_di_el_pt, trigger_di_mu_pt;
    double meff;
    double mll;
    double mT;
    double sign;
    bool trigger;
    int nbjets;
    double deltaphi;
    std::vector<TLorentzVector> leptons; 
};


#endif
