#ifndef _CMS_SMP_12_006
#define _CMS_SMP_12_006

#include "AnalysisBase.h"

class Cms_smp_12_006 : public AnalysisBase {
  public:
    Cms_smp_12_006(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Cms_smp_12_006() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
};


#endif
