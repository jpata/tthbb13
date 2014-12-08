""" CrabHelpers:
Collection of functions for simple crab3 submission.
"""

#######################################
# Imports
#######################################

import subprocess
import imp

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
           cfg_filename = "c_tmp.py"
           blacklist = []):
    """Submit a single job to the Grid"""

    # Import template, add parameters and save to new file
    imp.load_source("template", template_filename)
    import template    

    template.config.General.workArea = "crab_{0}_{1}_{2}".format(name, version, sample_shortname)
    template.config.General.requestName = "{0}_{1}_{2}".format(name, version, sample_shortname)
    template.config.JobType.psetName = cmssw_config_path + cmssw_config_script
    template.config.Data.inputDataset = Samples[sample_shortname]
    template.config.Data.unitsPerJob = 90
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
