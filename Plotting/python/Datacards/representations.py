import ROOT

from collections import OrderedDict

from utils import sum_sig_bkg, get_bins

import numpy as np

class DatacardRepresentation(object):
    def __init__(self, samples_sig=[], samples_bkg=[]):
        self.samples_sig = samples_sig
        self.samples_bkg = samples_bkg

        self.all_samples = []
        self.all_systematics = []

    def filter_hist(self, name):
        """Keeps only histograms we're interested in for SoB studies
        
        Args:
            name (string): Histogram name
        
        Returns:
            bool: If histogram should be kept or not
        """
        return True

    def get_key(self, name):
        """Maps a histogram name to a (sample, category, systematic) key
        
        Args:
            name (string): Histogram name
        
        Returns:
            tuple: (sample, category, systematic) identifier of the histogram
        """
        return ("sample", "category", "systematic")

    def get_all_histograms(self, infile):
        fi = ROOT.TFile(infile)
        ROOT.gROOT.cd()
        all_histograms = {
            k.GetName(): k.ReadObj().Clone()
            for k in fi.GetListOfKeys() if self.filter_hist(k.GetName())
        }
        fi.Close()
        return all_histograms

    def filter_key(self, key):
        samp, cat, syst = key
        return True

    def get_representation(self, infile):
        histograms = self.get_all_histograms(infile)

        #create dictionary with [category][sample][systematic] -> bin data
        nd = OrderedDict()
        cats = set([])
        samps = set([])
        systs = set([])
        for k in sorted(histograms.keys()):
            samp, cat, syst = self.get_key(k)
            if not self.filter_key((samp, cat, syst)):
                continue
            if not nd.has_key(cat):
                nd[cat] = OrderedDict()
            if not nd[cat].has_key(samp):
                nd[cat][samp] = OrderedDict()
            if not nd[cat][samp].has_key(syst):
                nd[cat][samp][syst] = OrderedDict()
            nd[cat][samp][syst] = get_bins(histograms[k])
            samps.add(samp)
            systs.add(syst)
            cats.add(cat)

        self.all_categories = list(cats)
        self.all_samples = list(samps)
        self.all_systematics = list(systs)

        return nd

    def calculate_signal_over_background(self, data):
        return sum_sig_bkg(
            data,
            self.samples_sig,
            self.samples_bkg,
        )

class KIT_SL_v13_DatacardRepresentation(DatacardRepresentation):
    def __init__(self):
        super(KIT_SL_v13_DatacardRepresentation, self).__init__(
            samples_sig = [
                'ttH_hbb'
            ],
            samples_bkg = [
                'ttbarOther',
                'ttbarPlusCCbar',
                'ttbarPlusB',
                'ttbarPlus2B',
                'ttbarPlusBBbar',
                'ttH_hcc',
                'ttH_htt',
                'ttH_hgg',
                'ttH_hgluglu',
                'ttH_hww',
                'ttH_hzz',
                'ttH_hzg',
                'singlet',
                'zjets',
                'wjets',
                'ttbarW',
                'ttbarZ',
                'diboson',
            ]
        )

    def filter_hist(self, name):
        return "finaldiscr" in name and not "BDTbin" in name

    def get_key(self, name):
        i0 = name.index("_finaldiscr")
        samp = name[0:i0]
        rest = name[i0+1:]
        if "_CMS" in rest:
            i1 = rest.index("_CMS")
            cat = rest[0:i1]
            syst = rest[i1+1:]
        else:
            cat = rest
            syst = "nominal"
        return samp, cat, syst

    def filter_key(self, key):
        samp, cat, syst = key
        if cat in [
            "finaldiscr_ljets_j4_t3",
            "finaldiscr_ljets_j4_t4",
            "finaldiscr_ljets_j5_t3",
            "finaldiscr_ljets_j5_tge4",
            "finaldiscr_ljets_jge6_t3",
            "finaldiscr_ljets_jge6_tge4",
            ]:
            return False
        return True

class DESY_DL_v13_DatacardRepresentation(DatacardRepresentation):
    def __init__(self):
        super(DESY_DL_v13_DatacardRepresentation, self).__init__(
            samples_sig = [
                'ttH_hbb'
            ],
            samples_bkg = [
                'ttbarOther',
                'ttbarPlusCCbar',
                'ttbarPlusB',
                'ttbarPlus2B',
                'ttbarPlusBBbar',
                'ttH_hcc',
                'ttH_htt',
                'ttH_hgg',
                'ttH_hgluglu',
                'ttH_hww',
                'ttH_hzz',
                'ttH_hzg',
                'singlet',
                'zjets',
                'wjets',
                'ttbarW',
                'ttbarZ',
                'diboson',
            ]
        )


    def get_all_histograms(self, infile):
        fi = ROOT.TFile(infile)
        ROOT.gROOT.cd()
        all_histograms = {}
        for cat in fi.GetListOfKeys():
            hists = cat.ReadObj().GetListOfKeys()
            for h in hists:
                name = "{0}/{1}".format(
                    cat.GetName(),
                    h.GetName()
                )
                if not self.filter_hist(name):
                    continue
                all_histograms[name] = h.ReadObj().Clone()
        fi.Close()
        return all_histograms

    def filter_hist(self, name):
        return "_BDT" in name and not "MetaInfo" in name

    def get_key(self, name):
        cat, rest = name.split("/")
        if "_CMS" in rest:
            i0 = rest.index("_CMS")
            samp = rest[0:i0]
            syst = rest[i0+1:]
        else:
            samp = rest
            syst = "nominal"
        return samp, cat, syst

class CombineRepresentation(DatacardRepresentation):
    def __init__(self):
        super(CombineRepresentation, self).__init__(
            samples_sig = [
                'total_signal'
            ],
            samples_bkg = [
                'total_background'
            ]
        )

    def get_all_histograms(self, infile):
        fi = ROOT.TFile(infile)
        ROOT.gROOT.cd()
        all_histograms = {}
        for shape_dir in ["shapes_fit_s", "shapes_fit_b", "shapes_prefit"]:
            sdir = fi.Get(shape_dir)
            cats = [k.GetName() for k in sdir.GetListOfKeys()]
            for cat in cats:
                cat_dir = sdir.Get(cat)
                hists = [k for k in cat_dir.GetListOfKeys()]
                for h in hists:
                    if h.GetName() in self.samples_sig+self.samples_bkg:
                        name = "{0}/{1}/{2}".format(
                            shape_dir,
                            cat,
                            h.GetName()
                        )
                        all_histograms[name] = h.ReadObj().Clone()
        fi.Close()
        return all_histograms

    def get_key(self, name):
        syst, cat, samp = name.split("/")
        return samp, cat, syst

    def filter_hist(self, name):
        return not "total_covar" in name

    def calculate_signal_over_background(self, data):
        ret = -100000
        if data["total_background"]["shapes_prefit"][0] > 0:
            ret = np.log10(
                data["total_signal"]["shapes_prefit"][0] / data["total_background"]["shapes_prefit"][0]
            )
        return ret

all_representations = {
    "KIT_SL_v13_DatacardRepresentation": KIT_SL_v13_DatacardRepresentation,
    "DESY_DL_v13_DatacardRepresentation": DESY_DL_v13_DatacardRepresentation,
}