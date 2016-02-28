#ifndef _ATLAS_1308_1841
#define _ATLAS_1308_1841
// AUTHOR: kitpc
// EMAIL: kitpc
#include "AnalysisBase.h"

class Atlas_1308_1841 : public AnalysisBase {
  public:
    Atlas_1308_1841(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_1308_1841() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
    ofstream fout1, fout2, fout3, fout4;
    static std::string namesCutflow[10];
};


#endif
