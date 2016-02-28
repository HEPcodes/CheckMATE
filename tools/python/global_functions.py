import hashlib
import os
import sys

from organize_paths_and_files import *

class AdvPrint:
    """Prints unless a flag is set"""
    
    def __init__(self):
        self.quiet = False
        self.cout_file = "#None"
    
    def mute(self):
        self.quiet = True
        
    def unmute(self):
        self.quiet = False
    
    def set_cout_file(self, cout_file):
      self.cout_file = cout_file
    
    def cout(self, message, option=""):
        if self.quiet == False:
            if option == "nlb":
                print message, 
            else:
                print message
        if self.cout_file != "#None":
            f = open(self.cout_file, "a")
            if option == "nlb":
                f.write(message)
            else:
                f.write(message+"\n")            
            f.close()        
            
    def cerr(self, message):
        sys.stderr.write(message)
        
    def cerr_exit(self, message):
        self.cerr("!!! ERROR !!!\n")
        self.cerr(message + "\n")
        self.cerr("Exiting.\n")
        exit(1) 
    
    
def remove_extra_spaces(text):  
  # Replaces more than two spaces by exactly two spaces, which is the Checkmate standard for separating columns
  while text.find("   ") != -1:
    text = text.replace("   ", "  ")
  return text


def get_analysis_info(analysis):
    """Exits if analysis is nonexisting, otherwise it will return the corresponding information saved in the global info file"""
    files = get_standard_files()
    f = open(files['list_of_analyses'])
    for line in f:
        line = remove_extra_spaces(line)
        # Split line into tokens; tokens[0] is name.
        tokens = line.split("  ")    
        if tokens[0] == analysis:
            return tokens[2].rstrip("\n")
    pr = AdvPrint()
    pr.cerr_exit("Analysis '"+analysis+"' is unknown.");
    
def md5_checksum(f):
    """Returns the md5 checksum of file f"""
    with open(f, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()    

def get_eventcounter(rdir, analysis):
    """If there already exist result files in rdir up to number N, return N+1. Otherwise 0"""
    rfiles = get_result_files(rdir, analysis)
    for eventcounter in range(1000):
        counter_used = False
        for rfile in rfiles["results_signal"]:
            if ("%03i" % eventcounter) in rfile:
                counter_used = True
        if not counter_used:
            return eventcounter        
    pr = AdvPrint()
    pr.cerr_exit("Eventcounter is out of range (>999)")
    
def check_agreement_of_identifiers_and_crosssections(events):
    """Events which belong to the same process must have the same cross section"""
    pr = AdvPrint()
    N = len(events['processes'])
    for i in range(N):
        for j in range(N):
            if events['processes'][i] == events['processes'][j] and events['xsects'][i] != events['xsects'][j]:
                pr.cerr_exit("Events from the same process must have identical cross sections!")
    return

def parse_progress(pfile):
    """Reads the progress file 'pfile' and puts its information into structured dictionaries"""
    results = dict()
    f = open(pfile)
    # First, read in all items of progress file.
    for line in f:
        line = line.rstrip()
        if line == "" or line[0] == "#":
            continue
          
        # Reduce spacing properly to split the string.        
        while line.find("   ") != -1:
          line = line.replace("   ", "  ")
        tokens = line.split("  ")
        #Prefix  Eventfile  Checksum  Xsect  Process  Date
        prefix = tokens[0]
        checksum = tokens[2]
        xsect = tokens[3]
        process = tokens[4]
        
        results[prefix] = dict()
        results[prefix]['prefix'] = prefix
        results[prefix]['checksum'] = checksum
        results[prefix]['xsect'] = xsect
        results[prefix]['process'] = process
    f.close()
    
    # Next, group items according to their processes
    processes = dict()
    prefixes = results.keys()
    prefixes.sort()
    for prefix in prefixes:
        result = results[prefix]
        process = result['process']
        # If the process is new, add to dict
        if process not in processes.keys():
            processes[process] = []
            processes[process].append(result)
        else:
            processes[process].append(result)            
    return processes

def format_columnated_file(unformated_file):
  uncolumnated_lines = list()
  columnated_lines = list()
  f = open(unformated_file, "r")
  # Read file and divice into columnated and uncolumnated lines
  # Keep order of lines in separate list  
  order = list()
  for line in f:
    line = line.rstrip()
    if line == "" or line[0:2] == "# ":
      uncolumnated_lines.append(line)
      order.append("u")
    elif line[0] == "@":
      uncolumnated_lines.append(line[1:])
      order.append("u")
    else:
      columnated_lines.append(line)
      order.append("c")
  
  # Divide items in columnated lines
  line_items = list()
  for line in columnated_lines:
    # Split whenever there are two or more spaces
    line = remove_extra_spaces(line)
    line_items.append(line.split("  "))
  trans_lines = zip(*line_items)
  col_widths = [max(len(c) for c in b)+2 for b in trans_lines]
  #col_width = max(len(word) for line in line_items for word in line) + 2  # padding
  
  f.close()
  f = open(unformated_file, "w")
  u = c = 0
  for i in range(len(order)):
    if order[i] == "u":
      f.write(uncolumnated_lines[u]+"\n")      
      u += 1
    else:
      line = line_items[c]      
      f.write("".join(word.ljust(col_width) for word, col_width in zip(line, col_widths))+"\n")
      c += 1
  
