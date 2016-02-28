#ifndef _ATLAS_PHYS_PUB_2013_011
#define _ATLAS_PHYS_PUB_2013_011
// AUTHOR: Jong Soo Kim
//  EMAIL: jongsoo.kim@tu-dortmund.de
#include "AnalysisBase.h"

class Atlas_phys_pub_2013_011 : public AnalysisBase {
  public:
    Atlas_phys_pub_2013_011(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_phys_pub_2013_011() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
};


#endif
