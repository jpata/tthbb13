#!/usr/bin/env python

import ROOT
import os

import math
from collections import OrderedDict

import numpy as np

class NestedDict(OrderedDict):
    def __getitem__(self, key):
        if key in self:
            return self.get(key)
        return self.setdefault(key, NestedDict())

def get_bins(hist):
    """Returns the (bin, error) data corresponding to a histogram
    
    Args:
        hist (TH1D): Input histogram
    
    Returns:
        dictionary (string -> (float, float)): Description
    """
    ret = OrderedDict()
    for ibin in range(1, hist.GetNbinsX() + 1):
        ret["bin_{0}".format(ibin)] = (
            hist.GetBinContent(ibin),
            hist.GetBinError(ibin)
        )
    return ret

def bins_to_category(data):
    """Given a nested dictionary of data[category][sample][sytematic][bin] -> bin data,
    creates per-bin categories
    
    Args:
        data (dict): bin data in a nested dict as [category][sample][sytematic][bin]
    
    Returns:
        dict: a dictionary of [bin category][sample][systematic]
    """
    ret = NestedDict()
    for cat in data.keys():
        for samp in data[cat].keys():
            for syst in data[cat][samp].keys():
                bins = data[cat][samp][syst]
                for b in bins.keys():
                    ret[(cat, b)][samp][syst] = bins[b]
    return ret

def reduce_dict(nd, func):
    """Given a dictionary of key -> val and a reduction function, produces
    a dictionary of key -> func(val)
    
    Args:
        nd (dict): Input dictionary
        func (TYPE): Reduction method that maps input dictionary values to output values 
    
    Returns:
        dict: output dictionary
    """
    ret = OrderedDict()
    for k in nd.keys():
        ret[k] = func(nd[k])
    return ret

def sum_sig_bkg(cat, samples_sig, samples_bkg):
    res = OrderedDict()
    res["sig"] = 0.0
    res["bkg"] = 0.0
    res["other"] = 0.0
    for samp, data in cat.items():
        if samp in samples_sig:
            k2 = "sig"
        elif samp in samples_bkg:
            k2 = "bkg"
        else:
            k2 = "other"

        res[k2] += data["nominal"][0]
    res["sob"] = -1
    if res["bkg"]>0:
        res["sob"] = res["sig"]/res["bkg"]
    res.pop("sig")
    res.pop("bkg")
    res.pop("other")
    res["sob_log"] = -10000
    if res["sob"] > 0:
        res["sob_log"] = np.log10(res["sob"])
    return res["sob_log"]

def make_hist(name, cat, sob_data, bins):
    nb = len(cat)
    h = ROOT.TH1D(name, name, len(bins), bins)
    ks = cat.keys()
    for i in range(nb):
        sob = sob_data[i]
        ibin = h.FindBin(sob)
        b = h.GetBinContent(ibin)
        e = h.GetBinError(ibin)
        h.SetBinContent(ibin, b+cat[ks[i]][0])
        h.SetBinError(ibin, math.sqrt(e**2 + cat[ks[i]][1]**2))
    return h

def make_hist_bins(name, cat, sob_data, nbins=10, lo=0, hi=0.5):
    nb = len(cat)
    h = ROOT.TH1D(name, name, nb, 0, nb)
    ks = cat.keys()
    for i in range(nb):
        h.SetBinContent(i + 1, cat[ks[i]][0])
        h.SetBinError(i + 1, cat[ks[i]][1])
        h.GetXaxis().SetBinLabel(i + 1, "_".join(list(ks[i])))
    return h

def PrintDatacard(categories, event_counts, filenames, dcof):
    number_of_bins = len(categories)
    number_of_backgrounds = len(list(set(reduce(lambda x,y:x+y, [c.out_processes for c in categories], [])))) - 1 
    analysis_categories = list(set([c.name for c in categories]))

    
    dcof.write("imax {0}\n".format(number_of_bins))
    dcof.write("jmax {0}\n".format(number_of_backgrounds))
    dcof.write("kmax *\n")
    dcof.write("---------------\n")

    for cat in categories:
        analysis_var = cat.discriminator
        dcof.write("shapes * {0} {1} $PROCESS/$CHANNEL/{2} $PROCESS/$CHANNEL/{2}_$SYSTEMATIC\n".format(
            cat.name,
            os.path.basename(filenames[cat.name]),
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

    for cat in categories:
        for i_sample, sample in enumerate(cat.out_processes):
            bins.append(cat.name)
            processes_0.append(sample)
            if sample in cat.signal_processes:
                i_sample = -i_sample
            processes_1.append(str(i_sample))
            rates.append(str(event_counts[cat.name][sample]))

    dcof.write("bin\t"+"\t".join(bins)+"\n")
    dcof.write("process\t"+"\t".join(processes_0)+"\n")
    dcof.write("process\t"+"\t".join(processes_1)+"\n")
    dcof.write("rate\t"+"\t".join(rates)+"\n")
    dcof.write("---------------\n")
    
    
    
    # Gather all shape uncerainties
    all_shape_uncerts = []
    all_scale_uncerts = []
    for cat in categories:
        for proc in cat.out_processes:
            all_shape_uncerts.extend(cat.shape_uncertainties[proc].keys())
            all_scale_uncerts.extend(cat.scale_uncertainties[proc].keys())
    # Uniquify
    all_shape_uncerts = sorted(list(set(all_shape_uncerts)))
    all_scale_uncerts = sorted(list(set(all_scale_uncerts)))
    
    for syst in all_shape_uncerts:
        dcof.write(syst + "\t shape \t")
        for cat in categories:
            for proc in cat.out_processes:
                if (cat.shape_uncertainties.has_key(proc) and
                    cat.shape_uncertainties[proc].has_key(syst)):
                    dcof.write(str(cat.shape_uncertainties[proc][syst]))
                else:
                    dcof.write("-")
                dcof.write("\t")
        dcof.write("\n")
    

    for syst in all_scale_uncerts:
        dcof.write(syst + "\t lnN \t")
        for cat in categories:
            for proc in cat.out_processes:
                if (cat.scale_uncertainties.has_key(proc) and
                    cat.scale_uncertainties[proc].has_key(syst)):
                    dcof.write(str(cat.scale_uncertainties[proc][syst]))
                else:
                    dcof.write("-")
                dcof.write("\t")
        dcof.write("\n")
    # 
    # shapename = os.path.basename(datacard.output_datacardname)
    # shapename_base = shapename.split(".")[0]
    # dcof.write("# Execute with:\n")
    # dcof.write("# combine -n {0} -M Asymptotic -t -1 {1} \n".format(shapename_base, shapename))


def makeStatVariations(tf, of, categories):
    """
    Given an input TFile and an output TFile, produces the histograms for
    bin-by-bin variations for the given categories.
    """
    ret = {}
    for cat in categories:
        ret[cat.name] = {}
        for proc in cat.out_processes:
            ret[cat.name][proc] = []
            hn = "{0}/{1}/{2}".format(proc, cat.name, cat.discriminator)
            h = tf.Get(hn)
            h = h.Clone()
            outdir = "{0}/{1}".format(proc, cat.name)
            if of.Get(outdir) == None:
                of.mkdir(outdir)
            outdir = of.Get(outdir)
            for ibin in range(1, h.GetNbinsX() + 1):
                systname = "{0}_{1}_Bin{2}".format(proc, cat.name, ibin)
                ret[cat.name][proc] += [systname]
                for sigma, sdir in [(+1, "Up"), (-1, "Down")]:
                    outdir.cd()
                    systname_sdir = h.GetName() + "_" + systname + sdir
                    hvar = h.Clone(systname_sdir)
                    delta = hvar.GetBinError(ibin)
                    c = hvar.GetBinContent(ibin) + sigma*delta
                    if c <= 10**-5 and h.Integral() > 0:
                        c = 10**-5
                    hvar.SetBinContent(ibin, c)
                    outdir.Add(hvar)
                    hvar.Write("", ROOT.TObject.kOverwrite)
    return ret
#end of makeStatVariations

def fakeData(infile, outfile, categories):
    dircache = {}
    for cat in categories:
        h = infile.Get("{0}/{1}/{2}".format(
            cat.out_processes[0], cat.name, cat.discriminator
        )).Clone()
        for proc in cat.out_processes[1:]:
            h2 = infile.Get("{0}/{1}/{2}".format(
                proc, cat.name, cat.discriminator
            ))
            h.Add(h2)

        outdir = "data_obs/{0}".format(cat.name)
        dircache[outdir] = h 

    # End of loop over categories
    for (k, v) in dircache.items():
        if outfile.Get(k) == None:
            outfile.mkdir(k)
        k = outfile.Get(k)
        v.SetDirectory(k)
        k.Write("", ROOT.TObject.kOverwrite)
#end of fakeData
