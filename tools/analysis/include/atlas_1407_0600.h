#ifndef _ATLAS_1407_0600
#define _ATLAS_1407_0600

#include "AnalysisBase.h"

class Atlas_1407_0600 : public AnalysisBase {
  public:
    Atlas_1407_0600(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_1407_0600() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
    double DeltaPhi4jmin;
    double meff4j;
    double HT4j;
    double meff;
    double meffincl;
    double mT;
    static std::string cf_index[12];
};


#endif
