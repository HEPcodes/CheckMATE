#ifndef _CMS_1408_3583
#define _CMS_1408_3583
// AUTHOR: s.b.
//  EMAIL: swasti@th.physik.uni-bonn.de
#include "AnalysisBase.h"

class Cms_1408_3583 : public AnalysisBase {
  public:
    Cms_1408_3583(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Cms_1408_3583() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
  TH1F* hist_Met_Master;
  TH1F* hist_PT_Master;  
  void outputHistFile(TH1F* inHist);
};


#endif
