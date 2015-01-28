""" CrabHelpers:
Collection of functions for simple crab3 submission.
"""

#######################################
# Imports
#######################################

import subprocess
import imp
import glob
import re
import os

from TTH.TTHNtupleAnalyzer.Samples import Samples, Samples_lumi
from TTH.TTHNtupleAnalyzer.Helpers import chunks

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
    #template.config.Data.unitsPerJob = Samples_lumi.get(sample_shortname, 90)
    template.config.Data.unitsPerJob = 90
    template.config.Site.storageSite = site

    if blacklist:
        template.config.Site.blacklist = blacklist


    outfile = open(cfg_filename, "w")
    outfile.write(str(template.config))
    outfile.close()

    print "Created config for", sample_shortname
    print "Now calling crab submit"

    #subprocess.call(["crab", "submit", "-c", "c_tmp.py"])
# End of submit


#######################################
# status
#######################################

import json
def status(name,
           sample_shortname,
           version,
           parse=False):
    """Get status of a single job on the Grid."""

    working_dir = "crab_{0}_{1}_{2}/crab_{0}_{1}_{2}".format(name, version, sample_shortname)

    if not parse:
        subprocess.call(["crab", "status", "-d", working_dir], stdout=of)
    else:
        of = open("crab.stdout", "w")
        subprocess.call(["crab", "status", "-d", working_dir, "--json"], stdout=of)
        of.close()
        of = open("crab.stdout", "r")
        lines = of.readlines()
        of.close()
        jsonlines = reduce(
            lambda x,y: dict(x.items() + y.items()),
            map(lambda x: eval(x.strip()), filter(lambda x: x.startswith("{"), lines)),
            {}
        )
        return jsonlines
# End of status


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
# get LFN
#######################################

def get_lfn(name, sample_shortname, version, status_dict, file_output=True, chunksize=500):
    """ Gets the LFNs of successful crab jobs.

    Uses `crab getoutput --dump` to successively get the output LFN of all
    crab jobs which are done

    Args:
        name (string): the nickname of the processing
        sample_shortname (string): the nickname of the sample to merge
        version (string): the processing version/tag of the sample to merge
        basepath (string): the base path for output files
        status_dict (dict): the state of the crab task, retrieved via status() by parsing
            `crab status --json`. Must contain str(job_id) as keys in the form
            {"123": {"State": "finished", ...}, ...}
        file_output (bool, optional): if True, save LFNs to an output file in the crab
            task directory.
        chunksize (int, optional): how many LFNs to get per one `crab getoutput` call.
            A number that is too large (>few k) will cause the crab server to timeout.

    Returns:
        dict(int->string): a map between the successful job ID-s and the LFNs of
            the output files.

    Raises:
        Exception: if `crab getoutput` failed more than an alloted amount of retries.
    """
    working_dir = "crab_{0}_{1}_{2}/crab_{0}_{1}_{2}".format(name, version, sample_shortname)

    lfns = {}
    for ch in chunks(status_dict.keys(), chunksize):
        ch = filter(lambda x: status_dict[x]["State"] == "finished", ch)
        ret = -1
        nretries = 0
        while ret != 0    :
            of = open("crab.stdout", "w")
            ret = subprocess.call(["crab", "getoutput", "-d", working_dir, "--dump", "--wait=120", "--jobids=" + ",".join(ch)] , stdout=of)
            of.close()
            nretries += 1
            if nretries > 10:
                raise Exception("ERROR: could not get output" + "".join(open("crab.stdout", "r").readlines()))
        of = open("crab.stdout", "r")
        lines = "".join(of.readlines())
        lines = lines.split("===")
        for line in lines:
            m = re.match(".*job ([0-9]+)\n.*\nLFN: (/.*root)\n", line)
            if m:
                lfns[int(m.group(1))] = m.group(2)
        print "got", len(lfns), "items"
    return lfns
# End of get LFN


#######################################
# hadd
#######################################

def hadd(name,
         sample_shortname,
         version,
         basepath = ""):
    """ Hadd all root files in basepath+jobname to basepath/jobname.root
    """

    input_dir = basepath + "{0}_{1}_{2}/*".format(name, version, sample_shortname)
    input_filenames = glob.glob(input_dir)

    output_filename = basepath + "{0}_{1}_{2}.root".format(name, version, sample_shortname)

    subprocess.call(["hadd", "-f", output_filename] + input_filenames)

def hadd_from_file(name,
         sample_shortname,
         version,
         basepath = ""):
    """ Merges the output of crab jobs which are in storage.

    The output file lists must be stored in the crab directory as files.txt.
    These file lists can be created using get_lfn(). This command uses ParHadd.py
    to speed up the merge.

    Args:
        sample_shortname (string): the nickname of the sample to merge
        version (string): the processing version/tag of the sample to merge
        basepath (string): the base path for output files

    Returns: nothing
    """

    input_fn = "crab_{0}_{1}_{2}/crab_{0}_{1}_{2}/files.txt".format(name, version, sample_shortname)
    if os.path.isfile(input_fn):
        input_filenames = map(lambda x: x.strip(), open(input_fn).readlines())
        if len(input_filenames)>0:
            output_filename = basepath + "/{0}_{1}_{2}.root".format(name, version, sample_shortname)
            #subprocess.call(["echo", "hadd", "-f", output_filename, "-n", "500"] + input_filenames)
            subprocess.call(["python", "../python/ParHadd.py", output_filename] + input_filenames)
            return
    print "no output from {0}".format(sample_shortname)
# End of hadd
