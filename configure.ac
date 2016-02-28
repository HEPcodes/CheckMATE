#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.63])
AC_INIT(CheckMATE, 1.2.0, daschm@uni-bonn.de)
AM_INIT_AUTOMAKE
# Checks for programs.
AC_PROG_CXX

# Checks for libraries.
# first command allows for --with-python but doesn't check the version. This is why we have two checks.
PY_PROG_PYTHON([2.7.3], ,AC_MSG_ERROR(You need Python 2.7.3+ to run CheckMATE. Use --with-python and refer to a valid python binary.) )
AM_PATH_PYTHON([2.7.3], ,AC_MSG_ERROR(You need Python 2.7.3+ to run CheckMATE. Use --with-python and refer to a valid python binary.) )
ROOT_PATH([5.20], , AC_MSG_ERROR(ROOT could not be initialised. Try using --with-rootsys and check whether you have ver. 5.34/06 or newer.))
ROOT_FEATURE(python, ,AC_MSG_ERROR(ROOT could be initialised but apparently it has been configured without Python functionality. Checkout the manual to find out how to add it.))
ROOT_FEATURE(minuit2, ,AC_MSG_ERROR(ROOT could be initialised but apparently it has been configured without Minuit2 functionality. Checkout the manual to find out how to add it.))
ROOT_FEATURE(roofit, ,AC_MSG_ERROR(ROOT could be initialised but apparently it has been configured without RooFit functionality. Checkout the manual to find out how to add it.))
AC_SUBST(ROOTSYS)

# Checks for header files.

# Checks for typedefs, structures, and compiler characteristics.

# Checks for library functions.

#AC_CONFIG_SUBDIRS([tools/delphes/Delphes-3.0.10X
#                   tools/analysis/extra/oxbridgekinetics-0.6])
 
AC_CONFIG_SUBDIRS([tools/delphes/Delphes-3.0.10X])
                   
AC_CONFIG_FILES([Makefile
                 tools/analysis/Makefile])
AC_OUTPUT
AC_MSG_RESULT([=== Subconfigurations Done ===])
AC_MSG_RESULT([Configuration of CheckMATE finished. Run 'make' to compile. If you have more than one core, you can use -j2 or even -j4 to speed up the compilation process. Note that you don't have to run 'make install' afterwards.])
