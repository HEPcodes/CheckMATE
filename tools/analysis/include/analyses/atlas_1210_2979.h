#ifndef _ATLAS_1210_2979
#define _ATLAS_1210_2979

#include "AnalysisBase.h"

class Atlas_1210_2979 : public AnalysisBase {
  public:
    Atlas_1210_2979(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_1210_2979() {}
  
    void initialize();
    void analyze();        
    void finalize();
    void outputHistFile(TH1F* inHist);

  private:
    
    TH1F *hist_lep_pt, *hist_delta_phi, *hist_lletmiss_pt, *hist_lletmiss_mT;
};



#endif
