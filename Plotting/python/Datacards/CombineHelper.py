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


########################################
# get_limit
########################################

def get_limit(datacard, output_path = "."):

    datacard_name = datacard.split("/")[-1].replace(".txt","")
    datacard_path = "/".join(datacard.split("/")[:-1])

    # Add a timestamp to the name
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    process_name = "{0}_{1}".format(datacard_name, timestamp)

    # Run combine
    combine_command = ["combine", 
                       "-n", process_name,
                       "-M", "Asymptotic",
                       "-t", "-1",
                       datacard_name + ".txt"]

    process = subprocess.Popen(combine_command,
                               stdout=subprocess.PIPE,
                               cwd=datacard_path)
    
    output = process.communicate()[0]

    # Put the output file in the corrrect place..
    # ..root file
    output_rootfile_name = "higgsCombine{0}.Asymptotic.mH120.root".format(process_name)
    shutil.move(os.path.join(datacard_path, output_rootfile_name),
                os.path.join(output_path, output_rootfile_name))
    # ..text file
    output_textfile_name = "out_{0}.log".format(process_name)
    of = open(os.path.join(output_path, output_textfile_name), "w")
    of.write(output)

    # And extact the lmit
    limit = 1000
    for line in output.split("\n"):
        if "Expected 50.0%" in line:
            limit = float(line.split("<")[-1].strip())
        
    print datacard_name, ":", limit
    
    return limit
# End of get_limit


