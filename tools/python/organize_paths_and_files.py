import os

def get_standard_paths():
    """Returns a dict of standard paths of the CheckMATE installation"""
    paths = dict()
    paths['checkmate'] = os.path.split(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])[0]
    paths['results'] = os.path.join(paths['checkmate'], 'results')
    paths['tools'] = os.path.join(paths['checkmate'], 'tools')
    
    paths['analysis'] = os.path.join(paths['tools'], 'analysis')
    paths['data'] = os.path.join(paths['checkmate'], 'data')
    paths['delphes'] = os.path.join(paths['tools'], 'delphes', 'Delphes-3.0.10X')
    paths['evaluation'] = os.path.join(paths['tools'], 'evaluation')
    return paths

def get_standard_files():
    """Returns a dict of standard files of the CheckMATE installation"""
    paths = get_standard_paths()
    files = dict()
    files['list_of_analyses'] = os.path.join(paths['data'], 'list_of_analyses.txt')
    files['analysis_bin'] = os.path.join(paths['analysis'], "doAnalysis")
    files['analysis_makefile'] = os.path.join(paths['analysis'], "Makefile.am")
    files['analysis_main'] = os.path.join(paths['analysis'], 'src', 'main.cc')
    files['analysis_template_source'] = os.path.join(paths['analysis'], 'src', 'template.cc.raw')
    files['analysis_template_CR_source'] = os.path.join(paths['analysis'], 'src', 'template_CR.cc.raw')
    files['analysis_template_header'] = os.path.join(paths['analysis'], 'include', 'template.h.raw')
    return files

def get_output_paths(odir, oname):
    """Returns a dict of paths given a particular output directory"""
    paths = dict()
    paths['output'] = os.path.join(odir, oname)
    paths['output_delphes'] = os.path.join(paths['output'], "delphes")
    paths['output_analysis'] = os.path.join(paths['output'], "analysis")
    paths['output_evaluation'] = os.path.join(paths['output'], "evaluation")
    return paths

def get_output_files(odir, oname, analyses, flags):
    """Returns a dict of files given a particular output directory"""
    files = dict()
    files['output_progress'] = os.path.join(odir, oname, "progress.txt")
    files['output_log_delphes'] = os.path.join(odir, oname, "delphes", "log_delphes.txt")
    files['output_log_analysis'] = os.path.join(odir, oname, "analysis", "log_analysis.txt")
    files['delphes_merged_config'] = os.path.join(odir, oname, "delphes", "merged.tcl")
    files['output_evaluation_event_numbers'] = dict()
    files['output_evaluation_r_limits'] = dict()
    files['output_evaluation_cl_limits'] = dict()
    files['output_evaluation_likelihood'] = dict()
    files['eff_tab'] = dict()
    for a in analyses:    
      files['output_evaluation_event_numbers'][a] = os.path.join(odir, oname, "evaluation", a+"_event_numbers.txt")
      files['output_evaluation_r_limits'][a] = os.path.join(odir, oname, "evaluation", a+"_r_limits.txt")
      files['output_evaluation_cl_limits'][a] = os.path.join(odir, oname, "evaluation", a+"_cl_limits.txt")
      files['output_evaluation_likelihood'][a] = os.path.join(odir, oname, "evaluation", a+"_likelihood.txt")
      files['eff_tab'][a] = os.path.join(odir, oname, "evaluation", a+"_eff_tab.txt")
    files['output_bestsignalregions'] = os.path.join(odir, oname, "evaluation", "best_signal_regions.txt")
    files['output_result'] = os.path.join(odir, oname, "result.txt")
    if flags["likelihood"]:
      files['likelihood'] = os.path.join(odir, oname, "likelihood.txt")
    return files                            

def get_analysis_files(analyses):
    """Returns a dict of standard files that contain analysis specific information"""
    paths = get_standard_paths()
    files = get_standard_files()
    files['analysis_settings'] = dict()
    files["analysis_source"] = dict()
    files["analysis_CR_source"] = dict()
    files["analysis_header"] = dict()
    files['delphes_config'] = dict()
    files['evaluation_reference'] = dict()
    for a in analyses:
        files['analysis_settings'][a] = os.path.join(paths['data'], a+'_var.j')
        files["analysis_source"][a] = os.path.join(paths['analysis'], 'src', a+'.cc')
        files["analysis_CR_source"][a] = os.path.join(paths['analysis'], 'src', a+'_CR.cc')
        files["analysis_header"][a] = os.path.join(paths['analysis'], 'include', a+'.h')
        files['delphes_config'][a] = os.path.join(paths['tools'], 'delphes', 'settings', a+'.tcl')
        files['evaluation_reference'][a] = os.path.join(paths['data'], a+'_ref.dat')
    return files

def get_result_files(rdir, analysis):
    """Returns a dict of files that belong to a certain analysis in a given result directory"""
    files = dict()
    # Get all files in output folder
    signals = [os.path.join(rdir, f) for f in os.listdir(rdir) if "signal" in f and analysis in f]
    cutflows = [os.path.join(rdir, f) for f in os.listdir(rdir) if "cutflow" in f and analysis in f]    
    files['results_signal'] = dict()
    # Read the prefix of every file and use it as key for the files dictionaries
    for i in range(len(signals)):
        prefix = os.path.split(signals[i])[1][0:3]
        files['results_signal'][prefix] = signals[i]
    return files
