########################################
# Imports
########################################

import sys
from copy import deepcopy
from itertools import izip

from TTH.MEAnalysis.samples_base import xsec
from TTH.Plotting.Datacards.AnalysisSpecificationClasses import Sample, Process, DataProcess, Category, Analysis, make_csv_categories_abstract, make_csv_groups_abstract
from TTH.Plotting.joosep.sparsinator import PROCESS_MAP, TRIGGERPATH_MAP
from TTH.MEAnalysis import samples_base


########################################
# Helper Functions
########################################

# From:
# http://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list
def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a)

def triplewise(iterable):
    "s -> (s0, s1, s2), (s3, s4, s5), (s5, s6, s7), ..."
    a = iter(iterable)
    return izip(a, a, a)

#For tt+jets, we need to apply the selection that splits the processes into
#different tt+jets categories (ttbarPlusBBbar, ttbarPlusCCbar etc)
def processCut(proc):
    n = PROCESS_MAP[proc]
    return ("process", n, n+1)

def splitByTriggerPath(processes, lumi):
    """
    Given a list of processes, add a cut on a trigger path (SLmu, SLele etc)
    and normalize to the given luminosity.
    """
    out = []
    _lumis = {
        "m": lumi["SingleMuon"],
        "e": lumi["SingleElectron"],
        "mm": lumi["DoubleMuon"],
        "em": lumi["MuonEG"],
        "ee": lumi["DoubleEG"],
        "fh": lumi["BTagCSV"],
    }

    for name, trigpath in TRIGGERPATH_MAP.items():
        for proc in processes:
            newproc = Process(
                input_name = proc.input_name,
                output_name = proc.output_name,
                xs_weight = _lumis[name] * proc.xs_weight,
                cuts = proc.cuts + [("triggerPath", trigpath, trigpath+1)]
            )
            out += [newproc]
    return out


########################################
# analysisFromConfig
########################################

def updateSamples(config, sample):
    config.set(sample.name, "files_load", sample.files_load)
    config.set(sample.name, "is_data", sample.is_data)
    config.set(sample.name, "step_size_sparsinator", sample.step_size_sparsinator)
    config.set(sample.name, "debug_max_files", sample.debug_max_files)
    config.set(sample.name, "ngen", sample.ngen)

def analysisFromConfig(config_file_path):
    """ Create Analysis object from cfg file """

    ########################################
    # Setup
    ########################################

    # Init config parser
    config = Analysis.getConfigParser(config_file_path)

    # Get information on sparse input
    sparse_version = config.get("general", "sparse_version")
    input_file = config.get("sparse_data", "infile")
    lumi = dict([(k, float(v)) for (k, v) in config.items("lumi")])
    blr_cuts = dict([(k, float(v)) for (k, v) in config.items("blr_cuts")])

    do_stat_variations = bool(config.get("general", "do_stat_variations"))
    do_fake_data = bool(config.get("general", "do_fake_data"))
    DEBUG = config.getboolean("general", "debug")

    ########################################
    # Samples
    ########################################

    samples_list = config.get("samples","samples_list").split()
    samples = []
    for sample_name in samples_list:
        sample = Sample.fromConfigParser(config, sample_name)
        samples += [sample]

    samples_dict = dict([(sample.name, sample) for sample in samples])

    ########################################
    # Processes
    ########################################
    
    process_lists = {}
    for process_list in config.get("general","process_lists").split():

        process_lists[process_list] = []

        is_data =  config.get(process_list, "is_data")

        for process in config.get(process_list,"processes").split():

            in_name  = config.get(process,"in")
            out_name = config.get(process,"out")

            # Build cuts..
            cuts = []
            # ..Process Cut
            if config.has_option(process, "process_cut"):
                cuts += [processCut( config.get(process, "process_cut"))]
            # ..Other cuts
            if config.has_option(process, "cuts"):
                for cut_name, lower, upper in triplewise(config.get(process,"cuts").split()):
                    cuts.append( (cut_name, int(lower), int(upper)) )

            # DATA
            if is_data == "True":
                process_lists[process_list].append(
                    DataProcess(
                        input_name = in_name,
                        output_name = out_name,
                        cuts = cuts,
                        lumi = lumi[config.get(process,"lumi")]))
            # SIMULATION
            else:
                process_lists[process_list].append(
                    Process(
                        input_name = in_name,
                        output_name = out_name,
                        cuts = cuts,
                        xs_weight = samples_base.xsec_sample[in_name]/samples_dict[in_name].ngen))
        # End loop over processes

        if config.get(process_list, "split_by_trigger_path") == "True":
            process_lists[process_list] = splitByTriggerPath(process_lists[process_list], lumi)    
    # End loop over processes lists

    # Prepare the process list for the analysis object
    # TODO: check if needed since we also have per category process lists
    processes = sum([process_lists[x] for x in config.get("general", "processes").split()],[])
            

    ########################################
    # Categories
    ########################################

    analysis_groups = {}

    for group in config.get("general","analysis_groups").split():

        cats = []
        for cat in config.get(group,"categories").split():

            template = config.get(cat, "template")

            cuts = []
            for cut_name, lower, upper in triplewise(config.get(cat,"cuts").split()):
                cuts.append( (cut_name, int(lower), int(upper)) )

            mc_processes = sum([process_lists[x] for x in config.get(template, "mc_processes").split()], [])
            data_processes = sum([process_lists[x] for x in config.get(template, "data_processes").split()], [])
            signal_processes = config.get(template, "signal_processes").split()

            common_shape_name = config.get(template, "common_shape_uncertainties")        
            common_shape_uncertainties = {k:float(v) for k,v in config.items(common_shape_name)}

            common_scale_name = config.get(template, "common_scale_uncertainties")
            common_scale_uncertainties = {k:float(v) for k,v in config.items(common_scale_name)}        

            scale_name = config.get(template, "scale_uncertainties")
            scale_uncertainties = {}
            for k,v in config.items(scale_name):
                scale_uncertainties[k] = {}
                for name, uncert in pairwise(v.split()):
                    scale_uncertainties[k][name] = float(uncert)

            if config.has_option(cat, "rebin"):
                rebin = int(config.get(cat,"rebin"))
            else:
                rebin = 1

            cats.append(
                Category(
                    name = cat,
                    cuts = cuts,
                    processes = mc_processes,
                    data_processes = data_processes,
                    signal_processes = signal_processes, 
                    common_shape_uncertainties = common_shape_uncertainties, 
                    common_scale_uncertainties = common_scale_uncertainties, 
                    scale_uncertainties = scale_uncertainties, 
                    discriminator = config.get(cat, "discriminator"),
                    src_histogram = config.get(template, "src_histogram"),
                    rebin = rebin,
                    do_limit = True))

            # Also add control variables
            if config.has_option(cat, "control_variables"):
                for cv in config.get(cat, "control_variables").split():
                    cats.append(
                        Category(
                            name = cat,
                            cuts = cuts,
                            processes = mc_processes,
                            data_processes = data_processes,
                            signal_processes = signal_processes, 
                            common_shape_uncertainties = common_shape_uncertainties, 
                            common_scale_uncertainties = common_scale_uncertainties, 
                            scale_uncertainties = scale_uncertainties, 
                            discriminator = cv,
                            src_histogram = config.get(template, "src_histogram"),
                            rebin = rebin,
                            do_limit = False))
                


            # End loop over categories
            
        analysis_groups[group] = cats        
    # End loop over groups of categories


    ########################################
    # Put everything together
    ########################################

    analysis = Analysis(
        debug = DEBUG,
        samples = samples,
        processes = processes,
        categories = cats,
        sparse_input_file = input_file,
        groups = analysis_groups,
        do_fake_data = do_fake_data,
        do_stat_variations = do_stat_variations
     )   

    return config.get("general","name"), analysis

# end of analysisFromConfig


########################################
# main
########################################

if __name__ == "__main__":
    an = analysisFromConfig(sys.argv[1])


# TODO: handle
#control_variables = [
#    "jetsByPt_0_pt",
#    "btag_LR_4b_2b_btagCSV_logit",
##    "btag_LR_4b_2b_btagCMVA_logit"
#]
#
# all_cats = make_control_categories(sl_categories)
#def make_control_categories(input_categories):
#    all_cats = copy.deepcopy(input_categories)
#    for discr in control_variables:
#        for cat in input_categories:
#            #Update only the discriminator, note that this is hacky and may not
#            #work in the future, because we assume the object is final
#            #after the constructor
#            newcat_d = cat.__dict__
#            newcat_d["discriminator"] = discr
#            newcat_d["do_limit"] = False
#            newcat = Category(**newcat_d)
#            all_cats += [newcat]
#    return all_cats
#
# TODO: Implement
##add single-category groups
#for cat in sl_categories:
#    analysis.groups[cat.full_name] = [cat]
## for cat in sl_categories_bdt:
##     analysis_bdt.groups[cat.full_name] = [cat]
#
