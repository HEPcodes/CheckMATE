#ifndef _CMS_SUS_13_016
#define _CMS_SUS_13_016
// AUTHOR: Jamie Tattersall
//  EMAIL: tattersall@thphys.uni-heidelberg.de
#include "AnalysisBase.h"

class Cms_sus_13_016 : public AnalysisBase {
  public:
    Cms_sus_13_016(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Cms_sus_13_016() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
};


#endif
