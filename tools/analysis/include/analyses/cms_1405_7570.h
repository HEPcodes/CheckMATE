#ifndef _CMS_1405_7570
#define _CMS_1405_7570
// AUTHOR: Krzysztof
//  EMAIL: krzysztof.rolbiecki@desy.de
#include "AnalysisBase.h"

class Cms_1405_7570 : public AnalysisBase {
  public:
    Cms_1405_7570(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Cms_1405_7570() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
};


#endif
