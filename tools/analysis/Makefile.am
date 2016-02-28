AUTOMAKE_OPTIONS = subdir-objects

bin_PROGRAMS = doAnalysis

doAnalysis_SOURCES = src/main.cc \
             src/AnalysisBase.cc include/AnalysisBase.h \
             src/mt2_bisect.cc include/mt2_bisect.h \
	     src/mctlib.cc include/mctlib.h \
   	     src/mt2bl_bisect.cc include/mt2bl_bisect.h

doAnalysis_SOURCES += src/atlas_1210_2979.cc include/atlas_1210_2979.h \
src/atlas_1308_2631_CR.cc src/atlas_1308_2631.cc include/atlas_1308_2631.h \
src/atlas_1402_7029.cc include/atlas_1402_7029.h \
src/atlas_1403_4853.cc include/atlas_1403_4853.h \
src/atlas_1403_5294.cc src/atlas_1403_5294_CR.cc include/atlas_1403_5294.h \
src/atlas_1404_2500.cc include/atlas_1404_2500.h \
src/atlas_1407_0583.cc include/atlas_1407_0583.h \
src/atlas_1407_0600.cc include/atlas_1407_0600.h \
src/atlas_1407_0608.cc include/atlas_1407_0608.h \
src/atlas_conf_2012_104_CR.cc src/atlas_conf_2012_104.cc include/atlas_conf_2012_104.h \
src/atlas_conf_2012_147_CR.cc src/atlas_conf_2012_147.cc include/atlas_conf_2012_147.h \
src/atlas_conf_2013_021.cc include/atlas_conf_2013_021.h \
src/atlas_conf_2013_024_CR.cc src/atlas_conf_2013_024.cc include/atlas_conf_2013_024.h \
src/atlas_conf_2013_031.cc include/atlas_conf_2013_031.h \
src/atlas_conf_2013_035.cc include/atlas_conf_2013_035.h \
src/atlas_conf_2013_036.cc include/atlas_conf_2013_036.h \
src/atlas_conf_2013_037.cc include/atlas_conf_2013_037.h \
src/atlas_conf_2013_047_CR.cc src/atlas_conf_2013_047.cc include/atlas_conf_2013_047.h \
src/atlas_conf_2013_048.cc include/atlas_conf_2013_048.h \
src/atlas_conf_2013_049_CR.cc src/atlas_conf_2013_049.cc include/atlas_conf_2013_049.h \
src/atlas_conf_2013_061_CR.cc src/atlas_conf_2013_061.cc include/atlas_conf_2013_061.h \
src/atlas_conf_2013_089_CR.cc src/atlas_conf_2013_089.cc include/atlas_conf_2013_089.h \
src/atlas_conf_2014_014.cc include/atlas_conf_2014_014.h \
src/atlas_conf_2014_033.cc include/atlas_conf_2014_033.h \
src/cms_1301_4698.cc include/cms_1301_4698.h \
src/cms_1303_2985_CR.cc src/cms_1303_2985.cc include/cms_1303_2985.h \
src/cms_1306_1126_WW.cc include/cms_1306_1126_WW.h \
src/cms_1405_7570.cc include/cms_1405_7570.h \
src/cms_smp_12_006.cc include/cms_smp_12_006.h \
src/cms_sus_12_019.cc include/cms_sus_12_019.h \
src/cms_sus_13_016.cc include/cms_sus_13_016.h 

doAnalysis_CXXFLAGS =  @ROOTCFLAGS@ -Iinclude -I$(abs_top_builddir)/tools/delphes/Delphes-3.0.10X
doAnalysis_LDADD =  -L@ROOTLIBDIR@ @ROOTGLIBS@ @ROOTLIBS@ -L$(abs_top_builddir)/tools/delphes/Delphes-3.0.10X -lEG -lDelphes

LD_RUN_PATH = @ROOTLIBDIR@:$(abs_top_builddir)/tools/delphes/Delphes-3.0.10X
ROOTSYS = @ROOTSYSTEM@
