#!/usr/bin/env python
import os, sys
import json

if len(sys.argv) < 2:
   exit("Usage: ./translator (file_var.j in old format) (file_var.j in new format)")
   
infile = sys.argv[1]
outfile = sys.argv[2]

injfile = open(infile, "rb")
parameters = json.loads(injfile.read())
injfile.close()
if "version" in parameters and parameters["version"] == 2.0:
   exit(infile+" is newest version already!")

try:
    # Add parameters that did not exist before
    parameters["expectation_known"] = "y"
    parameters["version"] = 2.0
    parameters["author"] = "CheckMATE"
    parameters["authoremail"] = "checkmate@projects.hepforge.org"

    # Remove parameters that should not be there
    if "files" in parameters:
       parameters.pop("files")
    if "CURRLEVEL" in parameters:
       parameters.pop("CURRLEVEL")

    # dict() parameters have to be put as dict()
    for p in parameters:
       if type(parameters[p]) in [type("string"), type(u"string")]:
         if (parameters[p].startswith("[") or parameters[p].startswith("{")):
           parameters[p] = eval(parameters[p])

    # Some integers have to be put as real integers
    parameters["electron_niso"] = int(parameters["electron_niso"])
    parameters["muon_niso"] = int(parameters["muon_niso"])
    parameters["photon_niso"] = int(parameters["photon_niso"])
    if parameters["jets_btagging"] == "y":
      parameters["jets_btagging_n"] = int(parameters["jets_btagging_n"])
except Exception, e:
    print str(e)
    print "Problem with "+infile

jfile = open(outfile, "wb")
jfile.write(json.dumps(parameters, sort_keys=True, indent=2))
jfile.close()

print "Translated "+infile+" successfully!"
