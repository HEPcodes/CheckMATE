#ifndef _ATLAS_1411_1559
#define _ATLAS_1411_1559
// AUTHOR: Cristina Marcos
//  EMAIL: mcristina.marcosm@gmail.com
#include "AnalysisBase.h"

class Atlas_1411_1559 : public AnalysisBase {
  public:
    Atlas_1411_1559(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Atlas_1411_1559() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
};


#endif
