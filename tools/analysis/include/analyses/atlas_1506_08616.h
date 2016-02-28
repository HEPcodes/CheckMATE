#ifndef _ATLAS_1506_08616
#define _ATLAS_1506_08616
// AUTHOR: K. Rolbiecki
//  EMAIL: krolb@fuw.edu.pl
#include "AnalysisBase.h"

class Atlas_1506_08616 : public AnalysisBase {
  public:
    Atlas_1506_08616(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_1506_08616() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
};


#endif
