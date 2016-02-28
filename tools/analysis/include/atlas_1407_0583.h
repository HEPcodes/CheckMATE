#ifndef _ATLAS_1407_0583
#define _ATLAS_1407_0583

#include "AnalysisBase.h"

class Atlas_1407_0583 : public AnalysisBase {
  public:
    Atlas_1407_0583(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_1407_0583() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
};


#endif
