import os, subprocess

def hadd_from_file(
        input_fn,
        name,
        basepath = "./"):
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
            output_filename = basepath + "/" + name + ".root"
            #subprocess.call(["echo", "hadd", "-f", output_filename, "-n", "500"] + input_filenames)
            subprocess.call(["python", os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/python/ParHadd.py", output_filename] + input_filenames)
            return output_filename
        else:
            print "no files in", input_fn
    return None
