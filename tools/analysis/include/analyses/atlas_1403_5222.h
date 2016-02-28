#ifndef _ATLAS_1403_5222
#define _ATLAS_1403_5222
// AUTHOR: KR
//  EMAIL: krolb@fuw.edu.pl
#include "AnalysisBase.h"

class Atlas_1403_5222 : public AnalysisBase {
  public:
    Atlas_1403_5222(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_1403_5222() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
};


#endif
