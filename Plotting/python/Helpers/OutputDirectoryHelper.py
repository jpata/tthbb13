#!/usr/bin/env python
"""
Helper script for the plotting scripts that takes care of two things:

CreateOutputDirs:
Create a output directory with subdirectories for all desired filetypes
dir_x/png/
dir_x/pdf/
...

MultiPrint:
Call the Print function for a ROOT object for all filetypes (png, pdf, ..) and 
print them into the correct path.
"""

########################################
# Imports
########################################

import os


########################################
# Global Settings
########################################

# Which outputs do we want?
li_output_filetypes = ["png", "pdf", "eps", "C"]



########################################
# Function Definitions
########################################

def CreateOutputDirs( output_dir ):
    ''' Create the directory output_dir (if it does not exist) and
    subdirectories for all filetypes (if these dont exist).

    Arguments:
    output_dir : (string) Name of the directory to create.
    '''

    # Create the output directory
    if not os.path.exists(output_dir):
        print "Creating output_dir:", output_dir 
        os.makedirs(output_dir)

    # Also make subdirectories for all filetypes
    for filetype in li_output_filetypes:
        if not os.path.exists(output_dir+filetype):
            print "Creating output_dir:", output_dir + filetype
            os.makedirs(output_dir+filetype)
    # end of filetpye loop
# end of CreateOutputDirs



def ManyPrint( canvas, output_dir, filename , islogy=False, islogx=False ):
    ''' Call the Print function of the canvas and draw it into the
    correct output directory for the different required output
    formats.
    Arguments:
    canvas : (ROOT TCanvas) object to print
    output_dir: (string) name of the output directory
    filename: (strint) filename to use (pdf/png/.. added automatically)
    '''
    logstring = ""
    if islogx or islogy:
        logstring = "_log"
    if islogx:
        logstring+="x"
    if islogy:
        logstring+="y"

    filename = filename.replace('[','_').replace(']','')
    
    # Loop over the output formats and call Print
    for filetype in li_output_filetypes:
        canvas.Print( output_dir + filetype + "/" + filename + logstring + "." + filetype )
    # end of filetype loop
# end of ManyPrint
