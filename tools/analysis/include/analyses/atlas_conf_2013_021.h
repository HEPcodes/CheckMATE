#ifndef _ATLAS_CONF_2013_021
#define _ATLAS_CONF_2013_021

#include "AnalysisBase.h"

class Atlas_conf_2013_021 : public AnalysisBase {
  public:
    Atlas_conf_2013_021(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_conf_2013_021() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
};


#endif
