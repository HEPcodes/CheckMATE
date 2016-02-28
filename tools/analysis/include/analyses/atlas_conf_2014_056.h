#ifndef _ATLAS_CONF_2014_056
#define _ATLAS_CONF_2014_056

#include "AnalysisBase.h"

class Atlas_conf_2014_056 : public AnalysisBase {
  public:
    Atlas_conf_2014_056(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_conf_2014_056() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
    TH1D *histo_phill, *histo_etadiff;
};


#endif
