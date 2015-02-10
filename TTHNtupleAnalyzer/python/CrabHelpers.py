""" CrabHelpers:
Collection of functions for simple crab3 submission.
"""

#######################################
# Imports
#######################################

import re
import os
import imp
import sys
import glob
import subprocess

from TTH.TTHNtupleAnalyzer.Samples import Samples, Samples_lumi
from TTH.TTHNtupleAnalyzer.Helpers import chunks


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

    #For very large samples, e.g tt + jets, a low file count can overflow CRAB3s built-in job limit of 13k
    template.config.Data.unitsPerJob = Samples_lumi.get(sample_shortname, 90)
    #template.config.Data.unitsPerJob = 90

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
                    glob_string = "*"):
    """Download a single job from the Grid using globus-url-copy instead of crab
    """

    timeout = 5 # seconds

    storage_host = "storage01.lcg.cscs.ch"
    gsiftp_base = "gsiftp://" + storage_host
    srm_base    = "srm://" + storage_host
    user_path_on_storage = "pnfs/lcg.cscs.ch/cms/trivcat/store/user/{0}/".format(user_name)
    local_mount_path = "/scratch/{0}/mount/storage/".format(user_name)
    output_path = os.path.join(basepath, "{0}_{1}_{2}".format(name, version, sample_shortname))

    crab_job_name = "crab_{0}_{1}_{2}".format(name, version, sample_shortname)
    sample_name = Samples[sample_shortname].split("/")[1]

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
# get LFN
#######################################

def get_lfn(name, sample_shortname, version, status_dict, file_output=True, chunksize=100):
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
    nchunk = 0
    for ch in chunks(status_dict.keys(), chunksize):
        ch = sorted(filter(lambda x: status_dict[x]["State"] == "finished", ch))
        ret = -1
        nretries = 0
        curlfns = {}
        if len(ch)==0:
            continue
        while ret != 0 or len(curlfns) != len(ch):
        #while ret != 0:
            try:
                print "getting LFN for chunk ", nchunk, len(ch)
                of = open("crab.stdout", "w")
                ret = subprocess.call(["crab", "getoutput", "-d", working_dir, "--dump", "--wait=120", "--jobids=" + ",".join(ch)] , stdout=of)
                #print "crab getoutput call", ret
                of.close()
                nretries += 1
                if nretries > 10:
                    print "exceeded maximum amount of retries"
                    break
                    #raise Exception("ERROR: could not get output" + "".join(open("crab.stdout", "r").readlines()))
                of = open("crab.stdout", "r")
                lines = "".join(of.readlines())
                #print lines
                if len(lines) == 0:
                    raise Exception("ERROR: could not get output, stdout was empty")
                lines = lines.split("===")
                totlines = "".join(lines)
                for line in lines:
                    m = re.match(".*job ([0-9]+).*\n.*\n.*LFN.* (/.*root).*", line)
                    if m:
                        curlfns[int(m.group(1))] = m.group(2)
                ready = "No files to retrieve" not in totlines
                if not ready:
                    break
                if ready and len(curlfns) == 0:
                    print totlines
                    raise Exception("Could not match any LFN using regex, probably CRAB3 output has changed")
                print "got {0} LFNs".format(len(curlfns))
            except Exception as e:
                print e
        nchunk += 1
        lfns.update(curlfns)
    ch = filter(lambda x: status_dict[x]["State"] == "finished", status_dict.keys())
    assert(len(lfns) == len(ch))
    return lfns
# End of get LFN


#######################################
# hadd
#######################################

def hadd(name,
         sample_shortname,
         version,
         basepath = "",
         infile_glob = "*",
         outfile_suffix = ""):
    """ Hadd all root files in basepath+jobname to basepath/jobname.root"""

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

    Returns: name of total root file if successful, otherwise nothing
    """

    input_fn = "crab_{0}_{1}_{2}/crab_{0}_{1}_{2}/files.txt".format(name, version, sample_shortname)
    if os.path.isfile(input_fn):
        input_filenames = map(lambda x: x.strip(), open(input_fn).readlines())
        to_process = []
        for inf in input_filenames:
            if not os.path.isfile(inf):
                print "ERROR: file", inf, "does not exist!"
                continue
            to_process += [inf]
        input_filenames = to_process
        if len(input_filenames)>0:
            output_filename = basepath + "/{0}_{1}_{2}.root".format(name, version, sample_shortname)
            #subprocess.call(["echo", "hadd", "-f", output_filename, "-n", "500"] + input_filenames)
            subprocess.call(["python", "../python/ParHadd.py", output_filename] + input_filenames)
            return output_filename
    print "no output from {0}".format(sample_shortname)
    return None
# End of hadd_from_file

def replicate(fname, site, path):
    """ Replicates the files created by hadd_from_file using SRM data replication

    The list of files to copy is processed by the data_replica.py script.

    Args:
        fname (string): name of the file that contains the filenames to replicate.
        site (string): the CMS site name to copy to
        path (string): the LFN prefix to copy to. Will be created by data_replica.py.

    Returns: the return code of the data_replica.py script
    """

    return subprocess.call([
        "python", "../python/data_replica.py",
        "--delete",
        "--from", "LOCAL",
        "--to", site,
        fname,
        path
        ]
    )
# End of replicate
