dnl ##### PYTHIA #####
AC_DEFUN([CHECK_PYTHIA],
[
  AC_MSG_CHECKING([for Pythia8 location])
  PYTHIAINCLUDE=""
  PYTHIALIBS="-lpythia8"
  AC_ARG_WITH(pythia,     
  AC_HELP_STRING([--with-pythia=DIR],[Location of Pythia8 installation]),
    [],
    [with_pythia=no])
  if test "x$with_pythia" = "xno"; then
    AC_MSG_RESULT("not found") 
  else
    AC_MSG_RESULT([$with_pythia])
    PYTHIAINCLUDE=-I$with_pythia/include
    PYTHIALIBS="-L$with_pythia/lib -lpythia8 -ldl -lm -lz"
    PYTHIALIBDIR="$with_pythia/lib"
    PYTHIAXMLDIR="\"$with_pythia/xmldir\""
  fi
  if test "x$with_pythia" != "xno"; then
  # Now lets see if the libraries work properly
    oldLIBS="$LIBS"
    oldLDFLAGS="$LDFLAGS"
    oldCPPFLAGS="$CPPFLAGS"
    LIBS="$LIBS $HEPMCLIBS `echo $PYTHIALIBS | sed -e 's! -R.* ! !'`"
    LDFLAGS="$LDFLAGS"
    CPPFLAGS="$CPPFLAGS $PYTHIAINCLUDE $HEPMCINCLUDE"
    AC_MSG_RESULT([$LDFLAGS])
    # check HepMC
    #AC_MSG_CHECKING([that HepMC works])
    #AC_LINK_IFELSE([AC_LANG_PROGRAM([[#include <HepMC/GenEvent.h>
    #]],[[HepMC::GenEvent();]])],[AC_MSG_RESULT([yes])],[AC_MSG_RESULT([no])
    #AC_MSG_ERROR([Use '--with-hepmc=' to set a path or use '--without-hepmc'.])
    #])               
    AC_CHECK_HEADERS([Pythia8/Pythia.h],[],[AC_MSG_ERROR([Cannot find Pythia header])])
    AM_COND_IF(HAVE_HEPMC, [AC_CHECK_HEADERS([Pythia8Plugins/HepMC2.h],[],[AC_MSG_ERROR([Cannot find Pythia8ToHepMC header])])])
  fi
  AM_CONDITIONAL(HAVE_PYTHIA,[test "x$with_pythia" != "xno"])
  AC_SUBST(PYTHIAINCLUDE)
  AC_SUBST(PYTHIALIBS)
  AC_SUBST(PYTHIALIBDIR)
  # AC_DEFINE_UNQUOTED(PYTHIAXMLDIR, $PYTHIAXMLDIR) Can maybe be useful later
])
