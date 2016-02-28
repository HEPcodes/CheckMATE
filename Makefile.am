ACLOCAL_AMFLAGS = -I m4
SUBDIRS = tools/delphes/Delphes-3.0.10X  tools/analysis
#SUBDIRS = tools/delphes/Delphes-3.0.10X tools/analysis/extra/oxbridgekinetics-0.6 tools/analysis
LD_RUN_PATH = @ROOTLIBDIR@
LD_LIBRARY_PATH = @ROOTLIBDIR@
DYLD_LIBRARY_PATH = @ROOTLIBDIR@
ROOTSYS = @ROOTSYSTEM@
export ROOTSYS
export LD_RUN_PATH
export LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH

all:
	@sed 's,\#!.*,\#!@PYTHON@,' tools/python/CheckMATE.raw > bin/CheckMATE;
	@chmod +x bin/CheckMATE;
	@sed 's,sys\.path\.append.*,sys\.path\.append("@ROOTLIBDIR@"),' tools/python/calculate_cls.py.raw | \
	sed 's,cdll\.LoadLibrary(.*/libCint.so\"),cdll\.LoadLibrary("@ROOTLIBDIR@/libCint.so\"),' | \
	sed 's,cdll\.LoadLibrary(.*/libCore.so\"),cdll\.LoadLibrary("@ROOTLIBDIR@/libCore.so\"),' | \
	sed 's,cdll\.LoadLibrary(.*/libThread.so\"),cdll\.LoadLibrary("@ROOTLIBDIR@/libThread.so\"),' | \
	sed 's,cdll\.LoadLibrary(.*/libRIO.so\"),cdll\.LoadLibrary("@ROOTLIBDIR@/libRIO.so\"),' | \
	sed 's,cdll\.LoadLibrary(.*/libMathCore.so\"),cdll\.LoadLibrary("@ROOTLIBDIR@/libMathCore.so\"),'  | \
	sed 's,cdll\.LoadLibrary(.*/libNet.so\"),cdll\.LoadLibrary("@ROOTLIBDIR@/libNet.so\"),'  | \
	sed 's,cdll\.LoadLibrary(.*/libTree.so\"),cdll\.LoadLibrary("@ROOTLIBDIR@/libTree.so\"),' > tools/python/calculate_cls.py;

AnalysisManager:
	@sed 's,\#!.*,\#!@PYTHON@,' tools/python/AnalysisManager.raw > bin/AnalysisManager;
	@chmod +x bin/AnalysisManager;
   
clean-local:
	-rm -f bin/CheckMATE
	-rm -f bin/AnalysisManager
	-rm -f tools/python/calculate_cls.py
