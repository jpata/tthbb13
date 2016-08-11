########################################
# Imports
########################################

import sys
from copy import deepcopy
from itertools import izip
import ConfigParser

from TTH.MEAnalysis.samples_base import xsec
from TTH.Plotting.Datacards.AnalysisSpecificationClasses import Sample, DataSample, Category, Analysis, make_csv_categories_abstract, make_csv_groups_abstract
from TTH.Plotting.joosep.sparsinator import PROCESS_MAP, TRIGGERPATH_MAP
from TTH.MEAnalysis import samples_base
from TTH.MEAnalysis.inputs import sparse_data


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

#For tt+jets, we need to apply the selection that splits the sample into
#different tt+jets categories (ttbarPlusBBbar, ttbarPlusCCbar etc)
def processCut(proc):
    n = PROCESS_MAP[proc]
    return ("process", n, n+1)

def splitByTriggerPath(samples, lumi):
    """
    Given a list of samples, add a cut on a trigger path (SLmu, SLele etc)
    and normalize to the given luminosity.
    """
    out = []
    _lumis = {
        "m": lumi["SingleMuon"],
        "e": lumi["SingleElectron"],
        "mm": lumi["DoubleMuon"],
        "em": lumi["MuonEG"],
        "ee": lumi["DoubleEG"],
    }

    for name, trigpath in TRIGGERPATH_MAP.items():
        for samp in samples:
            newsamp = Sample(
                input_name = samp.input_name,
                output_name = samp.output_name,
                xs_weight = _lumis[name] * samp.xs_weight,
                cuts = samp.cuts + [("triggerPath", trigpath, trigpath+1)]
            )
            out += [newsamp]
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
    config = ConfigParser.ConfigParser()
    config.optionxform = str # Turn on case-sensitivity
    config.read(config_file_path)

    # Get information on sparse input
    sparse_version = config.get("general", "sparse_version")
    input_file = sparse_data[sparse_version].infile
    ngen = sparse_data[sparse_version].ngen
    lumi = sparse_data[sparse_version].lumi
    blr_cuts = sparse_data[sparse_version].blr_cuts

    do_stat_variations = bool(config.get("general", "do_stat_variations"))
    do_fake_data = bool(config.get("general", "do_fake_data"))


    ########################################
    # Samples
    ########################################
    
    sample_lists = {}
    for sample_list in config.get("general","sample_lists").split():

        sample_lists[sample_list] = []

        is_data =  config.get(sample_list, "is_data")

        for sample in config.get(sample_list,"samples").split():

            in_name  = config.get(sample,"in")
            out_name = config.get(sample,"out")

            # Build cuts..
            cuts = []
            # ..Process Cut
            if config.has_option(sample, "process_cut"):
                cuts += processCut( config.get(sample, "process_cut"))
            # ..Other cuts
            if config.has_option(sample, "cuts"):
                for cut_name, lower, upper in triplewise(config.get(sample,"cuts").split()):
                    cuts.append( (cut_name, int(lower), int(upper)) )

            # DATA
            if is_data == "True":
                sample_lists[sample_list].append(
                    DataSample(
                        input_name = in_name,
                        output_name = out_name,
                        cuts = cuts,
                        lumi = lumi[config.get(sample,"lumi")]))
            # SIMULATION
            else:
                sample_lists[sample_list].append(
                    Sample(
                        input_name = in_name,
                        output_name = out_name,
                        cuts = cuts,
                        xs_weight = samples_base.xsec_sample[in_name]/ngen[in_name]))
        # End loop over samples

        if config.get(sample_list, "split_by_trigger_path") == "True":
            sample_lists[sample_list] = splitByTriggerPath(sample_lists[sample_list], lumi)    
    # End loop over samples lists

    # Prepare the samples list for the analysis object
    # TODO: check if needed since we also have per category sample lists
    samples = sum([sample_lists[x] for x in config.get("general", "samples").split()],[])
            

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

            mc_samples = sum([sample_lists[x] for x in config.get(template, "mc_samples").split()], [])
            data_samples = sum([sample_lists[x] for x in config.get(template, "data_samples").split()], [])
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
                rebin = float(config.get(cat,"rebin"))
            else:
                rebin = 1.

            cats.append(
                Category(
                    name = cat,
                    cuts = cuts,
                    samples = mc_samples,
                    data_samples = data_samples,
                    signal_processes = signal_processes, 
                    common_shape_uncertainties = common_shape_uncertainties, 
                    common_scale_uncertainties = common_scale_uncertainties, 
                    scale_uncertainties = scale_uncertainties, 
                    discriminator = config.get(cat, "discriminator"),
                    src_histogram = config.get(template, "src_histogram"),
                    rebin = rebin))
            # End loop over categories
            
        analysis_groups[group] = cats        
    # End loop over groups of categories


    ########################################
    # Put everything together
    ########################################

    analysis = Analysis(
        samples = samples,
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
    analysisFromConfig(sys.argv[1])


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
