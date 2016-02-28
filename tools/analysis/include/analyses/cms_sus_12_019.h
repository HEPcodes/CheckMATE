#ifndef _CMS_SUS_12_019
#define _CMS_SUS_12_019

#include "AnalysisBase.h"

class Cms_sus_12_019 : public AnalysisBase {
  public:
    Cms_sus_12_019(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Cms_sus_12_019() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
};


#endif
