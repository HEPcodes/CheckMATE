#include <cstring>
#include <cstdlib>
#include <iostream>
#include <map>
#include <stdio.h>
#include <vector>

#include "AnalysisBase.h"

//@@extraheader@@
#include "atlas_1308_2631.h" 
#include "atlas_conf_2012_104.h" 
#include "atlas_conf_2012_147.h" 
#include "atlas_conf_2013_024.h" 
#include "atlas_conf_2013_035.h" 
#include "atlas_conf_2013_047.h" 
#include "atlas_conf_2013_049.h" 
#include "atlas_conf_2013_061.h" 
#include "atlas_conf_2013_089.h" 

#include "cms_1303_2985.h" 
#include "cms_sus_13_016.h" 








int main(int argc, char* argv[]) {
    if(argc <= 6) {
	std::cerr << "Usage: doAnalysis [analysis] [inputFile] [outputFolder] [outputPrefix] {[xsect] [unit] [xsecterr] [unit]  {branches} {isolationflags}}" << std::endl;
	exit(1);
    }
    
    // First parameters determine analysis to be used and input/output file information.
    std::string analysis(argv[1]);
    std::string inputFile(argv[2]);
    std::string outputFolder(argv[3]);
    std::string outputPrefix(argv[4]);

    // Four further parameters give the cross section, errors and units to be used.
    double xsect = 0.0;
    double xsecterr = 0.0;
    if(argc>5)
      xsect = atof(argv[5])*units::strToUnit(std::string(argv[6]));
    if(argc>7)
      xsecterr = atof(argv[7])*units::strToUnit(std::string(argv[8]));
    
    // A map is used to save information about which branches of the root file have the corresponding information.
    std::map<std::string, std::string> branches;

    // Standard Values    
    branches["Event"] = "Event";
    branches["Particle"] = "Particle";
    branches["Track"] = "Track";
    branches["Tower"] = "Tower";
    branches["Jet"] = "Jet";
    branches["Jet2"] = "Jet2";
    branches["Electron"] = "Electron";
    branches["Photon"] = "Photon";
    branches["Muon"] = "Muon";
    branches["MissingET"] = "MissingET";

    // If a branch parameter is given, it encodes to-be-overwritten branch information in the form "branch1:name1;branch2:name2".
    if( argc >= 9) {
      char* longString = argv[9];
      std::string currKey = "";
      std::string currItem = "";
      bool fillItem = false;
      for (int i = 0; i < strlen(longString); i++) {
	  char c = longString[i];
	  if (c == ':')
	      fillItem = true;
	  else if (c == ';') {
	      fillItem = false;
	      branches.at(currKey) = currItem;
	      currKey = currItem = "";
	  }
	  else
	      fillItem == false ? currKey += c : currItem += c;
      }
    }

    // Same with isolation parameters with parameter 8
    // Note: Never save flag 0, since it is the 'internal minimum isolation'.
    std::map< std::string, std::vector<int> > flags;
    flags["electron_isolation"];
    flags["muon_isolation"];
    flags["photon_isolation"];
    flags["jet_btags"];
    flags["jet2_btags"];
    flags["randomseed"];
    if( argc >= 10) {
      char* longString = argv[10];
      std::string currKey = "";
      std::string currItem = "";
      bool fillItem = false;
      for (int i = 0; i < strlen(longString); i++) {
	  char c = longString[i];
	  if (c == ':')
	      fillItem = true;
	  else if (c == '[')
	      continue;
	  else if (c == ',') {
	      if ((currItem != "0")||(currKey == "jet_btags")||(currKey == "jet2_btags"))
                  flags.at(currKey).push_back(atoi(currItem.c_str()));
	      currItem = "";
	  }
	  else if (c == ']') {
	      if (((currItem != "0")||(currKey == "jet_btags")||(currKey == "jet2_btags"))&&(currItem != "")) // don't save 0 isolation and skip [] lists
		  flags.at(currKey).push_back(atoi(currItem.c_str()));
              fillItem = false;
	      currKey = currItem = "";
          }
	  else if (c == ';') 
	      continue;
	  else
	      fillItem == false ? currKey += c : currItem += c;
      }
    }
    
    
    if(analysis == "atlas_1308_2631") {
      Atlas_1308_2631 a(inputFile, outputFolder, outputPrefix, xsect, xsecterr, branches, flags);
      a.loopOverEvents();
    } 
    else if(analysis == "atlas_conf_2012_104") {
      Atlas_conf_2012_104 a(inputFile, outputFolder, outputPrefix, xsect, xsecterr, branches, flags);
      a.loopOverEvents();
    }
    else if(analysis == "atlas_conf_2012_104_CR") {
      Atlas_conf_2012_104_CR a(inputFile, outputFolder, outputPrefix, xsect, xsecterr, branches, flags);
      a.loopOverEvents();
    }
    else if(analysis == "atlas_conf_2012_147") {
      Atlas_conf_2012_147 a(inputFile, outputFolder, outputPrefix, xsect, xsecterr, branches, flags);
      a.loopOverEvents();
    }
    else if(analysis == "atlas_conf_2012_147_CR") {
      Atlas_conf_2012_147_CR a(inputFile, outputFolder, outputPrefix, xsect, xsecterr, branches, flags);
      a.loopOverEvents();
    }
    else if(analysis == "atlas_conf_2013_024") {
      Atlas_conf_2013_024 a(inputFile, outputFolder, outputPrefix, xsect, xsecterr, branches, flags);
      a.loopOverEvents();
    }
    else if(analysis == "atlas_conf_2013_024_CR") {
      Atlas_conf_2013_024_CR a(inputFile, outputFolder, outputPrefix, xsect, xsecterr, branches, flags);
      a.loopOverEvents();
    }
    else if(analysis == "atlas_conf_2013_035") {
      Atlas_conf_2013_035 a(inputFile, outputFolder, outputPrefix, xsect, xsecterr, branches, flags);
      a.loopOverEvents();
    }
    else if(analysis == "atlas_conf_2013_047") {
      Atlas_conf_2013_047 a(inputFile, outputFolder, outputPrefix, xsect, xsecterr, branches, flags);
      a.loopOverEvents();
    }
    else if(analysis == "atlas_conf_2013_047_CR") {
      Atlas_conf_2013_047_CR a(inputFile, outputFolder, outputPrefix, xsect, xsecterr, branches, flags);
      a.loopOverEvents();
    }
    else if(analysis == "atlas_conf_2013_049") {
      Atlas_conf_2013_049 a(inputFile, outputFolder, outputPrefix, xsect, xsecterr, branches, flags);
      a.loopOverEvents();
    }
    else if(analysis == "atlas_conf_2013_049_CR") {
      Atlas_conf_2013_049_CR a(inputFile, outputFolder, outputPrefix, xsect, xsecterr, branches, flags);
      a.loopOverEvents();
    }
    else if(analysis == "atlas_conf_2013_061") {
      Atlas_conf_2013_061 a(inputFile, outputFolder, outputPrefix, xsect, xsecterr, branches, flags);
      a.loopOverEvents();
    }
    else if(analysis == "atlas_conf_2013_061_CR") {
      Atlas_conf_2013_061_CR a(inputFile, outputFolder, outputPrefix, xsect, xsecterr, branches, flags);
      a.loopOverEvents();
    }
    else if(analysis == "atlas_conf_2013_089") {
      Atlas_conf_2013_089 a(inputFile, outputFolder, outputPrefix, xsect, xsecterr, branches, flags);
      a.loopOverEvents();
    }
    else if(analysis == "atlas_conf_2013_089_CR") {
      Atlas_conf_2013_089_CR a(inputFile, outputFolder, outputPrefix, xsect, xsecterr, branches, flags);
      a.loopOverEvents();
    }
    else if(analysis == "cms_1303_2985") {
      Cms_1303_2985 a(inputFile, outputFolder, outputPrefix, xsect, xsecterr, branches, flags);
      a.loopOverEvents();
    }
    else if(analysis == "cms_1303_2985_CR") {
      Cms_1303_2985_CR a(inputFile, outputFolder, outputPrefix, xsect, xsecterr, branches, flags);
      a.loopOverEvents();
    }
    else if(analysis == "cms_sus_13_016") {
      Cms_sus_13_016 a(inputFile, outputFolder, outputPrefix, xsect, xsecterr, branches, flags);
      a.loopOverEvents();
    }
//@@extracode@@
//      
    else {
    	std::cerr << "Analysis " << analysis << " unknown." << std::endl;
    }
    return 0;
}
