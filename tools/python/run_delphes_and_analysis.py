import datetime
import os
import gzip
import subprocess

from global_functions import *
from merge_delphes_settings import *

def run_delphes_and_analyze(analyses, events, files, flags, output, paths):
    """Runs Delphes on all event files plus the chosen analysis on the Delphes result"""
    eventcounter = get_eventcounter(paths['output_analysis'], analyses[0])
    
    events['delphes'] = []
    for i in range(len(events['raw'])):
        event_raw = events['raw'][i]
        (xsect_num, xsect_unit) = tuple(events['xsects'][i])
        (xsecterr_num, xsecterr_unit) = tuple(events['xsecterrs'][i])
        output.cout("* Processing file '"+event_raw+"'")
        
        # Prepare Delphes command.
        filetype = os.path.splitext(event_raw)[1].lower()
        files['delphes_bin'] = ""
        flags['compressed'] = False
        if filetype == ".gz":
            # Correct filetype is suffix before .gz
            filetype = os.path.splitext(os.path.splitext(event_raw)[0])[1].lower()
            event_extracted = gzip.open(event_raw, "rb")
            flags['compressed'] = True
        if filetype == ".lhe": 
            files['delphes_bin'] = os.path.join(paths['delphes'], "DelphesLHEF")
        elif filetype == ".hepmc": 
            files['delphes_bin'] = os.path.join(paths['delphes'],"DelphesHepMC")
        elif filetype == ".hep": 
            files['delphes_bin'] = os.path.join(paths['delphes'], "DelphesSTDHEP")
        else: output.cerr_exit("Error: event file has unknown type '"+filetype)
        event_delphes = os.path.join(paths['output_delphes'], "%03i_delphes.root" % eventcounter)
        
        # Merge settings
        (branches_per_analysis, flags_per_analysis, files, paths) = merge_settings(files, paths, flags)
        
        # Run Delphes and redirect output.
        output.cout("** - Delphes")
        if flags["skipdelphes"]:
          output.cout("      skipped")
        else:
            if not flags['compressed']:
                process = "%s %s %s %s" % (files['delphes_bin'], files['delphes_merged_config'], event_delphes, event_raw)
            else:
                process = "%s %s %s" % (files['delphes_bin'], files['delphes_config'], event_delphes)
                
            events['delphes'].append(event_delphes)
            
            try:
                if output.quiet:
                    p = subprocess.Popen(process.split(), bufsize=0, stdin = subprocess.PIPE, stderr = subprocess.STDOUT, stdout = subprocess.PIPE)
                else:
                    p = subprocess.Popen(process.split(), bufsize=0, stdin = subprocess.PIPE, stdout = subprocess.PIPE)
                if flags['compressed']:
                    p.stdin.write(event_extracted.read())
                output.set_cout_file(files["output_log_delphes"])
                if not flags["verbosemode"]:
                  output.mute()
                for line in iter(p.stdout.readline, ''):
                  strLine = str(line.rstrip())
                  output.cout(strLine)
                
                output.set_cout_file("#None")
                if not flags["quietmode"]:
                  output.unmute()
            except KeyboardInterrupt:
                try:
                    while True:
                        # Let Delphes terminate properly.
                        p.wait()
                        
                        # Decide how to proceed.
                        output.cerr("\nTerminated current Delphes process.\n")
                        output.cerr("Do you want to...\n")
                        output.cerr("\t ...continue with the next event? (c)\n")           
                        output.cerr("\t ...skip all further events and continue with evaluation? (e)\n")
                        output.cerr("\t ...terminate the whole run? (t)\n")
                        c = raw_input("")
                        if c == "c":
                            break # breaks try loop and continues run
                        elif c == "e":
                            return
                        elif c == "t":
                            exit(1)
                        else: 
                            continue
                except KeyboardInterrupt:
                    # If yet another interruption comes, abort.
                    if p.poll():
                        p.kill()
                    exit(1)        
        
        # Run analysis.
        output.cout("** - Analysis")
        for analysis in analyses:
            # Construct branch information for the analysis program
            branch_tuple = ""
            for b in branches_per_analysis[analysis]:
              branch_tuple += b+":"+branches_per_analysis[analysis][b]+";"
            flag_tuple = ""
            for f in flags_per_analysis[analysis]:
              flag_tuple += f+":"+str(flags_per_analysis[analysis][f]).replace(" ", "")+";"
            # Randomseed is saved as flag
            if flags["randomseed"] != 0:
              flag_tuple += "randomseed:["+str(flags["randomseed"])+"];"
            if flags["controlregions"]:
              analysis = analysis+"_CR" 
            output.cout("     -"+analysis)
            process ="%s %s %s %s %03i %s %s %s %s %s %s" % (files['analysis_bin'], analysis, event_delphes, paths['output_analysis'], eventcounter, xsect_num, xsect_unit, xsecterr_num, xsecterr_unit, branch_tuple, flag_tuple)
            if flags["verbosemode"]:
              output.cout("    "+process)
            if output.quiet:
                p = subprocess.Popen(process.split(), bufsize=0, stdin = subprocess.PIPE, stderr = subprocess.STDOUT, stdout = subprocess.PIPE)
            else:
                p = subprocess.Popen(process.split(), bufsize=0, stdin = subprocess.PIPE,  stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
            output.set_cout_file(files["output_log_analysis"])            
            if not flags["verbosemode"]:
              output.mute()
            output.cout("Run Analysis "+analysis+" with parameters "+str((files['analysis_bin'], analysis, event_delphes, paths['output_analysis'], eventcounter, xsect_num, xsect_unit, xsecterr_num, xsecterr_unit, branch_tuple, flag_tuple)))
            for line in iter(p.stdout.readline, ''):
              strLine = str(line.rstrip())
              output.cout(strLine)
            
            output.set_cout_file("#None")
            if not flags["quietmode"]:
              output.unmute()
              
            # Columnate all files in analysis folder that correspond to the given analysis
            for result_file in [f for f in os.listdir(paths['output_analysis']) if f.startswith("%03i" % eventcounter) and analysis in f]:
              format_columnated_file(os.path.join(paths['output_analysis'], result_file))
        
    
        # Update overall progress file
        progressfile = open(files['output_progress'], "a")
        # If file is empty, write header
        if os.stat(files['output_progress'])[6] == 0:
          progressfile.write("#Prefix  EventFile  Sigma  dSigma  Process  Date and Time of Procession\n")
        progressfile.write(("%03i"%eventcounter)+"  "+str(event_raw)+"  "+str(events['xsects'][i][0])+" "+str(events['xsects'][i][1])+"  "+str(events['xsecterrs'][i][0])+" "+str(events['xsecterrs'][i][1])+"  "+str(events['processes'][i])+"  "+str(datetime.datetime.now())+"\n")
        progressfile.close()
        format_columnated_file(files['output_progress'])
        
        # If in temporary mode, delete Delphes file.
        if flags['tempmode']:
            if os.path.isfile(event_delphes):
                os.remove(event_delphes)
            events['delphes'] = []
        eventcounter += 1
        output.cout("")
        
        # To prevent correlated results, increase random seed by 1 for the next event file
        #  if randomseeds have been set
        if flags["randomseed"] != 0:
          flags["randomseed"] += 1
        
    return
