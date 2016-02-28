#ifndef _ATLAS_CONF_2015_004
#define _ATLAS_CONF_2015_004
// AUTHOR: Jong Soo Kim
//  EMAIL: jsk@th.physik.uni-bonn.de
#include "AnalysisBase.h"

class Atlas_conf_2015_004 : public AnalysisBase {
  public:
    Atlas_conf_2015_004(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_conf_2015_004() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
};


#endif
