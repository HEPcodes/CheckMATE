#ifndef _CMS_1502_06031
#define _CMS_1502_06031
// AUTHOR: kitpc
//  EMAIL: kitpc
#include "AnalysisBase.h"

class Cms_1502_06031 : public AnalysisBase {
  public:
    Cms_1502_06031(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Cms_1502_06031() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
    ofstream fout1;
};


#endif
