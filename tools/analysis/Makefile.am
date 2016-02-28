AUTOMAKE_OPTIONS = subdir-objects

bin_PROGRAMS = doAnalysis

doAnalysis_SOURCES = src/main.cc \
             src/base/AnalysisBase.cc include/base/AnalysisBase.h \
             src/base/ETMiss.cc include/base/ETMiss.h \
             src/base/FinalStateObject.cc include/base/FinalStateObject.h \
             src/base/Units.cc include/base/Units.h \
             src/kinematics/mt2_bisect.cc include/kinematics/mt2_bisect.h \
             src/kinematics/mctlib.cc include/kinematics/mctlib.h \
             src/kinematics/mt2bl_bisect.cc include/kinematics/mt2bl_bisect.h

doAnalysis_SOURCES +=  src/analyses/atlas_1210_2979.cc include/analyses/atlas_1210_2979.h \
src/analyses/atlas_1308_1841.cc include/analyses/atlas_1308_1841.h \
src/analyses/atlas_1308_2631_CR.cc src/analyses/atlas_1308_2631.cc include/analyses/atlas_1308_2631.h \
src/analyses/atlas_1402_7029.cc include/analyses/atlas_1402_7029.h \
src/analyses/atlas_1403_4853.cc include/analyses/atlas_1403_4853.h \
src/analyses/atlas_1403_5222.cc include/analyses/atlas_1403_5222.h \
src/analyses/atlas_1403_5294.cc src/analyses/atlas_1403_5294_CR.cc include/analyses/atlas_1403_5294.h \
src/analyses/atlas_1404_2500.cc include/analyses/atlas_1404_2500.h \
src/analyses/atlas_1405_7875.cc include/analyses/atlas_1405_7875.h \
src/analyses/atlas_1407_0583.cc include/analyses/atlas_1407_0583.h \
src/analyses/atlas_1407_0600.cc include/analyses/atlas_1407_0600.h \
src/analyses/atlas_1407_0608.cc include/analyses/atlas_1407_0608.h \
src/analyses/atlas_1502_01518.cc include/analyses/atlas_1502_01518.h \
src/analyses/atlas_1503_03290.cc include/analyses/atlas_1503_03290.h \
 src/analyses/atlas_1506_08616.cc include/analyses/atlas_1506_08616.h \
src/analyses/atlas_conf_2012_104_CR.cc src/analyses/atlas_conf_2012_104.cc include/analyses/atlas_conf_2012_104.h \
src/analyses/atlas_conf_2012_147_CR.cc src/analyses/atlas_conf_2012_147.cc include/analyses/atlas_conf_2012_147.h \
src/analyses/atlas_conf_2013_021.cc include/analyses/atlas_conf_2013_021.h \
src/analyses/atlas_conf_2013_024_CR.cc src/analyses/atlas_conf_2013_024.cc include/analyses/atlas_conf_2013_024.h \
src/analyses/atlas_conf_2013_031.cc include/analyses/atlas_conf_2013_031.h \
src/analyses/atlas_conf_2013_035.cc include/analyses/atlas_conf_2013_035.h \
src/analyses/atlas_conf_2013_036.cc include/analyses/atlas_conf_2013_036.h \
src/analyses/atlas_conf_2013_037.cc include/analyses/atlas_conf_2013_037.h \
src/analyses/atlas_conf_2013_047_CR.cc src/analyses/atlas_conf_2013_047.cc include/analyses/atlas_conf_2013_047.h \
src/analyses/atlas_conf_2013_048.cc include/analyses/atlas_conf_2013_048.h \
src/analyses/atlas_conf_2013_049_CR.cc src/analyses/atlas_conf_2013_049.cc include/analyses/atlas_conf_2013_049.h \
src/analyses/atlas_conf_2014_056.cc include/analyses/atlas_conf_2014_056.h \
src/analyses/atlas_conf_2013_061_CR.cc src/analyses/atlas_conf_2013_061.cc include/analyses/atlas_conf_2013_061.h \
src/analyses/atlas_conf_2013_062.cc include/analyses/atlas_conf_2013_062.h \
src/analyses/atlas_conf_2013_089_CR.cc src/analyses/atlas_conf_2013_089.cc include/analyses/atlas_conf_2013_089.h \
src/analyses/atlas_conf_2014_014.cc include/analyses/atlas_conf_2014_014.h \
src/analyses/atlas_conf_2014_033.cc include/analyses/atlas_conf_2014_033.h \
src/analyses/cms_1301_4698_WW.cc include/analyses/cms_1301_4698_WW.h \
src/analyses/cms_1303_2985_CR.cc src/analyses/cms_1303_2985.cc include/analyses/cms_1303_2985.h \
src/analyses/cms_1306_1126_WW.cc include/analyses/cms_1306_1126_WW.h \
src/analyses/cms_1405_7570.cc include/analyses/cms_1405_7570.h \
src/analyses/cms_1502_06031.cc include/analyses/cms_1502_06031.h \
src/analyses/cms_smp_12_006.cc include/analyses/cms_smp_12_006.h \
src/analyses/cms_sus_12_019.cc include/analyses/cms_sus_12_019.h \
src/analyses/cms_sus_13_016.cc include/analyses/cms_sus_13_016.h 

#commented by liang at 10/6/2015
#doAnalysis_CXXFLAGS =  @ROOTCFLAGS@ -Iinclude/base -Iinclude/kinematics -Iinclude/analyses -I$(abs_top_builddir)/tools/delphes/Delphes-3.0.10X
#codes by liang at 10/6/2015
doAnalysis_CXXFLAGS =  @ROOTCFLAGS@ -Iinclude/base -Iinclude/kinematics -Iinclude/analyses -I$(abs_top_builddir)/tools/delphes/Delphes-3.0.10X -I$(abs_top_builddir)/tools/delphes/Delphes-3.0.10X/external

doAnalysis_LDADD =  -L@ROOTLIBDIR@ @ROOTGLIBS@ @ROOTLIBS@ -L$(abs_top_builddir)/tools/delphes/Delphes-3.0.10X -lEG -lDelphes

LD_RUN_PATH = @ROOTLIBDIR@:$(abs_top_builddir)/tools/delphes/Delphes-3.0.10X
ROOTSYS = @ROOTSYSTEM@
