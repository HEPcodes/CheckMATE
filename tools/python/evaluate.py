import os

from global_functions import *
from organize_paths_and_files import *
from calculate_cls import *
from likelihood import *
from math import sqrt, fabs

def siground(x, n = 4):
    if x == "_":
      return x
    x = float(x)
    format = "%." + str(n-1) + "f"    
    as_string = format % x
    return as_string

def read_reference_file(reference_file):
  f = open(reference_file)
  header_lines = [] # Header information which should be printed in all output files
  signal_regions = [] # All defined signal regions
  reference_columns = [] # All defined data columns
  reference_data = dict() # Reference data table
  for line in f:
    line = line.rstrip()
    # Ignore empty or commenting lines.
    if line == "" or line[0:2] == "##":
      continue
    # Lines starting with a # contain header information.
    elif line[0] == "#":
      header_lines.append(line)
    # The first line sets all the available reference items.
    elif reference_columns == []:
      line = remove_extra_spaces(line)
      tokens = line.split("  ")
      reference_columns = [c for c in tokens[1:]]
    # Otherwise, save data in reference table
    else:
      line = remove_extra_spaces(line)
      tokens = line.split("  ")
      sr = tokens[0]
      signal_regions.append(sr)
      reference_data[sr] = dict()
      for c in range(len(reference_columns)):
        reference_data[sr][reference_columns[c]] = tokens[c+1]
   
  header_lines.append("")     
  return (header_lines, signal_regions, reference_data)

  
def collect_n_events_per_file(result, files, signal_regions, output):
  # Check if file actually exists / was created. If it does/is not, something went wrong
  if (result['prefix'] not in files['results_signal']) or (not os.path.isfile(files['results_signal'][result['prefix']])):
    exit("ERROR: Required analysis result files do not exist. \n   It is very likely that something went wrong in the delphes and/or the analysis step. \n   Please check \n      "+files['output_log_delphes']+" \n      "+files['output_log_analysis']+" \n   for error messages and, should you not be able to fix them yourself, contact the authors under  \n      checkmate@projects.hepforge.org")
  f = open(files['results_signal'][result['prefix']], "r")
  n_events_per_file = dict()
  n_events_per_file["signal_sumofweights"] = dict() # Sum of weights of all events in a given signal region
  n_events_per_file["signal_sumofweights2"] = dict() # Sum of the squares of all these weights
  n_events_per_file["signal_normevents"] = dict() # Number of physical signal events after normalising to xsect and lumi
  
  n_events_per_file["signal_err_stat"] = dict() # Statistical Error on normalised number of events
  n_events_per_file["signal_err_sys"] = dict() # Systematical Error on normalised number of events
  
  n_events_per_file["total_mcevents"] = n_events_per_file["total_sumofweights"] = n_events_per_file["total_sumofweights2"] = n_events_per_file["total_normevents"] = 0 # As above, but before the analysis
  xsect = xsecterr = 0 # Given cross section and cross section error
  for sr in signal_regions:
    n_events_per_file["signal_sumofweights"][sr] = n_events_per_file["signal_sumofweights2"][sr] = n_events_per_file["signal_normevents"][sr] = n_events_per_file["signal_err_stat"][sr] = n_events_per_file["signal_err_sys"][sr] = 0 # Reset

  for line in f:
    # Ignore empty or commented lines
    line = line.rstrip()
    if line == "" or line[0] == "#":
      continue
      
    # Read file:
    line = remove_extra_spaces(line)
    tokens = [t for t in line.split("  ") if t != ""]
    # First, read information on total event number
    if tokens[0] == "MCEvents:":
      n_events_per_file["total_mcevents"] = float(tokens[1])
    elif tokens[0] == " SumOfWeights:":
      n_events_per_file["total_sumofweights"] = float(tokens[1])
    elif tokens[0] == " SumOfWeights2:":
      n_events_per_file["total_sumofweights2"] = float(tokens[1])
    elif tokens[0] == " NormEvents:":
      n_events_per_file["total_normevents"] = float(tokens[1])
    elif tokens[0] == "XSect:":
      xsect = float(tokens[1].split(" ")[0])
    elif tokens[0] == " Error:":      
      xsecterr = float(tokens[1].split(" ")[0])
    else:
    # SR  Sum_W  Sum_W2  Acc  N_Norm
      for sr in signal_regions:                        
        if tokens[0].startswith(sr):
          # Read number of events
          n_events_per_file["signal_sumofweights"][sr] = float(tokens[1])
          n_events_per_file["signal_sumofweights2"][sr] = float(tokens[2])
          n_events_per_file["signal_normevents"][sr] = float(tokens[4])
          
          if n_events_per_file["signal_sumofweights"][sr] <= 0:
            n_events_per_file["signal_err_stat"][sr] = 0
            n_events_per_file["signal_err_sys"][sr] = 0
          else:
            n_events_per_file["signal_err_stat"][sr] = n_events_per_file["signal_normevents"][sr]*sqrt(n_events_per_file["signal_sumofweights2"][sr])/n_events_per_file["signal_sumofweights"][sr]
            n_events_per_file["signal_err_sys"][sr] = n_events_per_file["signal_normevents"][sr]*xsecterr/xsect
  f.close()
  
  # Print file-wise results
  output.cout(result['prefix']+"  "+siground(n_events_per_file["total_mcevents"])+"  ", "nlb")
  for sr in signal_regions:
    output.cout(siground(n_events_per_file["signal_normevents"][sr])+"  "+siground(n_events_per_file["signal_err_stat"][sr])+"  "+siground(n_events_per_file["signal_err_sys"][sr])+"  ", "nlb")
  output.cout("")
  return n_events_per_file


def collect_n_events_per_process(results_per_process, signal_regions, files, output):
  n_events_per_process = dict()  
  n_events_per_process["signal_sumofweights"] = dict() # Sum of weights of all events in a given signal region
  n_events_per_process["signal_sumofweights2"] = dict() # Sum of the squares of all these weights
  n_events_per_process["signal_normevents"] = dict() # Number of physical signal events after normalising to xsect and lumi
  
  n_events_per_process["signal_err_stat"] = dict() # Statistical Error on normalised number of events
  n_events_per_process["signal_err_sys"] = dict() # Systematical Error on normalised number of events
  
  n_events_per_process["total_mcevents"] = n_events_per_process["total_sumofweights"] = n_events_per_process["total_sumofweights2"] = n_events_per_process["total_normevents"] = 0 # As above, but before the analysis
  for sr in signal_regions:
    n_events_per_process["signal_sumofweights"][sr] = n_events_per_process["signal_sumofweights2"][sr] = n_events_per_process["signal_normevents"][sr] = n_events_per_process["signal_err_stat"][sr] = n_events_per_process["signal_err_sys"][sr] = 0 # Reset

  delta_xsect = 0; # Will store xsecterr/xsect from the file-wise results
  for result in results_per_process:
    # Determine number of events of the given file
    n_events_per_file = collect_n_events_per_file(result, files, signal_regions, output)
    
    # Sum up all weights and all mc events
    n_events_per_process["total_mcevents"] += n_events_per_file["total_mcevents"]
    n_events_per_process["total_sumofweights"] += n_events_per_file["total_sumofweights"]
    n_events_per_process["total_sumofweights2"] += n_events_per_file["total_sumofweights2"]
    n_events_per_process["total_normevents"] = n_events_per_file["total_normevents"] # This number is universal for all files in a given process! It therefore must not be added but can taken from any file
    for sr in signal_regions:
      # Determine weighted average of all runs
      n_events_per_process["signal_sumofweights"][sr] += n_events_per_file["signal_sumofweights"][sr]
      n_events_per_process["signal_sumofweights2"][sr] += n_events_per_file["signal_sumofweights2"][sr]
      if n_events_per_file["signal_normevents"][sr] != 0: # If n == 0, just ignore. Any signal region with n != 0 is enough to define universal delta_xsect
        delta_xsect = n_events_per_file["signal_err_sys"][sr]/n_events_per_file["signal_normevents"][sr] # This number is universal for all signal regions
      
      
  # Find number of events per process and errors by determining the weighted sums  
  for sr in signal_regions:
    n_events_per_process["signal_normevents"][sr] = n_events_per_process["total_normevents"]*n_events_per_process["signal_sumofweights"][sr]/n_events_per_process["total_sumofweights"]
    if n_events_per_process["signal_sumofweights"][sr] <= 0:
      n_events_per_process["signal_err_stat"][sr] = 1.*n_events_per_process["total_normevents"]/n_events_per_process["total_sumofweights"] # Error on 1 Monte Carlo Event
      n_events_per_process["signal_err_sys"][sr] = 0
    else:
      n_events_per_process["signal_err_stat"][sr] = n_events_per_process["total_normevents"]*sqrt(n_events_per_process["signal_sumofweights2"][sr])/(n_events_per_process["total_sumofweights"])
      n_events_per_process["signal_err_sys"][sr] = n_events_per_process["signal_normevents"][sr]*delta_xsect
  
  # Print process-wise result
  output.cout("@--------------------------------------------------------------------------------------------------------------")
  output.cout("Tot  "+siground(n_events_per_process["total_mcevents"])+"  ", "nlb")
  for sr in signal_regions:
    output.cout(siground(n_events_per_process["signal_normevents"][sr])+"  "+siground(n_events_per_process["signal_err_stat"][sr])+"  "+siground(n_events_per_process["signal_err_sys"][sr])+"  ", "nlb")
  output.cout("")
  return n_events_per_process
  
def collect_n_events_per_run(signal_regions, files, output):
  processes = parse_progress(files['output_progress'])   
  
  n_events_per_run = dict()  
  n_events_per_run["signal_normevents"] = dict() # Number of physical signal events after normalising to xsect and lumi  
  n_events_per_run["signal_err_stat"] = dict() # Statistical Error on normalised number of events
  n_events_per_run["signal_err_sys"] = dict() # Systematical Error on normalised number of events
  
  n_events_per_run["total_mcevents"] = 0 
  for sr in signal_regions:
     n_events_per_run["signal_normevents"][sr] = n_events_per_run["signal_err_stat"][sr] = n_events_per_run["signal_err_sys"][sr] = 0 # Reset
  
  output.cout("Prefix  N_TotMC  ", "nlb")
  for sr in signal_regions:
    output.cout(sr+"  stat  sys  ", "nlb")
  output.cout("")  
  for process in processes.keys():
    output.cout("@")
    output.cout("@Process: "+str(process))
    # Determine Number of process-wise signal events.
    
    n_events_per_process = collect_n_events_per_process(processes[process], signal_regions, files, output)
    # Add to total result information
    n_events_per_run["total_mcevents"] += n_events_per_process["total_mcevents"]
    
    for sr in signal_regions:
      n_events_per_run["signal_normevents"][sr] += n_events_per_process["signal_normevents"][sr]
      n_events_per_run["signal_err_stat"][sr] += n_events_per_process["signal_err_stat"][sr]**2 # Added in quadrature
      n_events_per_run["signal_err_sys"][sr] += n_events_per_process["signal_err_sys"][sr]**2 # Added in quadrature
      
  # Print overall result
  output.cout("@")
  output.cout("@==============================================================================================================")
  output.cout("Tot  "+siground(n_events_per_run["total_mcevents"])+"  ", "nlb")
  for sr in signal_regions:
      n_events_per_run["signal_err_stat"][sr] = sqrt(n_events_per_run["signal_err_stat"][sr])
      n_events_per_run["signal_err_sys"][sr] = sqrt(n_events_per_run["signal_err_sys"][sr])
      output.cout(siground(n_events_per_run["signal_normevents"][sr])+"  "+siground(n_events_per_run["signal_err_stat"][sr])+"  "+siground(n_events_per_run["signal_err_sys"][sr])+"  ", "nlb")
  output.cout("")
  return n_events_per_run


def compare_to_cls_limit(reference_data, n_events, sr):
  results = dict()
  results["messages"] = []
  
  # Expected signal events from analyses
  results["signal_events"] = n_events["signal_normevents"][sr]
  results["signal_events_error_stat"] = n_events["signal_err_stat"][sr]
  results["signal_events_error_sys"] = n_events["signal_err_sys"][sr]
  results["signal_events_error_tot"] = sqrt(n_events["signal_err_stat"][sr]**2 + n_events["signal_err_sys"][sr]**2)
    
  results["observed_upper_limit"] = reference_data[sr]["S95_obs"]
  results["r_observed"] = results["signal_events"] / float(results["observed_upper_limit"])
  results["r_observed_cons"] = (results["signal_events"] - 1.95996*results["signal_events_error_tot"]) / float(results["observed_upper_limit"])
  results["r_observed_sysonly"] = (results["signal_events"] - 1.95996*results["signal_events_error_sys"]) / float(results["observed_upper_limit"])
  if results["r_observed_cons"] < 0:
    results["r_observed_cons"] = 0
      
  
  # If no expected upper limit is given, it cannot be evaluated
  if "S95_exp" not in reference_data[sr]:
    results["expected_upper_limit"] = float(reference_data[sr]["S95_obs"])
    results["messages"].append("No expected limit could be found in reference data. Using expected = observed.")
    results["r_expected"] = results["r_observed"]
    results["r_expected_cons"] = results["r_observed_cons"]
  # Otherwise, determine ratio
  else:    
    results["expected_upper_limit"] = float(reference_data[sr]["S95_exp"])
    results["r_expected"] = results["signal_events"] / float(results["expected_upper_limit"])
    results["r_expected_cons"] = (results["signal_events"] - 1.95996*results["signal_events_error_tot"]) / float(results["expected_upper_limit"])
    if results["r_expected_cons"] < 0:
      results["r_expected_cons"] = 0
  
  return results

def calculate_cls_limit(reference_data, n_events, sr, randomseed):
  results = dict()
  results["messages"] = []
  
  # Expected signal events from analyses
  results["signal_events"] = n_events["signal_normevents"][sr]
  results["signal_events_error_stat"] = n_events["signal_err_stat"][sr]
  results["signal_events_error_sys"] = n_events["signal_err_sys"][sr]
  results["signal_events_error_tot"] = sqrt(n_events["signal_err_stat"][sr]**2 + n_events["signal_err_sys"][sr]**2)
  
  # Determine the total background error.
  background_error = 0
  if "bkg_err" in reference_data[sr]:
    background_error = float(reference_data[sr]["bkg_err"])
  elif "bkg_errp" in reference_data[sr]:
    background_error = sqrt(float(reference_data[sr]["bkg_errp"])*float(reference_data[sr]["bkg_errp"])+float(reference_data[sr]["bkg_errm"])*float(reference_data[sr]["bkg_errm"]))/2.
  elif "bkg_err_sys" in reference_data[sr]:
    background_error = sqrt(float(reference_data[sr]["bkg_err_stat"])*float(reference_data[sr]["bkg_err_stat"])+float(reference_data[sr]["bkg_err_sys"])*float(reference_data[sr]["bkg_err_sys"]))
  elif "bkg_err_sysp" in reference_data[sr]:
    background_error = sqrt(float(reference_data[sr]["bkg_err_stat"])*float(reference_data[sr]["bkg_err_stat"])+float(reference_data[sr]["bkg_err_sysp"])*float(reference_data[sr]["bkg_err_sysp"])/4.+float(reference_data[sr]["bkg_err_sysp"])*float(reference_data[sr]["bkg_err_sysp"])/4.)
  else:
    background_error = 0
  reference_data[sr]["bkg_err_tot"] = background_error
  # Determine confidence limits. For conservative limits, use the 95% lower limit on S given 1 sigma delta S.
  if results["signal_events"] <= 0:
    results["expected_cls"] = 1
    results["expected_cls_err"] = 0
  else:
    (results["expected_cls"], results["expected_cls_err"]) = cls(float(reference_data[sr]["bkg"]), background_error, float(reference_data[sr]["bkg"]), results["signal_events"], results["signal_events_error_tot"], randomseed)
  #results["expected_cls_cons"] = 1
  #if results["signal_events"] > 1.95996*results["signal_events_error_tot"]:
  #  results["expected_cls_cons"] = cls(float(reference_data[sr]["bkg"]), background_error, float(reference_data[sr]["bkg"]), results["signal_events"]-1.95996*results["signal_events_error_tot"])[0]
  
  if results["signal_events"] <= 0:
    results["observed_cls"] = 1
    results["observed_cls_err"] = 0
  else:
    (results["observed_cls"], results["observed_cls_err"])  = cls(float(reference_data[sr]["bkg"]), background_error, float(reference_data[sr]["obs"]), results["signal_events"], results["signal_events_error_tot"], randomseed)
  #results["observed_cls_cons"] = 1
  #if results["signal_events"] > 1.95996*results["signal_events_error_tot"]:
  #  results["observed_cls_cons"] = cls(float(reference_data[sr]["bkg"]), background_error, float(reference_data[sr]["obs"]), results["signal_events"]-1.95996*results["signal_events_error_tot"])[0]
  return results

#-----------------------------------------------------------------------------
# Jamie added

def calculate_likelihood(reference_data, n_events, sr, randomseed):
  results = dict()
  results["messages"] = []
  
  # Expected signal events from analyses
  results["signal_events"] = n_events["signal_normevents"][sr]
  results["signal_events_error_stat"] =  0.  # n_events["signal_err_stat"][sr]
  results["signal_events_error_sys"] =  0.   #n_events["signal_err_sys"][sr]
  results["signal_events_error_tot"] = 0.   #sqrt(n_events["signal_err_stat"][sr]**2 + n_events["signal_err_sys"][sr]**2)
  
  # Determine the total background error.
  background_error = 0
  if "bkg_err" in reference_data[sr]:
    background_error = float(reference_data[sr]["bkg_err"])
  elif "bkg_errp" in reference_data[sr]:
    background_error = sqrt(float(reference_data[sr]["bkg_errp"])*float(reference_data[sr]["bkg_errp"])+float(reference_data[sr]["bkg_errm"])*float(reference_data[sr]["bkg_errm"]))/2.
  elif "bkg_err_sys" in reference_data[sr]:
    background_error = float(reference_data[sr]["bkg_err_sys"])
  elif "bkg_err_sysp" in reference_data[sr]:
    background_error = (float(reference_data[sr]["bkg_err_sysp"])+float(reference_data[sr]["bkg_err_sysm"]))/2.
  else:
    background_error = 0
  reference_data[sr]["bkg_err_tot"] = background_error

  results["likelihood"]  = likelihood(float(reference_data[sr]["bkg"]), background_error, float(reference_data[sr]["obs"]), results["signal_events"], results["signal_events_error_tot"], randomseed)
  #results["observed_cls_cons"] = 1
  #if results["signal_events"] > 1.95996*results["signal_events_error_tot"]:
  #  results["observed_cls_cons"] = cls(float(reference_data[sr]["bkg"]), background_error, float(reference_data[sr]["obs"]), results["signal_events"]-1.95996*results["signal_events_error_tot"])[0]
  return results

# End of Jamie Added
#----------------------------------------------------------------------------------



def evaluate(analyses, events, files, flags, output, paths):
  output.mute()
  # Remove old result files
  if os.path.isfile(files['output_result']):
    os.remove(files['output_result'])
  
  # Set header in "best signal region" file
  output.set_cout_file(files['output_bestsignalregions'])
  if flags["fullcl"] == True:
    output.cout("analysis  bestSR  r_obs^c  r_exp^c  CLs_obs  dCLs_obs  CLs_exp  dCLs_exp  S  dS_stat  dS_sys  dS_tot  B  dB  O  S95_obs  S95_exp")
  else:
    output.cout("analysis  bestSR  r_obs^c  r_exp^c  S  dS_stat  dS_sys  dS_tot  S95_obs  S95_exp")
  
  #Jamie added
  if flags["likelihood"] == True:
    for analysis in analyses:
      analysis_likelihood = dict()
      analysis_NSR = dict()
  
  overall_strongest_result = dict() # keeps track of the most constraining signal region's results over all analyses
  for analysis in analyses:
    analysis_strongest_result = dict() # keeps track of the most constraining signal region's results for this analysis
    
    # Update file information with all output files available in output directory.
    files.update(get_result_files(paths['output_analysis'], analysis))
      
    # Remove old result files
    if os.path.isfile(files['output_evaluation_event_numbers'][analysis]):
      os.remove(files['output_evaluation_event_numbers'][analysis])
    
    output.set_cout_file("#None")
    output.cout("** "+analysis+" **")
    # Read reference file to get all signal regions, all reference data and all header information to construct reference table and header lines.
    (header_lines, signal_regions, reference_data) = read_reference_file(files['evaluation_reference'][analysis])
    
    # Go through all analysed processes, add number of signal events and print information to the output file.
    output.set_cout_file(files['output_evaluation_event_numbers'][analysis])   
    for line in header_lines:
      output.cout("@"+line)
    n_events = collect_n_events_per_run(signal_regions, files, output)
    format_columnated_file(files['output_evaluation_event_numbers'][analysis])
      
    
    if os.path.isfile(files['output_evaluation_r_limits'][analysis]):
      os.remove(files['output_evaluation_r_limits'][analysis])
    output.set_cout_file(files['output_evaluation_r_limits'][analysis])
    ## Evaluate limits according to maximum event number given by the experiment     
    # Startup
    for line in header_lines:
        output.cout(line)
    first_line = True
    
    # Loop through all signal regions
    results_r = dict()
    for sr in signal_regions:
      # Calculate results.
      results_r[sr] = compare_to_cls_limit(reference_data, n_events, sr)
      
      # Compare to best result for this analysis.
      if analysis_strongest_result == {}:
        analysis_strongest_result = results_r[sr].copy()
        analysis_strongest_result["origin"] = sr
      else:
        # Consider the signal region with the largest expected r.
        # If the r values are equal, prefer the one with the smallest allowed Sexp
        if (results_r[sr]["r_expected_cons"] > analysis_strongest_result["r_expected_cons"]) or (results_r[sr]["r_expected_cons"] == analysis_strongest_result["r_expected_cons"] and results_r[sr]["expected_upper_limit"] < analysis_strongest_result["expected_upper_limit"]):
          analysis_strongest_result = results_r[sr].copy()
          analysis_strongest_result["origin"] = sr
        
      # Compare to best result over all analyses.
      if overall_strongest_result == {}:
        overall_strongest_result = results_r[sr].copy()
        overall_strongest_result["origin"] = analysis+" - "+sr
      else:
        # Consider the signal region with the largest expected r.
        if (results_r[sr]["r_expected_cons"] > overall_strongest_result["r_expected_cons"]) or (results_r[sr]["r_expected_cons"] == overall_strongest_result["r_expected_cons"] and results_r[sr]["expected_upper_limit"] < overall_strongest_result["expected_upper_limit"]):
          overall_strongest_result = results_r[sr].copy()
          overall_strongest_result["origin"] = analysis+" - "+sr
      
      # Print results_r.        
      if first_line:
        for m in results_r[sr]["messages"]:
          output.cout("@"+m)
        output.cout("SR  S  dS_stat  dS_sys  dS_tot  S95_obs  S95_exp  r^c_obs  r^c_exp")
        first_line = False
      output.cout(sr+"  "+str(siground(results_r[sr]["signal_events"]))+"  "+str(siground(results_r[sr]["signal_events_error_stat"]))+"  "+str(siground(results_r[sr]["signal_events_error_sys"]))+"  "+str(siground(results_r[sr]["signal_events_error_tot"]))+"  "+str(siground(results_r[sr]["observed_upper_limit"]))+"  "+str(siground(results_r[sr]["expected_upper_limit"]))+"  "+str(siground(results_r[sr]["r_observed_cons"]))+"  "+str(siground(results_r[sr]["r_expected_cons"])))


#----------------------------------------------------------
#Jamie new code

    #If desired, evaluate limits by calculating CLs    
    if flags["likelihood"] == True:
      # Reset old information
      results_likelihood = dict()
      analysis_likelihood[analysis] = 0.
      
      if os.path.isfile(files['output_evaluation_likelihood'][analysis]):
        os.remove(files['output_evaluation_likelihood'][analysis])
      output.set_cout_file(files['output_evaluation_likelihood'][analysis])

      # Startup
      for line in header_lines:
          output.cout(line)
      first_line = True

      analysis_NSR[analysis] = len(signal_regions)

      # Loop through all signal regions.
      for sr in signal_regions:
        # Evaluate results.
        results_likelihood[sr] = calculate_likelihood(reference_data, n_events, sr, flags["randomseed"])
        analysis_likelihood[analysis] = float(analysis_likelihood[analysis]) + float(results_likelihood[sr]["likelihood"])
        
       # Print results.
        if first_line:
          for m in results_likelihood[sr]["messages"]:
            output.cout(m)
          output.cout("SR  S  B  dB  O  Likelihood  Stan.Dev")
          first_line = False
        output.cout(sr+"  "+str(siground(results_likelihood[sr]["signal_events"]))+"  "+str(siground(float(reference_data[sr]["bkg"])))+"  "+str(siground(float(reference_data[sr]["bkg_err_tot"])))+"  "+str(siground(float(reference_data[sr]["obs"])))+"  "+str(siground(results_likelihood[sr]["likelihood"], 5))+"  "+str(siground(sqrt(results_likelihood[sr]["likelihood"]), 5)))
        

# End of new code
#--------------------------------------------------------------------------

    
    #If desired, evaluate limits by calculating CLs    
    if flags["fullcl"] == True:
      # Reset old information
      results_cls = dict()
      
      if os.path.isfile(files['output_evaluation_cl_limits'][analysis]):
        os.remove(files['output_evaluation_cl_limits'][analysis])
      output.set_cout_file(files['output_evaluation_cl_limits'][analysis])
      
      # Startup
      for line in header_lines:
          output.cout(line)
      first_line = True
      
      # Loop through all signal regions.
      for sr in signal_regions:
        # Evaluate results.
        results_cls[sr] = calculate_cls_limit(reference_data, n_events, sr, flags["randomseed"])
        
        # Compare to best result of this analysis.
        if "expected_cls" not in analysis_strongest_result:
          analysis_strongest_result = results_cls[sr].copy()
          analysis_strongest_result.update(results_r[sr])
          analysis_strongest_result["origin"] = sr
        else:
          # Consider the signal region with the smallest expected CLs.
          if (results_cls[sr]["expected_cls"] < analysis_strongest_result["expected_cls"]) or (results_cls[sr]["expected_cls"]  == analysis_strongest_result["expected_cls"] and results_r[sr]["expected_upper_limit"] < analysis_strongest_result["expected_upper_limit"]):
            analysis_strongest_result = results_cls[sr].copy()
            analysis_strongest_result.update(results_r[sr])
            analysis_strongest_result["origin"] = sr
        
        # Compare to best result over all analyses.
        if "expected_cls" not in overall_strongest_result:
          overall_strongest_result = results_cls[sr].copy()
          overall_strongest_result.update(results_r[sr])
          overall_strongest_result["origin"] = analysis+" - "+sr
        else:
          # Consider the signal region with the smallest expected CLs.
          if (results_cls[sr]["expected_cls"] < overall_strongest_result["expected_cls"]) or (results_cls[sr]["expected_cls"]  == overall_strongest_result["expected_cls"] and results_r[sr]["expected_upper_limit"] < overall_strongest_result["expected_upper_limit"]):
            overall_strongest_result = results_cls[sr].copy()
            overall_strongest_result.update(results_r[sr])
            overall_strongest_result["origin"] = analysis+" - "+sr
            
        # Print results.
        if first_line:
          for m in results_cls[sr]["messages"]:
            output.cout(m)
          output.cout("SR  S  dS_stat  dS_sys  dS_tot  B  dB  O  CL_obs  dCL_obs  CL_exp  dCL_exp")
          first_line = False
        output.cout(sr+"  "+str(siground(results_cls[sr]["signal_events"]))+"  "+str(siground(results_cls[sr]["signal_events_error_stat"]))+"  "+str(siground(results_cls[sr]["signal_events_error_sys"]))+"  "+str(siground(results_cls[sr]["signal_events_error_tot"]))+"  "+str(siground(float(reference_data[sr]["bkg"])))+"  "+str(siground(float(reference_data[sr]["bkg_err_tot"])))+"  "+str(siground(float(reference_data[sr]["obs"])))+"  "+str(siground(results_cls[sr]["observed_cls"], 5))+"  "+str(siground(results_cls[sr]["observed_cls_err"], 5))+"  "+str(siground(results_cls[sr]["expected_cls"], 5))+"  "+str(siground(results_cls[sr]["expected_cls_err"], 5)))
    
    # Print the best result of the given analysis into a 'best results' file
    output.set_cout_file(files['output_bestsignalregions'])
    if flags["fullcl"] == True:
      output.cout(analysis+"  "+analysis_strongest_result["origin"]+"  "+str(siground(analysis_strongest_result["r_observed_cons"]))+"  "+str(siground(analysis_strongest_result["r_expected_cons"]))+"  "+str(siground(analysis_strongest_result["observed_cls"], 5))+"  "+str(siground(analysis_strongest_result["observed_cls_err"], 5))+"  "+str(siground(analysis_strongest_result["expected_cls"], 5))+"  "+str(siground(analysis_strongest_result["expected_cls_err"], 5))+"  "+str(siground(analysis_strongest_result["signal_events"]))+"  "+str(siground(analysis_strongest_result["signal_events_error_stat"]))+"  "+str(siground(analysis_strongest_result["signal_events_error_sys"]))+"  "+str(siground(analysis_strongest_result["signal_events_error_tot"]))+"  "+str(siground(float(reference_data[analysis_strongest_result["origin"]]["bkg"])))+"  "+str(siground(float(reference_data[analysis_strongest_result["origin"]]["bkg_err_tot"])))+"  "+str(siground(float(reference_data[analysis_strongest_result["origin"]]["obs"])))+"  "+str(siground(results_r[analysis_strongest_result["origin"]]["observed_upper_limit"]))+"  "+str(siground(results_r[analysis_strongest_result["origin"]]["expected_upper_limit"])))
    else:
      output.cout(analysis+"  "+analysis_strongest_result["origin"]+"  "+str(siground(analysis_strongest_result["r_observed_cons"]))+"  "+str(siground(analysis_strongest_result["r_expected_cons"]))+"  "+str(siground(analysis_strongest_result["signal_events"]))+"  "+str(siground(analysis_strongest_result["signal_events_error_stat"]))+"  "+str(siground(analysis_strongest_result["signal_events_error_sys"]))+"  "+str(siground(analysis_strongest_result["signal_events_error_tot"]))+"  "+str(siground(analysis_strongest_result["observed_upper_limit"]))+"  "+str(siground(results_r[analysis_strongest_result["origin"]]["expected_upper_limit"])))
    output.mute()

  # Print final result
  format_columnated_file(files['output_bestsignalregions'])
  output.unmute()
  output.set_cout_file(files['output_result'])
  status = "Allowed"
  if flags["fullcl"]:
    test = "Calculation of CLs from determined signal"
    if overall_strongest_result["observed_cls"] < 0.05:
      status = "Excluded"
    result_cls = "cls_min = "+str(siground(overall_strongest_result["observed_cls"], 6))
    result_r = "r_max = "+str(siground(overall_strongest_result["r_observed_cons"], 6))
  else:
    test = "Calculation of r = signal/(95%CL limit on signal)"
    statusmessage = "r_max = "+str(overall_strongest_result["r_observed_cons"])
    if overall_strongest_result["r_observed_cons"] > 1:
      status = "Excluded"
    result_cls = ""
    result_r = "r_max = "+str(siground(overall_strongest_result["r_observed_cons"], 6))
  
  # Check if strongest result includes potential issues  
  warnings = list()
  if overall_strongest_result["signal_events_error_sys"] < overall_strongest_result["signal_events_error_stat"]:
    warnings.append("Error is dominated by Monte Carlo statistics!")
  if status == "Allowed" and overall_strongest_result["r_observed_cons"] < 1 and overall_strongest_result["r_observed_sysonly"] > 1:
    warnings.append("The model could be excluded if you provided more input events!")
    
  for line in header_lines:
    output.cout(line)
  output.cout("Test: "+test)
  # Check for possible warnings
  if len(warnings) != 0:
    for w in warnings:
      output.cout("Warning: "+w)
  output.cout("Result: "+status)
  if result_cls != "":
      output.cout("Result for CLs: "+result_cls)
  output.cout("Result for r: "+result_r)
  output.cout("SR: "+overall_strongest_result["origin"])
  #output.cout("MC_status:  Undefined")
  output.set_cout_file("#None")
  for a in analyses:
    format_columnated_file(files['output_evaluation_r_limits'][a])
    if flags["fullcl"]:      
      format_columnated_file(files['output_evaluation_cl_limits'][a])
    if flags["likelihood"]:      
      format_columnated_file(files['output_evaluation_likelihood'][a])  
  
  # Jamie added
  output.mute()
  if flags["likelihood"]:
    total_likelihood = float()
    total_NSR = float()
    if os.path.isfile(files['likelihood']):
      os.remove(files['likelihood'])
    output.set_cout_file(files['likelihood'])
    output.cout("Analysis  Likelihood  Chi^2/n.d.f")
    for a in analyses:
      output.cout(a+"  "+str(analysis_likelihood[a])+"  "+str(analysis_likelihood[a]/analysis_NSR[a]))
      total_likelihood = analysis_likelihood[a] + total_likelihood
      total_NSR = analysis_NSR[a] + total_NSR
    output.cout("Total_likelihood  "+str(total_likelihood)+"  "+str(total_likelihood/total_NSR))  
    format_columnated_file(files['likelihood']) 
  output.unmute()    
      
  return
