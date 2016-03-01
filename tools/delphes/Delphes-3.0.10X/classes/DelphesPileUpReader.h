#ifndef DelphesPileUpReader_h
#define DelphesPileUpReader_h

/** \class DelphesPileUpReader
 *
 *  Reads pile-up binary file
 *
 *
 *  $Date: 2013-03-08 09:25:30 +0100 (Fri, 08 Mar 2013) $
 *  $Revision: 1046 $
 *
 *
 *  \author P. Demin - UCL, Louvain-la-Neuve
 *
 */

#include <stdio.h>
#include <rpc/types.h>
#include <rpc/xdr.h>

class DelphesPileUpReader
{
public:

  DelphesPileUpReader(const char *fileName);

  ~DelphesPileUpReader();

  bool ReadParticle(int &pid,
    float &x, float &y, float &z, float &t,
    float &px, float &py, float &pz, float &e);

  bool ReadEntry(quad_t entry);

  quad_t GetEntries() const { return fEntries; }

private:

  quad_t fEntries;

  int fEntrySize;
  int fCounter;

  FILE *fPileUpFile;
  char *fIndex;
  char *fBuffer;

  XDR *fInputXDR;
  XDR *fIndexXDR;
  XDR *fBufferXDR;
};

#endif // DelphesPileUpReader_h


