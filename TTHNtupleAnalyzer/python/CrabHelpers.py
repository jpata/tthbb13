""" CrabHelpers:
Collection of functions for simple crab3 submission.
"""

#######################################
# Imports
#######################################

import os
import imp
import sys
import glob
import subprocess

try:
    import ROOT
except:
    pass

from TTH.TTHNtupleAnalyzer.Samples import Samples

#######################################
# update_progress
#######################################

## From: http://stackoverflow.com/questions/3160699/python-progress-bar
## Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%

def update_progress(progress):
    barLength = 30 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)


#######################################
# submit
#######################################

def submit(name,
           sample_shortname,
           version,        
           cmssw_config_path,
           cmssw_config_script = "Main_cfg.py",
           site = "T2_CH_CSCS",
           template_filename = "c_TEMPLATE.py",
           cfg_filename = "c_tmp.py",
           blacklist = []):
    """Submit a single job to the Grid"""

    # Import template, add parameters and save to new file
    imp.load_source("template", template_filename)
    import template    

    template.config.General.workArea = "crab_{0}_{1}_{2}".format(name, version, sample_shortname)
    template.config.General.requestName = "{0}_{1}_{2}".format(name, version, sample_shortname)
    template.config.JobType.psetName = cmssw_config_path + cmssw_config_script
    template.config.Data.inputDataset = Samples[sample_shortname]
    template.config.Site.storageSite = site

    if blacklist:
        template.config.Site.blacklist = blacklist


    outfile = open(cfg_filename, "w")
    outfile.write(str(template.config))
    outfile.close()

    print "Created config for", sample_shortname
    print "Now calling crab submit"

    subprocess.call(["crab", "submit", "-c", "c_tmp.py"])
# End of submit


#######################################
# status
#######################################

def status(name,
           sample_shortname,
           version):
    """Get status of a single job on the Grid."""

    working_dir = "crab_{0}_{1}_{2}/crab_{0}_{1}_{2}".format(name, version, sample_shortname)
    
    subprocess.call(["crab", "status", "-d", working_dir])
# End of status


#######################################
# kill
#######################################

def kill(name,
           sample_shortname,
           version):
    """Kill a single job on the Grid."""

    working_dir = "crab_{0}_{1}_{2}/crab_{0}_{1}_{2}".format(name, version, sample_shortname)
    
    subprocess.call(["crab", "kill", "-d", working_dir])
# End of kill


#######################################
# download
#######################################

def download(name,
             sample_shortname,
             version,        
             target_basepath):
    """Download a single job from the Grid. Assume we are in the same
    directory used for submission (crab_configs)
    and the crab working directory is of the form
    crab_ntop_v3_zprime_m1000_1p_13tev/crab_ntop_v3_zprime_m1000_1p_13tev

    Download to target_basepath + job name
    """

    working_dir = "crab_{0}_{1}_{2}/crab_{0}_{1}_{2}".format(name, version, sample_shortname)
    
    output_dir = target_basepath + "{0}_{1}_{2}".format(name, version, sample_shortname)    
    subprocess.call(["crab", "getoutput", "-d", working_dir, "--outputpath", output_dir])
# End of download


#######################################
# download_globus 
#######################################

def download_globus(name,
                    sample_shortname,
                    version,        
                    basepath,
                    user_name = "gregor",
                    glob_string = "*.root",
                    isVHBBHEPPY = False):
    """Download a single job from the Grid using globus-url-copy instead of crab
    """

    timeout = 5 # seconds
    
    storage_host = "storage01.lcg.cscs.ch"
    gsiftp_base = "gsiftp://" + storage_host
    srm_base    = "srm://" + storage_host
    user_path_on_storage = "pnfs/lcg.cscs.ch/cms/trivcat/store/user/{0}/".format(user_name)    
    local_mount_path = "/scratch/{0}/mount/storage/".format(user_name)
    output_path = os.path.join(basepath, "{0}_{1}_{2}".format(name, version, sample_shortname))

    sample_name = Samples[sample_shortname].split("/")[1]
    sample_name_and_tag = "__".join(Samples[sample_shortname].split("/")[1:3])
    
    if isVHBBHEPPY:
        crab_job_name = "{0}_{1}_{2}".format(name, version, sample_name_and_tag)
    else:
        crab_job_name = "crab_{0}_{1}_{2}".format(name, version, sample_shortname)

    # Make sure output directory exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Make sure the local mount path exists and mount remote storage into it
    if not os.path.exists(local_mount_path):
        os.makedirs(local_mount_path)
    subprocess.call(["gfalFS", "-s", local_mount_path, srm_base])

    # Use glob to get the full path of the files we are interested in.
    # The structure is user_path_on_storage / full sample name / name of crab job / timestamp / i / *.root
    # i starts at 0 and each i-directory holds the output of at most 1k jobs

    print os.path.join(local_mount_path, 
                       user_path_on_storage, 
                       "VHBBHeppy" + version,
                       sample_name,
                       crab_job_name,
                       "*/*")

    #sys.exit()

    if isVHBBHEPPY:
        directories_to_process = glob.glob( os.path.join(local_mount_path, 
                                                         user_path_on_storage, 
                                                         "VHBBHeppy" + version,
                                                         sample_name,
                                                         crab_job_name,
                                                         "*/*"))
    else:
        directories_to_process = glob.glob( os.path.join(local_mount_path, 
                                                         user_path_on_storage, 
                                                         sample_name,
                                                         crab_job_name,
                                                         "*/*"))
    

    # Loop over directories, get full list of files and download them
    for i, directory in enumerate(directories_to_process):
        files_to_download = glob.glob(os.path.join(directory, glob_string))
        print "Subdir:", i, "Number of files to download:", len(files_to_download)

        for ifn, fn in enumerate(files_to_download):
            source = os.path.join(gsiftp_base, fn.replace(local_mount_path, ""))
            target = os.path.join(output_path, os.path.basename(fn))
            subprocess.call(["globus-url-copy", "-stall-timeout", str(timeout), source, target])
            update_progress( 1. * ifn/len(files_to_download))
        # end of loop over files
        print ""
    # end of loop over directories

    # Finally: Unmount storage from local system
    subprocess.call(["gfalFS_umount", local_mount_path])

# End of download


#######################################
# hadd
#######################################

def hadd(name,
         sample_shortname,
         version,        
         basepath = "",
         infile_glob = "output-tagging_*.root*",
         outfile_suffix = "-tagging"
):
    """ Hadd all root files in basepath+jobname to basepath/jobname.root
    """

    input_dir = basepath + "{0}_{1}_{2}/{3}".format(name, 
                                                    version, 
                                                    sample_shortname,
                                                    infile_glob)    
    input_filenames = glob.glob(input_dir)
        
    # Only add the first 4k files (temp workaround)
    if len(input_filenames) > 4000:
        input_filenames = input_filenames[:4000]

    output_filename = basepath + "{0}_{1}_{2}{3}.root".format(name, 
                                                              version, 
                                                              sample_shortname,
                                                              outfile_suffix)    

    subprocess.call(["hadd", "-f", output_filename] + input_filenames)
# End of hadd


#######################################
# cleanup
#######################################

def cleanup(name,
         sample_shortname,
         version,        
         basepath = "",
         infile_glob = "output-tagging_*.root*"):
    """ 
    Remove all files for which GetEntries() fails. Useful after failed downloads.
    """

    input_dir = basepath + "{0}_{1}_{2}/{3}".format(name, 
                                                    version, 
                                                    sample_shortname,
                                                    infile_glob)    
    input_filenames = glob.glob(input_dir)
    if len(input_filenames)==0:
        print "No files found in ", input_dir
        return

    broken = []
    for i_fn, fn in  enumerate(input_filenames):
        print i_fn
        try:
            f = ROOT.TFile(fn, "update")
            t = f.tree
            x = t.GetEntries()
            
            t.GetEntry(10)
            m = t.ca15_mass
        
            if f.IsZombie():
                broken.append(fn)

            t.FlushBaskets()
            t.Write()

            f.Close()
        except AttributeError:
            broken.append(fn)
                            
    for fn in broken:
        print "Removing", fn
        os.remove(fn)
    
    print "{0} of {1} files removed. That's {2:.0f}%".format(len(broken), 
                                                             len(input_filenames),
                                                             100. * len(broken) / len(input_filenames))      
# End of cleanup
