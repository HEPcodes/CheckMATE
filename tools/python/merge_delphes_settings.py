import os
import pickle
import json
import sys
import shutil

from write_delphes_modules import *

def set_by_anyone(analyses, parameters, parameter_of_interest, value):
  for analysis in analyses:
    if parameters[analysis][parameter_of_interest] == value:
      return True
  return False

def save_module_information(function_output, output_file, module_name_list):
  (module_names, module_string) = function_output  
  f = open(output_file, "a")
  f.write(module_string)
  f.write("\n")
  if isinstance(module_names, list):
    for n in module_names:
      module_name_list.append(n)
  else:
    module_name_list.append(module_names)

# Read input parameters for all given analyses
def merge_settings(files, paths):
  parameters = dict()
  analyses = files["delphes_config"].keys()
  for analysis in analyses:
    jfile = open(os.path.join(paths['data'], analysis+"_var.j"), "rb")
    parameters[analysis] = json.loads(jfile.read())
    jfile.close()

  # Remove any existing merge config files
  if os.path.isfile(files['delphes_merged_config']):    
    os.remove(files["delphes_merged_config"])
  all_module_names = []
  
  # It will often be useful to know, which experiments are used
  atlas_used = False
  cms_used = False
  for a in analyses:
    if parameters[a]["experiment"] == "A":
      atlas_used = True
    elif parameters[a]["experiment"] == "C":
      cms_used = True
  
  ##=========================================================
  ## Particle Propagator, Tracking, Smearing and Calorimeter
  ##=========================================================
  ## (This information is set once for every experiment.)

  if atlas_used:
    save_module_information(set_startup_modules("A"), files['delphes_merged_config'], all_module_names)
  if cms_used:
    save_module_information(set_startup_modules("C"), files['delphes_merged_config'], all_module_names)

  #========================================================
  #                Photon Information
#========================================================
  # First determine experiment-dependent output
  # If any other analysis corresponds to a different experiment, print its output separately
  if atlas_used:
    save_module_information(set_photon_efficiency("A"), files['delphes_merged_config'], all_module_names)
  if cms_used:
    save_module_information(set_photon_efficiency("C"), files['delphes_merged_config'], all_module_names)
      
  # Now determine set of isolation criteria:
  # Go through all analyses and all respective criteria
  all_photon_isolation_sets = list()
  all_photon_isolation_lists = dict()
  for a in analyses:
    all_photon_isolation_lists[a] = list()
    for n in range(int(parameters[a]["photon_niso"])):
      # If this particular isolation has already been defined, use it, otherwise define new
      isolation_set = (parameters[a]["experiment"], eval(parameters[a]["photon_iso_source"])[n], eval(parameters[a]["photon_iso_dR"])[n], eval(parameters[a]["photon_iso_ptmin"])[n], eval(parameters[a]["photon_iso_ptratiomax"])[n], eval(parameters[a]["photon_iso_absorrel"])[n])
      same_isolation_found = False
      for i in range(len(all_photon_isolation_sets)):
        if isolation_set == all_photon_isolation_sets[i]:
          all_photon_isolation_lists[a].append(i)
          same_isolation_found = True
      if same_isolation_found == False:
        all_photon_isolation_lists[a].append(len(all_photon_isolation_sets))
        all_photon_isolation_sets.append(isolation_set)
  
  # Create all necessary modules to all isolation sets
  all_photon_isolation_modules = list()
  n_photon_isolation = 0
  for s in all_photon_isolation_sets:
    all_photon_isolation_modules.append(s)
    save_module_information(set_photon_isolation(n_photon_isolation, s), files['delphes_merged_config'], all_module_names)
    n_photon_isolation += 1
  

  #========================================================
  #                Electron Information
  #========================================================
  
  # First determine experiment-dependent output
  if atlas_used:
    save_module_information(set_electron_efficiency("A", "m"), files['delphes_merged_config'], all_module_names)
    save_module_information(set_electron_efficiency("A", "t"), files['delphes_merged_config'], all_module_names)
  if cms_used:
    save_module_information(set_electron_efficiency("C", ""), files['delphes_merged_config'], all_module_names)
  
  # Now determine set of isolation criteria:
  # Go through all analyses and all respective criteria
  all_electron_isolation_sets = list()
  all_electron_isolation_lists = dict()
  for a in analyses:
    all_electron_isolation_lists[a] = list()
    for n in range(int(parameters[a]["electron_niso"])):
      # If this particular isolation has already been defined, use it, otherwise define new
      isolation_set = (parameters[a]["experiment"], eval(parameters[a]["electron_iso_source"])[n], eval(parameters[a]["electron_iso_dR"])[n], eval(parameters[a]["electron_iso_ptmin"])[n], eval(parameters[a]["electron_iso_ptratiomax"])[n], eval(parameters[a]["electron_iso_absorrel"])[n])
      same_isolation_found = False
      for i in range(len(all_electron_isolation_sets)):
        if isolation_set == all_electron_isolation_sets[i]:
          all_electron_isolation_lists[a].append(i)
          same_isolation_found = True
      if same_isolation_found == False:
        all_electron_isolation_lists[a].append(len(all_electron_isolation_sets))
        all_electron_isolation_sets.append(isolation_set)
  
  # Create all necessary modules to all isolation sets
  all_electron_isolation_modules = list()
  n_electron_isolation = 0
  for s in all_electron_isolation_sets:
    all_electron_isolation_modules.append(s)
    save_module_information(set_electron_isolation(n_electron_isolation, s), files['delphes_merged_config'], all_module_names)
    n_electron_isolation += 1
  

  #========================================================
  #                Muon Information
  #========================================================
  
  # First determine experiment-dependent output
  if atlas_used:
    save_module_information(set_muon_efficiency("A", "2c"), files['delphes_merged_config'], all_module_names)
    save_module_information(set_muon_efficiency("A", "2s"), files['delphes_merged_config'], all_module_names)
  if cms_used:
    save_module_information(set_muon_efficiency("C", ""), files['delphes_merged_config'], all_module_names)
  
  # Now determine set of isolation criteria:
  # Go through all analyses and all respective criteria
  all_muon_isolation_sets = list()
  all_muon_isolation_lists = dict()
  for a in analyses:
    all_muon_isolation_lists[a] = list()
    for n in range(int(parameters[a]["muon_niso"])):
      # If this particular isolation has already been defined, use it, otherwise define new
      isolation_set = (parameters[a]["experiment"], eval(parameters[a]["muon_iso_source"])[n], eval(parameters[a]["muon_iso_dR"])[n], eval(parameters[a]["muon_iso_ptmin"])[n], eval(parameters[a]["muon_iso_ptratiomax"])[n], eval(parameters[a]["muon_iso_absorrel"])[n])
      same_isolation_found = False
      for i in range(len(all_muon_isolation_sets)):
        if isolation_set == all_muon_isolation_sets[i]:
          all_muon_isolation_lists[a].append(i)
          same_isolation_found = True
      if same_isolation_found == False:
        all_muon_isolation_lists[a].append(len(all_muon_isolation_sets))
        all_muon_isolation_sets.append(isolation_set)
  
  # Create all necessary modules to all isolation sets
  all_muon_isolation_modules = list()
  n_muon_isolation = 0
  for s in all_muon_isolation_sets:
    all_muon_isolation_modules.append(s)
    save_module_information(set_muon_isolation(n_muon_isolation, s), files['delphes_merged_config'], all_module_names)
    n_muon_isolation += 1
  
  #========================================================
  # Missing ET
  #========================================================
  # There must be one MissingET module for each experiment
  
  if atlas_used:
    save_module_information(set_missingET("A"), files['delphes_merged_config'], all_module_names)
  if cms_used:
    save_module_information(set_missingET("C"), files['delphes_merged_config'], all_module_names)

  #========================================================
  # Jets
  #========================================================
  # GENJETS
  # First determine the smalles minimumpt of a jet that any analysis demands for
  all_fastjet_modules_per_analysis = dict()
  all_secondary_fastjet_modules_per_analysis = dict()
  all_fastjet_modules = list()
  
#  all_genjet_modules_per_analysis = dict()
#  all_genjet_modules = list()
  
#  min_jet_pt = 1E10
#  for a in analyses:
#    if float(parameters[a]["jets_ptmin"]) < min_jet_pt:
#      min_jet_pt = float(parameters[a]["jets_ptmin"])

#  all_jet_dR = []
#  for a in analyses:
#    conedR = parameters[a]["jets_conedR"]
#    all_genjet_modules_per_analysis[a] = "GenJetFinder"+str(conedR).replace(".", "d")
#    if conedR not in all_jet_dR:
#      all_genjet_modules.append("GenJetFinder"+str(conedR).replace(".", "d"))
#      all_jet_dR.append(conedR)
#      save_module_information(set_genjet(conedR, min_jet_pt), files['delphes_merged_config'], all_module_names)

  # ATLAS FASTJET
  min_jet_pt = 1E10
  for a in analyses:
    if parameters[a]["experiment"] == "A":
      if float(parameters[a]["jets_ptmin"]) < min_jet_pt:
        min_jet_pt = float(parameters[a]["jets_ptmin"])

  all_jet_dR = []
  for a in analyses:
    if parameters[a]["experiment"] == "A":
      conedR = parameters[a]["jets_conedR"]
      all_fastjet_modules_per_analysis[a] = "FastJetFinderATLAS"+str(conedR).replace(".", "d")
      if conedR not in all_jet_dR:
        all_jet_dR.append(conedR)
        all_fastjet_modules.append("FastJetFinderATLAS"+str(conedR).replace(".", "d"))
        save_module_information(set_fastjet_and_constituentfilter(conedR, min_jet_pt, "A"), files['delphes_merged_config'], all_module_names)

  # CMS FASTJET
  min_jet_pt = 1E10
  for a in analyses:
    if parameters[a]["experiment"] == "C":
      if float(parameters[a]["jets_ptmin"]) < min_jet_pt:
        min_jet_pt = float(parameters[a]["jets_ptmin"])

  all_jet_dR = []
  for a in analyses:
    if parameters[a]["experiment"] == "C":
      conedR = parameters[a]["jets_conedR"]
      all_fastjet_modules_per_analysis[a] = "FastJetFinderCMS"+str(conedR).replace(".", "d")
      if conedR not in all_jet_dR:
        all_jet_dR.append(conedR)
        all_fastjet_modules.append("FastJetFinderCMS"+str(conedR).replace(".", "d"))
        save_module_information(set_fastjet_and_constituentfilter(conedR, min_jet_pt, "C"), files['delphes_merged_config'], all_module_names)
        
  
  # (if needed) SECOND ATLAS FASTJET  
  min_jet_pt = 1E10
  for a in analyses:
    if parameters[a]["experiment"] == "A" and parameters[a]["jets_second"] == "y":
      if float(parameters[a]["jets_ptmin_second"]) < min_jet_pt:
        min_jet_pt = float(parameters[a]["jets_ptmin_second"])

  all_jet_dR = []
  for a in analyses:
    if parameters[a]["experiment"] == "A" and parameters[a]["jets_second"] == "y":
      conedR = parameters[a]["jets_conedR_second"]
      all_secondary_fastjet_modules_per_analysis[a] = "FastJetFinderATLAS"+str(conedR).replace(".", "d")
      if conedR not in all_jet_dR:
        all_jet_dR.append(conedR)
        all_fastjet_modules.append("FastJetFinderATLAS"+str(conedR).replace(".", "d"))
        save_module_information(set_fastjet_and_constituentfilter(conedR, min_jet_pt, "A"), files['delphes_merged_config'], all_module_names)

  # (if needed) SECOND CMS FASTJET  
  min_jet_pt = 1E10
  for a in analyses:
    if parameters[a]["experiment"] == "C" and parameters[a]["jets_second"] == "y":
      if float(parameters[a]["jets_ptmin_second"]) < min_jet_pt:
        min_jet_pt = float(parameters[a]["jets_ptmin_second"])

  all_jet_dR = []
  for a in analyses:
    if parameters[a]["experiment"] == "C" and parameters[a]["jets_second"] == "y":
      conedR = parameters[a]["jets_conedR_second"]
      all_secondary_fastjet_modules_per_analysis[a] = "FastJetFinderCMS"+str(conedR).replace(".", "d")
      if conedR not in all_jet_dR:
        all_jet_dR.append(conedR)
        all_fastjet_modules.append("FastJetFinderCMS"+str(conedR).replace(".", "d"))
        save_module_information(set_fastjet_and_constituentfilter(conedR, min_jet_pt, "C"), files['delphes_merged_config'], all_module_names)


  
  #======================================
  # Jet Tagging
  #======================================
  # First find out, which b/tau tags are needed for which experiment/dR-jet setting.
  tags_per_jet_module = dict()
  all_jet_btagging_lists = dict()
  all_jet2_btagging_lists = dict()
  
  for m in all_fastjet_modules:
    tags_per_jet_module[m] = list()
    
  for a in analyses:
    all_jet_btagging_lists[a] = list()
    all_jet2_btagging_lists[a] = list()
    jet_module = all_fastjet_modules_per_analysis[a]
    jet_module_2 = ""
    if parameters[a]["jets_second"] == "y":
      jet_module_2 = all_secondary_fastjet_modules_per_analysis[a]
    
    if parameters[a]["jets_btagging"] == "y":
      for b_eff in eval(parameters[a]["jets_btagging_eff"]):
        if ["b", b_eff, parameters[a]["experiment"]] not in tags_per_jet_module[jet_module]:
          tags_per_jet_module[jet_module].append(["b", b_eff, parameters[a]["experiment"]])
          
        # b-flag = index in tag_list (but minus 1 if there is a 't' in the list)
        if ["t", parameters[a]["experiment"]] not in tags_per_jet_module[jet_module]:
          all_jet_btagging_lists[a].append(tags_per_jet_module[jet_module].index(["b", b_eff, parameters[a]["experiment"]]))
        else:
          all_jet_btagging_lists[a].append(tags_per_jet_module[jet_module].index(["b", b_eff, parameters[a]["experiment"]])-1)
          
        if jet_module_2 != "":
          if ["b", b_eff, parameters[a]["experiment"]] not in tags_per_jet_module[jet_module_2]:
            tags_per_jet_module[jet_module_2].append(["b", b_eff, parameters[a]["experiment"]])
          all_jet2_btagging_lists[a].append(tags_per_jet_module[jet_module_2].index(["b", b_eff, parameters[a]["experiment"]]))
          
        
    
    if parameters[a]["jets_tautagging"] == "y" and ["t", parameters[a]["experiment"]] not in tags_per_jet_module[jet_module]:
      tags_per_jet_module[jet_module].append(["t" , parameters[a]["experiment"]])
      
    if jet_module_2 != "" and parameters[a]["jets_tautagging"] == "y" and ["t" , parameters[a]["experiment"]] not in tags_per_jet_module[jet_module_2]:
      tags_per_jet_module[jet_module_2].append(["t" , parameters[a]["experiment"]])
  
  # Now put all jets through their respective flags
  for jet_module in all_fastjet_modules:
    n_bflags = 0
    for tags in tags_per_jet_module[jet_module]:
      if tags[0] == "b":
        save_module_information(set_btagger(jet_module, tags[1], n_bflags), files['delphes_merged_config'], all_module_names)
        n_bflags += 1
      if tags[0] == "t":
        save_module_information(set_tautagger(jet_module, tags[1]), files['delphes_merged_config'], all_module_names)

  #=========================================
  #             TreeWriter
  #=========================================
  # Consequtively try to find all output branches.
  # Also gather all information such that every analysis is connected to 
  # the corresponding modules
  # Syntax: [inputarray] [name of branch] [class of branch items] 
  all_branches = list()
  branches_per_analysis = dict()
  for a in analyses:
    branches_per_analysis[a] = dict()

#  all_branches.append(["Delphes/allParticles", "Particle", "GenParticle"])
#  for m in all_genjet_modules:
#    all_branches.append([m+"/jets", m.replace("Finder", ""), "Jet"])
#  for a in analyses:
#    branches_per_analysis[a]["Particle"] = "Particle"
#    branches_per_analysis[a]["GenJet"] = all_genjet_modules_per_analysis[a].replace("Finder", "")

  for a in analyses:
    experiment_i = parameters[a]["experiment"]
    if experiment_i == "A":
      branches_per_analysis[a]["Track"] = "TrackATLAS"
      branches_per_analysis[a]["Tower"] = "TowerATLAS"
      branches_per_analysis[a]["Photon"] = "PhotonATLAS"
      branches_per_analysis[a]["Electron"] = "ElectronATLAS"
      branches_per_analysis[a]["Muon"] = "MuonATLAS"
      branches_per_analysis[a]["MissingET"] = "MissingETATLAS"
      
    elif experiment_i == "C":
      branches_per_analysis[a]["Track"] = "TrackCMS"
      branches_per_analysis[a]["Tower"] = "TowerCMS"
      branches_per_analysis[a]["Photon"] = "PhotonCMS"
      branches_per_analysis[a]["Electron"] = "ElectronCMS"
      branches_per_analysis[a]["Muon"] = "MuonCMS"
      branches_per_analysis[a]["MissingET"] = "MissingETCMS"
  
  if atlas_used:
    all_branches.append(["TrackMergerATLAS/tracks", "TrackATLAS", "Track"])
    all_branches.append(["CalorimeterATLAS/towers", "TowerATLAS", "Tower"])
    all_branches.append(["CalorimeterATLAS/photons", "PhotonATLAS", "Photon"])
    all_branches.append(["ElectronEnergySmearingATLAS/electrons", "ElectronATLAS", "Electron"])
    all_branches.append(["MuonMomentumSmearingATLAS/muons", "MuonATLAS", "Muon"])
    all_branches.append(["MissingETATLAS/momentum", "MissingETATLAS", "MissingET"])
    
  if cms_used:
    all_branches.append(["TrackMergerCMS/tracks", "TrackCMS", "Track"])
    all_branches.append(["CalorimeterCMS/towers", "TowerCMS", "Tower"])
    all_branches.append(["CalorimeterCMS/photons", "PhotonCMS", "Photon"])
    all_branches.append(["ElectronEnergySmearingCMS/electrons", "ElectronCMS", "Electron"])
    all_branches.append(["MuonMomentumSmearingCMS/muons", "MuonCMS", "Muon"])
    all_branches.append(["MissingETCMS/momentum", "MissingETCMS", "MissingET"])

  for a in analyses:
    branches_per_analysis[a]["Jet"] = all_fastjet_modules_per_analysis[a].replace("Finder", "")
    if parameters[a]["jets_second"] == "y":
      branches_per_analysis[a]["Jet2"] = all_secondary_fastjet_modules_per_analysis[a].replace("Finder", "")

  for m in all_fastjet_modules:
    all_branches.append([m+"/jets", m.replace("Finder", ""), "Jet"])

  save_module_information(set_tree_writer(all_branches), files['delphes_merged_config'], all_module_names)    
  save_module_information(set_execution_path(all_module_names), files['delphes_merged_config'], all_module_names)
  
  flags_per_analysis = dict()
  for a in analyses:
    flags_per_analysis[a] = dict()
    
    flags_per_analysis[a]["electron_isolation"] = list()
    for i in all_electron_isolation_lists[a]:
      flags_per_analysis[a]["electron_isolation"].append(i)
      
    flags_per_analysis[a]["muon_isolation"] = list()
    for i in all_muon_isolation_lists[a]:
      flags_per_analysis[a]["muon_isolation"].append(i)
      
    flags_per_analysis[a]["photon_isolation"] = list()
    for i in all_photon_isolation_lists[a]:
      flags_per_analysis[a]["photon_isolation"].append(i)
    
    flags_per_analysis[a]["jet_btags"] = list()
    for i in all_jet_btagging_lists[a]:
      flags_per_analysis[a]["jet_btags"].append(i)
      
    flags_per_analysis[a]["jet2_btags"] = list()
    for i in all_jet2_btagging_lists[a]:
      flags_per_analysis[a]["jet2_btags"].append(i)
      
    
  
  return (branches_per_analysis, flags_per_analysis, files, paths)
