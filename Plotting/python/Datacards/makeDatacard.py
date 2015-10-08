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
        dcof.write("shapes * {0} {1} $PROCESS/$CHANNEL/{2} $PROCESS/$CHANNEL/{2}_$SYSTEMATIC\n".format(cat, datacard.histfilename, analysis_var))

    #dcof.write("shapes data_obs sl_jge6_tge4 /shome/jpata/tth/datacards/Sep7_ref2_spring15/fakeData.root $PROCESS/$CHANNEL/mem_d_nomatch_0 $PROCESS/$CHANNEL/mem_d_nomatch_0_$SYSTEMATIC\n")
        
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
    
# end of PrintDataCard
def MakeDatacard(infile_path, outfile_path, shapefile_path, do_stat_variations=False):
    """
    Makes shape.root and shape.txt for combine from an input root file with multiple categories.

    Different distributions can be defined for different categories, but only one
    must be defined for each category.

    Process 1 (first in TFile) defines the distribution names.

    All systematics must exist for all processes and categories.

    Example file structure:
        #process 1
        proc1/cat1/distr1
        proc1/cat1/distr1_CMS_syst1Up
        proc1/cat1/distr1_CMS_syst1Down
        ... (other systematics)

        proc1/cat2/distr1
        proc1/cat2/distr1_CMS_syst1Up
        proc1/cat2/distr1_CMS_syst1Down
        ...

        proc1/cat3/distr2
        proc1/cat3/distr2_CMS_syst1Up
        proc1/cat3/distr2_CMS_syst1Down
        
        #process 2
        proc2/cat1/distr1... (all systematics)
        proc2/cat2/distr1...
        proc2/cat3/distr2...

    Fit will be made combining cat1, cat2, cat3.

    All categories must exist for all processes.

    infile_path (string): path to ControlPlots.root with processes and categories
    outfile_path (string): path to output root file for combine (must be writable)
    shapefile_path (string): path to output txt file for combine (must be writable)

    do_stat_variations (bool) : enable or disable statistical bin-by-bin variations
    """
    infile = ROOT.TFile(infile_path)
    shutil.copy(infile_path, outfile_path)

    #datacard root file
    outfile = ROOT.TFile(outfile_path, "UPDATE")

    #get all processes in input file
    processes = getProcesses(infile)

    ####Step 1
    #get all histograms in input file, put to dict.
    # histmap = {}
    # for proc in processes:
    #     histmap[proc] = {}
    #     categories = getCategories(infile, proc)
    #     for cat in categories:
    #         distributions = getDistributions(infile, proc, cat)
    #         histmap[proc][cat] = {}
    #         for distr in distributions:
    #             histmap[proc][cat][distr] = infile.Get("{0}/{1}/{2}".format(proc, cat, distr)) 

    #get the first process and all categories 
    proc_first = processes[0]

    #currently just assume that tt+H has the same categories as every other process
    allcats = getCategories(infile, proc_first)

    ####Step 2
    #get the nominal histograms in each category
    hists_nominal = {}
    for cat in allcats:
        #get all histo names
        allhists = getDistributions(infile, proc_first, cat)

        #assume all systematics have "CMS" in them
        cat_hists_nominal = filter(lambda x: "CMS" not in x, allhists)
        if len(cat_hists_nominal) != 1:
            raise Exception("multiple nominal histogram per category")
        hist_nominal = cat_hists_nominal[0]
        hists_nominal[cat] = hist_nominal

        #copy all histograms to output file
        #copyHistograms(infile, outfile, allhists, [cat], processes)
        if do_stat_variations:
            makeStatVariations(outfile, outfile, [hist_nominal], [cat], processes)

        fakeData(outfile, outfile, [hist_nominal], [cat], processes)
    
    #now make a datacard object which knows about systematics
    dcard = Datacard(processes, allcats, hists_nominal)

    #configure root file name for shapes.txt
    dcard.histfilename = outfile_path

    #Need to also add statistical variations to Datacard.shape_uncertainties
    if do_stat_variations:
        for cat in allcats:
            #number of bins depends on distribution
            nbins = infile.Get("{0}/{1}/{2}".format(proc_first, cat, hists_nominal[cat])).GetNbinsX()
            dcard.addStatVariations(cat, nbins)

    #output shapes.txt
    shapefile = open(shapefile_path, "w")

    #Step 3: the total yields per processes
    event_counts = {}
    for process in dcard.processes:
        #print " sample", sample
        sampled = outfile.Get(process)
        assert(sampled != None)
        sampled.cd()
        event_counts[process] = {}
        for category in dcard.categories:
            histname = dcard.distributions[category]
            cat_dir = sampled.Get(category)
            if cat_dir != None:
                h = cat_dir.Get(histname)
                I = 0
                if h != None:
                    I = h.Integral()
                event_counts[process][category] = I
            else:
                event_counts[process][category] = 0

    #remove empty categories from fit to prevent combine error
    # if np_bin == 0: raise RuntimeError, "Bin %s has no processes contributing to it" % b
    #    RuntimeError: Bin btag_LR_4b_2b_logit__10_0__20_0__numJets__3__4 has no processes contributing to it
    categories = []
    for cutname in dcard.categories:
        s = 0
        sbg = 0
        for sample in dcard.processes:
            s += event_counts[sample][cutname]
            if "ttH" not in sample:
                sbg += event_counts[sample][cutname]
        if s > 0 and sbg > 0:
            categories += [cutname]
        else:
            print "removing category", cutname, s, sbg

    #override with list of good categories
    dcard.categories = categories

    PrintDatacard(event_counts, dcard, shapefile)
    shapefile.close()
    infile.Close()
    outfile.Close()

# end of MakeDatacard

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

if __name__ == "__main__":
    # Get the input proto-datacard

    # import cProfile
    # 
    # def f():
    #     #finalize datacard to txt file
    #     for i in range(10):
    #         MakeDatacard(sys.argv[1], "shapes.root", "shapes.txt", do_stat_variations=False)
    # 
    # cProfile.run("f()")
    
    # timeit.timeit("g()", number=10)
    MakeDatacard(sys.argv[1], "shapes.root", "shapes.txt", do_stat_variations=False)
