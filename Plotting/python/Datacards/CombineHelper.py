#!/usr/bin/env python
"""
Run the combine limit setting tool
"""

########################################
# Imports
########################################

import os
import shutil
import datetime
import subprocess
import ROOT
import numpy as np

from EnvForCombine import PATH, LD_LIBRARY_PATH, PYTHONPATH, GENREFLEX, ROOTSYS, ROOT_INCLUDE_PATH

def get_limits(fn):
    """
    Returns a length 6 vector with the expected limits and quantiles based on the
    combine root file.
    """
    f = ROOT.TFile(fn)

    #No root file created, fit failed
    if f==None or f.IsZombie():
        lims = np.zeros(6)
        quantiles = np.zeros(6)
        lims[:] = 99999
        return lims, quantiles
    tt = f.Get("limit")
    if tt==None or tt.IsZombie():
        lims = np.zeros(6)
        quantiles = np.zeros(6)
        lims[:] = 99999
        return lims, quantiles
    lims = np.zeros(6)
    quantiles = np.zeros(6)
    for i in range(tt.GetEntries()):
        tt.GetEntry(i)
        lims[i] = tt.limit
        quantiles[i] = tt.quantileExpected
    f.Close()
    return lims, quantiles

class LimitGetter(object):
    
    def __init__(self, output_path = "."):
        self.output_path = output_path

    def __call__(self, datacard):

        datacard_name = datacard.split("/")[-1].replace(".txt","")
        datacard_path = "/".join(datacard.split("/")[:-1])

        # Add a timestamp to the name
        #timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
        process_name = "{0}".format(datacard_name)

        # Run combine
        combine_command = ["combine", 
                           "-n", process_name,
                           "-M", "Asymptotic",
                           "-t", "-1",
                           datacard_name + ".txt"]
        
        process = subprocess.Popen(combine_command,
                                   stdout=subprocess.PIPE,
                                   cwd=datacard_path,
                                   env=dict(os.environ, 
                                            PATH=PATH,
                                            LD_LIBRARY_PATH = LD_LIBRARY_PATH,
                                            PYTHONPATH=PYTHONPATH,
                                            ROOT_INCLUDE_PATH = ROOT_INCLUDE_PATH,
                                            ROOTSYS = ROOTSYS,
                                            GENREFLEX = GENREFLEX
                                        ))
        
        output = process.communicate()[0]
        
        # Put the output file in the corrrect place..
        # ..root file
        output_rootfile_name = "higgsCombine{0}.Asymptotic.mH120.root".format(process_name)
        targetpath = os.path.join(self.output_path, output_rootfile_name)
        shutil.move(os.path.join(datacard_path, output_rootfile_name),
                   targetpath)
        # ..text file
        output_textfile_name = "out_{0}.log".format(process_name)
        of = open(os.path.join(self.output_path, output_textfile_name), "w")
        of.write(output)
        
        # And extact the lmit
        limit = 1000
        lims, quantiles = get_limits(targetpath)
        limit = lims[2]
        print datacard_name, ":", limit
        return lims, quantiles
    # End of get_limit

class DummyLimitGetter(object):
    
    def __init__(self, output_path = "."):
        self.output_path = output_path

    def __call__(self, datacard):
        print "calling limit on datacard", datacard
        return np.array([0,0,0,0,0,0]), None
    # End of get_limit
