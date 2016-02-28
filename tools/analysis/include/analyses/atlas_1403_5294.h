#ifndef _ATLAS_1403_5294
#define _ATLAS_1403_5294

#include "AnalysisBase.h"

class Atlas_1403_5294 : public AnalysisBase {
  public:
    Atlas_1403_5294(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_1403_5294() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
};


class Atlas_1403_5294_CR : public AnalysisBase {
  public:
    Atlas_1403_5294_CR(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr, std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_1403_5294_CR() {}
    
    void initialize();
    void analyze();        
    void finalize();

  private:
};

#endif
