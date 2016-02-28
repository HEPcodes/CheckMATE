#ifndef _ATLAS_1405_7875
#define _ATLAS_1405_7875

#include "AnalysisBase.h"

class Atlas_1405_7875 : public AnalysisBase {
  public:
    Atlas_1405_7875(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_1405_7875() {}
    
    void initialize();
    void analyze();        
    void finalize();

  private:
    double meff2J, meff3J, meff4J, meff4JW, meff5J, meff6J;
    bool flag4JW, flag3J, flag4J, flag5J, flag6J;
    static std::string nameSR[15];

};


#endif
