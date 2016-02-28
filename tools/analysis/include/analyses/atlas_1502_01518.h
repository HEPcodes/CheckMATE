#ifndef _ATLAS_1502_01518
#define _ATLAS_1502_01518
// AUTHOR: Jamie Tattersall
//  EMAIL: tattersall@thphys.uni-heidelberg.de
#include "AnalysisBase.h"

class Atlas_1502_01518 : public AnalysisBase {
  public:
    Atlas_1502_01518(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_1502_01518() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
};


#endif
