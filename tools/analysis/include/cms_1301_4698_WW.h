#ifndef _CMS_1301_4698_WW
#define _CMS_1301_4698_WW

#include "AnalysisBase.h"
#include "TH2F.h"

class Cms_1301_4698_ww : public AnalysisBase {
  public:
    Cms_1301_4698_ww(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Cms_1301_4698_ww() {}
  
    void initialize();
    void analyze();        
    void finalize();
    void outputHistFile(TH1D* inHist);

  private:
    TH1D *histo_ptmax, *histo_ptmin, *histo_ptll, *histo_mll, *histo_etadiff, *histo_etasum, *histo_sqrtsmin, *histo_dx;
    TH2D *histo_rap2D;
    int asy1p, asy1m, asy2p, asy2m;
};


#endif
