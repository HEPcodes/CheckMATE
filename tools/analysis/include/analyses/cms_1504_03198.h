#ifndef _CMS_1504_03198
#define _CMS_1504_03198
// AUTHOR: Junjie Cao, Liangliang Shang, Peiwen Wu, Jin Min Yang, Yang Zhang
//  EMAIL: junjiec@itp.ac.cn, shlwell1988@gmail.com, peiwen.wu123@gmail.com, jmyang@itp.ac.cn, zhangyang@itp.ac.cn
#include "AnalysisBase.h"

class Cms_1504_03198 : public AnalysisBase {
  public:
    Cms_1504_03198(std::string inFile, std::string outFol, std::string outPre, double xs, double xserr,  std::map<std::string, std::string> branches, std::map<std::string, std::vector<int> > flags) : AnalysisBase(inFile, outFol, outPre, xs, xserr, branches, flags)  {}               
    ~Cms_1504_03198() {}
  
    void initialize();
    void analyze();        
    void finalize();

  private:
};


#endif
