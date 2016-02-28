#ifndef _ATLAS_1308_2631
#define _ATLAS_1308_2631

#include "AnalysisBase.h"

class Atlas_1308_2631 : public AnalysisBase {
  public:
    Atlas_1308_2631(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_1308_2631() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
};


class Atlas_1308_2631_CR : public AnalysisBase {
  public:
    Atlas_1308_2631_CR(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr, std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_1308_2631_CR() {}
    
    void initialize();
    void analyze();        
    void finalize();

  private:
};

#endif
