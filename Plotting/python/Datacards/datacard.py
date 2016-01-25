import copy

class Datacard:
    def __init__(self, processes, categories, distributions):

        #list of all processes to consider
        self.processes = processes

        #Perform combined fit across these categories
        #list of category names (strings)
        self.categories = categories
        
        #map of category -> distributon name used for fit
        self.distributions = distributions

        # Subset of the reweighted distributions we want to use as syst. shape uncertainties    
        # To avoid copy paste
        self.common_shape_uncertainties = {
            "CMS_scale_j"       : 1,
            "CMS_ttH_CSVLF"       : 1,
            "CMS_ttH_CSVHF"       : 1,
            "CMS_ttH_CSVcErr1"    : 1,
            "CMS_ttH_CSVcErr2"    : 1,
            "CMS_ttH_CSVHFStats1"   : 1,
            "CMS_ttH_CSVHFStats2"   : 1,
            "CMS_ttH_CSVLFStats1"   : 1,
            "CMS_ttH_CSVLFStats2"   : 1,
        }
    
        #deepcopy otherwise dicts will be linked
        self.total_shape_uncert = {
            "ttH_hbb" : copy.deepcopy(self.common_shape_uncertainties),
            "ttH_nohbb" : copy.deepcopy(self.common_shape_uncertainties),
            "ttbarPlus2B" : copy.deepcopy(self.common_shape_uncertainties),
            "ttbarPlusB" : copy.deepcopy(self.common_shape_uncertainties),
            "ttbarPlusBBbar" : copy.deepcopy(self.common_shape_uncertainties),
            "ttbarPlusCCbar" : copy.deepcopy(self.common_shape_uncertainties),
            "ttbarOther" : copy.deepcopy(self.common_shape_uncertainties),
        }

        self.common_scale_uncertainties = {
            "ttH_hbb" : {
                "lumi" : 1.045,
                "QCDscale_ttH" : 1.133,
                "pdf_gg" : 1.083,
            },
            "ttH_nohbb" : {
                "lumi" : 1.045
            },
            "ttbarPlus2B" : {
                "bgnorm_ttbarPlus2B" : 1.5,
                "QCDscale_ttbar" : 1.030,
                "pdf_gg" : 1.026,
                "lumi": 1.045
            },
            "ttbarPlusB" : {
                "bgnorm_ttbarPlusB" : 1.5,
                "QCDscale_ttbar" : 1.030,
                "pdf_gg" : 1.026,
                "lumi": 1.045
            },
            "ttbarPlusBBbar" : {
                "bgnorm_ttbarPlusBBbar" : 1.5,
                "QCDscale_ttbar" : 1.030,
                "pdf_gg" : 1.026,
                "lumi": 1.045
            },
            "ttbarPlusCCbar" : {
                "bgnorm_ttbarPlusCCbar" : 1.5,
                "QCDscale_ttbar" : 1.030,
                "pdf_gg" : 1.026,
                "lumi": 1.045
            },
            "ttbarOther" : {
                "lumi": 1.045,
                "QCDscale_ttbar" : 1.030,
                "pdf_gg" : 1.026,
            },
        }
        # value: normalization uncertainty
        self.scale_uncertainties = {
        }

        #These processes will be considered as signal in the limit setting
        self.signal_processes = [
            "ttH_hbb",
            "ttH_nohbb"
        ]


        self.output_datacardname = "shapes.txt"

        # nested dictionaries: category/sample/uncertainty/scale
        self.shape_uncertainties = {}

        #build from common shape uncertainties
        for cat in self.categories:
            self.shape_uncertainties[cat] = {}
            for proc in self.processes:
                self.shape_uncertainties[cat][proc] = copy.deepcopy(self.total_shape_uncert[proc])

            self.scale_uncertainties[cat] = {}
            for proc in self.processes:
                self.scale_uncertainties[cat][proc] = copy.deepcopy(self.common_scale_uncertainties[proc])
                
    def addStatVariations(self, category, nbins):
        #Add MC statistical uncertainties
        for proc in self.processes:
            if not self.shape_uncertainties.has_key(category):
                self.shape_uncertainties[category] = {}
            if not self.shape_uncertainties[category].has_key(proc):
                self.shape_uncertainties[category][proc] = {}
            for ibin in range(1, nbins + 1):
                self.shape_uncertainties[category][proc]["{0}_{1}_Bin{2}".format(proc, category, ibin)] = 1
