#ifndef _CMS_1306_1126_WW
#define _CMS_1306_1126_WW

#include "AnalysisBase.h"
#include "TH2F.h"

class Cms_1306_1126_ww : public AnalysisBase {
  public:
    Cms_1306_1126_ww(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Cms_1306_1126_ww() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
    TH1D *histo_ptmax, *histo_ptmin, *histo_ptll, *histo_mll, *histo_etadiff, *histo_etasum, *histo_sqrtsmin;
    TH2D *histo_rap2D;
};


#endif
