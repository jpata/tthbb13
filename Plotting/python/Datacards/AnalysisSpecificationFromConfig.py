########################################
# Imports
########################################

import sys
import pdb
from copy import deepcopy

from TTH.MEAnalysis.samples_base import xsec
from TTH.Plotting.Datacards.AnalysisSpecificationClasses import Cut, Sample, Process, DataProcess, Category, Analysis, pairwise, triplewise, make_csv_categories_abstract, make_csv_groups_abstract
from TTH.Plotting.joosep.sparsinator import PROCESS_MAP, TRIGGERPATH_MAP
from TTH.MEAnalysis import samples_base


########################################
# Helper Functions
########################################

#For tt+jets, we need to apply the selection that splits the processes into
#different tt+jets categories (ttbarPlusBBbar, ttbarPlusCCbar etc)
def processCut(proc):
    n = PROCESS_MAP[proc]
    return ("process", n, n+1)

def processCutTree(proc):
    if proc == "ttbarPlusB":
        return "(ttCls == 51)"
    elif proc == "ttbarPlus2B":
        return "(ttCls == 52)"
    elif proc == "ttbarPlusBBbar":
        return "(ttCls >= 53)"
    elif proc == "ttbarPlusCCbar":
        return "(ttCls >= 41 && ttCls <= 45)"
    elif proc == "ttbarOther":
        return "(ttCls == 0)"

def splitByTriggerPath(processes, lumi, cuts_dict):
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
                cuts = proc.cuts + [cuts_dict["triggerPath_{0}".format(name)]]
            )
            out += [newproc]
    return out


########################################
# analysisFromConfig
########################################

def analysisFromConfig(config_file_path):
    """ Create Analysis object from cfg file """

    ########################################
    # Setup
    ########################################

    # Init config parser
    config = Analysis.getConfigParser(config_file_path)

    # Get information on sparse input
    input_file = config.get("sparse_data", "infile")
    lumi = dict([(k, float(v)) for (k, v) in config.items("lumi")])
    blr_cuts = dict([(k, float(v)) for (k, v) in config.items("blr_cuts")])

    
    do_stat_variations = config.getboolean("general", "do_stat_variations")    
    do_fake_data = config.getboolean("general", "do_fake_data")
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
    # Cuts
    ########################################

    cuts_list = config.get("cuts","cuts_list").split()
    cuts = []
    for cut_name in cuts_list:
        cut = Cut.fromConfigParser(config, cut_name)
        cuts += [cut]

    cuts_dict = dict([(cut.name, cut) for cut in cuts])

    ########################################
    # Processes
    ########################################
    
    process_lists = {}
    process_lists_original = {}
    for process_list in config.get("general","process_lists").split():


        process_lists_original[process_list] = []
        process_lists[process_list] = []


        is_data =  config.get(process_list, "is_data")

        for process in config.get(process_list,"processes").split():

            in_name  = config.get(process,"in")
            out_name = config.get(process,"out")

            # Build cuts..
            cuts = []
            # ..Process Cut
            if config.has_option(process, "cuts"):
                for cut in config.get(process,"cuts").split():
                    cuts.append(cuts_dict[cut])

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

        #post-processing of processes
        #split by trigger path
        if config.get(process_list, "split_by_trigger_path") == "True":
            process_lists_original[process_list] = process_lists[process_list]
            process_lists[process_list] = splitByTriggerPath(
                process_lists[process_list],
                lumi,
                cuts_dict
            )    
    # End loop over processes lists

    # Prepare the process list for the analysis object
    # TODO: check if needed since we also have per category process lists
    processes = sum([process_lists[x] for x in config.get("general", "processes").split()],[])

    #Processes in unsplit form
    processes_original = []
    for pl in process_lists_original.values():
        for proc in pl:
            processes_original.append(proc)

    ########################################
    # Categories
    ########################################

    analysis_groups = {}

    all_cats = []
    
    for group in config.get("general","analysis_groups").split():

        cats = []
        for cat in config.get(group,"categories").split():

            template = config.get(cat, "template")

            cuts = []
            for cut_name, lower, upper in triplewise(config.get(cat,"cuts").split()):
                cuts.append( (cut_name, float(lower), float(upper)) )

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
        all_cats.extend(cats)
    # End loop over groups of categories

    # Uniquify all categories
    all_cats = list(set(all_cats))


    ########################################
    # Put everything together
    ########################################

    analysis = Analysis(
        config = config,
        debug = DEBUG,
        samples = samples,
        cuts = cuts_dict,
        processes = processes,
        processes_unsplit = processes_original,
        categories = all_cats,
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
