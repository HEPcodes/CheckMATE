#ifndef _ATLAS_1407_0608
#define _ATLAS_1407_0608

#include "AnalysisBase.h"

class Atlas_1407_0608 : public AnalysisBase {
  public:
    Atlas_1407_0608(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_1407_0608() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
};


#endif