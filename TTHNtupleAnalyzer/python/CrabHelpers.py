""" CrabHelpers:
Collection of functions for simple crab3 submission.
"""

#######################################
# Imports
#######################################

import subprocess
import imp
import glob

from TTH.TTHNtupleAnalyzer.Samples import Samples


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
        
    output_filename = basepath + "{0}_{1}_{2}{3}.root".format(name, 
                                                              version, 
                                                              sample_shortname,
                                                              outfile_suffix)    

    subprocess.call(["hadd", "-f", output_filename] + input_filenames)
# End of hadd
