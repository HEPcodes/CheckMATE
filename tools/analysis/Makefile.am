AUTOMAKE_OPTIONS = subdir-objects

bin_PROGRAMS = doAnalysis

doAnalysis_SOURCES = src/main.cc \
             src/AnalysisBase.cc include/AnalysisBase.h \
             src/mt2_bisect.cc include/mt2_bisect.h \
	     src/mctlib.cc include/mctlib.h \
   	     src/mt2bl_bisect.cc include/mt2bl_bisect.h

doAnalysis_SOURCES += src/atlas_conf_2013_089_CR.cc src/atlas_conf_2013_089.cc include/atlas_conf_2013_089.h src/atlas_conf_2013_047_CR.cc src/atlas_conf_2013_047.cc include/atlas_conf_2013_047.h src/atlas_conf_2012_104_CR.cc src/atlas_conf_2012_104.cc include/atlas_conf_2012_104.h src/cms_1303_2985_CR.cc src/cms_1303_2985.cc include/cms_1303_2985.h src/atlas_conf_2012_147_CR.cc src/atlas_conf_2012_147.cc include/atlas_conf_2012_147.h src/atlas_conf_2013_024_CR.cc src/atlas_conf_2013_024.cc include/atlas_conf_2013_024.h src/atlas_conf_2013_035.cc include/atlas_conf_2013_035.h src/atlas_conf_2013_061_CR.cc src/atlas_conf_2013_061.cc include/atlas_conf_2013_061.h  src/atlas_conf_2013_049_CR.cc src/atlas_conf_2013_049.cc include/atlas_conf_2013_049.h 

doAnalysis_CXXFLAGS =  @ROOTCFLAGS@ -Iinclude -I$(abs_top_builddir)/tools/delphes/Delphes-3.0.10X
doAnalysis_LDADD =  -L@ROOTLIBDIR@ @ROOTGLIBS@ @ROOTLIBS@ -L$(abs_top_builddir)/tools/delphes/Delphes-3.0.10X -lEG -lDelphes

LD_RUN_PATH = @ROOTLIBDIR@:$(abs_top_builddir)/tools/delphes/Delphes-3.0.10X
ROOTSYS = @ROOTSYSTEM@
