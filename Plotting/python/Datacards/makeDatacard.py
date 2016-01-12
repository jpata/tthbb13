#!/usr/bin/env python
import ROOT, shutil
ROOT.gROOT.SetBatch(True)
#ROOT.gErrorIgnoreLevel = ROOT.kError
import sys, imp, os, copy
from Samples import samples_dict
from datacardCombiner import makeStatVariations, copyHistograms, defaultHistogram, fakeData, combineCategories
from datacard import Datacard
def PrintDatacard(event_counts, datacard, dcof):

    number_of_bins = len(datacard.categories)
    number_of_backgrounds = len(datacard.processes) - 1 
    analysis_categories = list(datacard.categories)

    dcof.write("imax {0}\n".format(number_of_bins))
    dcof.write("jmax {0}\n".format(number_of_backgrounds))
    dcof.write("kmax *\n")
    dcof.write("---------------\n")

    for cat in datacard.categories:
        analysis_var = datacard.distributions[cat]
        dcof.write("shapes * {0} {1} $PROCESS/$CHANNEL/{2} $PROCESS/$CHANNEL/{2}_$SYSTEMATIC\n".format(
            cat,
            datacard.filenames_cat[cat],
            analysis_var)
        )
        
    dcof.write("---------------\n")

    dcof.write("bin\t" +  "\t".join(analysis_categories) + "\n")
    dcof.write("observation\t" + "\t".join("-1" for _ in analysis_categories) + "\n")
    dcof.write("---------------\n")

    bins        = []
    processes_0 = []
    processes_1 = []
    rates       = []

    # Conversion: 
    # Example: ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8_hbb -> ttH_hbb

    for cat in datacard.categories:
        for i_sample, sample in enumerate(datacard.processes):
            bins.append(cat)
            processes_0.append(sample)
            if sample in datacard.signal_processes:
                i_sample = -i_sample
            processes_1.append(str(i_sample))
            rates.append(str(event_counts[sample][cat]))

    dcof.write("bin\t"+"\t".join(bins)+"\n")
    dcof.write("process\t"+"\t".join(processes_0)+"\n")
    dcof.write("process\t"+"\t".join(processes_1)+"\n")
    dcof.write("rate\t"+"\t".join(rates)+"\n")
    dcof.write("---------------\n")

    # Gather all scale uncerainties
    all_scale_uncerts = []
    for k,v in datacard.scale_uncertainties.iteritems():
        for kk, vv in v.iteritems():
            all_scale_uncerts.extend(vv.keys())
    # Uniquify
    all_scale_uncerts = list(set(all_scale_uncerts))

    for scale in all_scale_uncerts:
        dcof.write(scale + "\t lnN \t")
        for cat in analysis_categories:
            for sample in datacard.processes:
                if (cat in datacard.scale_uncertainties.keys() and 
                    sample in datacard.scale_uncertainties[cat].keys() and 
                    scale in datacard.scale_uncertainties[cat][sample].keys()):
                    dcof.write(str(datacard.scale_uncertainties[cat][sample][scale]))
                else:
                    dcof.write("-")
                dcof.write("\t")
        dcof.write("\n")

    # Gather all shape uncerainties
    all_shape_uncerts = []
    for k,v in datacard.shape_uncertainties.iteritems():
        for kk, vv in v.iteritems():
            all_shape_uncerts.extend(vv.keys())
    # Uniquify
    all_shape_uncerts = list(set(all_shape_uncerts))

    for shape in all_shape_uncerts:
        dcof.write(shape + "\t shape \t")
        for cat in analysis_categories:
            for sample in datacard.processes:
                if (cat in datacard.shape_uncertainties.keys() and 
                    sample in datacard.shape_uncertainties[cat].keys() and 
                    shape in datacard.shape_uncertainties[cat][sample].keys()):
                    dcof.write(str(datacard.shape_uncertainties[cat][sample][shape]))
                else:
                    dcof.write("-")
                dcof.write("\t")
        dcof.write("\n")
    
    shapename = os.path.basename(datacard.output_datacardname)
    shapename_base = shapename.split(".")[0]
    dcof.write("# Execute with:\n")
    dcof.write("# combine -n {0} -M Asymptotic -t -1 {1} \n".format(shapename_base, shapename))

def MakeDatacard2(
    categorization,
    infile_paths,
    shapefile_path,
    do_stat_variations=False,
    ignore_splittings=False
    ):
    categories = categorization.getCategories(ignore_splittings)
    #FIXME: hardcoded signal process name

    #Find yields per category
    badcats = []

    for cat in categories:
        #FIXME: if category discriminator is None, this will crash as event_counts is not evaluated for skipped categories
        #need to skip category here as well if disc==None
        sig = categorization.event_counts["ttH_hbb"][cat]
        bkg = sum([categorization.event_counts[k][cat] for k in categorization.getProcesses() if k!="ttH_hbb"])
        if sig == 0 and bkg == 0:
            badcats += [cat]

    for cat in badcats:
        print "removing category", cat
        categories.pop(categories.index(cat))

    dcard = Datacard(
        categorization.getProcesses(),
        categories,
        categorization.getLeafDiscriminators(ignore_splittings)
    )
    leaves = categorization.get_leaves(ignore_splittings)

    if do_stat_variations:
        #add statistical variations to datacard based on categorization
        for leaf in leaves:
            nbins = categorization.axes[leaf.discriminator_axis].nbins
            dcard.addStatVariations(str(leaf), nbins)

    dcard.filenames_cat = infile_paths
    shapefile = open(shapefile_path, "w")
    PrintDatacard(categorization.event_counts, dcard, shapefile)

import datacard as datacard

def getProcesses(ofile):
    """
    Get all the processes defined in a histogram file
    """

    processes = []
    for k in ofile.GetListOfKeys():
        processes += [k.GetName()]
    return processes

def getCategories(ofile, process):
    """
    Get all the categories defined for a process
    """

    categories = []
    d = ofile.Get(process)
    for k in d.GetListOfKeys():
        categories += [k.GetName()]
    return categories

def getDistributions(ofile, process, category):
    """
    Get all the histograms/distributions defined for a process and category
    """

    distributions = []
    d = ofile.Get(process + "/" + category)
    for k in d.GetListOfKeys():
        distributions += [k.GetName()]
    return distributions
