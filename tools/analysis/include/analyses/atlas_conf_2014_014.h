#ifndef _ATLAS_CONF_2014_014
#define _ATLAS_CONF_2014_014

#include "AnalysisBase.h"
#include "TH2F.h"

class Atlas_conf_2014_014 : public AnalysisBase {
  public:
    Atlas_conf_2014_014(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_conf_2014_014() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
    
    TH1D *histo_etadiff, *histo_etasum, *histo_dx;
};


#endif
