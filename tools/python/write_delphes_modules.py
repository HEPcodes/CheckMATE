def set_startup_modules(experiment):
  module_string = set_particle_propagator(experiment)[1] + set_tracking_efficiencies(experiment)[1] + set_smearing(experiment)[1] +  set_track_merger(experiment)[1] +  set_calorimeter(experiment)[1] +  set_eflow_merger(experiment)[1]
  module_names = [set_particle_propagator(experiment)[0]] + set_tracking_efficiencies(experiment)[0] + set_smearing(experiment)[0] +  [set_track_merger(experiment)[0]] +  [set_calorimeter(experiment)[0]] +  [set_eflow_merger(experiment)[0]]
  return (module_names, module_string)

def set_particle_propagator(experiment):
  module_string = ""
  module_name = ""
  if experiment == "A":
    module_name = "ParticlePropagatorATLAS"
    module_string = """
module ParticlePropagator ParticlePropagatorATLAS {
  set InputArray Delphes/stableParticles
  set OutputArray stableParticles
  set ChargedHadronOutputArray chargedHadrons
  set ElectronOutputArray electrons
  set MuonOutputArray muons
  
  set Radius 1.15
  set HalfLength 3.51
  set Bz 2.0
}
"""
  elif experiment == "C":
    module_name = "ParticlePropagatorCMS"
    module_string = """
module ParticlePropagator ParticlePropagatorCMS {
  set InputArray Delphes/stableParticles
  set OutputArray stableParticles
  set ChargedHadronOutputArray chargedHadrons
  set ElectronOutputArray electrons
  set MuonOutputArray muons
  
  set Radius 1.29
  set HalfLength 3.00
  set Bz 3.8
}
"""
  else:
    exit("Error: Experiment "+experiment+" not known.")
  return (module_name, module_string)

def set_tracking_efficiencies(experiment):
  module_string = ""
  module_name = ""
  if experiment == "A":
    module_names = ["ChargedHadronTrackingEfficiencyATLAS", "ElectronTrackingEfficiencyATLAS", "MuonTrackingEfficiencyATLAS"]
    module_string = """
module Efficiency ChargedHadronTrackingEfficiencyATLAS {
  set InputArray ParticlePropagatorATLAS/chargedHadrons
  set OutputArray chargedHadrons

  set EfficiencyFormula {                                                    (pt <= 0.1)   * (0.00) + \
                                           (abs(eta) <= 1.5) * (pt > 0.1   && pt <= 1.0)   * (0.70) + \
                                           (abs(eta) <= 1.5) * (pt > 1.0)                  * (0.95) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 0.1   && pt <= 1.0)   * (0.60) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 1.0)                  * (0.85) + \
                         (abs(eta) > 2.5)                                                  * (0.00)}
}

module Efficiency ElectronTrackingEfficiencyATLAS {
  set InputArray ParticlePropagatorATLAS/electrons
  set OutputArray electrons

  set EfficiencyFormula {                                                    (pt <= 0.1)   * (0.00) + \
                                           (abs(eta) <= 1.5) * (pt > 0.1   && pt <= 1.0)   * (0.73) + \
                                           (abs(eta) <= 1.5) * (pt > 1.0   && pt <= 1.0e2) * (0.95) + \
                                           (abs(eta) <= 1.5) * (pt > 1.0e2)                * (0.99) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 0.1   && pt <= 1.0)   * (0.50) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 1.0   && pt <= 1.0e2) * (0.83) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 1.0e2)                * (0.90) + \
                         (abs(eta) > 2.5)                                                  * (0.00)}
}

module Efficiency MuonTrackingEfficiencyATLAS {
  set InputArray ParticlePropagatorATLAS/muons
  set OutputArray muons

  set EfficiencyFormula {                                                    (pt <= 0.1)   * (0.00) + \
                                           (abs(eta) <= 1.5) * (pt > 0.1   && pt <= 1.0)   * (0.75) + \
                                           (abs(eta) <= 1.5) * (pt > 1.0)                  * (0.99) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 0.1   && pt <= 1.0)   * (0.70) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 1.0)                  * (0.98) + \
                         (abs(eta) > 2.5)                                                  * (0.00)}
}
"""
  elif experiment == "C":
    module_names = ["ChargedHadronTrackingEfficiencyCMS", "ElectronTrackingEfficiencyCMS", "MuonTrackingEfficiencyCMS"]
    module_string = """
module Efficiency ChargedHadronTrackingEfficiencyCMS {
  set InputArray ParticlePropagatorCMS/chargedHadrons
  set OutputArray chargedHadrons

  # add EfficiencyFormula {efficiency formula as a function of eta and pt}

  # tracking efficiency formula for charged hadrons
  set EfficiencyFormula {                                                    (pt <= 0.1)   * (0.00) + \
                                           (abs(eta) <= 1.5) * (pt > 0.1   && pt <= 1.0)   * (0.70) + \
                                           (abs(eta) <= 1.5) * (pt > 1.0)                  * (0.95) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 0.1   && pt <= 1.0)   * (0.60) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 1.0)                  * (0.85) + \
                         (abs(eta) > 2.5)                                                  * (0.00)}
}
module Efficiency ElectronTrackingEfficiencyCMS {
  set InputArray ParticlePropagatorCMS/electrons
  set OutputArray electrons

  set EfficiencyFormula {                                                    (pt <= 0.1)   * (0.00) + \
                                           (abs(eta) <= 1.5) * (pt > 0.1   && pt <= 1.0)   * (0.73) + \
                                           (abs(eta) <= 1.5) * (pt > 1.0   && pt <= 1.0e2) * (0.95) + \
                                           (abs(eta) <= 1.5) * (pt > 1.0e2)                * (0.99) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 0.1   && pt <= 1.0)   * (0.50) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 1.0   && pt <= 1.0e2) * (0.83) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 1.0e2)                * (0.90) + \
                         (abs(eta) > 2.5)                                                  * (0.00)}
}

module Efficiency MuonTrackingEfficiencyCMS {
  set InputArray ParticlePropagatorCMS/muons
  set OutputArray muons

  set EfficiencyFormula {                                                    (pt <= 0.1)   * (0.00) + \
                                           (abs(eta) <= 1.5) * (pt > 0.1   && pt <= 1.0)   * (0.75) + \
                                           (abs(eta) <= 1.5) * (pt > 1.0)                  * (0.99) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 0.1   && pt <= 1.0)   * (0.70) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 1.0)                  * (0.98) + \
                         (abs(eta) > 2.5)                                                  * (0.00)}
}

"""
  else:
    exit("Error: Experiment "+experiment+" not known.")
  return (module_names, module_string)

def set_smearing(experiment):
  
  # Muon Fit parameters (We thank Florian Jetter for providing these)
  
  # Momentum for transition of low momentum ATLAS reconstruction to Z' invariant mass shape fit.
  trans=100.0
  
  # Fit to Z' invariant mass distribution at masses 1.5TeV and 2.5TeV CERN-PH-EP-2014-053, arXiv:1405.4123v2 
  # Linear fit. Parameters a,d,g,l not used, e.g. b + c * pt

  # Eta<1.05
  a = 0
  b = -0.0193760449145
  c = 0.000323217527579
  # 1.05 < Eta < 2.0
  d = 0
  e = -0.00375088921447
  f = 0.000318372382021
  # Eta > 2.0
  g = 0
  h = -0.0142181617427
  k = 0.000265583078347
  

  # Weight to apply to ID/MS detector resolution: weight * ID + (1-weight) * MS
  weight = 0.77606210482

  
  # ATLAS Muon reconstruction CERN-PH-EP-2014-151
  # Pseudoexperiments with Eq(9) to create gaussian and thus sigma/pt
  # Fit to:  sqrt(a/pt**2 + b + c pt**2)

  # ID Detector
  #  Eta<1.05
  atlas_ID_a = 0.0162922778815	
  atlas_ID_b = 3.98210232503e-05	
  atlas_ID_c = 2.04874310022e-08
  # 1.05 < Eta < 2.0
  atlas_ID_d = 1.60216481783e-06
  atlas_ID_e = 0.000104210453477
  atlas_ID_f = 8.4293604369e-08
  # 2.0 < Eta
  atlas_ID_g = 4.14162127826e-05	
  atlas_ID_h = 4.71002561732e-05	
  atlas_ID_i = 7.36887029151e-09

  # MS Detector
  atlas_MS_a = 1.38828212398e-05	
  atlas_MS_b = 1.15840050992e-05	
  atlas_MS_c = 1.03517299177e-11

  atlas_MS_d = 0.00102757703667	
  atlas_MS_e = 0.000350143367228	
  atlas_MS_f = 1.92312928027e-10

  atlas_MS_g = 0.000129262858873	
  atlas_MS_h = 0.000289554742539	
  atlas_MS_i = 1.26545113277e-12
  
  params = {
    'trans' : str(trans),
    'weight' : str(weight),
    'a' : str(a), 
    'b' : str(b), 
    'c' : str(c), 
    'd' : str(d),
    'e' : str(e),
    'f' : str(f),
    'g' : str(g),
    'h' : str(h),
    'k' : str(k),
    'atlas_ID_a' : str(atlas_ID_a),
    'atlas_ID_b' : str(atlas_ID_b),
    'atlas_ID_c' : str(atlas_ID_c),
    'atlas_ID_d' : str(atlas_ID_d),
    'atlas_ID_e' : str(atlas_ID_e),
    'atlas_ID_f' : str(atlas_ID_f),
    'atlas_ID_g' : str(atlas_ID_g),
    'atlas_ID_h' : str(atlas_ID_h),
    'atlas_ID_i' : str(atlas_ID_i),
    'atlas_MS_a' : str(atlas_MS_a),
    'atlas_MS_b' : str(atlas_MS_b),
    'atlas_MS_c' : str(atlas_MS_c),
    'atlas_MS_d' : str(atlas_MS_d),
    'atlas_MS_e' : str(atlas_MS_e),
    'atlas_MS_f' : str(atlas_MS_f),
    'atlas_MS_g' : str(atlas_MS_g),
    'atlas_MS_h' : str(atlas_MS_h),
    'atlas_MS_i' : str(atlas_MS_i)
    }

  module_string = ""
  if experiment == "A":
    module_names = ["ChargedHadronMomentumSmearingATLAS", "ElectronEnergySmearingATLAS", "MuonMomentumSmearingATLAS"] 
    module_string = """
module MomentumSmearing ChargedHadronMomentumSmearingATLAS {
  set InputArray ChargedHadronTrackingEfficiencyATLAS/chargedHadrons
  set OutputArray chargedHadrons

  set ResolutionFormula {                  (abs(eta) <= 1.5) * (pt > 0.1   && pt <= 1.0)   * (0.02) + \\
                                           (abs(eta) <= 1.5) * (pt > 1.0   && pt <= 1.0e1) * (0.01) + \\
                                           (abs(eta) <= 1.5) * (pt > 1.0e1 && pt <= 2.0e2) * (0.03) + \\
                                           (abs(eta) <= 1.5) * (pt > 2.0e2)                * (0.05) + \\
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 0.1   && pt <= 1.0)   * (0.03) + \\
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 1.0   && pt <= 1.0e1) * (0.02) + \\
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 1.0e1 && pt <= 2.0e2) * (0.04) + \\
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 2.0e2)                * (0.05)}
}

module EnergySmearing ElectronEnergySmearingATLAS {
  set InputArray ElectronTrackingEfficiencyATLAS/electrons
  set OutputArray electrons

  set ResolutionFormula { \\
     (abs(eta)< 0.1)*energy*sqrt(pow(0.09372/sqrt(energy), 2) + pow(0.012, 2))+ \\
     (abs(eta)>= 0.1)*(abs(eta)< 0.2) * energy*sqrt(pow(0.09555/sqrt(energy), 2) + pow(0.012, 2))+ \\
     (abs(eta)>= 0.2)*(abs(eta)< 0.3) * energy*sqrt(pow(0.09622/sqrt(energy), 2) + pow(0.012, 2))+ \\
     (abs(eta)>= 0.3)*(abs(eta)< 0.4) * energy*sqrt(pow(0.10007/sqrt(energy), 2) + pow(0.012, 2))+ \\
     (abs(eta)>= 0.4)*(abs(eta)< 0.5) * energy*sqrt(pow(0.10707/sqrt(energy), 2) + pow(0.012, 2))+ \\
     (abs(eta)>= 0.5)*(abs(eta)< 0.6) * energy*sqrt(pow(0.11536/sqrt(energy), 2) + pow(0.012, 2))+ \\
     (abs(eta)>= 0.6)*(abs(eta)< 0.7) * energy*sqrt(pow(0.12471/sqrt(energy), 2) + pow(0.012, 2))+ \\
     (abs(eta)>= 0.7)*(abs(eta)< 0.8) * energy*sqrt(pow(0.13641/sqrt(energy), 2) + pow(0.012, 2))+ \\
     (abs(eta)>= 0.8)*(abs(eta)< 0.9) * energy*sqrt(pow(0.15039/sqrt(energy), 2) + pow(0.012, 2))+ \\
     (abs(eta)>= 0.9)*(abs(eta)< 1.0) * energy*sqrt(pow(0.16067/sqrt(energy), 2) + pow(0.012, 2))+ \\
     (abs(eta)>= 1.0)*(abs(eta)< 1.1) * energy*sqrt(pow(0.17159/sqrt(energy), 2) + pow(0.012, 2))+ \\
     (abs(eta)>= 1.1)*(abs(eta)< 1.2) * energy*sqrt(pow(0.18019/sqrt(energy), 2) + pow(0.012, 2))+ \\
     (abs(eta)>= 1.2)*(abs(eta)< 1.3) * energy*sqrt(pow(0.19383/sqrt(energy), 2) + pow(0.012, 2))+ \\
     (abs(eta)>= 1.3)*(abs(eta)< 1.37) * energy*sqrt(pow(0.21058/sqrt(energy), 2) + pow(0.012, 2))+ \\
     (abs(eta)>= 1.37)*(abs(eta)< 1.6) * energy*sqrt(pow(0.22071/sqrt(energy), 2) + pow(0.018, 2))+ \\
     (abs(eta)>= 1.6)*(abs(eta)< 1.7) * energy*sqrt(pow(0.19193/sqrt(energy), 2) + pow(0.018, 2))+ \\
     (abs(eta)>= 1.7)*(abs(eta)< 1.8) * energy*sqrt(pow(0.18400/sqrt(energy), 2) + pow(0.018, 2))+ \\
     (abs(eta)>= 1.8)*(abs(eta)< 1.9) * energy*sqrt(pow(0.16564/sqrt(energy), 2) + pow(0.018, 2))+ \\
     (abs(eta)>= 1.9)*(abs(eta)< 2.0) * energy*sqrt(pow(0.16168/sqrt(energy), 2) + pow(0.018, 2))+ \\
     (abs(eta)>= 2.0)*(abs(eta)< 2.1) * energy*sqrt(pow(0.16049/sqrt(energy), 2) + pow(0.018, 2))+ \\
     (abs(eta)>= 2.1)*(abs(eta)< 2.2) * energy*sqrt(pow(0.16759/sqrt(energy), 2) + pow(0.018, 2))+ \\
     (abs(eta)>= 2.2)*(abs(eta)< 2.3) * energy*sqrt(pow(0.16665/sqrt(energy), 2) + pow(0.018, 2))+ \\
     (abs(eta)>= 2.3)*(abs(eta)< 2.4) * energy*sqrt(pow(0.16665/sqrt(energy), 2) + pow(0.018, 2))+ \\
     (abs(eta)>= 2.4)* energy*sqrt(pow(0.16665/sqrt(energy), 2) + pow(0.018, 2))}
}

module MomentumSmearing MuonMomentumSmearingATLAS {
  set InputArray MuonTrackingEfficiencyATLAS/muons
  set OutputArray muons

  set ResolutionFormula {(pt>%(trans)s)*(\\
  (eta <= 1.05) * (pt>%(trans)s)*(%(b)s + %(c)s * pt) +\\
  (eta > 1.05) * \\
  (eta <= 2.0) * (pt>%(trans)s)*(%(e)s + %(f)s * pt ) +\\
  (eta > 2.0 ) * (pt>%(trans)s)*(%(h)s + %(k)s * pt) \\
  )+ \\
  (pt <= %(trans)s) * (\\
  %(weight)s* (
  (eta <= 1.05) * sqrt(%(atlas_ID_a)s/pow(pt,2) + %(atlas_ID_b)s + %(atlas_ID_c)s * pow(pt,2)) +\\
  (eta > 1.05) * (eta <= 2.0) * sqrt(%(atlas_ID_d)s/pow(pt,2) + %(atlas_ID_e)s + %(atlas_ID_f)s * pow(pt,2))  +\\
  (eta > 2.0 ) * sqrt(%(atlas_ID_g)s/pow(pt,2) + %(atlas_ID_h)s + %(atlas_ID_i)s * pow(pt,2)) \\
  ) + \\
  (1 - %(weight)s) * (\\
  (eta <= 1.05) * sqrt(%(atlas_MS_a)s/pow(pt,2) + %(atlas_MS_b)s + %(atlas_MS_c)s * pow(pt,2)) +\\
  (eta > 1.05) * (eta <= 2.0) * sqrt(%(atlas_MS_d)s/pow(pt,2) + %(atlas_MS_e)s + %(atlas_MS_f)s * pow(pt,2))  +\\
  (eta > 2.0 ) * sqrt(%(atlas_MS_g)s/pow(pt,2) + %(atlas_MS_h)s + %(atlas_MS_i)s * pow(pt,2))
)\\
)
}
}
"""%params 
  elif experiment == "C":
    module_names = ["ChargedHadronMomentumSmearingCMS", "ElectronEnergySmearingCMS", "MuonMomentumSmearingCMS"]
    module_string = """
module MomentumSmearing ChargedHadronMomentumSmearingCMS {
  set InputArray ChargedHadronTrackingEfficiencyCMS/chargedHadrons
  set OutputArray chargedHadrons

  set ResolutionFormula {                  (abs(eta) <= 1.5) * (pt > 0.1   && pt <= 1.0)   * (0.02) + \
                                           (abs(eta) <= 1.5) * (pt > 1.0   && pt <= 1.0e1) * (0.01) + \
                                           (abs(eta) <= 1.5) * (pt > 1.0e1 && pt <= 2.0e2) * (0.03) + \
                                           (abs(eta) <= 1.5) * (pt > 2.0e2)                * (0.05) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 0.1   && pt <= 1.0)   * (0.03) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 1.0   && pt <= 1.0e1) * (0.02) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 1.0e1 && pt <= 2.0e2) * (0.04) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 2.0e2)                * (0.05)}
}

module EnergySmearing ElectronEnergySmearingCMS {
  set InputArray ElectronTrackingEfficiencyCMS/electrons
  set OutputArray electrons

  set ResolutionFormula {                  (abs(eta) <= 2.5) * (energy > 0.1   && energy <= 2.5e1) * (energy*0.015) + \
                                           (abs(eta) <= 2.5) * (energy > 2.5e1)                    * sqrt(energy^2*0.005^2 + energy*0.05^2 + 0.25^2) + \
                         (abs(eta) > 2.5 && abs(eta) <= 3.0)                                       * sqrt(energy^2*0.005^2 + energy*0.05^2 + 0.25^2) + \
                         (abs(eta) > 3.0 && abs(eta) <= 5.0)                                       * sqrt(energy^2*0.107^2 + energy*2.08^2)}
}

module MomentumSmearing MuonMomentumSmearingCMS {
  set InputArray MuonTrackingEfficiencyCMS/muons
  set OutputArray muons

  set ResolutionFormula {                  (abs(eta) <= 1.5) * (pt > 0.1   && pt <= 1.0)   * (0.03) + \
                                           (abs(eta) <= 1.5) * (pt > 1.0   && pt <= 1.0e1) * (0.02) + \
                                           (abs(eta) <= 1.5) * (pt > 1.0e1 && pt <= 2.0e2) * (0.03) + \
                                           (abs(eta) <= 1.5) * (pt > 2.0e2)                * (0.05) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 0.1   && pt <= 1.0)   * (0.04) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 1.0   && pt <= 1.0e1) * (0.03) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 1.0e1 && pt <= 2.0e2) * (0.04) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 2.0e2)                * (0.05)}
}
"""
  else:
    exit("Error: Experiment "+experiment+" not known.")
  return (module_names, module_string)

def set_track_merger(experiment):
  module_name = ""
  module_string = ""
  if experiment == "A":
    module_name = "TrackMergerATLAS"
    module_string = """
module Merger TrackMergerATLAS {
  add InputArray ChargedHadronMomentumSmearingATLAS/chargedHadrons
  add InputArray ElectronEnergySmearingATLAS/electrons
  set OutputArray tracks
}
    """
  elif experiment == "C":
    module_name = "TrackMergerCMS"
    module_string = """
module Merger TrackMergerCMS {
  add InputArray ChargedHadronMomentumSmearingCMS/chargedHadrons
  add InputArray ElectronEnergySmearingCMS/electrons
  set OutputArray tracks
}
    """
  else:
    exit("Error: Experiment "+experiment+" not known.")
  return (module_name, module_string)

def set_calorimeter(experiment):
  module_name = ""
  module_string = ""
  if experiment == "A":
    module_name = "CalorimeterATLAS"
    module_string = """
module Calorimeter CalorimeterATLAS {
  set ParticleInputArray ParticlePropagatorATLAS/stableParticles
  set TrackInputArray TrackMergerATLAS/tracks
  set TowerOutputArray towers
  set PhotonOutputArray photons
  set EFlowTrackOutputArray eflowTracks
  set EFlowTowerOutputArray eflowTowers
  
  set pi [expr {acos(-1)}]
  set PhiBins {}
  for {set i -18} {$i <= 18} {incr i} {
    add PhiBins [expr {$i * $pi/18.0}]
  }
  foreach eta {-3.2 -2.5 -2.4 -2.3 -2.2 -2.1 -2 -1.9 -1.8 -1.7 -1.6 -1.5 -1.4 -1.3 -1.2 -1.1 -1 -0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2 2.1 2.2 2.3 2.4 2.5 2.6 3.3} {
    add EtaPhiBins $eta $PhiBins
  }
  set PhiBins {}
  for {set i -9} {$i <= 9} {incr i} {
    add PhiBins [expr {$i * $pi/9.0}]
  }
  foreach eta {-4.9 -4.7 -4.5 -4.3 -4.1 -3.9 -3.7 -3.5 -3.3 -3 -2.8 -2.6 2.8 3 3.2 3.5 3.7 3.9 4.1 4.3 4.5 4.7 4.9} {
    add EtaPhiBins $eta $PhiBins
  }
  add EnergyFraction {0} {0.0 1.0}
  add EnergyFraction {11} {1.0 0.0}
  add EnergyFraction {22} {1.0 0.0}
  add EnergyFraction {111} {1.0 0.0}
  add EnergyFraction {12} {0.0 0.0}
  add EnergyFraction {13} {0.0 0.0}
  add EnergyFraction {14} {0.0 0.0}
  add EnergyFraction {16} {0.0 0.0}
  add EnergyFraction {1000012} {0.0 0.0}
  add EnergyFraction {5000012} {0.0 0.0}
  add EnergyFraction {1000022} {0.0 0.0}
  add EnergyFraction {1000023} {0.0 0.0}
  add EnergyFraction {1000025} {0.0 0.0}
  add EnergyFraction {1000035} {0.0 0.0}
  add EnergyFraction {1000039} {0.0 0.0}
  add EnergyFraction {1000045} {0.0 0.0}
  add EnergyFraction {310} {0.3 0.7}
  add EnergyFraction {3122} {0.3 0.7}
  set ECalResolutionFormula {                  (abs(eta) <= 3.2) * sqrt(energy^2*0.0017^2 + energy*0.101^2) + \
                             (abs(eta) > 3.2 && abs(eta) <= 4.9) * sqrt(energy^2*0.0350^2 + energy*0.285^2)}
  set HCalResolutionFormula {                  (abs(eta) <= 1.7) * sqrt(energy^2*0.0302^2 + energy*0.5205^2+1.59^2) + \
                             (abs(eta) > 1.7 && abs(eta) <= 3.2) * sqrt(energy^2*0.0500^2 + energy*0.706^2) + \
                             (abs(eta) > 3.2 && abs(eta) <= 4.9) * sqrt(energy^2*0.09420^2 + energy*0.075^2)}
}
    """
  elif experiment == "C":
    module_name = "CalorimeterCMS"
    module_string = """
module Calorimeter CalorimeterCMS {
  set ParticleInputArray ParticlePropagatorCMS/stableParticles
  set TrackInputArray TrackMergerCMS/tracks
  set TowerOutputArray towers
  set PhotonOutputArray photons
  set EFlowTrackOutputArray eflowTracks
  set EFlowTowerOutputArray eflowTowers
  
  set pi [expr {acos(-1)}]
  set PhiBins {}
  for {set i -36} {$i <= 36} {incr i} {
    add PhiBins [expr {$i * $pi/36.0}]
  }
  foreach eta {-1.566 -1.479 -1.392 -1.305 -1.218 -1.131 -1.044 -0.957 -0.87 -0.783 -0.696 -0.609 -0.522 -0.435 -0.348 -0.261 -0.174 -0.087 0 0.087 0.174 0.261 0.348 0.435 0.522 0.609 0.696 0.783 0.87 0.957 1.044 1.131 1.218 1.305 1.392 1.479 1.566 1.653} {
    add EtaPhiBins $eta $PhiBins
  }
  set PhiBins {}
  for {set i -18} {$i <= 18} {incr i} {
    add PhiBins [expr {$i * $pi/18.0}]
  }
  foreach eta {-4.35 -4.175 -4 -3.825 -3.65 -3.475 -3.3 -3.125 -2.95 -2.868 -2.65 -2.5 -2.322 -2.172 -2.043 -1.93 -1.83 -1.74 -1.653 1.74 1.83 1.93 2.043 2.172 2.322 2.5 2.65 2.868 2.95 3.125 3.3 3.475 3.65 3.825 4 4.175 4.35 4.525} {
    add EtaPhiBins $eta $PhiBins
  }
  set PhiBins {}
  for {set i -9} {$i <= 9} {incr i} {
    add PhiBins [expr {$i * $pi/9.0}]
  }
  foreach eta {-5 -4.7 -4.525 4.7 5} {
    add EtaPhiBins $eta $PhiBins
  }
  add EnergyFraction {0} {0.0 1.0}
  add EnergyFraction {11} {1.0 0.0}
  add EnergyFraction {22} {1.0 0.0}
  add EnergyFraction {111} {1.0 0.0}
  add EnergyFraction {12} {0.0 0.0}
  add EnergyFraction {13} {0.0 0.0}
  add EnergyFraction {14} {0.0 0.0}
  add EnergyFraction {16} {0.0 0.0}
  add EnergyFraction {1000022} {0.0 0.0}
  add EnergyFraction {1000023} {0.0 0.0}
  add EnergyFraction {1000025} {0.0 0.0}
  add EnergyFraction {1000035} {0.0 0.0}
  add EnergyFraction {1000039} {0.0 0.0}
  add EnergyFraction {1000045} {0.0 0.0}
  add EnergyFraction {310} {0.3 0.7}
  add EnergyFraction {3122} {0.3 0.7}
  set ECalResolutionFormula {                  (abs(eta) <= 3.0) * sqrt(energy^2*0.005^2 + energy*0.05^2 + 0.25^2) + \
                             (abs(eta) > 3.0 && abs(eta) <= 5.0) * sqrt(energy^2*0.107^2 + energy*2.08^2)}
  set HCalResolutionFormula {                  (abs(eta) <= 3.0) * sqrt(energy^2*0.050^2 + energy*1.50^2) + \
                             (abs(eta) > 3.0 && abs(eta) <= 5.0) * sqrt(energy^2*0.130^2 + energy*2.70^2)}
}   
    """
  else:
    exit("Error: Experiment "+experiment+" not known.")
  return (module_name, module_string)

def set_eflow_merger(experiment):
  module_name = ""
  module_string = ""
  if experiment == "A":
    module_name = "EFlowMergerATLAS"
    module_string = """
module Merger EFlowMergerATLAS {
  add InputArray CalorimeterATLAS/eflowTracks
  add InputArray CalorimeterATLAS/eflowTowers
  set OutputArray eflow
}
    """
  elif experiment == "C":
    module_name = "EFlowMergerCMS"
    module_string = """
module Merger EFlowMergerCMS {
  add InputArray CalorimeterCMS/eflowTracks
  add InputArray CalorimeterCMS/eflowTowers
  set OutputArray eflow
}
    """
  else:
    exit("Error: Experiment "+experiment+" not known.")
  return (module_name, module_string)

def set_photon_efficiency(experiment):
  module_name = ""
  module_string = ""
  if experiment == "A":
    module_name = "PhotonEfficiencyATLAS"
    module_string = """
module Efficiency PhotonEfficiencyATLAS {
  set InputArray CalorimeterATLAS/photons
  set OutputArray photons
  
  set FlagValue 1
  set KillUponFail true
  set EfficiencyFormula {                                      (pt <= 10.0) * (0.00) + \\
                                           (abs(eta) <= 1.5) * (pt > 10.0)  * (0.95) + \\
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 10.0)  * (0.85) + \\
                         (abs(eta) > 2.5)                                   * (0.00)}
}
"""
  elif experiment == "C":
    module_name = "PhotonEfficiencyCMS"
    module_string = """
module Efficiency PhotonEfficiencyCMS {
  set InputArray CalorimeterCMS/photons
  set OutputArray photons

  set FlagValue 1
  set KillUponFail true
  set EfficiencyFormula {                                      (pt <= 10.0) * (0.00) + \
                                           (abs(eta) <= 1.5) * (pt > 10.0)  * (0.95) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 10.0)  * (0.85) + \
                         (abs(eta) > 2.5)                                   * (0.00)}
}
"""
  else:
    exit("Error: Experiment "+experiment+" not known.")
  return (module_name, module_string)
    
def set_photon_isolation(n_iso, isolation_set):
  # Define correct candidate input array
  experiment = ""
  if isolation_set[0] == "A":
    experiment = "ATLAS"
  elif isolation_set[0] == "C":
    experiment = "CMS"
  else:
    exit("Error: Experiment "+experiment+" not known.")
    
  # Define correct isolation input array  
  isolation_input = "EFlowMerger"+experiment+"/eflow"
  if isolation_set[1] == "t":
    isolation_input = "TrackMerger"+experiment+"/tracks"       
  # Define correct abs_or_rel criterion
  absolute_limit = "false"
  if isolation_set[5] == "a":
    absolute_limit = "true"         
  module_name = "PhotonIsolation"+experiment+str(n_iso)
  module_string = """
module Isolation PhotonIsolation"""+experiment+str(n_iso)+""" {
  set CandidateInputArray PhotonEfficiency"""+experiment+"""/photons
  set IsolationInputArray """+isolation_input+"""
  
  set KillUponFail false
  set FlagValue """+str(pow(2, n_iso))+"""
  set AddFlag true
  
  set DeltaRMax """+str(eval(isolation_set[2]))+"""
  set PTMin """+str(eval(isolation_set[3]))+"""
  set PTRatioMax """+str(eval(isolation_set[4]))+"""
  set UsePTSum """+absolute_limit+"""
}
"""
  return (module_name, module_string)

def set_electron_efficiency(experiment, category):
  module_name = ""
  module_string = ""
  if experiment == "A":  
    m1 = "0.766841"
    m2 = "0.1509"
    m3 = "0.145237"
    m4 = "29.1152"
    id_eff_medium = "(pt<80)*("+m1+"+"+m2+"/(1.+exp(-"+m3+"*(pt-"+m4+"))))+(pt>80)*0.945052"
  
    t1 = "0.564986"
    t2 = "0.279235"
    t3 = "0.078647"
    t4 = "22.2707"
    id_eff_tight_ET = "(pt<80)*("+t1+"+"+t2+"/(1.+exp(-"+t3+"*(pt-"+t4+"))))+(pt>80)*0.883427"
    
    u1 = "0.674979"
    u2 = "0.160224"
    u3 = "1.91773"
    id_eff_tight_eta = "("+u1+"+"+u2+"*exp(-pow(eta/"+u3+", 2)))/0.776796"
    
    #Jamie has reduced efficiency to 80% for pt > 80 GeV.
    #id_eff_tight = "(0.98*(pt<80)*("+t1+"+"+t2+"/(1.+exp(-"+t3+"*(pt-"+t4+"))))+(pt>80)*0.8)"

    
    if category == "m":
      module_name = "ElectronEfficiencyATLASMedium"
      r1 = "0.98741"
      r2 = "0.0127525"   
      r3 = "-0.0175679"  
      r4 = "0.00521283"
      r5 = "-0.000449114"
      rec_eff = r1+"+"+r2+"*pow(eta, 2)+"+r3+"*pow(eta, 4)+"+r4+"*pow(eta, 6)+"+r5+"*pow(eta, 8)"
      
      module_string = """
module Efficiency ElectronEfficiencyATLASMedium {
  set InputArray ElectronEnergySmearingATLAS/electrons
  
  set FlagValue 1
  set KillUponFail false
  
  # Reconstruction * Identification
  # Reconstruction: ATL-COM-PHYS-2013-1287
  # Identification: ATL-COM-PHYS-2013-1287
  set EfficiencyFormula { \\
      (abs(eta) < 2.5)*("""+rec_eff+""")*(pt>7.0)*("""+id_eff_medium+""")
    }
}
"""
    elif category == "t":
      module_name = "ElectronEfficiencyATLASMediumTight"
      module_string = """
module Efficiency ElectronEfficiencyATLASMediumTight {
  set InputArray ElectronEnergySmearingATLAS/electrons

  set FlagValue 2
  set AddFlag true
  set KillUponFail false
  
  # Identification_Tight / Identification_Medium (see above)
  # Identification_Tight: ATL-COM-PHYS-2013-1287
  
  set EfficiencyFormula { \\
    (pt>7.0)*("""+id_eff_tight_ET+"""*"""+id_eff_tight_eta+""")/("""+id_eff_medium+""")
  }
}
"""
  elif experiment == "C":
    module_name = "ElectronEfficiencyCMS"
    module_string = """
module Efficiency ElectronEfficiencyCMS {
  set InputArray ElectronEnergySmearingCMS/electrons
  
  set FlagValue 1
  set KillUponFail false

  set EfficiencyFormula {                                      (pt <= 10.0) * (0.00) + \
                                           (abs(eta) <= 1.5) * (pt > 10.0)  * (0.95) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 10.0)  * (0.85) + \
                         (abs(eta) > 2.5)
    }
}
"""
  else:
    exit("Error: Experiment "+experiment+" not known.")
  return (module_name, module_string)

#
def set_electron_isolation(n_iso, isolation_set):
  #isoset = (exp,  isosource, isodr, isptmin, isoptratiomax, isoabsorrel)
  #Define correct candidate input array
  experiment = ""
  suffix = ""
  if isolation_set[0] == "A":
    experiment = "ATLAS"
  elif isolation_set[0] == "C":
    experiment = "CMS"
    suffix = ""
  else:
    exit("Error: Experiment "+experiment+" not known.")
    
  isolation_input = "EFlowMerger"+experiment+"/eflow"
  if isolation_set[1] == "t":
    isolation_input = "TrackMerger"+experiment+"/tracks"       
  # Define correct abs_or_rel criterion
  absolute_limit = "false"
  ratio_or_sum = "PTRatioMax"
  if isolation_set[5] == "a":
    absolute_limit = "true"  
    ratio_or_sum = "PTSumMax" 
    
  module_name = "ElectronIsolation"""+experiment+str(n_iso)
  module_string = """
module Isolation ElectronIsolation"""+experiment+str(n_iso)+""" {
  set CandidateInputArray ElectronEnergySmearing"""+experiment+"""/electrons
  set IsolationInputArray """+isolation_input+"""
  
  set KillUponFail false
  set FlagValue """+str(pow(2, n_iso))+"""
  set AddFlag true
  
  set DeltaRMax """+str(eval(isolation_set[2]))+"""
  set PTMin """+str(eval(isolation_set[3]))+"""
  set """+ratio_or_sum+""" """+str(eval(isolation_set[4]))+"""
  set UsePTSum """+absolute_limit+"""
}
"""
  return (module_name, module_string)

def set_muon_efficiency(experiment, category):
  module_name = ""
  module_string = ""
  if experiment == "A":
    if category == "2s":
      module_name = "MuonEfficiencyATLASChain2Combplusstandalone"
      module_string = """
module Efficiency MuonEfficiencyATLASChain2Combplusstandalone {
  set InputArray MuonMomentumSmearingATLAS/muons
  
  set FlagValue 1
  set AddFlag true
  set KillUponFail false

  set EfficiencyFormula { \ 
  (abs(eta) < 0.1)*0.83 + (abs(eta) >= 0.1)*(
  (eta>=-2.5)*(eta<-2.005)*( (phi>=3.009)*(phi<3.142)*0.98825+ (phi>=2.948)*(phi<3.009)*0.9832+ (phi>=2.849)*(phi<2.948)*0.9832+ (phi>=2.629)*(phi<2.849)*0.9832+ (phi>=2.529)*(phi<2.629)*0.9832+ (phi>=2.471)*(phi<2.529)*0.9832+ (phi>=2.21)*(phi<2.471)*0.98825+ (phi>=2.174)*(phi<2.21)*0.9832+ (phi>=2.065)*(phi<2.174)*0.9832+ (phi>=1.855)*(phi<2.065)*0.9832+ (phi>=1.745)*(phi<1.855)*0.9832+ (phi>=1.695)*(phi<1.745)*0.9832+ (phi>=1.436)*(phi<1.695)*0.98825+ (phi>=1.386)*(phi<1.436)*0.9832+ (phi>=1.276)*(phi<1.386)*0.9832+ (phi>=1.066)*(phi<1.276)*0.9832+ (phi>=0.957)*(phi<1.066)*0.9832+ (phi>=0.916)*(phi<0.957)*0.9832+ (phi>=0.657)*(phi<0.916)*0.98825+ (phi>=0.596)*(phi<0.657)*0.9832+ (phi>=0.496)*(phi<0.596)*0.9832+ (phi>=0.277)*(phi<0.496)*0.9832+ (phi>=0.178)*(phi<0.277)*0.9832+ (phi>=0.142)*(phi<0.178)*0.9832+ (phi>=-0.142)*(phi<0.142)*0.98825+ (phi>=-0.178)*(phi<-0.142)*0.9832+ (phi>=-0.277)*(phi<-0.178)*0.9832+ (phi>=-0.496)*(phi<-0.277)*0.9832+ (phi>=-0.596)*(phi<-0.496)*0.9832+ (phi>=-0.657)*(phi<-0.596)
*0.9832+ (phi>=-0.916)*(phi<-0.657)*0.98825+ (phi>=-0.957)*(phi<-0.916)*0.9832+ (phi>=-1.018)*(phi<-0.957)*0.9832+ (phi>=-1.066)*(phi<-1.018)*0.9832+ (phi>=-1.276)*(phi<-1.066)*0.9832+ (phi>=-1.357)*(phi<-1.276)*0.9832+ (phi>=-1.386)*(phi<-1.357)*0.9832+ (phi>=-1.436)*(phi<-1.386)*0.9832+ (phi>=-1.695)*(phi<-1.436)*0.98825+ (phi>=-1.745)*(phi<-1.695)*0.9832+ (phi>=-1.797)*(phi<-1.745)*0.9832+ (phi>=-1.855)*(phi<-1.797)*0.9832+ (phi>=-2.065)*(phi<-1.855)*0.9832+ (phi>=-2.134)*(phi<-2.065)*0.9832+ (phi>=-2.174)*(phi<-2.134)*0.9832+ (phi>=-2.21)*(phi<-2.174)*0.9832+ (phi>=-2.471)*(phi<-2.21)*0.98825+ (phi>=-2.529)*(phi<-2.471)*0.9832+ (phi>=-2.629)*(phi<-2.529)*0.9832+ (phi>=-2.849)*(phi<-2.629)*0.9832+ (phi>=-2.948)*(phi<-2.849)*0.9832+ (phi>=-3.009)*(phi<-2.948)*0.9832+ (phi>=-3.142)*(phi<-3.009)*0.98825 )+
  (eta>=-2.005)*(eta<-1.955)*( (phi>=3.009)*(phi<3.142)*0.99227+ (phi>=2.948)*(phi<3.009)*0.99413+ (phi>=2.849)*(phi<2.948)*0.9832+ (phi>=2.629)*(phi<2.849)*0.9832+ (phi>=2.529)*(phi<2.629)*0.9832+ (phi>=2.471)*(phi<2.529)*0.99413+ (phi>=2.21)*(phi<2.471)*0.99227+ (phi>=2.174)*(phi<2.21)*0.99413+ (phi>=2.065)*(phi<2.174)*0.9832+ (phi>=1.855)*(phi<2.065)*0.9832+ (phi>=1.745)*(phi<1.855)*0.9832+ (phi>=1.695)*(phi<1.745)*0.99413+ (phi>=1.436)*(phi<1.695)*0.99227+ (phi>=1.386)*(phi<1.436)*0.99413+ (phi>=1.276)*(phi<1.386)*0.9832+ (phi>=1.066)*(phi<1.276)*0.9832+ (phi>=0.957)*(phi<1.066)*0.9832+ (phi>=0.916)*(phi<0.957)*0.99413+ (phi>=0.657)*(phi<0.916)*0.99227+ (phi>=0.596)*(phi<0.657)*0.99413+ (phi>=0.496)*(phi<0.596)*0.9832+ (phi>=0.277)*(phi<0.496)*0.9832+ (phi>=0.178)*(phi<0.277)*0.9832+ (phi>=0.142)*(phi<0.178)*0.99413+ (phi>=-0.142)*(phi<0.142)*0.99227+ (phi>=-0.178)*(phi<-0.142)*0.99413+ (phi>=-0.277)*(phi<-0.178)*0.9832+ (phi>=-0.496)*(phi<-0.277)*0.9832+ (phi>=-0.596)*(phi<-0.496)*0.9832+ (phi>=-0.657)*(
phi<-0.596)*0.99413+ (phi>=-0.916)*(phi<-0.657)*0.99227+ (phi>=-0.957)*(phi<-0.916)*0.99413+ (phi>=-1.018)*(phi<-0.957)*0.9832+ (phi>=-1.066)*(phi<-1.018)*0.9832+ (phi>=-1.276)*(phi<-1.066)*0.9832+ (phi>=-1.357)*(phi<-1.276)*0.9832+ (phi>=-1.386)*(phi<-1.357)*0.9832+ (phi>=-1.436)*(phi<-1.386)*0.99413+ (phi>=-1.695)*(phi<-1.436)*0.99227+ (phi>=-1.745)*(phi<-1.695)*0.99413+ (phi>=-1.797)*(phi<-1.745)*0.9832+ (phi>=-1.855)*(phi<-1.797)*0.9832+ (phi>=-2.065)*(phi<-1.855)*0.9832+ (phi>=-2.134)*(phi<-2.065)*0.9832+ (phi>=-2.174)*(phi<-2.134)*0.9832+ (phi>=-2.21)*(phi<-2.174)*0.99413+ (phi>=-2.471)*(phi<-2.21)*0.99227+ (phi>=-2.529)*(phi<-2.471)*0.99413+ (phi>=-2.629)*(phi<-2.529)*0.9832+ (phi>=-2.849)*(phi<-2.629)*0.9832+ (phi>=-2.948)*(phi<-2.849)*0.9832+ (phi>=-3.009)*(phi<-2.948)*0.99413+ (phi>=-3.142)*(phi<-3.009)*0.99227 )+
  (eta>=-1.955)*(eta<-1.709)*( (phi>=3.009)*(phi<3.142)*0.99227+ (phi>=2.948)*(phi<3.009)*0.99413+ (phi>=2.849)*(phi<2.948)*0.99413+ (phi>=2.629)*(phi<2.849)*0.99413+ (phi>=2.529)*(phi<2.629)*0.99413+ (phi>=2.471)*(phi<2.529)*0.99413+ (phi>=2.21)*(phi<2.471)*0.99227+ (phi>=2.174)*(phi<2.21)*0.99413+ (phi>=2.065)*(phi<2.174)*0.99413+ (phi>=1.855)*(phi<2.065)*0.99413+ (phi>=1.745)*(phi<1.855)*0.99413+ (phi>=1.695)*(phi<1.745)*0.99413+ (phi>=1.436)*(phi<1.695)*0.99227+ (phi>=1.386)*(phi<1.436)*0.99413+ (phi>=1.276)*(phi<1.386)*0.99413+ (phi>=1.066)*(phi<1.276)*0.99413+ (phi>=0.957)*(phi<1.066)*0.99413+ (phi>=0.916)*(phi<0.957)*0.99413+ (phi>=0.657)*(phi<0.916)*0.99227+ (phi>=0.596)*(phi<0.657)*0.99413+ (phi>=0.496)*(phi<0.596)*0.99413+ (phi>=0.277)*(phi<0.496)*0.99413+ (phi>=0.178)*(phi<0.277)*0.99413+ (phi>=0.142)*(phi<0.178)*0.99413+ (phi>=-0.142)*(phi<0.142)*0.99227+ (phi>=-0.178)*(phi<-0.142)*0.99413+ (phi>=-0.277)*(phi<-0.178)*0.99413+ (phi>=-0.496)*(phi<-0.277)*0.99413+ (phi>=-0.596)*(phi<-0.496)*0.99413+ 
(phi>=-0.657)*(phi<-0.596)*0.99413+ (phi>=-0.916)*(phi<-0.657)*0.99227+ (phi>=-0.957)*(phi<-0.916)*0.99413+ (phi>=-1.018)*(phi<-0.957)*0.99413+ (phi>=-1.066)*(phi<-1.018)*0.99413+ (phi>=-1.276)*(phi<-1.066)*0.99413+ (phi>=-1.357)*(phi<-1.276)*0.99413+ (phi>=-1.386)*(phi<-1.357)*0.99413+ (phi>=-1.436)*(phi<-1.386)*0.99413+ (phi>=-1.695)*(phi<-1.436)*0.99227+ (phi>=-1.745)*(phi<-1.695)*0.99413+ (phi>=-1.797)*(phi<-1.745)*0.99413+ (phi>=-1.855)*(phi<-1.797)*0.99413+ (phi>=-2.065)*(phi<-1.855)*0.99413+ (phi>=-2.134)*(phi<-2.065)*0.99413+ (phi>=-2.174)*(phi<-2.134)*0.99413+ (phi>=-2.21)*(phi<-2.174)*0.99413+ (phi>=-2.471)*(phi<-2.21)*0.99227+ (phi>=-2.529)*(phi<-2.471)*0.99413+ (phi>=-2.629)*(phi<-2.529)*0.99413+ (phi>=-2.849)*(phi<-2.629)*0.99413+ (phi>=-2.948)*(phi<-2.849)*0.99413+ (phi>=-3.009)*(phi<-2.948)*0.99413+ (phi>=-3.142)*(phi<-3.009)*0.99227 )+
  (eta>=-1.709)*(eta<-1.411)*( (phi>=3.009)*(phi<3.142)*0.99227+ (phi>=2.948)*(phi<3.009)*0.99413+ (phi>=2.849)*(phi<2.948)*0.99413+ (phi>=2.629)*(phi<2.849)*0.9931+ (phi>=2.529)*(phi<2.629)*0.99413+ (phi>=2.471)*(phi<2.529)*0.99413+ (phi>=2.21)*(phi<2.471)*0.99227+ (phi>=2.174)*(phi<2.21)*0.99413+ (phi>=2.065)*(phi<2.174)*0.99413+ (phi>=1.855)*(phi<2.065)*0.9931+ (phi>=1.745)*(phi<1.855)*0.99413+ (phi>=1.695)*(phi<1.745)*0.99413+ (phi>=1.436)*(phi<1.695)*0.99227+ (phi>=1.386)*(phi<1.436)*0.99413+ (phi>=1.276)*(phi<1.386)*0.99413+ (phi>=1.066)*(phi<1.276)*0.9931+ (phi>=0.957)*(phi<1.066)*0.99413+ (phi>=0.916)*(phi<0.957)*0.99413+ (phi>=0.657)*(phi<0.916)*0.99227+ (phi>=0.596)*(phi<0.657)*0.99413+ (phi>=0.496)*(phi<0.596)*0.99413+ (phi>=0.277)*(phi<0.496)*0.9931+ (phi>=0.178)*(phi<0.277)*0.99413+ (phi>=0.142)*(phi<0.178)*0.99413+ (phi>=-0.142)*(phi<0.142)*0.99227+ (phi>=-0.178)*(phi<-0.142)*0.99413+ (phi>=-0.277)*(phi<-0.178)*0.99413+ (phi>=-0.496)*(phi<-0.277)*0.9931+ (phi>=-0.596)*(phi<-0.496)*0.99413+ (
phi>=-0.657)*(phi<-0.596)*0.99413+ (phi>=-0.916)*(phi<-0.657)*0.99227+ (phi>=-0.957)*(phi<-0.916)*0.99413+ (phi>=-1.018)*(phi<-0.957)*0.99413+ (phi>=-1.066)*(phi<-1.018)*0.99413+ (phi>=-1.276)*(phi<-1.066)*0.9931+ (phi>=-1.357)*(phi<-1.276)*0.99413+ (phi>=-1.386)*(phi<-1.357)*0.99413+ (phi>=-1.436)*(phi<-1.386)*0.99413+ (phi>=-1.695)*(phi<-1.436)*0.99227+ (phi>=-1.745)*(phi<-1.695)*0.99413+ (phi>=-1.797)*(phi<-1.745)*0.99413+ (phi>=-1.855)*(phi<-1.797)*0.99413+ (phi>=-2.065)*(phi<-1.855)*0.9931+ (phi>=-2.134)*(phi<-2.065)*0.99413+ (phi>=-2.174)*(phi<-2.134)*0.99413+ (phi>=-2.21)*(phi<-2.174)*0.99413+ (phi>=-2.471)*(phi<-2.21)*0.99227+ (phi>=-2.529)*(phi<-2.471)*0.99413+ (phi>=-2.629)*(phi<-2.529)*0.99413+ (phi>=-2.849)*(phi<-2.629)*0.9931+ (phi>=-2.948)*(phi<-2.849)*0.99413+ (phi>=-3.009)*(phi<-2.948)*0.99413+ (phi>=-3.142)*(phi<-3.009)*0.99227 )+
  (eta>=-1.411)*(eta<-1.238)*( (phi>=3.009)*(phi<3.142)*0.99227+ (phi>=2.948)*(phi<3.009)*0.99413+ (phi>=2.849)*(phi<2.948)*0.99413+ (phi>=2.629)*(phi<2.849)*0.99413+ (phi>=2.529)*(phi<2.629)*0.99413+ (phi>=2.471)*(phi<2.529)*0.99413+ (phi>=2.21)*(phi<2.471)*0.99227+ (phi>=2.174)*(phi<2.21)*0.99413+ (phi>=2.065)*(phi<2.174)*0.99413+ (phi>=1.855)*(phi<2.065)*0.99413+ (phi>=1.745)*(phi<1.855)*0.99413+ (phi>=1.695)*(phi<1.745)*0.99413+ (phi>=1.436)*(phi<1.695)*0.99227+ (phi>=1.386)*(phi<1.436)*0.99413+ (phi>=1.276)*(phi<1.386)*0.99413+ (phi>=1.066)*(phi<1.276)*0.99413+ (phi>=0.957)*(phi<1.066)*0.99413+ (phi>=0.916)*(phi<0.957)*0.99413+ (phi>=0.657)*(phi<0.916)*0.99227+ (phi>=0.596)*(phi<0.657)*0.99413+ (phi>=0.496)*(phi<0.596)*0.99413+ (phi>=0.277)*(phi<0.496)*0.99413+ (phi>=0.178)*(phi<0.277)*0.99413+ (phi>=0.142)*(phi<0.178)*0.99413+ (phi>=-0.142)*(phi<0.142)*0.99227+ (phi>=-0.178)*(phi<-0.142)*0.99413+ (phi>=-0.277)*(phi<-0.178)*0.99413+ (phi>=-0.496)*(phi<-0.277)*0.99413+ (phi>=-0.596)*(phi<-0.496)*0.99413+ 
(phi>=-0.657)*(phi<-0.596)*0.99413+ (phi>=-0.916)*(phi<-0.657)*0.99227+ (phi>=-0.957)*(phi<-0.916)*0.99413+ (phi>=-1.018)*(phi<-0.957)*0.99413+ (phi>=-1.066)*(phi<-1.018)*0.99413+ (phi>=-1.276)*(phi<-1.066)*0.99413+ (phi>=-1.357)*(phi<-1.276)*0.99413+ (phi>=-1.386)*(phi<-1.357)*0.99413+ (phi>=-1.436)*(phi<-1.386)*0.99413+ (phi>=-1.695)*(phi<-1.436)*0.99227+ (phi>=-1.745)*(phi<-1.695)*0.99413+ (phi>=-1.797)*(phi<-1.745)*0.99413+ (phi>=-1.855)*(phi<-1.797)*0.99413+ (phi>=-2.065)*(phi<-1.855)*0.99413+ (phi>=-2.134)*(phi<-2.065)*0.99413+ (phi>=-2.174)*(phi<-2.134)*0.99413+ (phi>=-2.21)*(phi<-2.174)*0.99413+ (phi>=-2.471)*(phi<-2.21)*0.99227+ (phi>=-2.529)*(phi<-2.471)*0.99413+ (phi>=-2.629)*(phi<-2.529)*0.99413+ (phi>=-2.849)*(phi<-2.629)*0.99413+ (phi>=-2.948)*(phi<-2.849)*0.99413+ (phi>=-3.009)*(phi<-2.948)*0.99413+ (phi>=-3.142)*(phi<-3.009)*0.99227 )+
  (eta>=-1.238)*(eta<-1.163)*( (phi>=3.009)*(phi<3.142)*0.99227+ (phi>=2.948)*(phi<3.009)*0.99413+ (phi>=2.849)*(phi<2.948)*0.99413+ (phi>=2.629)*(phi<2.849)*0.99268+ (phi>=2.529)*(phi<2.629)*0.99413+ (phi>=2.471)*(phi<2.529)*0.99413+ (phi>=2.21)*(phi<2.471)*0.99227+ (phi>=2.174)*(phi<2.21)*0.99413+ (phi>=2.065)*(phi<2.174)*0.99413+ (phi>=1.855)*(phi<2.065)*0.99268+ (phi>=1.745)*(phi<1.855)*0.99413+ (phi>=1.695)*(phi<1.745)*0.99413+ (phi>=1.436)*(phi<1.695)*0.99227+ (phi>=1.386)*(phi<1.436)*0.99413+ (phi>=1.276)*(phi<1.386)*0.99413+ (phi>=1.066)*(phi<1.276)*0.99268+ (phi>=0.957)*(phi<1.066)*0.99413+ (phi>=0.916)*(phi<0.957)*0.99413+ (phi>=0.657)*(phi<0.916)*0.99227+ (phi>=0.596)*(phi<0.657)*0.99413+ (phi>=0.496)*(phi<0.596)*0.99413+ (phi>=0.277)*(phi<0.496)*0.99268+ (phi>=0.178)*(phi<0.277)*0.99413+ (phi>=0.142)*(phi<0.178)*0.99413+ (phi>=-0.142)*(phi<0.142)*0.99227+ (phi>=-0.178)*(phi<-0.142)*0.99413+ (phi>=-0.277)*(phi<-0.178)*0.99413+ (phi>=-0.496)*(phi<-0.277)*0.99268+ (phi>=-0.596)*(phi<-0.496)*0.99413+ 
(phi>=-0.657)*(phi<-0.596)*0.99413+ (phi>=-0.916)*(phi<-0.657)*0.99227+ (phi>=-0.957)*(phi<-0.916)*0.99413+ (phi>=-1.018)*(phi<-0.957)*0.99413+ (phi>=-1.066)*(phi<-1.018)*0.99413+ (phi>=-1.276)*(phi<-1.066)*0.99268+ (phi>=-1.357)*(phi<-1.276)*0.99413+ (phi>=-1.386)*(phi<-1.357)*0.99413+ (phi>=-1.436)*(phi<-1.386)*0.99413+ (phi>=-1.695)*(phi<-1.436)*0.99227+ (phi>=-1.745)*(phi<-1.695)*0.99413+ (phi>=-1.797)*(phi<-1.745)*0.99413+ (phi>=-1.855)*(phi<-1.797)*0.99413+ (phi>=-2.065)*(phi<-1.855)*0.99268+ (phi>=-2.134)*(phi<-2.065)*0.99413+ (phi>=-2.174)*(phi<-2.134)*0.99413+ (phi>=-2.21)*(phi<-2.174)*0.99413+ (phi>=-2.471)*(phi<-2.21)*0.99227+ (phi>=-2.529)*(phi<-2.471)*0.99413+ (phi>=-2.629)*(phi<-2.529)*0.99413+ (phi>=-2.849)*(phi<-2.629)*0.99268+ (phi>=-2.948)*(phi<-2.849)*0.99413+ (phi>=-3.009)*(phi<-2.948)*0.99413+ (phi>=-3.142)*(phi<-3.009)*0.99227 )+
  (eta>=-1.163)*(eta<-1.113)*( (phi>=3.009)*(phi<3.142)*0.99227+ (phi>=2.948)*(phi<3.009)*0.99413+ (phi>=2.849)*(phi<2.948)*0.99268+ (phi>=2.629)*(phi<2.849)*0.99268+ (phi>=2.529)*(phi<2.629)*0.99268+ (phi>=2.471)*(phi<2.529)*0.99413+ (phi>=2.21)*(phi<2.471)*0.99227+ (phi>=2.174)*(phi<2.21)*0.99413+ (phi>=2.065)*(phi<2.174)*0.99268+ (phi>=1.855)*(phi<2.065)*0.99268+ (phi>=1.745)*(phi<1.855)*0.99268+ (phi>=1.695)*(phi<1.745)*0.99413+ (phi>=1.436)*(phi<1.695)*0.99227+ (phi>=1.386)*(phi<1.436)*0.99413+ (phi>=1.276)*(phi<1.386)*0.99268+ (phi>=1.066)*(phi<1.276)*0.99268+ (phi>=0.957)*(phi<1.066)*0.99268+ (phi>=0.916)*(phi<0.957)*0.99413+ (phi>=0.657)*(phi<0.916)*0.99227+ (phi>=0.596)*(phi<0.657)*0.99413+ (phi>=0.496)*(phi<0.596)*0.99268+ (phi>=0.277)*(phi<0.496)*0.99268+ (phi>=0.178)*(phi<0.277)*0.99268+ (phi>=0.142)*(phi<0.178)*0.99413+ (phi>=-0.142)*(phi<0.142)*0.99227+ (phi>=-0.178)*(phi<-0.142)*0.99413+ (phi>=-0.277)*(phi<-0.178)*0.99268+ (phi>=-0.496)*(phi<-0.277)*0.99268+ (phi>=-0.596)*(phi<-0.496)*0.99268+ 
(phi>=-0.657)*(phi<-0.596)*0.99413+ (phi>=-0.916)*(phi<-0.657)*0.99227+ (phi>=-0.957)*(phi<-0.916)*0.99413+ (phi>=-1.018)*(phi<-0.957)*0.99268+ (phi>=-1.066)*(phi<-1.018)*0.99268+ (phi>=-1.276)*(phi<-1.066)*0.99268+ (phi>=-1.357)*(phi<-1.276)*0.99268+ (phi>=-1.386)*(phi<-1.357)*0.99268+ (phi>=-1.436)*(phi<-1.386)*0.99413+ (phi>=-1.695)*(phi<-1.436)*0.99227+ (phi>=-1.745)*(phi<-1.695)*0.99413+ (phi>=-1.797)*(phi<-1.745)*0.99268+ (phi>=-1.855)*(phi<-1.797)*0.99268+ (phi>=-2.065)*(phi<-1.855)*0.99268+ (phi>=-2.134)*(phi<-2.065)*0.99268+ (phi>=-2.174)*(phi<-2.134)*0.99268+ (phi>=-2.21)*(phi<-2.174)*0.99413+ (phi>=-2.471)*(phi<-2.21)*0.99227+ (phi>=-2.529)*(phi<-2.471)*0.99413+ (phi>=-2.629)*(phi<-2.529)*0.99268+ (phi>=-2.849)*(phi<-2.629)*0.99268+ (phi>=-2.948)*(phi<-2.849)*0.99268+ (phi>=-3.009)*(phi<-2.948)*0.99413+ (phi>=-3.142)*(phi<-3.009)*0.99227 )+
  (eta>=-1.113)*(eta<-0.965)*( (phi>=3.009)*(phi<3.142)*0.99268+ (phi>=2.948)*(phi<3.009)*0.99268+ (phi>=2.849)*(phi<2.948)*0.99268+ (phi>=2.629)*(phi<2.849)*0.99268+ (phi>=2.529)*(phi<2.629)*0.99268+ (phi>=2.471)*(phi<2.529)*0.99268+ (phi>=2.21)*(phi<2.471)*0.99268+ (phi>=2.174)*(phi<2.21)*0.99268+ (phi>=2.065)*(phi<2.174)*0.99268+ (phi>=1.855)*(phi<2.065)*0.99268+ (phi>=1.745)*(phi<1.855)*0.99268+ (phi>=1.695)*(phi<1.745)*0.99268+ (phi>=1.436)*(phi<1.695)*0.99268+ (phi>=1.386)*(phi<1.436)*0.99268+ (phi>=1.276)*(phi<1.386)*0.99268+ (phi>=1.066)*(phi<1.276)*0.99268+ (phi>=0.957)*(phi<1.066)*0.99268+ (phi>=0.916)*(phi<0.957)*0.99268+ (phi>=0.657)*(phi<0.916)*0.99268+ (phi>=0.596)*(phi<0.657)*0.99268+ (phi>=0.496)*(phi<0.596)*0.99268+ (phi>=0.277)*(phi<0.496)*0.99268+ (phi>=0.178)*(phi<0.277)*0.99268+ (phi>=0.142)*(phi<0.178)*0.99268+ (phi>=-0.142)*(phi<0.142)*0.99268+ (phi>=-0.178)*(phi<-0.142)*0.99268+ (phi>=-0.277)*(phi<-0.178)*0.99268+ (phi>=-0.496)*(phi<-0.277)*0.99268+ (phi>=-0.596)*(phi<-0.496)*0.99268+ 
(phi>=-0.657)*(phi<-0.596)*0.99268+ (phi>=-0.916)*(phi<-0.657)*0.99268+ (phi>=-0.957)*(phi<-0.916)*0.99268+ (phi>=-1.018)*(phi<-0.957)*0.99268+ (phi>=-1.066)*(phi<-1.018)*0.99268+ (phi>=-1.276)*(phi<-1.066)*0.99268+ (phi>=-1.357)*(phi<-1.276)*0.99268+ (phi>=-1.386)*(phi<-1.357)*0.99268+ (phi>=-1.436)*(phi<-1.386)*0.99268+ (phi>=-1.695)*(phi<-1.436)*0.99268+ (phi>=-1.745)*(phi<-1.695)*0.99268+ (phi>=-1.797)*(phi<-1.745)*0.99268+ (phi>=-1.855)*(phi<-1.797)*0.99268+ (phi>=-2.065)*(phi<-1.855)*0.99268+ (phi>=-2.134)*(phi<-2.065)*0.99268+ (phi>=-2.174)*(phi<-2.134)*0.99268+ (phi>=-2.21)*(phi<-2.174)*0.99268+ (phi>=-2.471)*(phi<-2.21)*0.99268+ (phi>=-2.529)*(phi<-2.471)*0.99268+ (phi>=-2.629)*(phi<-2.529)*0.99268+ (phi>=-2.849)*(phi<-2.629)*0.99268+ (phi>=-2.948)*(phi<-2.849)*0.99268+ (phi>=-3.009)*(phi<-2.948)*0.99268+ (phi>=-3.142)*(phi<-3.009)*0.99268 )+
  (eta>=-0.965)*(eta<-0.817)*( (phi>=3.009)*(phi<3.142)*0.92673+ (phi>=2.948)*(phi<3.009)*0.92673+ (phi>=2.849)*(phi<2.948)*0.95991+ (phi>=2.629)*(phi<2.849)*0.99351+ (phi>=2.529)*(phi<2.629)*0.95991+ (phi>=2.471)*(phi<2.529)*0.92673+ (phi>=2.21)*(phi<2.471)*0.92673+ (phi>=2.174)*(phi<2.21)*0.92673+ (phi>=2.065)*(phi<2.174)*0.95991+ (phi>=1.855)*(phi<2.065)*0.99351+ (phi>=1.745)*(phi<1.855)*0.95991+ (phi>=1.695)*(phi<1.745)*0.92673+ (phi>=1.436)*(phi<1.695)*0.92673+ (phi>=1.386)*(phi<1.436)*0.92673+ (phi>=1.276)*(phi<1.386)*0.95991+ (phi>=1.066)*(phi<1.276)*0.99351+ (phi>=0.957)*(phi<1.066)*0.95991+ (phi>=0.916)*(phi<0.957)*0.92673+ (phi>=0.657)*(phi<0.916)*0.92673+ (phi>=0.596)*(phi<0.657)*0.92673+ (phi>=0.496)*(phi<0.596)*0.95991+ (phi>=0.277)*(phi<0.496)*0.99351+ (phi>=0.178)*(phi<0.277)*0.95991+ (phi>=0.142)*(phi<0.178)*0.92673+ (phi>=-0.142)*(phi<0.142)*0.92673+ (phi>=-0.178)*(phi<-0.142)*0.92673+ (phi>=-0.277)*(phi<-0.178)*0.95991+ (phi>=-0.496)*(phi<-0.277)*0.99351+ (phi>=-0.596)*(phi<-0.496)*0.95991+ 
(phi>=-0.657)*(phi<-0.596)*0.92673+ (phi>=-0.916)*(phi<-0.657)*0.92673+ (phi>=-0.957)*(phi<-0.916)*0.92673+ (phi>=-1.018)*(phi<-0.957)*0.95991+ (phi>=-1.066)*(phi<-1.018)*0.98444+ (phi>=-1.276)*(phi<-1.066)*0.98444+ (phi>=-1.357)*(phi<-1.276)*0.98444+ (phi>=-1.386)*(phi<-1.357)*0.95991+ (phi>=-1.436)*(phi<-1.386)*0.92673+ (phi>=-1.695)*(phi<-1.436)*0.92673+ (phi>=-1.745)*(phi<-1.695)*0.92673+ (phi>=-1.797)*(phi<-1.745)*0.95991+ (phi>=-1.855)*(phi<-1.797)*0.98444+ (phi>=-2.065)*(phi<-1.855)*0.98444+ (phi>=-2.134)*(phi<-2.065)*0.98444+ (phi>=-2.174)*(phi<-2.134)*0.95991+ (phi>=-2.21)*(phi<-2.174)*0.92673+ (phi>=-2.471)*(phi<-2.21)*0.92673+ (phi>=-2.529)*(phi<-2.471)*0.92673+ (phi>=-2.629)*(phi<-2.529)*0.95991+ (phi>=-2.849)*(phi<-2.629)*0.99351+ (phi>=-2.948)*(phi<-2.849)*0.95991+ (phi>=-3.009)*(phi<-2.948)*0.92673+ (phi>=-3.142)*(phi<-3.009)*0.92673 )+
  (eta>=-0.817)*(eta<-0.519)*( (phi>=3.009)*(phi<3.142)*0.92673+ (phi>=2.948)*(phi<3.009)*0.92673+ (phi>=2.849)*(phi<2.948)*0.95991+ (phi>=2.629)*(phi<2.849)*0.99351+ (phi>=2.529)*(phi<2.629)*0.95991+ (phi>=2.471)*(phi<2.529)*0.92673+ (phi>=2.21)*(phi<2.471)*0.92673+ (phi>=2.174)*(phi<2.21)*0.92673+ (phi>=2.065)*(phi<2.174)*0.95991+ (phi>=1.855)*(phi<2.065)*0.99351+ (phi>=1.745)*(phi<1.855)*0.95991+ (phi>=1.695)*(phi<1.745)*0.92673+ (phi>=1.436)*(phi<1.695)*0.92673+ (phi>=1.386)*(phi<1.436)*0.92673+ (phi>=1.276)*(phi<1.386)*0.95991+ (phi>=1.066)*(phi<1.276)*0.99351+ (phi>=0.957)*(phi<1.066)*0.95991+ (phi>=0.916)*(phi<0.957)*0.92673+ (phi>=0.657)*(phi<0.916)*0.92673+ (phi>=0.596)*(phi<0.657)*0.92673+ (phi>=0.496)*(phi<0.596)*0.95991+ (phi>=0.277)*(phi<0.496)*0.99351+ (phi>=0.178)*(phi<0.277)*0.95991+ (phi>=0.142)*(phi<0.178)*0.92673+ (phi>=-0.142)*(phi<0.142)*0.92673+ (phi>=-0.178)*(phi<-0.142)*0.92673+ (phi>=-0.277)*(phi<-0.178)*0.95991+ (phi>=-0.496)*(phi<-0.277)*0.99351+ (phi>=-0.596)*(phi<-0.496)*0.95991+ 
(phi>=-0.657)*(phi<-0.596)*0.92673+ (phi>=-0.916)*(phi<-0.657)*0.92673+ (phi>=-0.957)*(phi<-0.916)*0.92673+ (phi>=-1.018)*(phi<-0.957)*0.95991+ (phi>=-1.066)*(phi<-1.018)*0.98444+ (phi>=-1.276)*(phi<-1.066)*0.98444+ (phi>=-1.357)*(phi<-1.276)*0.98444+ (phi>=-1.386)*(phi<-1.357)*0.98444+ (phi>=-1.436)*(phi<-1.386)*0.98444+ (phi>=-1.695)*(phi<-1.436)*0.98444+ (phi>=-1.745)*(phi<-1.695)*0.98444+ (phi>=-1.797)*(phi<-1.745)*0.98444+ (phi>=-1.855)*(phi<-1.797)*0.98444+ (phi>=-2.065)*(phi<-1.855)*0.98444+ (phi>=-2.134)*(phi<-2.065)*0.98444+ (phi>=-2.174)*(phi<-2.134)*0.95991+ (phi>=-2.21)*(phi<-2.174)*0.92673+ (phi>=-2.471)*(phi<-2.21)*0.92673+ (phi>=-2.529)*(phi<-2.471)*0.92673+ (phi>=-2.629)*(phi<-2.529)*0.95991+ (phi>=-2.849)*(phi<-2.629)*0.99351+ (phi>=-2.948)*(phi<-2.849)*0.95991+ (phi>=-3.009)*(phi<-2.948)*0.92673+ (phi>=-3.142)*(phi<-3.009)*0.92673 )+
  (eta>=-0.519)*(eta<0.519)*( (phi>=3.009)*(phi<3.142)*0.92673+ (phi>=2.948)*(phi<3.009)*0.92673+ (phi>=2.849)*(phi<2.948)*0.95991+ (phi>=2.629)*(phi<2.849)*0.99351+ (phi>=2.529)*(phi<2.629)*0.95991+ (phi>=2.471)*(phi<2.529)*0.92673+ (phi>=2.21)*(phi<2.471)*0.92673+ (phi>=2.174)*(phi<2.21)*0.92673+ (phi>=2.065)*(phi<2.174)*0.95991+ (phi>=1.855)*(phi<2.065)*0.99351+ (phi>=1.745)*(phi<1.855)*0.95991+ (phi>=1.695)*(phi<1.745)*0.92673+ (phi>=1.436)*(phi<1.695)*0.92673+ (phi>=1.386)*(phi<1.436)*0.92673+ (phi>=1.276)*(phi<1.386)*0.95991+ (phi>=1.066)*(phi<1.276)*0.99351+ (phi>=0.957)*(phi<1.066)*0.95991+ (phi>=0.916)*(phi<0.957)*0.92673+ (phi>=0.657)*(phi<0.916)*0.92673+ (phi>=0.596)*(phi<0.657)*0.92673+ (phi>=0.496)*(phi<0.596)*0.95991+ (phi>=0.277)*(phi<0.496)*0.99351+ (phi>=0.178)*(phi<0.277)*0.95991+ (phi>=0.142)*(phi<0.178)*0.92673+ (phi>=-0.142)*(phi<0.142)*0.92673+ (phi>=-0.178)*(phi<-0.142)*0.92673+ (phi>=-0.277)*(phi<-0.178)*0.95991+ (phi>=-0.496)*(phi<-0.277)*0.99351+ (phi>=-0.596)*(phi<-0.496)*0.95991+ (
phi>=-0.657)*(phi<-0.596)*0.92673+ (phi>=-0.916)*(phi<-0.657)*0.92673+ (phi>=-0.957)*(phi<-0.916)*0.92673+ (phi>=-1.018)*(phi<-0.957)*0.95991+ (phi>=-1.066)*(phi<-1.018)*0.98444+ (phi>=-1.276)*(phi<-1.066)*0.98444+ (phi>=-1.357)*(phi<-1.276)*0.98444+ (phi>=-1.386)*(phi<-1.357)*0.95991+ (phi>=-1.436)*(phi<-1.386)*0.92673+ (phi>=-1.695)*(phi<-1.436)*0.92673+ (phi>=-1.745)*(phi<-1.695)*0.92673+ (phi>=-1.797)*(phi<-1.745)*0.95991+ (phi>=-1.855)*(phi<-1.797)*0.98444+ (phi>=-2.065)*(phi<-1.855)*0.98444+ (phi>=-2.134)*(phi<-2.065)*0.98444+ (phi>=-2.174)*(phi<-2.134)*0.95991+ (phi>=-2.21)*(phi<-2.174)*0.92673+ (phi>=-2.471)*(phi<-2.21)*0.92673+ (phi>=-2.529)*(phi<-2.471)*0.92673+ (phi>=-2.629)*(phi<-2.529)*0.95991+ (phi>=-2.849)*(phi<-2.629)*0.99351+ (phi>=-2.948)*(phi<-2.849)*0.95991+ (phi>=-3.009)*(phi<-2.948)*0.92673+ (phi>=-3.142)*(phi<-3.009)*0.92673 )+
  (eta>=0.519)*(eta<0.817)*( (phi>=3.009)*(phi<3.142)*0.92673+ (phi>=2.948)*(phi<3.009)*0.92673+ (phi>=2.849)*(phi<2.948)*0.95991+ (phi>=2.629)*(phi<2.849)*0.99351+ (phi>=2.529)*(phi<2.629)*0.95991+ (phi>=2.471)*(phi<2.529)*0.92673+ (phi>=2.21)*(phi<2.471)*0.92673+ (phi>=2.174)*(phi<2.21)*0.92673+ (phi>=2.065)*(phi<2.174)*0.95991+ (phi>=1.855)*(phi<2.065)*0.99351+ (phi>=1.745)*(phi<1.855)*0.95991+ (phi>=1.695)*(phi<1.745)*0.92673+ (phi>=1.436)*(phi<1.695)*0.92673+ (phi>=1.386)*(phi<1.436)*0.92673+ (phi>=1.276)*(phi<1.386)*0.95991+ (phi>=1.066)*(phi<1.276)*0.99351+ (phi>=0.957)*(phi<1.066)*0.95991+ (phi>=0.916)*(phi<0.957)*0.92673+ (phi>=0.657)*(phi<0.916)*0.92673+ (phi>=0.596)*(phi<0.657)*0.92673+ (phi>=0.496)*(phi<0.596)*0.95991+ (phi>=0.277)*(phi<0.496)*0.99351+ (phi>=0.178)*(phi<0.277)*0.95991+ (phi>=0.142)*(phi<0.178)*0.92673+ (phi>=-0.142)*(phi<0.142)*0.92673+ (phi>=-0.178)*(phi<-0.142)*0.92673+ (phi>=-0.277)*(phi<-0.178)*0.95991+ (phi>=-0.496)*(phi<-0.277)*0.99351+ (phi>=-0.596)*(phi<-0.496)*0.95991+ (
phi>=-0.657)*(phi<-0.596)*0.92673+ (phi>=-0.916)*(phi<-0.657)*0.92673+ (phi>=-0.957)*(phi<-0.916)*0.92673+ (phi>=-1.018)*(phi<-0.957)*0.95991+ (phi>=-1.066)*(phi<-1.018)*0.98444+ (phi>=-1.276)*(phi<-1.066)*0.98444+ (phi>=-1.357)*(phi<-1.276)*0.98444+ (phi>=-1.386)*(phi<-1.357)*0.98444+ (phi>=-1.436)*(phi<-1.386)*0.98444+ (phi>=-1.695)*(phi<-1.436)*0.98444+ (phi>=-1.745)*(phi<-1.695)*0.98444+ (phi>=-1.797)*(phi<-1.745)*0.98444+ (phi>=-1.855)*(phi<-1.797)*0.98444+ (phi>=-2.065)*(phi<-1.855)*0.98444+ (phi>=-2.134)*(phi<-2.065)*0.98444+ (phi>=-2.174)*(phi<-2.134)*0.95991+ (phi>=-2.21)*(phi<-2.174)*0.92673+ (phi>=-2.471)*(phi<-2.21)*0.92673+ (phi>=-2.529)*(phi<-2.471)*0.92673+ (phi>=-2.629)*(phi<-2.529)*0.95991+ (phi>=-2.849)*(phi<-2.629)*0.99351+ (phi>=-2.948)*(phi<-2.849)*0.95991+ (phi>=-3.009)*(phi<-2.948)*0.92673+ (phi>=-3.142)*(phi<-3.009)*0.92673 )+
  (eta>=0.817)*(eta<0.965)*( (phi>=3.009)*(phi<3.142)*0.92673+ (phi>=2.948)*(phi<3.009)*0.92673+ (phi>=2.849)*(phi<2.948)*0.95991+ (phi>=2.629)*(phi<2.849)*0.99351+ (phi>=2.529)*(phi<2.629)*0.95991+ (phi>=2.471)*(phi<2.529)*0.92673+ (phi>=2.21)*(phi<2.471)*0.92673+ (phi>=2.174)*(phi<2.21)*0.92673+ (phi>=2.065)*(phi<2.174)*0.95991+ (phi>=1.855)*(phi<2.065)*0.99351+ (phi>=1.745)*(phi<1.855)*0.95991+ (phi>=1.695)*(phi<1.745)*0.92673+ (phi>=1.436)*(phi<1.695)*0.92673+ (phi>=1.386)*(phi<1.436)*0.92673+ (phi>=1.276)*(phi<1.386)*0.95991+ (phi>=1.066)*(phi<1.276)*0.99351+ (phi>=0.957)*(phi<1.066)*0.95991+ (phi>=0.916)*(phi<0.957)*0.92673+ (phi>=0.657)*(phi<0.916)*0.92673+ (phi>=0.596)*(phi<0.657)*0.92673+ (phi>=0.496)*(phi<0.596)*0.95991+ (phi>=0.277)*(phi<0.496)*0.99351+ (phi>=0.178)*(phi<0.277)*0.95991+ (phi>=0.142)*(phi<0.178)*0.92673+ (phi>=-0.142)*(phi<0.142)*0.92673+ (phi>=-0.178)*(phi<-0.142)*0.92673+ (phi>=-0.277)*(phi<-0.178)*0.95991+ (phi>=-0.496)*(phi<-0.277)*0.99351+ (phi>=-0.596)*(phi<-0.496)*0.95991+ (
phi>=-0.657)*(phi<-0.596)*0.92673+ (phi>=-0.916)*(phi<-0.657)*0.92673+ (phi>=-0.957)*(phi<-0.916)*0.92673+ (phi>=-1.018)*(phi<-0.957)*0.95991+ (phi>=-1.066)*(phi<-1.018)*0.98444+ (phi>=-1.276)*(phi<-1.066)*0.98444+ (phi>=-1.357)*(phi<-1.276)*0.98444+ (phi>=-1.386)*(phi<-1.357)*0.95991+ (phi>=-1.436)*(phi<-1.386)*0.92673+ (phi>=-1.695)*(phi<-1.436)*0.92673+ (phi>=-1.745)*(phi<-1.695)*0.92673+ (phi>=-1.797)*(phi<-1.745)*0.95991+ (phi>=-1.855)*(phi<-1.797)*0.98444+ (phi>=-2.065)*(phi<-1.855)*0.98444+ (phi>=-2.134)*(phi<-2.065)*0.98444+ (phi>=-2.174)*(phi<-2.134)*0.95991+ (phi>=-2.21)*(phi<-2.174)*0.92673+ (phi>=-2.471)*(phi<-2.21)*0.92673+ (phi>=-2.529)*(phi<-2.471)*0.92673+ (phi>=-2.629)*(phi<-2.529)*0.95991+ (phi>=-2.849)*(phi<-2.629)*0.99351+ (phi>=-2.948)*(phi<-2.849)*0.95991+ (phi>=-3.009)*(phi<-2.948)*0.92673+ (phi>=-3.142)*(phi<-3.009)*0.92673 )+
  (eta>=0.965)*(eta<1.113)*( (phi>=3.009)*(phi<3.142)*0.99268+ (phi>=2.948)*(phi<3.009)*0.99268+ (phi>=2.849)*(phi<2.948)*0.99268+ (phi>=2.629)*(phi<2.849)*0.99268+ (phi>=2.529)*(phi<2.629)*0.99268+ (phi>=2.471)*(phi<2.529)*0.99268+ (phi>=2.21)*(phi<2.471)*0.99268+ (phi>=2.174)*(phi<2.21)*0.99268+ (phi>=2.065)*(phi<2.174)*0.99268+ (phi>=1.855)*(phi<2.065)*0.99268+ (phi>=1.745)*(phi<1.855)*0.99268+ (phi>=1.695)*(phi<1.745)*0.99268+ (phi>=1.436)*(phi<1.695)*0.99268+ (phi>=1.386)*(phi<1.436)*0.99268+ (phi>=1.276)*(phi<1.386)*0.99268+ (phi>=1.066)*(phi<1.276)*0.99268+ (phi>=0.957)*(phi<1.066)*0.99268+ (phi>=0.916)*(phi<0.957)*0.99268+ (phi>=0.657)*(phi<0.916)*0.99268+ (phi>=0.596)*(phi<0.657)*0.99268+ (phi>=0.496)*(phi<0.596)*0.99268+ (phi>=0.277)*(phi<0.496)*0.99268+ (phi>=0.178)*(phi<0.277)*0.99268+ (phi>=0.142)*(phi<0.178)*0.99268+ (phi>=-0.142)*(phi<0.142)*0.99268+ (phi>=-0.178)*(phi<-0.142)*0.99268+ (phi>=-0.277)*(phi<-0.178)*0.99268+ (phi>=-0.496)*(phi<-0.277)*0.99268+ (phi>=-0.596)*(phi<-0.496)*0.99268+ (
phi>=-0.657)*(phi<-0.596)*0.99268+ (phi>=-0.916)*(phi<-0.657)*0.99268+ (phi>=-0.957)*(phi<-0.916)*0.99268+ (phi>=-1.018)*(phi<-0.957)*0.99268+ (phi>=-1.066)*(phi<-1.018)*0.99268+ (phi>=-1.276)*(phi<-1.066)*0.99268+ (phi>=-1.357)*(phi<-1.276)*0.99268+ (phi>=-1.386)*(phi<-1.357)*0.99268+ (phi>=-1.436)*(phi<-1.386)*0.99268+ (phi>=-1.695)*(phi<-1.436)*0.99268+ (phi>=-1.745)*(phi<-1.695)*0.99268+ (phi>=-1.797)*(phi<-1.745)*0.99268+ (phi>=-1.855)*(phi<-1.797)*0.99268+ (phi>=-2.065)*(phi<-1.855)*0.99268+ (phi>=-2.134)*(phi<-2.065)*0.99268+ (phi>=-2.174)*(phi<-2.134)*0.99268+ (phi>=-2.21)*(phi<-2.174)*0.99268+ (phi>=-2.471)*(phi<-2.21)*0.99268+ (phi>=-2.529)*(phi<-2.471)*0.99268+ (phi>=-2.629)*(phi<-2.529)*0.99268+ (phi>=-2.849)*(phi<-2.629)*0.99268+ (phi>=-2.948)*(phi<-2.849)*0.99268+ (phi>=-3.009)*(phi<-2.948)*0.99268+ (phi>=-3.142)*(phi<-3.009)*0.99268 )+
  (eta>=1.113)*(eta<1.163)*( (phi>=3.009)*(phi<3.142)*0.99227+ (phi>=2.948)*(phi<3.009)*0.99413+ (phi>=2.849)*(phi<2.948)*0.99268+ (phi>=2.629)*(phi<2.849)*0.99268+ (phi>=2.529)*(phi<2.629)*0.99268+ (phi>=2.471)*(phi<2.529)*0.99413+ (phi>=2.21)*(phi<2.471)*0.99227+ (phi>=2.174)*(phi<2.21)*0.99413+ (phi>=2.065)*(phi<2.174)*0.99268+ (phi>=1.855)*(phi<2.065)*0.99268+ (phi>=1.745)*(phi<1.855)*0.99268+ (phi>=1.695)*(phi<1.745)*0.99413+ (phi>=1.436)*(phi<1.695)*0.99227+ (phi>=1.386)*(phi<1.436)*0.99413+ (phi>=1.276)*(phi<1.386)*0.99268+ (phi>=1.066)*(phi<1.276)*0.99268+ (phi>=0.957)*(phi<1.066)*0.99268+ (phi>=0.916)*(phi<0.957)*0.99413+ (phi>=0.657)*(phi<0.916)*0.99227+ (phi>=0.596)*(phi<0.657)*0.99413+ (phi>=0.496)*(phi<0.596)*0.99268+ (phi>=0.277)*(phi<0.496)*0.99268+ (phi>=0.178)*(phi<0.277)*0.99268+ (phi>=0.142)*(phi<0.178)*0.99413+ (phi>=-0.142)*(phi<0.142)*0.99227+ (phi>=-0.178)*(phi<-0.142)*0.99413+ (phi>=-0.277)*(phi<-0.178)*0.99268+ (phi>=-0.496)*(phi<-0.277)*0.99268+ (phi>=-0.596)*(phi<-0.496)*0.99268+ (
phi>=-0.657)*(phi<-0.596)*0.99413+ (phi>=-0.916)*(phi<-0.657)*0.99227+ (phi>=-0.957)*(phi<-0.916)*0.99413+ (phi>=-1.018)*(phi<-0.957)*0.99268+ (phi>=-1.066)*(phi<-1.018)*0.99268+ (phi>=-1.276)*(phi<-1.066)*0.99268+ (phi>=-1.357)*(phi<-1.276)*0.99268+ (phi>=-1.386)*(phi<-1.357)*0.99268+ (phi>=-1.436)*(phi<-1.386)*0.99413+ (phi>=-1.695)*(phi<-1.436)*0.99227+ (phi>=-1.745)*(phi<-1.695)*0.99413+ (phi>=-1.797)*(phi<-1.745)*0.99268+ (phi>=-1.855)*(phi<-1.797)*0.99268+ (phi>=-2.065)*(phi<-1.855)*0.99268+ (phi>=-2.134)*(phi<-2.065)*0.99268+ (phi>=-2.174)*(phi<-2.134)*0.99268+ (phi>=-2.21)*(phi<-2.174)*0.99413+ (phi>=-2.471)*(phi<-2.21)*0.99227+ (phi>=-2.529)*(phi<-2.471)*0.99413+ (phi>=-2.629)*(phi<-2.529)*0.99268+ (phi>=-2.849)*(phi<-2.629)*0.99268+ (phi>=-2.948)*(phi<-2.849)*0.99268+ (phi>=-3.009)*(phi<-2.948)*0.99413+ (phi>=-3.142)*(phi<-3.009)*0.99227 )+
  (eta>=1.163)*(eta<1.238)*( (phi>=3.009)*(phi<3.142)*0.99227+ (phi>=2.948)*(phi<3.009)*0.99413+ (phi>=2.849)*(phi<2.948)*0.99413+ (phi>=2.629)*(phi<2.849)*0.99268+ (phi>=2.529)*(phi<2.629)*0.99413+ (phi>=2.471)*(phi<2.529)*0.99413+ (phi>=2.21)*(phi<2.471)*0.99227+ (phi>=2.174)*(phi<2.21)*0.99413+ (phi>=2.065)*(phi<2.174)*0.99413+ (phi>=1.855)*(phi<2.065)*0.99268+ (phi>=1.745)*(phi<1.855)*0.99413+ (phi>=1.695)*(phi<1.745)*0.99413+ (phi>=1.436)*(phi<1.695)*0.99227+ (phi>=1.386)*(phi<1.436)*0.99413+ (phi>=1.276)*(phi<1.386)*0.99413+ (phi>=1.066)*(phi<1.276)*0.99268+ (phi>=0.957)*(phi<1.066)*0.99413+ (phi>=0.916)*(phi<0.957)*0.99413+ (phi>=0.657)*(phi<0.916)*0.99227+ (phi>=0.596)*(phi<0.657)*0.99413+ (phi>=0.496)*(phi<0.596)*0.99413+ (phi>=0.277)*(phi<0.496)*0.99268+ (phi>=0.178)*(phi<0.277)*0.99413+ (phi>=0.142)*(phi<0.178)*0.99413+ (phi>=-0.142)*(phi<0.142)*0.99227+ (phi>=-0.178)*(phi<-0.142)*0.99413+ (phi>=-0.277)*(phi<-0.178)*0.99413+ (phi>=-0.496)*(phi<-0.277)*0.99268+ (phi>=-0.596)*(phi<-0.496)*0.99413+ (
phi>=-0.657)*(phi<-0.596)*0.99413+ (phi>=-0.916)*(phi<-0.657)*0.99227+ (phi>=-0.957)*(phi<-0.916)*0.99413+ (phi>=-1.018)*(phi<-0.957)*0.99413+ (phi>=-1.066)*(phi<-1.018)*0.99413+ (phi>=-1.276)*(phi<-1.066)*0.99268+ (phi>=-1.357)*(phi<-1.276)*0.99413+ (phi>=-1.386)*(phi<-1.357)*0.99413+ (phi>=-1.436)*(phi<-1.386)*0.99413+ (phi>=-1.695)*(phi<-1.436)*0.99227+ (phi>=-1.745)*(phi<-1.695)*0.99413+ (phi>=-1.797)*(phi<-1.745)*0.99413+ (phi>=-1.855)*(phi<-1.797)*0.99413+ (phi>=-2.065)*(phi<-1.855)*0.99268+ (phi>=-2.134)*(phi<-2.065)*0.99413+ (phi>=-2.174)*(phi<-2.134)*0.99413+ (phi>=-2.21)*(phi<-2.174)*0.99413+ (phi>=-2.471)*(phi<-2.21)*0.99227+ (phi>=-2.529)*(phi<-2.471)*0.99413+ (phi>=-2.629)*(phi<-2.529)*0.99413+ (phi>=-2.849)*(phi<-2.629)*0.99268+ (phi>=-2.948)*(phi<-2.849)*0.99413+ (phi>=-3.009)*(phi<-2.948)*0.99413+ (phi>=-3.142)*(phi<-3.009)*0.99227 )+
  (eta>=1.238)*(eta<1.411)*( (phi>=3.009)*(phi<3.142)*0.99227+ (phi>=2.948)*(phi<3.009)*0.99413+ (phi>=2.849)*(phi<2.948)*0.99413+ (phi>=2.629)*(phi<2.849)*0.99413+ (phi>=2.529)*(phi<2.629)*0.99413+ (phi>=2.471)*(phi<2.529)*0.99413+ (phi>=2.21)*(phi<2.471)*0.99227+ (phi>=2.174)*(phi<2.21)*0.99413+ (phi>=2.065)*(phi<2.174)*0.99413+ (phi>=1.855)*(phi<2.065)*0.99413+ (phi>=1.745)*(phi<1.855)*0.99413+ (phi>=1.695)*(phi<1.745)*0.99413+ (phi>=1.436)*(phi<1.695)*0.99227+ (phi>=1.386)*(phi<1.436)*0.99413+ (phi>=1.276)*(phi<1.386)*0.99413+ (phi>=1.066)*(phi<1.276)*0.99413+ (phi>=0.957)*(phi<1.066)*0.99413+ (phi>=0.916)*(phi<0.957)*0.99413+ (phi>=0.657)*(phi<0.916)*0.99227+ (phi>=0.596)*(phi<0.657)*0.99413+ (phi>=0.496)*(phi<0.596)*0.99413+ (phi>=0.277)*(phi<0.496)*0.99413+ (phi>=0.178)*(phi<0.277)*0.99413+ (phi>=0.142)*(phi<0.178)*0.99413+ (phi>=-0.142)*(phi<0.142)*0.99227+ (phi>=-0.178)*(phi<-0.142)*0.99413+ (phi>=-0.277)*(phi<-0.178)*0.99413+ (phi>=-0.496)*(phi<-0.277)*0.99413+ (phi>=-0.596)*(phi<-0.496)*0.99413+ (
phi>=-0.657)*(phi<-0.596)*0.99413+ (phi>=-0.916)*(phi<-0.657)*0.99227+ (phi>=-0.957)*(phi<-0.916)*0.99413+ (phi>=-1.018)*(phi<-0.957)*0.99413+ (phi>=-1.066)*(phi<-1.018)*0.99413+ (phi>=-1.276)*(phi<-1.066)*0.99413+ (phi>=-1.357)*(phi<-1.276)*0.99413+ (phi>=-1.386)*(phi<-1.357)*0.99413+ (phi>=-1.436)*(phi<-1.386)*0.99413+ (phi>=-1.695)*(phi<-1.436)*0.99227+ (phi>=-1.745)*(phi<-1.695)*0.99413+ (phi>=-1.797)*(phi<-1.745)*0.99413+ (phi>=-1.855)*(phi<-1.797)*0.99413+ (phi>=-2.065)*(phi<-1.855)*0.99413+ (phi>=-2.134)*(phi<-2.065)*0.99413+ (phi>=-2.174)*(phi<-2.134)*0.99413+ (phi>=-2.21)*(phi<-2.174)*0.99413+ (phi>=-2.471)*(phi<-2.21)*0.99227+ (phi>=-2.529)*(phi<-2.471)*0.99413+ (phi>=-2.629)*(phi<-2.529)*0.99413+ (phi>=-2.849)*(phi<-2.629)*0.99413+ (phi>=-2.948)*(phi<-2.849)*0.99413+ (phi>=-3.009)*(phi<-2.948)*0.99413+ (phi>=-3.142)*(phi<-3.009)*0.99227 )+
  (eta>=1.411)*(eta<1.709)*( (phi>=3.009)*(phi<3.142)*0.99227+ (phi>=2.948)*(phi<3.009)*0.99413+ (phi>=2.849)*(phi<2.948)*0.99413+ (phi>=2.629)*(phi<2.849)*0.9931+ (phi>=2.529)*(phi<2.629)*0.99413+ (phi>=2.471)*(phi<2.529)*0.99413+ (phi>=2.21)*(phi<2.471)*0.99227+ (phi>=2.174)*(phi<2.21)*0.99413+ (phi>=2.065)*(phi<2.174)*0.99413+ (phi>=1.855)*(phi<2.065)*0.9931+ (phi>=1.745)*(phi<1.855)*0.99413+ (phi>=1.695)*(phi<1.745)*0.99413+ (phi>=1.436)*(phi<1.695)*0.99227+ (phi>=1.386)*(phi<1.436)*0.99413+ (phi>=1.276)*(phi<1.386)*0.99413+ (phi>=1.066)*(phi<1.276)*0.9931+ (phi>=0.957)*(phi<1.066)*0.99413+ (phi>=0.916)*(phi<0.957)*0.99413+ (phi>=0.657)*(phi<0.916)*0.99227+ (phi>=0.596)*(phi<0.657)*0.99413+ (phi>=0.496)*(phi<0.596)*0.99413+ (phi>=0.277)*(phi<0.496)*0.9931+ (phi>=0.178)*(phi<0.277)*0.99413+ (phi>=0.142)*(phi<0.178)*0.99413+ (phi>=-0.142)*(phi<0.142)*0.99227+ (phi>=-0.178)*(phi<-0.142)*0.99413+ (phi>=-0.277)*(phi<-0.178)*0.99413+ (phi>=-0.496)*(phi<-0.277)*0.9931+ (phi>=-0.596)*(phi<-0.496)*0.99413+ (phi>=-
0.657)*(phi<-0.596)*0.99413+ (phi>=-0.916)*(phi<-0.657)*0.99227+ (phi>=-0.957)*(phi<-0.916)*0.99413+ (phi>=-1.018)*(phi<-0.957)*0.99413+ (phi>=-1.066)*(phi<-1.018)*0.99413+ (phi>=-1.276)*(phi<-1.066)*0.9931+ (phi>=-1.357)*(phi<-1.276)*0.99413+ (phi>=-1.386)*(phi<-1.357)*0.99413+ (phi>=-1.436)*(phi<-1.386)*0.99413+ (phi>=-1.695)*(phi<-1.436)*0.99227+ (phi>=-1.745)*(phi<-1.695)*0.99413+ (phi>=-1.797)*(phi<-1.745)*0.99413+ (phi>=-1.855)*(phi<-1.797)*0.99413+ (phi>=-2.065)*(phi<-1.855)*0.9931+ (phi>=-2.134)*(phi<-2.065)*0.99413+ (phi>=-2.174)*(phi<-2.134)*0.99413+ (phi>=-2.21)*(phi<-2.174)*0.99413+ (phi>=-2.471)*(phi<-2.21)*0.99227+ (phi>=-2.529)*(phi<-2.471)*0.99413+ (phi>=-2.629)*(phi<-2.529)*0.99413+ (phi>=-2.849)*(phi<-2.629)*0.9931+ (phi>=-2.948)*(phi<-2.849)*0.99413+ (phi>=-3.009)*(phi<-2.948)*0.99413+ (phi>=-3.142)*(phi<-3.009)*0.99227 )+
  (eta>=1.709)*(eta<1.955)*( (phi>=3.009)*(phi<3.142)*0.99227+ (phi>=2.948)*(phi<3.009)*0.99413+ (phi>=2.849)*(phi<2.948)*0.99413+ (phi>=2.629)*(phi<2.849)*0.99413+ (phi>=2.529)*(phi<2.629)*0.99413+ (phi>=2.471)*(phi<2.529)*0.99413+ (phi>=2.21)*(phi<2.471)*0.99227+ (phi>=2.174)*(phi<2.21)*0.99413+ (phi>=2.065)*(phi<2.174)*0.99413+ (phi>=1.855)*(phi<2.065)*0.99413+ (phi>=1.745)*(phi<1.855)*0.99413+ (phi>=1.695)*(phi<1.745)*0.99413+ (phi>=1.436)*(phi<1.695)*0.99227+ (phi>=1.386)*(phi<1.436)*0.99413+ (phi>=1.276)*(phi<1.386)*0.99413+ (phi>=1.066)*(phi<1.276)*0.99413+ (phi>=0.957)*(phi<1.066)*0.99413+ (phi>=0.916)*(phi<0.957)*0.99413+ (phi>=0.657)*(phi<0.916)*0.99227+ (phi>=0.596)*(phi<0.657)*0.99413+ (phi>=0.496)*(phi<0.596)*0.99413+ (phi>=0.277)*(phi<0.496)*0.99413+ (phi>=0.178)*(phi<0.277)*0.99413+ (phi>=0.142)*(phi<0.178)*0.99413+ (phi>=-0.142)*(phi<0.142)*0.99227+ (phi>=-0.178)*(phi<-0.142)*0.99413+ (phi>=-0.277)*(phi<-0.178)*0.99413+ (phi>=-0.496)*(phi<-0.277)*0.99413+ (phi>=-0.596)*(phi<-0.496)*0.99413+ (
phi>=-0.657)*(phi<-0.596)*0.99413+ (phi>=-0.916)*(phi<-0.657)*0.99227+ (phi>=-0.957)*(phi<-0.916)*0.99413+ (phi>=-1.018)*(phi<-0.957)*0.99413+ (phi>=-1.066)*(phi<-1.018)*0.99413+ (phi>=-1.276)*(phi<-1.066)*0.99413+ (phi>=-1.357)*(phi<-1.276)*0.99413+ (phi>=-1.386)*(phi<-1.357)*0.99413+ (phi>=-1.436)*(phi<-1.386)*0.99413+ (phi>=-1.695)*(phi<-1.436)*0.99227+ (phi>=-1.745)*(phi<-1.695)*0.99413+ (phi>=-1.797)*(phi<-1.745)*0.99413+ (phi>=-1.855)*(phi<-1.797)*0.99413+ (phi>=-2.065)*(phi<-1.855)*0.99413+ (phi>=-2.134)*(phi<-2.065)*0.99413+ (phi>=-2.174)*(phi<-2.134)*0.99413+ (phi>=-2.21)*(phi<-2.174)*0.99413+ (phi>=-2.471)*(phi<-2.21)*0.99227+ (phi>=-2.529)*(phi<-2.471)*0.99413+ (phi>=-2.629)*(phi<-2.529)*0.99413+ (phi>=-2.849)*(phi<-2.629)*0.99413+ (phi>=-2.948)*(phi<-2.849)*0.99413+ (phi>=-3.009)*(phi<-2.948)*0.99413+ (phi>=-3.142)*(phi<-3.009)*0.99227 )+
  (eta>=1.955)*(eta<2.005)*( (phi>=3.009)*(phi<3.142)*0.99227+ (phi>=2.948)*(phi<3.009)*0.99413+ (phi>=2.849)*(phi<2.948)*0.9832+ (phi>=2.629)*(phi<2.849)*0.9832+ (phi>=2.529)*(phi<2.629)*0.9832+ (phi>=2.471)*(phi<2.529)*0.99413+ (phi>=2.21)*(phi<2.471)*0.99227+ (phi>=2.174)*(phi<2.21)*0.99413+ (phi>=2.065)*(phi<2.174)*0.9832+ (phi>=1.855)*(phi<2.065)*0.9832+ (phi>=1.745)*(phi<1.855)*0.9832+ (phi>=1.695)*(phi<1.745)*0.99413+ (phi>=1.436)*(phi<1.695)*0.99227+ (phi>=1.386)*(phi<1.436)*0.99413+ (phi>=1.276)*(phi<1.386)*0.9832+ (phi>=1.066)*(phi<1.276)*0.9832+ (phi>=0.957)*(phi<1.066)*0.9832+ (phi>=0.916)*(phi<0.957)*0.99413+ (phi>=0.657)*(phi<0.916)*0.99227+ (phi>=0.596)*(phi<0.657)*0.99413+ (phi>=0.496)*(phi<0.596)*0.9832+ (phi>=0.277)*(phi<0.496)*0.9832+ (phi>=0.178)*(phi<0.277)*0.9832+ (phi>=0.142)*(phi<0.178)*0.99413+ (phi>=-0.142)*(phi<0.142)*0.99227+ (phi>=-0.178)*(phi<-0.142)*0.99413+ (phi>=-0.277)*(phi<-0.178)*0.9832+ (phi>=-0.496)*(phi<-0.277)*0.9832+ (phi>=-0.596)*(phi<-0.496)*0.9832+ (phi>=-0.657)*(
phi<-0.596)*0.99413+ (phi>=-0.916)*(phi<-0.657)*0.99227+ (phi>=-0.957)*(phi<-0.916)*0.99413+ (phi>=-1.018)*(phi<-0.957)*0.9832+ (phi>=-1.066)*(phi<-1.018)*0.9832+ (phi>=-1.276)*(phi<-1.066)*0.9832+ (phi>=-1.357)*(phi<-1.276)*0.9832+ (phi>=-1.386)*(phi<-1.357)*0.9832+ (phi>=-1.436)*(phi<-1.386)*0.99413+ (phi>=-1.695)*(phi<-1.436)*0.99227+ (phi>=-1.745)*(phi<-1.695)*0.99413+ (phi>=-1.797)*(phi<-1.745)*0.9832+ (phi>=-1.855)*(phi<-1.797)*0.9832+ (phi>=-2.065)*(phi<-1.855)*0.9832+ (phi>=-2.134)*(phi<-2.065)*0.9832+ (phi>=-2.174)*(phi<-2.134)*0.9832+ (phi>=-2.21)*(phi<-2.174)*0.99413+ (phi>=-2.471)*(phi<-2.21)*0.99227+ (phi>=-2.529)*(phi<-2.471)*0.99413+ (phi>=-2.629)*(phi<-2.529)*0.9832+ (phi>=-2.849)*(phi<-2.629)*0.9832+ (phi>=-2.948)*(phi<-2.849)*0.9832+ (phi>=-3.009)*(phi<-2.948)*0.99413+ (phi>=-3.142)*(phi<-3.009)*0.99227 )+
  (eta>=2.005)*(eta<2.5)*( (phi>=3.009)*(phi<3.142)*0.98825+ (phi>=2.948)*(phi<3.009)*0.9832+ (phi>=2.849)*(phi<2.948)*0.9832+ (phi>=2.629)*(phi<2.849)*0.9832+ (phi>=2.529)*(phi<2.629)*0.9832+ (phi>=2.471)*(phi<2.529)*0.9832+ (phi>=2.21)*(phi<2.471)*0.98825+ (phi>=2.174)*(phi<2.21)*0.9832+ (phi>=2.065)*(phi<2.174)*0.9832+ (phi>=1.855)*(phi<2.065)*0.9832+ (phi>=1.745)*(phi<1.855)*0.9832+ (phi>=1.695)*(phi<1.745)*0.9832+ (phi>=1.436)*(phi<1.695)*0.98825+ (phi>=1.386)*(phi<1.436)*0.9832+ (phi>=1.276)*(phi<1.386)*0.9832+ (phi>=1.066)*(phi<1.276)*0.9832+ (phi>=0.957)*(phi<1.066)*0.9832+ (phi>=0.916)*(phi<0.957)*0.9832+ (phi>=0.657)*(phi<0.916)*0.98825+ (phi>=0.596)*(phi<0.657)*0.9832+ (phi>=0.496)*(phi<0.596)*0.9832+ (phi>=0.277)*(phi<0.496)*0.9832+ (phi>=0.178)*(phi<0.277)*0.9832+ (phi>=0.142)*(phi<0.178)*0.9832+ (phi>=-0.142)*(phi<0.142)*0.98825+ (phi>=-0.178)*(phi<-0.142)*0.9832+ (phi>=-0.277)*(phi<-0.178)*0.9832+ (phi>=-0.496)*(phi<-0.277)*0.9832+ (phi>=-0.596)*(phi<-0.496)*0.9832+ (phi>=-0.657)*(phi<-0.596)*
0.9832+ (phi>=-0.916)*(phi<-0.657)*0.98825+ (phi>=-0.957)*(phi<-0.916)*0.9832+ (phi>=-1.018)*(phi<-0.957)*0.9832+ (phi>=-1.066)*(phi<-1.018)*0.9832+ (phi>=-1.276)*(phi<-1.066)*0.9832+ (phi>=-1.357)*(phi<-1.276)*0.9832+ (phi>=-1.386)*(phi<-1.357)*0.9832+ (phi>=-1.436)*(phi<-1.386)*0.9832+ (phi>=-1.695)*(phi<-1.436)*0.98825+ (phi>=-1.745)*(phi<-1.695)*0.9832+ (phi>=-1.797)*(phi<-1.745)*0.9832+ (phi>=-1.855)*(phi<-1.797)*0.9832+ (phi>=-2.065)*(phi<-1.855)*0.9832+ (phi>=-2.134)*(phi<-2.065)*0.9832+ (phi>=-2.174)*(phi<-2.134)*0.9832+ (phi>=-2.21)*(phi<-2.174)*0.9832+ (phi>=-2.471)*(phi<-2.21)*0.98825+ (phi>=-2.529)*(phi<-2.471)*0.9832+ (phi>=-2.629)*(phi<-2.529)*0.9832+ (phi>=-2.849)*(phi<-2.629)*0.9832+ (phi>=-2.948)*(phi<-2.849)*0.9832+ (phi>=-3.009)*(phi<-2.948)*0.9832+ (phi>=-3.142)*(phi<-3.009)*0.98825 )
  )}
}
"""
    #Jamie has added extra 0.98 factor. 
    # old code for pt > 80 GeV, now removed: (0.95*(pt > 80.0) + (pt<80.0))*
    elif category == "2c":
      module_name = "MuonEfficiencyATLASChain2Comb"
      module_string = """
module Efficiency MuonEfficiencyATLASChain2Comb {
  set InputArray MuonMomentumSmearingATLAS/muons
  
  set FlagValue 2
  set AddFlag true
  set KillUponFail false

  
  set EfficiencyFormula { \ 
  ((abs(eta) < 0.1)*1. + (abs(eta) >= 0.1)*(
  (eta>=-2.5)*(eta<-2.005)*( (phi>=3.009)*(phi<3.142)*0.97785+ (phi>=2.948)*(phi<3.009)*0.97637+ (phi>=2.849)*(phi<2.948)*0.97637+ (phi>=2.629)*(phi<2.849)*0.97637+ (phi>=2.529)*(phi<2.629)*0.97637+ (phi>=2.471)*(phi<2.529)*0.97637+ (phi>=2.21)*(phi<2.471)*0.97785+ (phi>=2.174)*(phi<2.21)*0.97637+ (phi>=2.065)*(phi<2.174)*0.97637+ (phi>=1.855)*(phi<2.065)*0.97637+ (phi>=1.745)*(phi<1.855)*0.97637+ (phi>=1.695)*(phi<1.745)*0.97637+ (phi>=1.436)*(phi<1.695)*0.97785+ (phi>=1.386)*(phi<1.436)*0.97637+ (phi>=1.276)*(phi<1.386)*0.97637+ (phi>=1.066)*(phi<1.276)*0.97637+ (phi>=0.957)*(phi<1.066)*0.97637+ (phi>=0.916)*(phi<0.957)*0.97637+ (phi>=0.657)*(phi<0.916)*0.97785+ (phi>=0.596)*(phi<0.657)*0.97637+ (phi>=0.496)*(phi<0.596)*0.97637+ (phi>=0.277)*(phi<0.496)*0.97637+ (phi>=0.178)*(phi<0.277)*0.97637+ (phi>=0.142)*(phi<0.178)*0.97637+ (phi>=-0.142)*(phi<0.142)*0.97785+ (phi>=-0.178)*(phi<-0.142)*0.97637+ (phi>=-0.277)*(phi<-0.178)*0.97637+ (phi>=-0.496)*(phi<-0.277)*0.97637+ (phi>=-0.596)*(phi<-0.496)*0.97637+ (
phi>=-0.657)*(phi<-0.596)*0.97637+ (phi>=-0.916)*(phi<-0.657)*0.97785+ (phi>=-0.957)*(phi<-0.916)*0.97637+ (phi>=-1.018)*(phi<-0.957)*0.97637+ (phi>=-1.066)*(phi<-1.018)*0.97637+ (phi>=-1.276)*(phi<-1.066)*0.97637+ (phi>=-1.357)*(phi<-1.276)*0.97637+ (phi>=-1.386)*(phi<-1.357)*0.97637+ (phi>=-1.436)*(phi<-1.386)*0.97637+ (phi>=-1.695)*(phi<-1.436)*0.97785+ (phi>=-1.745)*(phi<-1.695)*0.97637+ (phi>=-1.797)*(phi<-1.745)*0.97637+ (phi>=-1.855)*(phi<-1.797)*0.97637+ (phi>=-2.065)*(phi<-1.855)*0.97637+ (phi>=-2.134)*(phi<-2.065)*0.97637+ (phi>=-2.174)*(phi<-2.134)*0.97637+ (phi>=-2.21)*(phi<-2.174)*0.97637+ (phi>=-2.471)*(phi<-2.21)*0.97785+ (phi>=-2.529)*(phi<-2.471)*0.97637+ (phi>=-2.629)*(phi<-2.529)*0.97637+ (phi>=-2.849)*(phi<-2.629)*0.97637+ (phi>=-2.948)*(phi<-2.849)*0.97637+ (phi>=-3.009)*(phi<-2.948)*0.97637+ (phi>=-3.142)*(phi<-3.009)*0.97785 )+
  (eta>=-2.005)*(eta<-1.955)*( (phi>=3.009)*(phi<3.142)*0.97711+ (phi>=2.948)*(phi<3.009)*0.98161+ (phi>=2.849)*(phi<2.948)*0.97637+ (phi>=2.629)*(phi<2.849)*0.97637+ (phi>=2.529)*(phi<2.629)*0.97637+ (phi>=2.471)*(phi<2.529)*0.98161+ (phi>=2.21)*(phi<2.471)*0.97711+ (phi>=2.174)*(phi<2.21)*0.98161+ (phi>=2.065)*(phi<2.174)*0.97637+ (phi>=1.855)*(phi<2.065)*0.97637+ (phi>=1.745)*(phi<1.855)*0.97637+ (phi>=1.695)*(phi<1.745)*0.98161+ (phi>=1.436)*(phi<1.695)*0.97711+ (phi>=1.386)*(phi<1.436)*0.98161+ (phi>=1.276)*(phi<1.386)*0.97637+ (phi>=1.066)*(phi<1.276)*0.97637+ (phi>=0.957)*(phi<1.066)*0.97637+ (phi>=0.916)*(phi<0.957)*0.98161+ (phi>=0.657)*(phi<0.916)*0.97711+ (phi>=0.596)*(phi<0.657)*0.98161+ (phi>=0.496)*(phi<0.596)*0.97637+ (phi>=0.277)*(phi<0.496)*0.97637+ (phi>=0.178)*(phi<0.277)*0.97637+ (phi>=0.142)*(phi<0.178)*0.98161+ (phi>=-0.142)*(phi<0.142)*0.97711+ (phi>=-0.178)*(phi<-0.142)*0.98161+ (phi>=-0.277)*(phi<-0.178)*0.97637+ (phi>=-0.496)*(phi<-0.277)*0.97637+ (phi>=-0.596)*(phi<-0.496)*0.97637+ 
(phi>=-0.657)*(phi<-0.596)*0.98161+ (phi>=-0.916)*(phi<-0.657)*0.97711+ (phi>=-0.957)*(phi<-0.916)*0.98161+ (phi>=-1.018)*(phi<-0.957)*0.97637+ (phi>=-1.066)*(phi<-1.018)*0.97637+ (phi>=-1.276)*(phi<-1.066)*0.97637+ (phi>=-1.357)*(phi<-1.276)*0.97637+ (phi>=-1.386)*(phi<-1.357)*0.97637+ (phi>=-1.436)*(phi<-1.386)*0.98161+ (phi>=-1.695)*(phi<-1.436)*0.97711+ (phi>=-1.745)*(phi<-1.695)*0.98161+ (phi>=-1.797)*(phi<-1.745)*0.97637+ (phi>=-1.855)*(phi<-1.797)*0.97637+ (phi>=-2.065)*(phi<-1.855)*0.97637+ (phi>=-2.134)*(phi<-2.065)*0.97637+ (phi>=-2.174)*(phi<-2.134)*0.97637+ (phi>=-2.21)*(phi<-2.174)*0.98161+ (phi>=-2.471)*(phi<-2.21)*0.97711+ (phi>=-2.529)*(phi<-2.471)*0.98161+ (phi>=-2.629)*(phi<-2.529)*0.97637+ (phi>=-2.849)*(phi<-2.629)*0.97637+ (phi>=-2.948)*(phi<-2.849)*0.97637+ (phi>=-3.009)*(phi<-2.948)*0.98161+ (phi>=-3.142)*(phi<-3.009)*0.97711 )+
  (eta>=-1.955)*(eta<-1.709)*( (phi>=3.009)*(phi<3.142)*0.97711+ (phi>=2.948)*(phi<3.009)*0.98161+ (phi>=2.849)*(phi<2.948)*0.98161+ (phi>=2.629)*(phi<2.849)*0.98161+ (phi>=2.529)*(phi<2.629)*0.98161+ (phi>=2.471)*(phi<2.529)*0.98161+ (phi>=2.21)*(phi<2.471)*0.97711+ (phi>=2.174)*(phi<2.21)*0.98161+ (phi>=2.065)*(phi<2.174)*0.98161+ (phi>=1.855)*(phi<2.065)*0.98161+ (phi>=1.745)*(phi<1.855)*0.98161+ (phi>=1.695)*(phi<1.745)*0.98161+ (phi>=1.436)*(phi<1.695)*0.97711+ (phi>=1.386)*(phi<1.436)*0.98161+ (phi>=1.276)*(phi<1.386)*0.98161+ (phi>=1.066)*(phi<1.276)*0.98161+ (phi>=0.957)*(phi<1.066)*0.98161+ (phi>=0.916)*(phi<0.957)*0.98161+ (phi>=0.657)*(phi<0.916)*0.97711+ (phi>=0.596)*(phi<0.657)*0.98161+ (phi>=0.496)*(phi<0.596)*0.98161+ (phi>=0.277)*(phi<0.496)*0.98161+ (phi>=0.178)*(phi<0.277)*0.98161+ (phi>=0.142)*(phi<0.178)*0.98161+ (phi>=-0.142)*(phi<0.142)*0.97711+ (phi>=-0.178)*(phi<-0.142)*0.98161+ (phi>=-0.277)*(phi<-0.178)*0.98161+ (phi>=-0.496)*(phi<-0.277)*0.98161+ (phi>=-0.596)*(phi<-0.496)*0.98161+ 
(phi>=-0.657)*(phi<-0.596)*0.98161+ (phi>=-0.916)*(phi<-0.657)*0.97711+ (phi>=-0.957)*(phi<-0.916)*0.98161+ (phi>=-1.018)*(phi<-0.957)*0.98161+ (phi>=-1.066)*(phi<-1.018)*0.98161+ (phi>=-1.276)*(phi<-1.066)*0.98161+ (phi>=-1.357)*(phi<-1.276)*0.98161+ (phi>=-1.386)*(phi<-1.357)*0.98161+ (phi>=-1.436)*(phi<-1.386)*0.98161+ (phi>=-1.695)*(phi<-1.436)*0.97711+ (phi>=-1.745)*(phi<-1.695)*0.98161+ (phi>=-1.797)*(phi<-1.745)*0.98161+ (phi>=-1.855)*(phi<-1.797)*0.98161+ (phi>=-2.065)*(phi<-1.855)*0.98161+ (phi>=-2.134)*(phi<-2.065)*0.98161+ (phi>=-2.174)*(phi<-2.134)*0.98161+ (phi>=-2.21)*(phi<-2.174)*0.98161+ (phi>=-2.471)*(phi<-2.21)*0.97711+ (phi>=-2.529)*(phi<-2.471)*0.98161+ (phi>=-2.629)*(phi<-2.529)*0.98161+ (phi>=-2.849)*(phi<-2.629)*0.98161+ (phi>=-2.948)*(phi<-2.849)*0.98161+ (phi>=-3.009)*(phi<-2.948)*0.98161+ (phi>=-3.142)*(phi<-3.009)*0.97711 )+
  (eta>=-1.709)*(eta<-1.411)*( (phi>=3.009)*(phi<3.142)*0.97711+ (phi>=2.948)*(phi<3.009)*0.98161+ (phi>=2.849)*(phi<2.948)*0.98161+ (phi>=2.629)*(phi<2.849)*0.97394+ (phi>=2.529)*(phi<2.629)*0.98161+ (phi>=2.471)*(phi<2.529)*0.98161+ (phi>=2.21)*(phi<2.471)*0.97711+ (phi>=2.174)*(phi<2.21)*0.98161+ (phi>=2.065)*(phi<2.174)*0.98161+ (phi>=1.855)*(phi<2.065)*0.97394+ (phi>=1.745)*(phi<1.855)*0.98161+ (phi>=1.695)*(phi<1.745)*0.98161+ (phi>=1.436)*(phi<1.695)*0.97711+ (phi>=1.386)*(phi<1.436)*0.98161+ (phi>=1.276)*(phi<1.386)*0.98161+ (phi>=1.066)*(phi<1.276)*0.97394+ (phi>=0.957)*(phi<1.066)*0.98161+ (phi>=0.916)*(phi<0.957)*0.98161+ (phi>=0.657)*(phi<0.916)*0.97711+ (phi>=0.596)*(phi<0.657)*0.98161+ (phi>=0.496)*(phi<0.596)*0.98161+ (phi>=0.277)*(phi<0.496)*0.97394+ (phi>=0.178)*(phi<0.277)*0.98161+ (phi>=0.142)*(phi<0.178)*0.98161+ (phi>=-0.142)*(phi<0.142)*0.97711+ (phi>=-0.178)*(phi<-0.142)*0.98161+ (phi>=-0.277)*(phi<-0.178)*0.98161+ (phi>=-0.496)*(phi<-0.277)*0.97394+ (phi>=-0.596)*(phi<-0.496)*0.98161+ 
(phi>=-0.657)*(phi<-0.596)*0.98161+ (phi>=-0.916)*(phi<-0.657)*0.97711+ (phi>=-0.957)*(phi<-0.916)*0.98161+ (phi>=-1.018)*(phi<-0.957)*0.98161+ (phi>=-1.066)*(phi<-1.018)*0.98161+ (phi>=-1.276)*(phi<-1.066)*0.97394+ (phi>=-1.357)*(phi<-1.276)*0.98161+ (phi>=-1.386)*(phi<-1.357)*0.98161+ (phi>=-1.436)*(phi<-1.386)*0.98161+ (phi>=-1.695)*(phi<-1.436)*0.97711+ (phi>=-1.745)*(phi<-1.695)*0.98161+ (phi>=-1.797)*(phi<-1.745)*0.98161+ (phi>=-1.855)*(phi<-1.797)*0.98161+ (phi>=-2.065)*(phi<-1.855)*0.97394+ (phi>=-2.134)*(phi<-2.065)*0.98161+ (phi>=-2.174)*(phi<-2.134)*0.98161+ (phi>=-2.21)*(phi<-2.174)*0.98161+ (phi>=-2.471)*(phi<-2.21)*0.97711+ (phi>=-2.529)*(phi<-2.471)*0.98161+ (phi>=-2.629)*(phi<-2.529)*0.98161+ (phi>=-2.849)*(phi<-2.629)*0.97394+ (phi>=-2.948)*(phi<-2.849)*0.98161+ (phi>=-3.009)*(phi<-2.948)*0.98161+ (phi>=-3.142)*(phi<-3.009)*0.97711 )+
  (eta>=-1.411)*(eta<-1.238)*( (phi>=3.009)*(phi<3.142)*0.97711+ (phi>=2.948)*(phi<3.009)*0.98161+ (phi>=2.849)*(phi<2.948)*0.98161+ (phi>=2.629)*(phi<2.849)*0.98161+ (phi>=2.529)*(phi<2.629)*0.98161+ (phi>=2.471)*(phi<2.529)*0.98161+ (phi>=2.21)*(phi<2.471)*0.97711+ (phi>=2.174)*(phi<2.21)*0.98161+ (phi>=2.065)*(phi<2.174)*0.98161+ (phi>=1.855)*(phi<2.065)*0.98161+ (phi>=1.745)*(phi<1.855)*0.98161+ (phi>=1.695)*(phi<1.745)*0.98161+ (phi>=1.436)*(phi<1.695)*0.97711+ (phi>=1.386)*(phi<1.436)*0.98161+ (phi>=1.276)*(phi<1.386)*0.98161+ (phi>=1.066)*(phi<1.276)*0.98161+ (phi>=0.957)*(phi<1.066)*0.98161+ (phi>=0.916)*(phi<0.957)*0.98161+ (phi>=0.657)*(phi<0.916)*0.97711+ (phi>=0.596)*(phi<0.657)*0.98161+ (phi>=0.496)*(phi<0.596)*0.98161+ (phi>=0.277)*(phi<0.496)*0.98161+ (phi>=0.178)*(phi<0.277)*0.98161+ (phi>=0.142)*(phi<0.178)*0.98161+ (phi>=-0.142)*(phi<0.142)*0.97711+ (phi>=-0.178)*(phi<-0.142)*0.98161+ (phi>=-0.277)*(phi<-0.178)*0.98161+ (phi>=-0.496)*(phi<-0.277)*0.98161+ (phi>=-0.596)*(phi<-0.496)*0.98161+ 
(phi>=-0.657)*(phi<-0.596)*0.98161+ (phi>=-0.916)*(phi<-0.657)*0.97711+ (phi>=-0.957)*(phi<-0.916)*0.98161+ (phi>=-1.018)*(phi<-0.957)*0.98161+ (phi>=-1.066)*(phi<-1.018)*0.98161+ (phi>=-1.276)*(phi<-1.066)*0.98161+ (phi>=-1.357)*(phi<-1.276)*0.98161+ (phi>=-1.386)*(phi<-1.357)*0.98161+ (phi>=-1.436)*(phi<-1.386)*0.98161+ (phi>=-1.695)*(phi<-1.436)*0.97711+ (phi>=-1.745)*(phi<-1.695)*0.98161+ (phi>=-1.797)*(phi<-1.745)*0.98161+ (phi>=-1.855)*(phi<-1.797)*0.98161+ (phi>=-2.065)*(phi<-1.855)*0.98161+ (phi>=-2.134)*(phi<-2.065)*0.98161+ (phi>=-2.174)*(phi<-2.134)*0.98161+ (phi>=-2.21)*(phi<-2.174)*0.98161+ (phi>=-2.471)*(phi<-2.21)*0.97711+ (phi>=-2.529)*(phi<-2.471)*0.98161+ (phi>=-2.629)*(phi<-2.529)*0.98161+ (phi>=-2.849)*(phi<-2.629)*0.98161+ (phi>=-2.948)*(phi<-2.849)*0.98161+ (phi>=-3.009)*(phi<-2.948)*0.98161+ (phi>=-3.142)*(phi<-3.009)*0.97711 )+
  (eta>=-1.238)*(eta<-1.163)*( (phi>=3.009)*(phi<3.142)*0.97711+ (phi>=2.948)*(phi<3.009)*0.98161+ (phi>=2.849)*(phi<2.948)*0.98161+ (phi>=2.629)*(phi<2.849)*0.97573+ (phi>=2.529)*(phi<2.629)*0.98161+ (phi>=2.471)*(phi<2.529)*0.98161+ (phi>=2.21)*(phi<2.471)*0.97711+ (phi>=2.174)*(phi<2.21)*0.98161+ (phi>=2.065)*(phi<2.174)*0.98161+ (phi>=1.855)*(phi<2.065)*0.97573+ (phi>=1.745)*(phi<1.855)*0.98161+ (phi>=1.695)*(phi<1.745)*0.98161+ (phi>=1.436)*(phi<1.695)*0.97711+ (phi>=1.386)*(phi<1.436)*0.98161+ (phi>=1.276)*(phi<1.386)*0.98161+ (phi>=1.066)*(phi<1.276)*0.97573+ (phi>=0.957)*(phi<1.066)*0.98161+ (phi>=0.916)*(phi<0.957)*0.98161+ (phi>=0.657)*(phi<0.916)*0.97711+ (phi>=0.596)*(phi<0.657)*0.98161+ (phi>=0.496)*(phi<0.596)*0.98161+ (phi>=0.277)*(phi<0.496)*0.97573+ (phi>=0.178)*(phi<0.277)*0.98161+ (phi>=0.142)*(phi<0.178)*0.98161+ (phi>=-0.142)*(phi<0.142)*0.97711+ (phi>=-0.178)*(phi<-0.142)*0.98161+ (phi>=-0.277)*(phi<-0.178)*0.98161+ (phi>=-0.496)*(phi<-0.277)*0.97573+ (phi>=-0.596)*(phi<-0.496)*0.98161+ 
(phi>=-0.657)*(phi<-0.596)*0.98161+ (phi>=-0.916)*(phi<-0.657)*0.97711+ (phi>=-0.957)*(phi<-0.916)*0.98161+ (phi>=-1.018)*(phi<-0.957)*0.98161+ (phi>=-1.066)*(phi<-1.018)*0.98161+ (phi>=-1.276)*(phi<-1.066)*0.97573+ (phi>=-1.357)*(phi<-1.276)*0.98161+ (phi>=-1.386)*(phi<-1.357)*0.98161+ (phi>=-1.436)*(phi<-1.386)*0.98161+ (phi>=-1.695)*(phi<-1.436)*0.97711+ (phi>=-1.745)*(phi<-1.695)*0.98161+ (phi>=-1.797)*(phi<-1.745)*0.98161+ (phi>=-1.855)*(phi<-1.797)*0.98161+ (phi>=-2.065)*(phi<-1.855)*0.97573+ (phi>=-2.134)*(phi<-2.065)*0.98161+ (phi>=-2.174)*(phi<-2.134)*0.98161+ (phi>=-2.21)*(phi<-2.174)*0.98161+ (phi>=-2.471)*(phi<-2.21)*0.97711+ (phi>=-2.529)*(phi<-2.471)*0.98161+ (phi>=-2.629)*(phi<-2.529)*0.98161+ (phi>=-2.849)*(phi<-2.629)*0.97573+ (phi>=-2.948)*(phi<-2.849)*0.98161+ (phi>=-3.009)*(phi<-2.948)*0.98161+ (phi>=-3.142)*(phi<-3.009)*0.97711 )+
  (eta>=-1.163)*(eta<-1.113)*( (phi>=3.009)*(phi<3.142)*0.97711+ (phi>=2.948)*(phi<3.009)*0.98161+ (phi>=2.849)*(phi<2.948)*0.97573+ (phi>=2.629)*(phi<2.849)*0.97573+ (phi>=2.529)*(phi<2.629)*0.97573+ (phi>=2.471)*(phi<2.529)*0.98161+ (phi>=2.21)*(phi<2.471)*0.97711+ (phi>=2.174)*(phi<2.21)*0.98161+ (phi>=2.065)*(phi<2.174)*0.97573+ (phi>=1.855)*(phi<2.065)*0.97573+ (phi>=1.745)*(phi<1.855)*0.97573+ (phi>=1.695)*(phi<1.745)*0.98161+ (phi>=1.436)*(phi<1.695)*0.97711+ (phi>=1.386)*(phi<1.436)*0.98161+ (phi>=1.276)*(phi<1.386)*0.97573+ (phi>=1.066)*(phi<1.276)*0.97573+ (phi>=0.957)*(phi<1.066)*0.97573+ (phi>=0.916)*(phi<0.957)*0.98161+ (phi>=0.657)*(phi<0.916)*0.97711+ (phi>=0.596)*(phi<0.657)*0.98161+ (phi>=0.496)*(phi<0.596)*0.97573+ (phi>=0.277)*(phi<0.496)*0.97573+ (phi>=0.178)*(phi<0.277)*0.97573+ (phi>=0.142)*(phi<0.178)*0.98161+ (phi>=-0.142)*(phi<0.142)*0.97711+ (phi>=-0.178)*(phi<-0.142)*0.98161+ (phi>=-0.277)*(phi<-0.178)*0.97573+ (phi>=-0.496)*(phi<-0.277)*0.97573+ (phi>=-0.596)*(phi<-0.496)*0.97573+ 
(phi>=-0.657)*(phi<-0.596)*0.98161+ (phi>=-0.916)*(phi<-0.657)*0.97711+ (phi>=-0.957)*(phi<-0.916)*0.98161+ (phi>=-1.018)*(phi<-0.957)*0.97573+ (phi>=-1.066)*(phi<-1.018)*0.97573+ (phi>=-1.276)*(phi<-1.066)*0.97573+ (phi>=-1.357)*(phi<-1.276)*0.97573+ (phi>=-1.386)*(phi<-1.357)*0.97573+ (phi>=-1.436)*(phi<-1.386)*0.98161+ (phi>=-1.695)*(phi<-1.436)*0.97711+ (phi>=-1.745)*(phi<-1.695)*0.98161+ (phi>=-1.797)*(phi<-1.745)*0.97573+ (phi>=-1.855)*(phi<-1.797)*0.97573+ (phi>=-2.065)*(phi<-1.855)*0.97573+ (phi>=-2.134)*(phi<-2.065)*0.97573+ (phi>=-2.174)*(phi<-2.134)*0.97573+ (phi>=-2.21)*(phi<-2.174)*0.98161+ (phi>=-2.471)*(phi<-2.21)*0.97711+ (phi>=-2.529)*(phi<-2.471)*0.98161+ (phi>=-2.629)*(phi<-2.529)*0.97573+ (phi>=-2.849)*(phi<-2.629)*0.97573+ (phi>=-2.948)*(phi<-2.849)*0.97573+ (phi>=-3.009)*(phi<-2.948)*0.98161+ (phi>=-3.142)*(phi<-3.009)*0.97711 )+
  (eta>=-1.113)*(eta<-0.965)*( (phi>=3.009)*(phi<3.142)*0.97573+ (phi>=2.948)*(phi<3.009)*0.97573+ (phi>=2.849)*(phi<2.948)*0.97573+ (phi>=2.629)*(phi<2.849)*0.97573+ (phi>=2.529)*(phi<2.629)*0.97573+ (phi>=2.471)*(phi<2.529)*0.97573+ (phi>=2.21)*(phi<2.471)*0.97573+ (phi>=2.174)*(phi<2.21)*0.97573+ (phi>=2.065)*(phi<2.174)*0.97573+ (phi>=1.855)*(phi<2.065)*0.97573+ (phi>=1.745)*(phi<1.855)*0.97573+ (phi>=1.695)*(phi<1.745)*0.97573+ (phi>=1.436)*(phi<1.695)*0.97573+ (phi>=1.386)*(phi<1.436)*0.97573+ (phi>=1.276)*(phi<1.386)*0.97573+ (phi>=1.066)*(phi<1.276)*0.97573+ (phi>=0.957)*(phi<1.066)*0.97573+ (phi>=0.916)*(phi<0.957)*0.97573+ (phi>=0.657)*(phi<0.916)*0.97573+ (phi>=0.596)*(phi<0.657)*0.97573+ (phi>=0.496)*(phi<0.596)*0.97573+ (phi>=0.277)*(phi<0.496)*0.97573+ (phi>=0.178)*(phi<0.277)*0.97573+ (phi>=0.142)*(phi<0.178)*0.97573+ (phi>=-0.142)*(phi<0.142)*0.97573+ (phi>=-0.178)*(phi<-0.142)*0.97573+ (phi>=-0.277)*(phi<-0.178)*0.97573+ (phi>=-0.496)*(phi<-0.277)*0.97573+ (phi>=-0.596)*(phi<-0.496)*0.97573+ 
(phi>=-0.657)*(phi<-0.596)*0.97573+ (phi>=-0.916)*(phi<-0.657)*0.97573+ (phi>=-0.957)*(phi<-0.916)*0.97573+ (phi>=-1.018)*(phi<-0.957)*0.97573+ (phi>=-1.066)*(phi<-1.018)*0.97573+ (phi>=-1.276)*(phi<-1.066)*0.97573+ (phi>=-1.357)*(phi<-1.276)*0.97573+ (phi>=-1.386)*(phi<-1.357)*0.97573+ (phi>=-1.436)*(phi<-1.386)*0.97573+ (phi>=-1.695)*(phi<-1.436)*0.97573+ (phi>=-1.745)*(phi<-1.695)*0.97573+ (phi>=-1.797)*(phi<-1.745)*0.97573+ (phi>=-1.855)*(phi<-1.797)*0.97573+ (phi>=-2.065)*(phi<-1.855)*0.97573+ (phi>=-2.134)*(phi<-2.065)*0.97573+ (phi>=-2.174)*(phi<-2.134)*0.97573+ (phi>=-2.21)*(phi<-2.174)*0.97573+ (phi>=-2.471)*(phi<-2.21)*0.97573+ (phi>=-2.529)*(phi<-2.471)*0.97573+ (phi>=-2.629)*(phi<-2.529)*0.97573+ (phi>=-2.849)*(phi<-2.629)*0.97573+ (phi>=-2.948)*(phi<-2.849)*0.97573+ (phi>=-3.009)*(phi<-2.948)*0.97573+ (phi>=-3.142)*(phi<-3.009)*0.97573 )+
  (eta>=-0.965)*(eta<-0.817)*( (phi>=3.009)*(phi<3.142)*0.99234+ (phi>=2.948)*(phi<3.009)*0.99234+ (phi>=2.849)*(phi<2.948)*0.98288+ (phi>=2.629)*(phi<2.849)*0.98371+ (phi>=2.529)*(phi<2.629)*0.98288+ (phi>=2.471)*(phi<2.529)*0.99234+ (phi>=2.21)*(phi<2.471)*0.99234+ (phi>=2.174)*(phi<2.21)*0.99234+ (phi>=2.065)*(phi<2.174)*0.98288+ (phi>=1.855)*(phi<2.065)*0.98371+ (phi>=1.745)*(phi<1.855)*0.98288+ (phi>=1.695)*(phi<1.745)*0.99234+ (phi>=1.436)*(phi<1.695)*0.99234+ (phi>=1.386)*(phi<1.436)*0.99234+ (phi>=1.276)*(phi<1.386)*0.98288+ (phi>=1.066)*(phi<1.276)*0.98371+ (phi>=0.957)*(phi<1.066)*0.98288+ (phi>=0.916)*(phi<0.957)*0.99234+ (phi>=0.657)*(phi<0.916)*0.99234+ (phi>=0.596)*(phi<0.657)*0.99234+ (phi>=0.496)*(phi<0.596)*0.98288+ (phi>=0.277)*(phi<0.496)*0.98371+ (phi>=0.178)*(phi<0.277)*0.98288+ (phi>=0.142)*(phi<0.178)*0.99234+ (phi>=-0.142)*(phi<0.142)*0.99234+ (phi>=-0.178)*(phi<-0.142)*0.99234+ (phi>=-0.277)*(phi<-0.178)*0.98288+ (phi>=-0.496)*(phi<-0.277)*0.98371+ (phi>=-0.596)*(phi<-0.496)*0.98288+ 
(phi>=-0.657)*(phi<-0.596)*0.99234+ (phi>=-0.916)*(phi<-0.657)*0.99234+ (phi>=-0.957)*(phi<-0.916)*0.99234+ (phi>=-1.018)*(phi<-0.957)*0.98288+ (phi>=-1.066)*(phi<-1.018)*0.96983+ (phi>=-1.276)*(phi<-1.066)*0.96983+ (phi>=-1.357)*(phi<-1.276)*0.96983+ (phi>=-1.386)*(phi<-1.357)*0.98288+ (phi>=-1.436)*(phi<-1.386)*0.99234+ (phi>=-1.695)*(phi<-1.436)*0.99234+ (phi>=-1.745)*(phi<-1.695)*0.99234+ (phi>=-1.797)*(phi<-1.745)*0.98288+ (phi>=-1.855)*(phi<-1.797)*0.96983+ (phi>=-2.065)*(phi<-1.855)*0.96983+ (phi>=-2.134)*(phi<-2.065)*0.96983+ (phi>=-2.174)*(phi<-2.134)*0.98288+ (phi>=-2.21)*(phi<-2.174)*0.99234+ (phi>=-2.471)*(phi<-2.21)*0.99234+ (phi>=-2.529)*(phi<-2.471)*0.99234+ (phi>=-2.629)*(phi<-2.529)*0.98288+ (phi>=-2.849)*(phi<-2.629)*0.98371+ (phi>=-2.948)*(phi<-2.849)*0.98288+ (phi>=-3.009)*(phi<-2.948)*0.99234+ (phi>=-3.142)*(phi<-3.009)*0.99234 )+
  (eta>=-0.817)*(eta<-0.519)*( (phi>=3.009)*(phi<3.142)*0.99234+ (phi>=2.948)*(phi<3.009)*0.99234+ (phi>=2.849)*(phi<2.948)*0.98288+ (phi>=2.629)*(phi<2.849)*0.98371+ (phi>=2.529)*(phi<2.629)*0.98288+ (phi>=2.471)*(phi<2.529)*0.99234+ (phi>=2.21)*(phi<2.471)*0.99234+ (phi>=2.174)*(phi<2.21)*0.99234+ (phi>=2.065)*(phi<2.174)*0.98288+ (phi>=1.855)*(phi<2.065)*0.98371+ (phi>=1.745)*(phi<1.855)*0.98288+ (phi>=1.695)*(phi<1.745)*0.99234+ (phi>=1.436)*(phi<1.695)*0.99234+ (phi>=1.386)*(phi<1.436)*0.99234+ (phi>=1.276)*(phi<1.386)*0.98288+ (phi>=1.066)*(phi<1.276)*0.98371+ (phi>=0.957)*(phi<1.066)*0.98288+ (phi>=0.916)*(phi<0.957)*0.99234+ (phi>=0.657)*(phi<0.916)*0.99234+ (phi>=0.596)*(phi<0.657)*0.99234+ (phi>=0.496)*(phi<0.596)*0.98288+ (phi>=0.277)*(phi<0.496)*0.98371+ (phi>=0.178)*(phi<0.277)*0.98288+ (phi>=0.142)*(phi<0.178)*0.99234+ (phi>=-0.142)*(phi<0.142)*0.99234+ (phi>=-0.178)*(phi<-0.142)*0.99234+ (phi>=-0.277)*(phi<-0.178)*0.98288+ (phi>=-0.496)*(phi<-0.277)*0.98371+ (phi>=-0.596)*(phi<-0.496)*0.98288+ 
(phi>=-0.657)*(phi<-0.596)*0.99234+ (phi>=-0.916)*(phi<-0.657)*0.99234+ (phi>=-0.957)*(phi<-0.916)*0.99234+ (phi>=-1.018)*(phi<-0.957)*0.98288+ (phi>=-1.066)*(phi<-1.018)*0.96983+ (phi>=-1.276)*(phi<-1.066)*0.96983+ (phi>=-1.357)*(phi<-1.276)*0.96983+ (phi>=-1.386)*(phi<-1.357)*0.96983+ (phi>=-1.436)*(phi<-1.386)*0.96983+ (phi>=-1.695)*(phi<-1.436)*0.96983+ (phi>=-1.745)*(phi<-1.695)*0.96983+ (phi>=-1.797)*(phi<-1.745)*0.96983+ (phi>=-1.855)*(phi<-1.797)*0.96983+ (phi>=-2.065)*(phi<-1.855)*0.96983+ (phi>=-2.134)*(phi<-2.065)*0.96983+ (phi>=-2.174)*(phi<-2.134)*0.98288+ (phi>=-2.21)*(phi<-2.174)*0.99234+ (phi>=-2.471)*(phi<-2.21)*0.99234+ (phi>=-2.529)*(phi<-2.471)*0.99234+ (phi>=-2.629)*(phi<-2.529)*0.98288+ (phi>=-2.849)*(phi<-2.629)*0.98371+ (phi>=-2.948)*(phi<-2.849)*0.98288+ (phi>=-3.009)*(phi<-2.948)*0.99234+ (phi>=-3.142)*(phi<-3.009)*0.99234 )+
  (eta>=-0.519)*(eta<0.519)*( (phi>=3.009)*(phi<3.142)*0.99234+ (phi>=2.948)*(phi<3.009)*0.99234+ (phi>=2.849)*(phi<2.948)*0.98288+ (phi>=2.629)*(phi<2.849)*0.98371+ (phi>=2.529)*(phi<2.629)*0.98288+ (phi>=2.471)*(phi<2.529)*0.99234+ (phi>=2.21)*(phi<2.471)*0.99234+ (phi>=2.174)*(phi<2.21)*0.99234+ (phi>=2.065)*(phi<2.174)*0.98288+ (phi>=1.855)*(phi<2.065)*0.98371+ (phi>=1.745)*(phi<1.855)*0.98288+ (phi>=1.695)*(phi<1.745)*0.99234+ (phi>=1.436)*(phi<1.695)*0.99234+ (phi>=1.386)*(phi<1.436)*0.99234+ (phi>=1.276)*(phi<1.386)*0.98288+ (phi>=1.066)*(phi<1.276)*0.98371+ (phi>=0.957)*(phi<1.066)*0.98288+ (phi>=0.916)*(phi<0.957)*0.99234+ (phi>=0.657)*(phi<0.916)*0.99234+ (phi>=0.596)*(phi<0.657)*0.99234+ (phi>=0.496)*(phi<0.596)*0.98288+ (phi>=0.277)*(phi<0.496)*0.98371+ (phi>=0.178)*(phi<0.277)*0.98288+ (phi>=0.142)*(phi<0.178)*0.99234+ (phi>=-0.142)*(phi<0.142)*0.99234+ (phi>=-0.178)*(phi<-0.142)*0.99234+ (phi>=-0.277)*(phi<-0.178)*0.98288+ (phi>=-0.496)*(phi<-0.277)*0.98371+ (phi>=-0.596)*(phi<-0.496)*0.98288+ (
phi>=-0.657)*(phi<-0.596)*0.99234+ (phi>=-0.916)*(phi<-0.657)*0.99234+ (phi>=-0.957)*(phi<-0.916)*0.99234+ (phi>=-1.018)*(phi<-0.957)*0.98288+ (phi>=-1.066)*(phi<-1.018)*0.96983+ (phi>=-1.276)*(phi<-1.066)*0.96983+ (phi>=-1.357)*(phi<-1.276)*0.96983+ (phi>=-1.386)*(phi<-1.357)*0.98288+ (phi>=-1.436)*(phi<-1.386)*0.99234+ (phi>=-1.695)*(phi<-1.436)*0.99234+ (phi>=-1.745)*(phi<-1.695)*0.99234+ (phi>=-1.797)*(phi<-1.745)*0.98288+ (phi>=-1.855)*(phi<-1.797)*0.96983+ (phi>=-2.065)*(phi<-1.855)*0.96983+ (phi>=-2.134)*(phi<-2.065)*0.96983+ (phi>=-2.174)*(phi<-2.134)*0.98288+ (phi>=-2.21)*(phi<-2.174)*0.99234+ (phi>=-2.471)*(phi<-2.21)*0.99234+ (phi>=-2.529)*(phi<-2.471)*0.99234+ (phi>=-2.629)*(phi<-2.529)*0.98288+ (phi>=-2.849)*(phi<-2.629)*0.98371+ (phi>=-2.948)*(phi<-2.849)*0.98288+ (phi>=-3.009)*(phi<-2.948)*0.99234+ (phi>=-3.142)*(phi<-3.009)*0.99234 )+
  (eta>=0.519)*(eta<0.817)*( (phi>=3.009)*(phi<3.142)*0.99234+ (phi>=2.948)*(phi<3.009)*0.99234+ (phi>=2.849)*(phi<2.948)*0.98288+ (phi>=2.629)*(phi<2.849)*0.98371+ (phi>=2.529)*(phi<2.629)*0.98288+ (phi>=2.471)*(phi<2.529)*0.99234+ (phi>=2.21)*(phi<2.471)*0.99234+ (phi>=2.174)*(phi<2.21)*0.99234+ (phi>=2.065)*(phi<2.174)*0.98288+ (phi>=1.855)*(phi<2.065)*0.98371+ (phi>=1.745)*(phi<1.855)*0.98288+ (phi>=1.695)*(phi<1.745)*0.99234+ (phi>=1.436)*(phi<1.695)*0.99234+ (phi>=1.386)*(phi<1.436)*0.99234+ (phi>=1.276)*(phi<1.386)*0.98288+ (phi>=1.066)*(phi<1.276)*0.98371+ (phi>=0.957)*(phi<1.066)*0.98288+ (phi>=0.916)*(phi<0.957)*0.99234+ (phi>=0.657)*(phi<0.916)*0.99234+ (phi>=0.596)*(phi<0.657)*0.99234+ (phi>=0.496)*(phi<0.596)*0.98288+ (phi>=0.277)*(phi<0.496)*0.98371+ (phi>=0.178)*(phi<0.277)*0.98288+ (phi>=0.142)*(phi<0.178)*0.99234+ (phi>=-0.142)*(phi<0.142)*0.99234+ (phi>=-0.178)*(phi<-0.142)*0.99234+ (phi>=-0.277)*(phi<-0.178)*0.98288+ (phi>=-0.496)*(phi<-0.277)*0.98371+ (phi>=-0.596)*(phi<-0.496)*0.98288+ (
phi>=-0.657)*(phi<-0.596)*0.99234+ (phi>=-0.916)*(phi<-0.657)*0.99234+ (phi>=-0.957)*(phi<-0.916)*0.99234+ (phi>=-1.018)*(phi<-0.957)*0.98288+ (phi>=-1.066)*(phi<-1.018)*0.96983+ (phi>=-1.276)*(phi<-1.066)*0.96983+ (phi>=-1.357)*(phi<-1.276)*0.96983+ (phi>=-1.386)*(phi<-1.357)*0.96983+ (phi>=-1.436)*(phi<-1.386)*0.96983+ (phi>=-1.695)*(phi<-1.436)*0.96983+ (phi>=-1.745)*(phi<-1.695)*0.96983+ (phi>=-1.797)*(phi<-1.745)*0.96983+ (phi>=-1.855)*(phi<-1.797)*0.96983+ (phi>=-2.065)*(phi<-1.855)*0.96983+ (phi>=-2.134)*(phi<-2.065)*0.96983+ (phi>=-2.174)*(phi<-2.134)*0.98288+ (phi>=-2.21)*(phi<-2.174)*0.99234+ (phi>=-2.471)*(phi<-2.21)*0.99234+ (phi>=-2.529)*(phi<-2.471)*0.99234+ (phi>=-2.629)*(phi<-2.529)*0.98288+ (phi>=-2.849)*(phi<-2.629)*0.98371+ (phi>=-2.948)*(phi<-2.849)*0.98288+ (phi>=-3.009)*(phi<-2.948)*0.99234+ (phi>=-3.142)*(phi<-3.009)*0.99234 )+
  (eta>=0.817)*(eta<0.965)*( (phi>=3.009)*(phi<3.142)*0.99234+ (phi>=2.948)*(phi<3.009)*0.99234+ (phi>=2.849)*(phi<2.948)*0.98288+ (phi>=2.629)*(phi<2.849)*0.98371+ (phi>=2.529)*(phi<2.629)*0.98288+ (phi>=2.471)*(phi<2.529)*0.99234+ (phi>=2.21)*(phi<2.471)*0.99234+ (phi>=2.174)*(phi<2.21)*0.99234+ (phi>=2.065)*(phi<2.174)*0.98288+ (phi>=1.855)*(phi<2.065)*0.98371+ (phi>=1.745)*(phi<1.855)*0.98288+ (phi>=1.695)*(phi<1.745)*0.99234+ (phi>=1.436)*(phi<1.695)*0.99234+ (phi>=1.386)*(phi<1.436)*0.99234+ (phi>=1.276)*(phi<1.386)*0.98288+ (phi>=1.066)*(phi<1.276)*0.98371+ (phi>=0.957)*(phi<1.066)*0.98288+ (phi>=0.916)*(phi<0.957)*0.99234+ (phi>=0.657)*(phi<0.916)*0.99234+ (phi>=0.596)*(phi<0.657)*0.99234+ (phi>=0.496)*(phi<0.596)*0.98288+ (phi>=0.277)*(phi<0.496)*0.98371+ (phi>=0.178)*(phi<0.277)*0.98288+ (phi>=0.142)*(phi<0.178)*0.99234+ (phi>=-0.142)*(phi<0.142)*0.99234+ (phi>=-0.178)*(phi<-0.142)*0.99234+ (phi>=-0.277)*(phi<-0.178)*0.98288+ (phi>=-0.496)*(phi<-0.277)*0.98371+ (phi>=-0.596)*(phi<-0.496)*0.98288+ (
phi>=-0.657)*(phi<-0.596)*0.99234+ (phi>=-0.916)*(phi<-0.657)*0.99234+ (phi>=-0.957)*(phi<-0.916)*0.99234+ (phi>=-1.018)*(phi<-0.957)*0.98288+ (phi>=-1.066)*(phi<-1.018)*0.96983+ (phi>=-1.276)*(phi<-1.066)*0.96983+ (phi>=-1.357)*(phi<-1.276)*0.96983+ (phi>=-1.386)*(phi<-1.357)*0.98288+ (phi>=-1.436)*(phi<-1.386)*0.99234+ (phi>=-1.695)*(phi<-1.436)*0.99234+ (phi>=-1.745)*(phi<-1.695)*0.99234+ (phi>=-1.797)*(phi<-1.745)*0.98288+ (phi>=-1.855)*(phi<-1.797)*0.96983+ (phi>=-2.065)*(phi<-1.855)*0.96983+ (phi>=-2.134)*(phi<-2.065)*0.96983+ (phi>=-2.174)*(phi<-2.134)*0.98288+ (phi>=-2.21)*(phi<-2.174)*0.99234+ (phi>=-2.471)*(phi<-2.21)*0.99234+ (phi>=-2.529)*(phi<-2.471)*0.99234+ (phi>=-2.629)*(phi<-2.529)*0.98288+ (phi>=-2.849)*(phi<-2.629)*0.98371+ (phi>=-2.948)*(phi<-2.849)*0.98288+ (phi>=-3.009)*(phi<-2.948)*0.99234+ (phi>=-3.142)*(phi<-3.009)*0.99234 )+
  (eta>=0.965)*(eta<1.113)*( (phi>=3.009)*(phi<3.142)*0.97573+ (phi>=2.948)*(phi<3.009)*0.97573+ (phi>=2.849)*(phi<2.948)*0.97573+ (phi>=2.629)*(phi<2.849)*0.97573+ (phi>=2.529)*(phi<2.629)*0.97573+ (phi>=2.471)*(phi<2.529)*0.97573+ (phi>=2.21)*(phi<2.471)*0.97573+ (phi>=2.174)*(phi<2.21)*0.97573+ (phi>=2.065)*(phi<2.174)*0.97573+ (phi>=1.855)*(phi<2.065)*0.97573+ (phi>=1.745)*(phi<1.855)*0.97573+ (phi>=1.695)*(phi<1.745)*0.97573+ (phi>=1.436)*(phi<1.695)*0.97573+ (phi>=1.386)*(phi<1.436)*0.97573+ (phi>=1.276)*(phi<1.386)*0.97573+ (phi>=1.066)*(phi<1.276)*0.97573+ (phi>=0.957)*(phi<1.066)*0.97573+ (phi>=0.916)*(phi<0.957)*0.97573+ (phi>=0.657)*(phi<0.916)*0.97573+ (phi>=0.596)*(phi<0.657)*0.97573+ (phi>=0.496)*(phi<0.596)*0.97573+ (phi>=0.277)*(phi<0.496)*0.97573+ (phi>=0.178)*(phi<0.277)*0.97573+ (phi>=0.142)*(phi<0.178)*0.97573+ (phi>=-0.142)*(phi<0.142)*0.97573+ (phi>=-0.178)*(phi<-0.142)*0.97573+ (phi>=-0.277)*(phi<-0.178)*0.97573+ (phi>=-0.496)*(phi<-0.277)*0.97573+ (phi>=-0.596)*(phi<-0.496)*0.97573+ (
phi>=-0.657)*(phi<-0.596)*0.97573+ (phi>=-0.916)*(phi<-0.657)*0.97573+ (phi>=-0.957)*(phi<-0.916)*0.97573+ (phi>=-1.018)*(phi<-0.957)*0.97573+ (phi>=-1.066)*(phi<-1.018)*0.97573+ (phi>=-1.276)*(phi<-1.066)*0.97573+ (phi>=-1.357)*(phi<-1.276)*0.97573+ (phi>=-1.386)*(phi<-1.357)*0.97573+ (phi>=-1.436)*(phi<-1.386)*0.97573+ (phi>=-1.695)*(phi<-1.436)*0.97573+ (phi>=-1.745)*(phi<-1.695)*0.97573+ (phi>=-1.797)*(phi<-1.745)*0.97573+ (phi>=-1.855)*(phi<-1.797)*0.97573+ (phi>=-2.065)*(phi<-1.855)*0.97573+ (phi>=-2.134)*(phi<-2.065)*0.97573+ (phi>=-2.174)*(phi<-2.134)*0.97573+ (phi>=-2.21)*(phi<-2.174)*0.97573+ (phi>=-2.471)*(phi<-2.21)*0.97573+ (phi>=-2.529)*(phi<-2.471)*0.97573+ (phi>=-2.629)*(phi<-2.529)*0.97573+ (phi>=-2.849)*(phi<-2.629)*0.97573+ (phi>=-2.948)*(phi<-2.849)*0.97573+ (phi>=-3.009)*(phi<-2.948)*0.97573+ (phi>=-3.142)*(phi<-3.009)*0.97573 )+
  (eta>=1.113)*(eta<1.163)*( (phi>=3.009)*(phi<3.142)*0.97711+ (phi>=2.948)*(phi<3.009)*0.98161+ (phi>=2.849)*(phi<2.948)*0.97573+ (phi>=2.629)*(phi<2.849)*0.97573+ (phi>=2.529)*(phi<2.629)*0.97573+ (phi>=2.471)*(phi<2.529)*0.98161+ (phi>=2.21)*(phi<2.471)*0.97711+ (phi>=2.174)*(phi<2.21)*0.98161+ (phi>=2.065)*(phi<2.174)*0.97573+ (phi>=1.855)*(phi<2.065)*0.97573+ (phi>=1.745)*(phi<1.855)*0.97573+ (phi>=1.695)*(phi<1.745)*0.98161+ (phi>=1.436)*(phi<1.695)*0.97711+ (phi>=1.386)*(phi<1.436)*0.98161+ (phi>=1.276)*(phi<1.386)*0.97573+ (phi>=1.066)*(phi<1.276)*0.97573+ (phi>=0.957)*(phi<1.066)*0.97573+ (phi>=0.916)*(phi<0.957)*0.98161+ (phi>=0.657)*(phi<0.916)*0.97711+ (phi>=0.596)*(phi<0.657)*0.98161+ (phi>=0.496)*(phi<0.596)*0.97573+ (phi>=0.277)*(phi<0.496)*0.97573+ (phi>=0.178)*(phi<0.277)*0.97573+ (phi>=0.142)*(phi<0.178)*0.98161+ (phi>=-0.142)*(phi<0.142)*0.97711+ (phi>=-0.178)*(phi<-0.142)*0.98161+ (phi>=-0.277)*(phi<-0.178)*0.97573+ (phi>=-0.496)*(phi<-0.277)*0.97573+ (phi>=-0.596)*(phi<-0.496)*0.97573+ (
phi>=-0.657)*(phi<-0.596)*0.98161+ (phi>=-0.916)*(phi<-0.657)*0.97711+ (phi>=-0.957)*(phi<-0.916)*0.98161+ (phi>=-1.018)*(phi<-0.957)*0.97573+ (phi>=-1.066)*(phi<-1.018)*0.97573+ (phi>=-1.276)*(phi<-1.066)*0.97573+ (phi>=-1.357)*(phi<-1.276)*0.97573+ (phi>=-1.386)*(phi<-1.357)*0.97573+ (phi>=-1.436)*(phi<-1.386)*0.98161+ (phi>=-1.695)*(phi<-1.436)*0.97711+ (phi>=-1.745)*(phi<-1.695)*0.98161+ (phi>=-1.797)*(phi<-1.745)*0.97573+ (phi>=-1.855)*(phi<-1.797)*0.97573+ (phi>=-2.065)*(phi<-1.855)*0.97573+ (phi>=-2.134)*(phi<-2.065)*0.97573+ (phi>=-2.174)*(phi<-2.134)*0.97573+ (phi>=-2.21)*(phi<-2.174)*0.98161+ (phi>=-2.471)*(phi<-2.21)*0.97711+ (phi>=-2.529)*(phi<-2.471)*0.98161+ (phi>=-2.629)*(phi<-2.529)*0.97573+ (phi>=-2.849)*(phi<-2.629)*0.97573+ (phi>=-2.948)*(phi<-2.849)*0.97573+ (phi>=-3.009)*(phi<-2.948)*0.98161+ (phi>=-3.142)*(phi<-3.009)*0.97711 )+
  (eta>=1.163)*(eta<1.238)*( (phi>=3.009)*(phi<3.142)*0.97711+ (phi>=2.948)*(phi<3.009)*0.98161+ (phi>=2.849)*(phi<2.948)*0.98161+ (phi>=2.629)*(phi<2.849)*0.97573+ (phi>=2.529)*(phi<2.629)*0.98161+ (phi>=2.471)*(phi<2.529)*0.98161+ (phi>=2.21)*(phi<2.471)*0.97711+ (phi>=2.174)*(phi<2.21)*0.98161+ (phi>=2.065)*(phi<2.174)*0.98161+ (phi>=1.855)*(phi<2.065)*0.97573+ (phi>=1.745)*(phi<1.855)*0.98161+ (phi>=1.695)*(phi<1.745)*0.98161+ (phi>=1.436)*(phi<1.695)*0.97711+ (phi>=1.386)*(phi<1.436)*0.98161+ (phi>=1.276)*(phi<1.386)*0.98161+ (phi>=1.066)*(phi<1.276)*0.97573+ (phi>=0.957)*(phi<1.066)*0.98161+ (phi>=0.916)*(phi<0.957)*0.98161+ (phi>=0.657)*(phi<0.916)*0.97711+ (phi>=0.596)*(phi<0.657)*0.98161+ (phi>=0.496)*(phi<0.596)*0.98161+ (phi>=0.277)*(phi<0.496)*0.97573+ (phi>=0.178)*(phi<0.277)*0.98161+ (phi>=0.142)*(phi<0.178)*0.98161+ (phi>=-0.142)*(phi<0.142)*0.97711+ (phi>=-0.178)*(phi<-0.142)*0.98161+ (phi>=-0.277)*(phi<-0.178)*0.98161+ (phi>=-0.496)*(phi<-0.277)*0.97573+ (phi>=-0.596)*(phi<-0.496)*0.98161+ (
phi>=-0.657)*(phi<-0.596)*0.98161+ (phi>=-0.916)*(phi<-0.657)*0.97711+ (phi>=-0.957)*(phi<-0.916)*0.98161+ (phi>=-1.018)*(phi<-0.957)*0.98161+ (phi>=-1.066)*(phi<-1.018)*0.98161+ (phi>=-1.276)*(phi<-1.066)*0.97573+ (phi>=-1.357)*(phi<-1.276)*0.98161+ (phi>=-1.386)*(phi<-1.357)*0.98161+ (phi>=-1.436)*(phi<-1.386)*0.98161+ (phi>=-1.695)*(phi<-1.436)*0.97711+ (phi>=-1.745)*(phi<-1.695)*0.98161+ (phi>=-1.797)*(phi<-1.745)*0.98161+ (phi>=-1.855)*(phi<-1.797)*0.98161+ (phi>=-2.065)*(phi<-1.855)*0.97573+ (phi>=-2.134)*(phi<-2.065)*0.98161+ (phi>=-2.174)*(phi<-2.134)*0.98161+ (phi>=-2.21)*(phi<-2.174)*0.98161+ (phi>=-2.471)*(phi<-2.21)*0.97711+ (phi>=-2.529)*(phi<-2.471)*0.98161+ (phi>=-2.629)*(phi<-2.529)*0.98161+ (phi>=-2.849)*(phi<-2.629)*0.97573+ (phi>=-2.948)*(phi<-2.849)*0.98161+ (phi>=-3.009)*(phi<-2.948)*0.98161+ (phi>=-3.142)*(phi<-3.009)*0.97711 )+
  (eta>=1.238)*(eta<1.411)*( (phi>=3.009)*(phi<3.142)*0.97711+ (phi>=2.948)*(phi<3.009)*0.98161+ (phi>=2.849)*(phi<2.948)*0.98161+ (phi>=2.629)*(phi<2.849)*0.98161+ (phi>=2.529)*(phi<2.629)*0.98161+ (phi>=2.471)*(phi<2.529)*0.98161+ (phi>=2.21)*(phi<2.471)*0.97711+ (phi>=2.174)*(phi<2.21)*0.98161+ (phi>=2.065)*(phi<2.174)*0.98161+ (phi>=1.855)*(phi<2.065)*0.98161+ (phi>=1.745)*(phi<1.855)*0.98161+ (phi>=1.695)*(phi<1.745)*0.98161+ (phi>=1.436)*(phi<1.695)*0.97711+ (phi>=1.386)*(phi<1.436)*0.98161+ (phi>=1.276)*(phi<1.386)*0.98161+ (phi>=1.066)*(phi<1.276)*0.98161+ (phi>=0.957)*(phi<1.066)*0.98161+ (phi>=0.916)*(phi<0.957)*0.98161+ (phi>=0.657)*(phi<0.916)*0.97711+ (phi>=0.596)*(phi<0.657)*0.98161+ (phi>=0.496)*(phi<0.596)*0.98161+ (phi>=0.277)*(phi<0.496)*0.98161+ (phi>=0.178)*(phi<0.277)*0.98161+ (phi>=0.142)*(phi<0.178)*0.98161+ (phi>=-0.142)*(phi<0.142)*0.97711+ (phi>=-0.178)*(phi<-0.142)*0.98161+ (phi>=-0.277)*(phi<-0.178)*0.98161+ (phi>=-0.496)*(phi<-0.277)*0.98161+ (phi>=-0.596)*(phi<-0.496)*0.98161+ (
phi>=-0.657)*(phi<-0.596)*0.98161+ (phi>=-0.916)*(phi<-0.657)*0.97711+ (phi>=-0.957)*(phi<-0.916)*0.98161+ (phi>=-1.018)*(phi<-0.957)*0.98161+ (phi>=-1.066)*(phi<-1.018)*0.98161+ (phi>=-1.276)*(phi<-1.066)*0.98161+ (phi>=-1.357)*(phi<-1.276)*0.98161+ (phi>=-1.386)*(phi<-1.357)*0.98161+ (phi>=-1.436)*(phi<-1.386)*0.98161+ (phi>=-1.695)*(phi<-1.436)*0.97711+ (phi>=-1.745)*(phi<-1.695)*0.98161+ (phi>=-1.797)*(phi<-1.745)*0.98161+ (phi>=-1.855)*(phi<-1.797)*0.98161+ (phi>=-2.065)*(phi<-1.855)*0.98161+ (phi>=-2.134)*(phi<-2.065)*0.98161+ (phi>=-2.174)*(phi<-2.134)*0.98161+ (phi>=-2.21)*(phi<-2.174)*0.98161+ (phi>=-2.471)*(phi<-2.21)*0.97711+ (phi>=-2.529)*(phi<-2.471)*0.98161+ (phi>=-2.629)*(phi<-2.529)*0.98161+ (phi>=-2.849)*(phi<-2.629)*0.98161+ (phi>=-2.948)*(phi<-2.849)*0.98161+ (phi>=-3.009)*(phi<-2.948)*0.98161+ (phi>=-3.142)*(phi<-3.009)*0.97711 )+
  (eta>=1.411)*(eta<1.709)*( (phi>=3.009)*(phi<3.142)*0.97711+ (phi>=2.948)*(phi<3.009)*0.98161+ (phi>=2.849)*(phi<2.948)*0.98161+ (phi>=2.629)*(phi<2.849)*0.97394+ (phi>=2.529)*(phi<2.629)*0.98161+ (phi>=2.471)*(phi<2.529)*0.98161+ (phi>=2.21)*(phi<2.471)*0.97711+ (phi>=2.174)*(phi<2.21)*0.98161+ (phi>=2.065)*(phi<2.174)*0.98161+ (phi>=1.855)*(phi<2.065)*0.97394+ (phi>=1.745)*(phi<1.855)*0.98161+ (phi>=1.695)*(phi<1.745)*0.98161+ (phi>=1.436)*(phi<1.695)*0.97711+ (phi>=1.386)*(phi<1.436)*0.98161+ (phi>=1.276)*(phi<1.386)*0.98161+ (phi>=1.066)*(phi<1.276)*0.97394+ (phi>=0.957)*(phi<1.066)*0.98161+ (phi>=0.916)*(phi<0.957)*0.98161+ (phi>=0.657)*(phi<0.916)*0.97711+ (phi>=0.596)*(phi<0.657)*0.98161+ (phi>=0.496)*(phi<0.596)*0.98161+ (phi>=0.277)*(phi<0.496)*0.97394+ (phi>=0.178)*(phi<0.277)*0.98161+ (phi>=0.142)*(phi<0.178)*0.98161+ (phi>=-0.142)*(phi<0.142)*0.97711+ (phi>=-0.178)*(phi<-0.142)*0.98161+ (phi>=-0.277)*(phi<-0.178)*0.98161+ (phi>=-0.496)*(phi<-0.277)*0.97394+ (phi>=-0.596)*(phi<-0.496)*0.98161+ (
phi>=-0.657)*(phi<-0.596)*0.98161+ (phi>=-0.916)*(phi<-0.657)*0.97711+ (phi>=-0.957)*(phi<-0.916)*0.98161+ (phi>=-1.018)*(phi<-0.957)*0.98161+ (phi>=-1.066)*(phi<-1.018)*0.98161+ (phi>=-1.276)*(phi<-1.066)*0.97394+ (phi>=-1.357)*(phi<-1.276)*0.98161+ (phi>=-1.386)*(phi<-1.357)*0.98161+ (phi>=-1.436)*(phi<-1.386)*0.98161+ (phi>=-1.695)*(phi<-1.436)*0.97711+ (phi>=-1.745)*(phi<-1.695)*0.98161+ (phi>=-1.797)*(phi<-1.745)*0.98161+ (phi>=-1.855)*(phi<-1.797)*0.98161+ (phi>=-2.065)*(phi<-1.855)*0.97394+ (phi>=-2.134)*(phi<-2.065)*0.98161+ (phi>=-2.174)*(phi<-2.134)*0.98161+ (phi>=-2.21)*(phi<-2.174)*0.98161+ (phi>=-2.471)*(phi<-2.21)*0.97711+ (phi>=-2.529)*(phi<-2.471)*0.98161+ (phi>=-2.629)*(phi<-2.529)*0.98161+ (phi>=-2.849)*(phi<-2.629)*0.97394+ (phi>=-2.948)*(phi<-2.849)*0.98161+ (phi>=-3.009)*(phi<-2.948)*0.98161+ (phi>=-3.142)*(phi<-3.009)*0.97711 )+
  (eta>=1.709)*(eta<1.955)*( (phi>=3.009)*(phi<3.142)*0.97711+ (phi>=2.948)*(phi<3.009)*0.98161+ (phi>=2.849)*(phi<2.948)*0.98161+ (phi>=2.629)*(phi<2.849)*0.98161+ (phi>=2.529)*(phi<2.629)*0.98161+ (phi>=2.471)*(phi<2.529)*0.98161+ (phi>=2.21)*(phi<2.471)*0.97711+ (phi>=2.174)*(phi<2.21)*0.98161+ (phi>=2.065)*(phi<2.174)*0.98161+ (phi>=1.855)*(phi<2.065)*0.98161+ (phi>=1.745)*(phi<1.855)*0.98161+ (phi>=1.695)*(phi<1.745)*0.98161+ (phi>=1.436)*(phi<1.695)*0.97711+ (phi>=1.386)*(phi<1.436)*0.98161+ (phi>=1.276)*(phi<1.386)*0.98161+ (phi>=1.066)*(phi<1.276)*0.98161+ (phi>=0.957)*(phi<1.066)*0.98161+ (phi>=0.916)*(phi<0.957)*0.98161+ (phi>=0.657)*(phi<0.916)*0.97711+ (phi>=0.596)*(phi<0.657)*0.98161+ (phi>=0.496)*(phi<0.596)*0.98161+ (phi>=0.277)*(phi<0.496)*0.98161+ (phi>=0.178)*(phi<0.277)*0.98161+ (phi>=0.142)*(phi<0.178)*0.98161+ (phi>=-0.142)*(phi<0.142)*0.97711+ (phi>=-0.178)*(phi<-0.142)*0.98161+ (phi>=-0.277)*(phi<-0.178)*0.98161+ (phi>=-0.496)*(phi<-0.277)*0.98161+ (phi>=-0.596)*(phi<-0.496)*0.98161+ (
phi>=-0.657)*(phi<-0.596)*0.98161+ (phi>=-0.916)*(phi<-0.657)*0.97711+ (phi>=-0.957)*(phi<-0.916)*0.98161+ (phi>=-1.018)*(phi<-0.957)*0.98161+ (phi>=-1.066)*(phi<-1.018)*0.98161+ (phi>=-1.276)*(phi<-1.066)*0.98161+ (phi>=-1.357)*(phi<-1.276)*0.98161+ (phi>=-1.386)*(phi<-1.357)*0.98161+ (phi>=-1.436)*(phi<-1.386)*0.98161+ (phi>=-1.695)*(phi<-1.436)*0.97711+ (phi>=-1.745)*(phi<-1.695)*0.98161+ (phi>=-1.797)*(phi<-1.745)*0.98161+ (phi>=-1.855)*(phi<-1.797)*0.98161+ (phi>=-2.065)*(phi<-1.855)*0.98161+ (phi>=-2.134)*(phi<-2.065)*0.98161+ (phi>=-2.174)*(phi<-2.134)*0.98161+ (phi>=-2.21)*(phi<-2.174)*0.98161+ (phi>=-2.471)*(phi<-2.21)*0.97711+ (phi>=-2.529)*(phi<-2.471)*0.98161+ (phi>=-2.629)*(phi<-2.529)*0.98161+ (phi>=-2.849)*(phi<-2.629)*0.98161+ (phi>=-2.948)*(phi<-2.849)*0.98161+ (phi>=-3.009)*(phi<-2.948)*0.98161+ (phi>=-3.142)*(phi<-3.009)*0.97711 )+
  (eta>=1.955)*(eta<2.005)*( (phi>=3.009)*(phi<3.142)*0.97711+ (phi>=2.948)*(phi<3.009)*0.98161+ (phi>=2.849)*(phi<2.948)*0.97637+ (phi>=2.629)*(phi<2.849)*0.97637+ (phi>=2.529)*(phi<2.629)*0.97637+ (phi>=2.471)*(phi<2.529)*0.98161+ (phi>=2.21)*(phi<2.471)*0.97711+ (phi>=2.174)*(phi<2.21)*0.98161+ (phi>=2.065)*(phi<2.174)*0.97637+ (phi>=1.855)*(phi<2.065)*0.97637+ (phi>=1.745)*(phi<1.855)*0.97637+ (phi>=1.695)*(phi<1.745)*0.98161+ (phi>=1.436)*(phi<1.695)*0.97711+ (phi>=1.386)*(phi<1.436)*0.98161+ (phi>=1.276)*(phi<1.386)*0.97637+ (phi>=1.066)*(phi<1.276)*0.97637+ (phi>=0.957)*(phi<1.066)*0.97637+ (phi>=0.916)*(phi<0.957)*0.98161+ (phi>=0.657)*(phi<0.916)*0.97711+ (phi>=0.596)*(phi<0.657)*0.98161+ (phi>=0.496)*(phi<0.596)*0.97637+ (phi>=0.277)*(phi<0.496)*0.97637+ (phi>=0.178)*(phi<0.277)*0.97637+ (phi>=0.142)*(phi<0.178)*0.98161+ (phi>=-0.142)*(phi<0.142)*0.97711+ (phi>=-0.178)*(phi<-0.142)*0.98161+ (phi>=-0.277)*(phi<-0.178)*0.97637+ (phi>=-0.496)*(phi<-0.277)*0.97637+ (phi>=-0.596)*(phi<-0.496)*0.97637+ (
phi>=-0.657)*(phi<-0.596)*0.98161+ (phi>=-0.916)*(phi<-0.657)*0.97711+ (phi>=-0.957)*(phi<-0.916)*0.98161+ (phi>=-1.018)*(phi<-0.957)*0.97637+ (phi>=-1.066)*(phi<-1.018)*0.97637+ (phi>=-1.276)*(phi<-1.066)*0.97637+ (phi>=-1.357)*(phi<-1.276)*0.97637+ (phi>=-1.386)*(phi<-1.357)*0.97637+ (phi>=-1.436)*(phi<-1.386)*0.98161+ (phi>=-1.695)*(phi<-1.436)*0.97711+ (phi>=-1.745)*(phi<-1.695)*0.98161+ (phi>=-1.797)*(phi<-1.745)*0.97637+ (phi>=-1.855)*(phi<-1.797)*0.97637+ (phi>=-2.065)*(phi<-1.855)*0.97637+ (phi>=-2.134)*(phi<-2.065)*0.97637+ (phi>=-2.174)*(phi<-2.134)*0.97637+ (phi>=-2.21)*(phi<-2.174)*0.98161+ (phi>=-2.471)*(phi<-2.21)*0.97711+ (phi>=-2.529)*(phi<-2.471)*0.98161+ (phi>=-2.629)*(phi<-2.529)*0.97637+ (phi>=-2.849)*(phi<-2.629)*0.97637+ (phi>=-2.948)*(phi<-2.849)*0.97637+ (phi>=-3.009)*(phi<-2.948)*0.98161+ (phi>=-3.142)*(phi<-3.009)*0.97711 )+
  (eta>=2.005)*(eta<2.5)*( (phi>=3.009)*(phi<3.142)*0.97785+ (phi>=2.948)*(phi<3.009)*0.97637+ (phi>=2.849)*(phi<2.948)*0.97637+ (phi>=2.629)*(phi<2.849)*0.97637+ (phi>=2.529)*(phi<2.629)*0.97637+ (phi>=2.471)*(phi<2.529)*0.97637+ (phi>=2.21)*(phi<2.471)*0.97785+ (phi>=2.174)*(phi<2.21)*0.97637+ (phi>=2.065)*(phi<2.174)*0.97637+ (phi>=1.855)*(phi<2.065)*0.97637+ (phi>=1.745)*(phi<1.855)*0.97637+ (phi>=1.695)*(phi<1.745)*0.97637+ (phi>=1.436)*(phi<1.695)*0.97785+ (phi>=1.386)*(phi<1.436)*0.97637+ (phi>=1.276)*(phi<1.386)*0.97637+ (phi>=1.066)*(phi<1.276)*0.97637+ (phi>=0.957)*(phi<1.066)*0.97637+ (phi>=0.916)*(phi<0.957)*0.97637+ (phi>=0.657)*(phi<0.916)*0.97785+ (phi>=0.596)*(phi<0.657)*0.97637+ (phi>=0.496)*(phi<0.596)*0.97637+ (phi>=0.277)*(phi<0.496)*0.97637+ (phi>=0.178)*(phi<0.277)*0.97637+ (phi>=0.142)*(phi<0.178)*0.97637+ (phi>=-0.142)*(phi<0.142)*0.97785+ (phi>=-0.178)*(phi<-0.142)*0.97637+ (phi>=-0.277)*(phi<-0.178)*0.97637+ (phi>=-0.496)*(phi<-0.277)*0.97637+ (phi>=-0.596)*(phi<-0.496)*0.97637+ (
phi>=-0.657)*(phi<-0.596)*0.97637+ (phi>=-0.916)*(phi<-0.657)*0.97785+ (phi>=-0.957)*(phi<-0.916)*0.97637+ (phi>=-1.018)*(phi<-0.957)*0.97637+ (phi>=-1.066)*(phi<-1.018)*0.97637+ (phi>=-1.276)*(phi<-1.066)*0.97637+ (phi>=-1.357)*(phi<-1.276)*0.97637+ (phi>=-1.386)*(phi<-1.357)*0.97637+ (phi>=-1.436)*(phi<-1.386)*0.97637+ (phi>=-1.695)*(phi<-1.436)*0.97785+ (phi>=-1.745)*(phi<-1.695)*0.97637+ (phi>=-1.797)*(phi<-1.745)*0.97637+ (phi>=-1.855)*(phi<-1.797)*0.97637+ (phi>=-2.065)*(phi<-1.855)*0.97637+ (phi>=-2.134)*(phi<-2.065)*0.97637+ (phi>=-2.174)*(phi<-2.134)*0.97637+ (phi>=-2.21)*(phi<-2.174)*0.97637+ (phi>=-2.471)*(phi<-2.21)*0.97785+ (phi>=-2.529)*(phi<-2.471)*0.97637+ (phi>=-2.629)*(phi<-2.529)*0.97637+ (phi>=-2.849)*(phi<-2.629)*0.97637+ (phi>=-2.948)*(phi<-2.849)*0.97637+ (phi>=-3.009)*(phi<-2.948)*0.97637+ (phi>=-3.142)*(phi<-3.009)*0.97785 )
  ))}
}
"""
  elif experiment == "C":
    module_name = "MuonEfficiencyCMS"
    module_string = """
module Efficiency MuonEfficiencyCMS {
  set InputArray MuonMomentumSmearingCMS/muons
  set OutputArray muons

  set EfficiencyFormula {                                      (pt <= 10.0) * (0.00) + \
                                           (abs(eta) <= 1.5) * (pt > 10.0)  * (0.95) + \
                         (abs(eta) > 1.5 && abs(eta) <= 2.4) * (pt > 10.0)  * (0.85) + \
                         (abs(eta) > 2.4)                                   * (0.00)}
}
"""
  else:
    exit("Error: Experiment "+experiment+" not known.")
  return (module_name, module_string)

def set_muon_isolation(n_iso, isolation_set):
  # Define correct candidate input array
  experiment = ""
  suffix = ""
  if isolation_set[0] == "A":
    experiment = "ATLAS"
  elif isolation_set[0] == "C":
    experiment = "CMS"
  else:
    exit("Error: Experiment "+experiment+" not known.")
    
  # Define correct isolation input array  
  isolation_input = "EFlowMerger"+experiment+"/eflow"
  if isolation_set[1] == "t":
    isolation_input = "TrackMerger"+experiment+"/tracks"       
  # Define correct abs_or_rel criterion
  absolute_limit = "false"
  ratio_or_sum = "PTRatioMax"
  if isolation_set[5] == "a":
    absolute_limit = "true"  
    ratio_or_sum = "PTSumMax"       
  module_name = "MuonIsolation"+experiment+str(n_iso)
  module_string = """
module Isolation """+module_name+""" {
  set CandidateInputArray MuonMomentumSmearing"""+experiment+"""/muons
  set IsolationInputArray """+isolation_input+"""
  set OutputArray muons
  
  set KillUponFail false
  set FlagValue """+str(pow(2, n_iso))+"""
  set AddFlag true
  
  set DeltaRMax """+str(eval(isolation_set[2]))+"""
  set PTMin """+str(eval(isolation_set[3]))+"""
  set """+ratio_or_sum+""" """+str(eval(isolation_set[4]))+"""
  set UsePTSum """+absolute_limit+"""
}
"""
  return (module_name, module_string)

def set_missingET(experiment):
  input_muons = ""
  input_flow = ""
  module_name = ""
  if experiment == "A":
    input_flow = "EFlowMergerATLAS/eflow"
    module_name = "MissingETATLAS"
  elif experiment == "C":
    input_flow = "EFlowMergerCMS/eflow"
    module_name = "MissingETCMS"
  module_string = """
module Merger """+module_name+""" {
  add InputArray """+input_flow+"""
  set MomentumOutputArray momentum
}
"""
  return (module_name, module_string)
 
def set_genjet(conedR, ptmin):
  drstring = conedR.replace(".", "d")
  module_name = "GenJetFinder"+drstring
  module_string = """
module FastJetFinder GenJetFinder"""+drstring+""" {
  set InputArray Delphes/stableParticles
  set OutputArray jets

  set JetAlgorithm 6
  set ParameterR """+conedR+"""
  set ConeRadius 0.5
  set SeedThreshold 1.0
  set ConeAreaFraction 1.0
  set AdjacencyCut 2.0
  set OverlapThreshold 0.75
  set MaxIterations 100
  set MaxPairSize 2
  set Iratch 1
  set JetPTMin """+str(ptmin)+"""
}
"""
  return (module_name, module_string)

def set_fastjet_and_constituentfilter(conedR, ptmin, experiment):
  suffix = ""
  if experiment == "A":
    suffix = "ATLAS"
  elif experiment == "C":
    suffix = "CMS"
  drstring = conedR.replace(".", "d")
  module_name = ["FastJetFinderCreate"+suffix+drstring, "FastJetFinder"+suffix+drstring]
  module_string = """
module FastJetFinder FastJetFinderCreate"""+suffix+drstring+""" {
  set InputArray EFlowMerger"""+suffix+"""/eflow
  set OutputArray jets

  set JetAlgorithm 6
  set ParameterR """+conedR+"""
  set ConeRadius 0.5
  set SeedThreshold 1.0
  set ConeAreaFraction 1.0
  set AdjacencyCut 2.0
  set OverlapThreshold 0.75
  set MaxIterations 100
  set MaxPairSize 2
  set Iratch 1
  set JetPTMin """+str(ptmin)+"""
}

module EnergyScale FastJetFinder"""+suffix+drstring+""" {
  set InputArray FastJetFinderCreate"""+suffix+drstring+"""/jets
  set OutputArray jets

 # scale formula for jets
  set ScaleFormula {1.08}
}
"""
  return (module_name, module_string)

def rejection(x):
  A  = 54.3809          
  c  = -4.15601         
  d  = 7.59943          
  f  = -6.72996         
  g  = 2.28954          
  A2 = 5806.98          
  B2 = -24674.2         
  C2 = 39321.6          
  D2 = -27849.7         
  E2 = 7395.3           

  if x < 0.86:
   return pow(10, (A*(x+c*x**2+d*x**3+f*x**4+g*x**5)))
  else:
   return pow(10, A2+B2*x+C2*x**2+D2*x**3+E2*x**4)
 
def c_rejection(x):  
   A = 29.2836
   c = -4.57183
   d = 8.49607
   f = -7.25358
   g = 2.33026  
   return pow(10, (A*(x+c*x**2+d*x**3+f*x**4+g*x**5)))
   
def set_btagger(jet_module, b_eff, n_bflag):
  from math import exp
  x = float(b_eff)/100.
  jet_rej = rejection(x)
  jet_rej_norm = rejection(0.7)
  c_rej = c_rejection(x)
  c_rej_norm = c_rejection(0.7)

#  ljets = "  add EfficiencyFormula {0} {1./(238.65*(pt*pt-33.388*pt+290.796)*exp(-(pt+641.967)*(pt+641.967)/(268.67*268.67))*"+str(jet_rej)+"/"+str(jet_rej_norm)+")}\n"
#  cjets = "  add EfficiencyFormula {4} {"+b_eff+"/70.*(0.460622*1/(1+exp(-0.0463993)*(pt-20.4359)))}\n"

  # Jamie Temp test

#  ljets = "  add EfficiencyFormula {0} {0.}\n"
#  cjets = "  add EfficiencyFormula {4} {0.}\n"


  # Jamie light fake rate with flat tail

#  A = "6.70478"
#  x0 = "-314.552"
#  s = "203.098"
#  b = "-24.7093"
#  c = "13.8598"
#  n = "3.63772"
#  A2 = "0.00034589"

#  ljets = "  add EfficiencyFormula {0} { (pt<=40)*(1./("+A2+"*(pt**"+n+"))) + (pt>40)*(1./(("+A+"*(pt*pt+"+b+"*pt+"+c+")*exp(-(pt-"+x0+")**2/("+s+"**2))+34))) }\n"

# Recovered function with flat tail

  f0 = "0.0105802"
  f1 = "6.46503e-06"
  f2 = "4.02822e-08"

  g0 = "0.00661067"
  g1 = "6.48582e-05"
  g2 = "-3.123e-08"

  # We use a combined version of ATLAS-CONF-2012-040 [3a + 4a] and rescale to the given efficiency using ATLAS-CONF-2012-043 [1a]
  ljets = "  add EfficiencyFormula {0} {0.8*((abs(eta)<=1.3)*("+f0+"+"+f1+"*pt+"+f2+"*pt*pt)+(abs(eta)>1.3)*(abs(eta)<2.5)*("+g0+"+"+g1+"*pt+"+g2+"*pt*pt))*"+str(jet_rej_norm)+"/"+str(jet_rej)+"}\n"

#  ljets = "  add EfficiencyFormula {0} {0.0}\n"

  # The pt distribution is taken from ATLAS-CONF-2012-039 [5a] and is rescaled to the given working point according to ATLAS-CONF-2012-043 [1b]
  cjets = "  add EfficiencyFormula {4} {0.4*(0.460622*1./(1.+exp(-0.0463993*(pt-20.4359))))*"+str(c_rej_norm)+"/"+str(c_rej)+"}\n"

#  cjets = "  add EfficiencyFormula {4} {0.2}\n"  

  # We take a distribution fitted to both ATLAS-CONF-2012-043 (3a) and ATLAS-CONF-2012-097 (10a), assuming a damping for large pt and reducing the total efficiency phenomenologically (in real events, the algorithm most likely do worse than what the given working point efficiency says
  y0 = "0.5523"
  x0 = "47.6071"
  A = "0.2102"
  k = "0.1258"
  r = "308.197"
  # bjets = "  add EfficiencyFormula {5} {"+tag_combo[0]+"/70*("+y0+"+"+A+"*1./(1.+exp(-"+k+"*(pt-"+x0+"))))*(0.7+0.05*exp(-pt/"+r+"))/0.75}\n" Flat in highpt
  # bjets = "  add EfficiencyFormula {5} {"+b_eff+"/70.*("+y0+"+"+A+"*1./(1.+exp(-"+k+"*(pt-"+x0+"))))*(0.7+0.05*exp(-pt/"+r+"))/0.75*((pt>100)*(-0.000902977*pt+0.75962)/(-0.0902977+0.75962)+(pt<=100)*1)}\n"
  # Jamie version below
  bjets = "  add EfficiencyFormula {5} {"+b_eff+"/82.*("+y0+"+"+A+"*1./(1.+exp(-"+k+"*(pt-"+x0+"))))*(0.7+0.05*exp(-pt/"+r+"))/0.75*( (pt>100)*(1.+(pt-100.)*(-0.0007))+(pt<=100)*1)}\n"

  module_name = "BTagging_"+jet_module+"_"+str(b_eff)
  module_string = """
module BTagging """+module_name+""" {
  set PartonInputArray Delphes/partons
  set JetInputArray """+jet_module+"""/jets
    
  set KillUponFail false
  set FlagValue """+str(pow(2, n_bflag))+"""
  set AddFlag true
  
  set DeltaR 0.4
  set PartonPTMin 1.0
  set PartonEtaMax 2.5
  """+ljets+cjets+bjets+"""
  }  
  """  
  return (module_name, module_string)

def set_tautagger(jet_module, experiment):
  suffix = ""
  if experiment =="A":
    suffix = "ATLAS"
  elif experiment == "C":
    suffix = "CMS"
  module_names = ["TauTagging_"+jet_module+"_l", "TauTagging_"+jet_module+"_m", "TauTagging_"+jet_module+"_t"]
  
  x0 = "1.2"
  A  = "(-0.875)"
  s  = "0.294"
  A2 = "0.886"
  s2 = "0.286"
  A3 = "(-0.0268)"
  s3 = "1.16"
  A4 = "0.00419"
  s4 = "10.9"    
  k = "0.94"
  average = "0.955623"
  eff_string_s1loose_eta = "("+k+" + "+A+"*exp(-(abs(eta)-"+x0+")**2/"+s+"**2) + "+A2+"*exp(-(abs(eta)-"+x0+")**2/"+s2+"**2) -"+A3+"*sin(eta)/eta*exp(-eta**2/"+s3+"**2) + "+A4+"*eta**2*exp(-eta**2/"+s4+"**2))/"+average
  x0 = "1.2"
  A = "(-0.283)"
  s = "(-0.303)"
  A2 = "0.309"
  s2 = "(-0.256)"
  A3 = "0.0346"
  s3 = "0.113"
  A4 = "(-0.0796)"
  s4 = "1.25"
  k = "0.91"
  average = "0.877616"
  eff_string_s1medium_eta = "("+k+" + "+A+"*exp(-(abs(eta)-"+x0+")**2/"+s+"**2) + "+A2+"*exp(-(abs(eta)-"+x0+")**2/"+s2+"**2) -"+A3+"*sin(eta)/eta*exp(-eta**2/"+s3+"**2) + "+A4+"*eta**2*exp(-eta**2/"+s4+"**2))/"+average
  x0 = "1.2"
  A  = "(-0.472)"
  s  = "0.304"
  A2 = "0.503"
  s2 = "0.258"
  A3 = "0.0594"
  s3 = "0.102"
  A4 = "(-0.0851)"
  s4 = "1.42"
  k = "0.84"
  average = "0.789361"
  eff_string_s1tight_eta = "("+k+" + "+A+"*exp(-(abs(eta)-"+x0+")**2/"+s+"**2) + "+A2+"*exp(-(abs(eta)-"+x0+")**2/"+s2+"**2) -"+A3+"*sin(eta)/eta*exp(-eta**2/"+s3+"**2) + "+A4+"*eta**2*exp(-eta**2/"+s4+"**2))/"+average
 
  A1 = "0.0354"
  B1 = "0.0994"
  C1 = "0.928"
  D1 = "(-5.52e-05)"  
  E1 = "0.966"
  F1 = "55.1"
  eff_string_s1loose_pt1 = "(pt < 80)*("+C1+"+"+A1+"/(1+exp("+B1+"*(pt-"+F1+")))) + (pt >= 80)*("+D1+"*pt+"+E1+")" 
  A1 = "0.0613"
  B1 = "0.0922"
  C1 = "0.833"
  D1 = "(-0.000190)"
  E1 = "0.893"
  F1 = "57.8"  
  eff_string_s1medium_pt1 = "(pt < 80)*("+C1+"+"+A1+"/(1+exp("+B1+"*(pt-"+F1+")))) + (pt >= 80)*("+D1+"*pt+"+E1+")"
  A1 = "0.0706"
  B1 = "0.140"
  C1 = "0.738"
  D1 = "(-0.000259)"
  E1 = "0.812"
  F1 = "61.4"
  eff_string_s1tight_pt1 = "(pt < 80)*("+C1+"+"+A1+"/(1+exp("+B1+"*(pt-"+F1+")))) + (pt >= 80)*("+D1+"*pt+"+E1+")"
  
  x0 = "15"
  A1 = "0.670"
  A2 = "100"
  A3 = "0.0974"
  A4 = "2.34"
  A5 = "2.04"
  B1 = "(-2.55)"
  B2 = "1.16"
  B3 = "0.427"
  B4 = "0.846"
  C1 = "2.14e-05"    
  C2 = "0.0223"   
  eff_string_s1loose_pt2 = A1+" + (pt < 105)*"+A2+"*sin("+A3+"*(pt-"+x0+")+"+A4+")/pt**"+A5+" + (pt >= 105)*"+A2+"*sin("+A3+"*(105-"+x0+")+"+A4+")/105**"+A5+" + "+B1+"*pt**"+B2+"*exp(-"+B3+"*pt**"+B4+") + (pt < 80 + 2./"+C2+")*"+C1+"*(pt-80)**2*exp(-"+C2+"*(pt-80)) + (pt >= 80 + 2./"+C2+")*"+C1+"*(2./"+C2+")**2*exp(-2.)"
  x0 = "15"
  A1 = "0.586"
  A2 = "100"
  A3 = "0.0997"
  A4 = "2.23"
  A5 = "1.91"
  B1 = "(-2.69)"
  B2 = "1.23"
  B3 = "0.483"
  B4 = "0.791"
  C1 = "3.46e-05"    
  C2 = "0.0223"
  eff_string_s1medium_pt2 = A1+" + (pt < 105)*"+A2+"*sin("+A3+"*(pt-"+x0+")+"+A4+")/pt**"+A5+" + (pt >= 105)*"+A2+"*sin("+A3+"*(105-"+x0+")+"+A4+")/105**"+A5+" + "+B1+"*pt**"+B2+"*exp(-"+B3+"*pt**"+B4+") + (pt < 80 + 2./"+C2+")*"+C1+"*(pt-80)**2*exp(-"+C2+"*(pt-80)) + (pt >= 80 + 2./"+C2+")*"+C1+"*(2./"+C2+")**2*exp(-2.)"
  A1 = "0.388"
  A2 = "100"
  A3 = "0.101"
  A4 = "2.16"
  A5 = "1.79"
  B1 = "(-2.78)"
  B2 = "1.17"
  B3 = "0.377"
  B4 = "0.799"
  C1 = "6.17e-05"   
  C2 = "0.0292"  
  eff_string_s1tight_pt2 = A1+" + (pt < 105)*"+A2+"*sin("+A3+"*(pt-"+x0+")+"+A4+")/pt**"+A5+" + (pt >= 105)*"+A2+"*sin("+A3+"*(105-"+x0+")+"+A4+")/105**"+A5+" + "+B1+"*pt**"+B2+"*exp(-"+B3+"*pt**"+B4+") + (pt < 80 + 2./"+C2+")*"+C1+"*(pt-80)**2*exp(-"+C2+"*(pt-80)) + (pt >= 80 + 2./"+C2+")*"+C1+"*(2./"+C2+")**2*exp(-2.)"
  
  x0 = "15"
  A1 = "0.594"
  A2 = "99.6"
  A3 = "0.0958"
  A4 = "2.09"
  A5 = "1.92"
  B1 = "(-6.44)"
  B2 = "0.143"
  B3 = "0.106"
  B4 = "1.08"
  C1 = "4.22e-05"   
  C2 = "0.0192"
  eff_string_s3loose = A1+" + (pt < 105)*"+A2+"*sin("+A3+"*(pt-"+x0+")+"+A4+")/pt**"+A5+" + (pt >= 105)*"+A2+"*sin("+A3+"*(105-"+x0+")+"+A4+")/105**"+A5+" + "+B1+"*pt**"+B2+"*exp(-"+B3+"*pt**"+B4+") + (pt < 80 + 2./"+C2+")*"+C1+"*(pt-80)**2*exp(-"+C2+"*(pt-80)) + (pt >= 80 + 2./"+C2+")*"+C1+"*(2./"+C2+")**2*exp(-2.)"
  x0 = "15"
  A1 = "0.510"
  A2 = "100"
  A3 = "0.0950"
  A4 = "2.18"
  A5 = "1.86"
  B1 = "(-2.322)"
  B2 = "0.924"
  B3 = "0.233"
  B4 = "0.940"
  C1 = "5.00e-05"    
  C2 = "0.0191"
  eff_string_s3medium = A1+" + (pt < 105)*"+A2+"*sin("+A3+"*(pt-"+x0+")+"+A4+")/pt**"+A5+" + (pt >= 105)*"+A2+"*sin("+A3+"*(105-"+x0+")+"+A4+")/105**"+A5+" + "+B1+"*pt**"+B2+"*exp(-"+B3+"*pt**"+B4+") + (pt < 80 + 2./"+C2+")*"+C1+"*(pt-80)**2*exp(-"+C2+"*(pt-80)) + (pt >= 80 + 2./"+C2+")*"+C1+"*(2./"+C2+")**2*exp(-2.)"
  x0 = "15"
  A1 = "0.324"
  A2 = "100"
  A3 = "0.0971"
  A4 = "2.09"
  A5 = "1.78"
  B1 = "(-2.29)"
  B2 = "0.671"
  B3 = "0.104"
  B4 = "1.096"
  C1 = "6.30e-05"      
  C2 = "0.0212"
  eff_string_s3tight = A1+" + (pt < 105)*"+A2+"*sin("+A3+"*(pt-"+x0+")+"+A4+")/pt**"+A5+" + (pt >= 105)*"+A2+"*sin("+A3+"*(105-"+x0+")+"+A4+")/105**"+A5+" + "+B1+"*pt**"+B2+"*exp(-"+B3+"*pt**"+B4+") + (pt < 80 + 2./"+C2+")*"+C1+"*(pt-80)**2*exp(-"+C2+"*(pt-80)) + (pt >= 80 + 2./"+C2+")*"+C1+"*(2./"+C2+")**2*exp(-2.)"
  
  
  A1 = "0.717"
  B1 = "0.0789"
  C1 = "0.00182"
  D1 = "0.106"
  E1 = "0.0973"
  F1 = "64.3"
  eff_string_b1loose = "(pt < 80)*("+A1+"*exp(-"+B1+"*pt)+"+C1+"*pt)+(pt >= 80)*("+D1+"*(1-1/(1+exp("+E1+"*(pt-"+F1+")))))"
  
  A1 = "0.301"
  B1 = "0.0720"
  C1 = "0.000935"
  D1 = "0.0627"
  E1 = "0.0144"
  F1 = "20.0"
  eff_string_b1medium = "(pt < 80)*("+A1+"*exp(-"+B1+"*pt)+"+C1+"*pt)+(pt >= 80)*("+D1+"*(1-1/(1+exp("+E1+"*(pt-"+F1+")))))"
  
  A1 = "0.117"
  B1 = "0.0742"
  C1 = "0.000359"
  D1 = "0.0192"
  E1 = "0.0247"
  F1 = "46.8"
  eff_string_b1tight = "(pt < 80)*("+A1+"*exp(-"+B1+"*pt)+"+C1+"*pt)+(pt >= 80)*("+D1+"*(1-1/(1+exp("+E1+"*(pt-"+F1+")))))"
  
  A1 = "0.265"
  B1 = "0.0827"
  C1 = "0.000226"
  D1 = "0.0124"
  E1 = "0.0228"
  F1 = "4.08"
  eff_string_b3loose = "(pt < 80)*("+A1+"*exp(-"+B1+"*pt)+"+C1+"*pt)+(pt >= 80)*("+D1+"*(1-1/(1+exp("+E1+"*(pt-"+F1+")))))"
  
  A1 = "0.154"
  B1 = "0.0832"
  C1 = "0.000136"
  D1 = "0.00906"
  E1 = "0.0119"
  F1 = "20.0"
  eff_string_b3medium = "(pt < 80)*("+A1+"*exp(-"+B1+"*pt)+"+C1+"*pt)+(pt >= 80)*("+D1+"*(1-1/(1+exp("+E1+"*(pt-"+F1+")))))"
  
  A1 = "0.0579"
  B1 = "0.0880"
  C1 = "4.08e-05"     
  D1 = "0.00314"
  E1 = "0.0173"
  F1 = "78.9"
  eff_string_b3tight = "(pt < 80)*("+A1+"*exp(-"+B1+"*pt)+"+C1+"*pt)+(pt >= 80)*("+D1+"*(1-1/(1+exp("+E1+"*(pt-"+F1+")))))"
 
  module_string = """
module TauTagging TauTagging_"""+jet_module+"""_l {
  set ParticleInputArray Delphes/allParticles
  set PartonInputArray Delphes/partons
  set TrackInputArray TrackMerger"""+suffix+"""/tracks
  set JetInputArray """+jet_module+"""/jets
   
  set DeltaR 0.2
  set TauPTMin 1.0
  set TauEtaMax 2.5
  
  set KillUponFail false
  set FlagValue 1
  set AddFlag false
  add EfficiencyFormula {1} {("""+eff_string_s1loose_eta+""")*("""+eff_string_s1loose_pt1+""")*("""+eff_string_s1loose_pt2+""")/((abs(eta)<=1.5)*0.95 + (abs(eta)>1.5)*0.85) }
  add EfficiencyFormula {2} {("""+eff_string_s3loose+""")}
  add EfficiencyFormula {-1} {("""+eff_string_b1loose+""")/((abs(eta)<=1.5)*0.95 + (abs(eta)>1.5)*0.85)}
  add EfficiencyFormula {-2} {("""+eff_string_b3loose+""")}
}

module TauTagging TauTagging_"""+jet_module+"""_m {
  set ParticleInputArray Delphes/allParticles
  set PartonInputArray Delphes/partons
  set TrackInputArray TrackMerger"""+suffix+"""/tracks
  set JetInputArray """+jet_module+"""/jets
   
  set DeltaR 0.2
  set TauPTMin 1.0
  set TauEtaMax 2.5
  
  set KillUponFail false
  set FlagValue 2
  set AddFlag false
  
  add EfficiencyFormula {1} {("""+eff_string_s1medium_eta+""")*("""+eff_string_s1medium_pt1+""")*("""+eff_string_s1medium_pt2+""")/((abs(eta)<=1.5)*0.95 + (abs(eta)>1.5)*0.85)}
  add EfficiencyFormula {2} {("""+eff_string_s3medium+""")}
  add EfficiencyFormula {-1} {("""+eff_string_b1medium+""")/((abs(eta)<=1.5)*0.95 + (abs(eta)>1.5)*0.85)}
  add EfficiencyFormula {-2} {("""+eff_string_b3medium+""")}
}


module TauTagging TauTagging_"""+jet_module+"""_t {
  set ParticleInputArray Delphes/allParticles
  set PartonInputArray Delphes/partons
  set TrackInputArray TrackMerger"""+suffix+"""/tracks
  set JetInputArray """+jet_module+"""/jets
   
  set DeltaR 0.2
  set TauPTMin 1.0
  set TauEtaMax 2.5
  
  set KillUponFail false
  set FlagValue 3
  set AddFlag false
  
  add EfficiencyFormula {1} {("""+eff_string_s1tight_eta+""")*("""+eff_string_s1tight_pt1+""")*("""+eff_string_s1tight_pt2+""")/((abs(eta)<=1.5)*0.95 + (abs(eta)>1.5)*0.85)}
  add EfficiencyFormula {2} {("""+eff_string_s3tight+""")}
  add EfficiencyFormula {-1} {("""+eff_string_b1tight+""")/((abs(eta)<=1.5)*0.95 + (abs(eta)>1.5)*0.85)}
  add EfficiencyFormula {-2} {("""+eff_string_b3tight+""")}
}
"""
  return (module_names, module_string)
  
def set_tree_writer(all_branches):  
  module_name = "TreeWriter"
  module_string = """
module TreeWriter TreeWriter {
"""
  for b in all_branches:
    module_string += "  add Branch "+b[0]+" "+b[1]+" "+b[2]+"\n"
  module_string += """}
"""
  return (module_name, module_string)

def set_execution_path(all_modules):
  module_name = "ExecutionPath"
  module_string = """
set ExecutionPath {
"""
  for m in all_modules:
    if m.strip() == "":
      continue
    module_string += "  "+m+"\n"
  module_string += """
}
"""
  return (module_name, module_string)
