class Datacard:
    def __init__(self):
        #these exist in the input file
        self.basecategories = dict([
        ])

        #merge commands to make limit categories
        self.combines = {
        }

        #Perform combined fit across these categories
        self.categories = {
        }

        #derived for 50% tt+H efficiency
        #variable is logit(bLR) = log(bLR/(1-bLR))
        self.blr_cuts = {
         'dl_j3_t2': 0.2,
         'dl_jge3_tge3': 4.4,
         'dl_jge4_t2': 0.5,
         'dl_jge4_tge4': 8.9,
         'sl_j4_t3': 4.1,
         'sl_j4_t4': 9.8,
         'sl_j5_t3': 4.4,
         'sl_j5_tge4': 8.9,
         'sl_jge6_t2': 0.8,
         'sl_jge6_t3': 4.4,
         'sl_jge6_tge4': 8.3
        }

        #Draw histograms with these systematic weights
        #The list consists of all systematic weight scenarios that will be evaluated
        #(NAME, WEIGHT) -> will create hist_NAME with weight str (WEIGHT * (cut))
        self.weights = [
                #Nominal weights
                ("",                    "bTagWeight"),

                #no weights applied
                #("unweighted",          "1.0"),
                
                #only b weight applied
                #("bw",                  "bTagWeight"),
                
                
                            
                #JES, needs variated per-event bTagWeight as well
                ("CMS_scale_jUp",       "bTagWeight_JESUp"),
                ("CMS_scale_jDown",     "bTagWeight_JESDown"),
                
                #CSV variations
                ("CMS_ttH_CSVLFUp",         "bTagWeight_LFUp"),
                ("CMS_ttH_CSVLFDown",       "bTagWeight_LFDown"),
                ("CMS_ttH_CSVHFUp",         "bTagWeight_HFUp"),
                ("CMS_ttH_CSVHFDown",       "bTagWeight_HFDown"),
                ("CMS_ttH_CSVStats1Up",     "bTagWeight_Stats1Up"),
                ("CMS_ttH_CSVStats1Down",   "bTagWeight_Stats1Down"),
                ("CMS_ttH_CSVStats2Up",     "bTagWeight_Stats2Up"),
                ("CMS_ttH_CSVStats2Down",   "bTagWeight_Stats2Down"),
        ]

        # Subset of the reweighted distributions we want to use as syst. shape uncertainties    
        # To avoid copy paste
        self.common_shape_uncertainties = {
            "CMS_scale_j"       : 1,
            "CMS_ttH_CSVLF"       : 1,
            "CMS_ttH_CSVHF"       : 1,
            "CMS_ttH_CSVStats1"   : 1,
            "CMS_ttH_CSVStats2"   : 1,
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

        # nested dictionaries: category/sample/uncertainty/scale
        self.shape_uncertainties = {
        }


        self.common_scale_uncertainties = {
            "ttH_hbb" : {
                "lumi" : 1.05
            },
            "ttH_nohbb" : {
                "lumi" : 1.05
            },
            "ttbarPlus2B" : {
                "bgnorm_ttbarPlus2B" : 1.5,
                "lumi": 1.05
            },
            "ttbarPlusB" : {
                "bgnorm_ttbarPlusB" : 1.3,
                "lumi": 1.05
            },
            "ttbarPlusBBbar" : {
                "bgnorm_ttbarPlusBBbar" : 1.3,
                "lumi": 1.05
            },
            "ttbarPlusCCbar" : {
                "bgnorm_ttbarPlusCCbar" : 1.3,
                "lumi": 1.05
            },
            "ttbarOther" : {
                "bgnorm_ttbarOther" : 1.3,
                "lumi": 1.05
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

        self.processes = [
            "ttH_hbb",
            "ttH_nohbb",
            "ttbarPlus2B",
            "ttbarPlusB",
            "ttbarPlusBBbar",
            "ttbarPlusCCbar",
            "ttbarOther",
        ]

        self.histfilename = "ControlPlots.root"
        voutput_datacardname = "shapes.txt"

        voutput_basepath = "./"

        # luminosity we're interested in (measure in pb-1)
        self.lumi = 10000. # 10fb-1

    def addStatVariations(self):
        #Add MC statistical uncertainties
        for cat in self.categories.keys():
            #self.shape_uncertainties.update({cat: {}})
            for proc in self.processes:
                if not self.shape_uncertainties.has_key(cat):
                    self.shape_uncertainties[cat] = {}
                if not self.shape_uncertainties[cat].has_key(proc):
                    self.shape_uncertainties[cat][proc] = {}
                for ibin in range(1,7):
                    self.shape_uncertainties[cat][proc]["{0}_{1}_Bin{2}".format(proc, cat, ibin)] = 1
        #print self.shape_uncertainties
import copy

def makeCardBtagLR(name, basecats):
    card = Datacard()

    suffix = ""
    if "_sj" in name:
        suffix += "_sj"

    for basecat, var in basecats.items():
        card.basecategories[basecat + "_boosted_blrH"] = var + suffix
        card.basecategories[basecat + "_nonboosted_blrH"] = var
        card.basecategories[basecat + "_boosted_blrL"] = var + suffix
        card.basecategories[basecat + "_nonboosted_blrL"] = var
        card.categories[basecat + "_blrH"] = var
        card.categories[basecat + "_blrL"] = var
        card.combines[basecat + "_blrH"] = [basecat + "_boosted_blrH", basecat + "_nonboosted_blrH"]
        card.combines[basecat + "_blrL"] = [basecat + "_boosted_blrL", basecat + "_nonboosted_blrL"]
        card.shape_uncertainties[basecat + "_blrH"] = copy.deepcopy(card.total_shape_uncert)
        card.shape_uncertainties[basecat + "_blrL"] = copy.deepcopy(card.total_shape_uncert)
        card.scale_uncertainties[basecat + "_blrH"] = copy.deepcopy(card.common_scale_uncertainties)
        card.scale_uncertainties[basecat + "_blrL"] = copy.deepcopy(card.common_scale_uncertainties)
    card.output_datacardname = "shapes_Cblr_{0}.txt".format(name)
    return card

def makeCardBoosted(name, basecats):
    card = Datacard()
    
    suffix = ""
    if "_sj" in name:
        suffix += "_sj"

    for basecat, var in basecats.items():
        card.basecategories[basecat + "_boosted"] = var + suffix
        card.basecategories[basecat + "_nonboosted"] = var
        card.categories[basecat + "_boosted"] = var + suffix
        card.categories[basecat + "_nonboosted"] = var
        card.shape_uncertainties[basecat + "_boosted"] = copy.deepcopy(card.total_shape_uncert)
        card.shape_uncertainties[basecat + "_nonboosted"] = copy.deepcopy(card.total_shape_uncert)
        card.scale_uncertainties[basecat + "_boosted"] = copy.deepcopy(card.common_scale_uncertainties)
        card.scale_uncertainties[basecat + "_nonboosted"] = copy.deepcopy(card.common_scale_uncertainties)
    card.output_datacardname = "shapes_Cboost_{0}.txt".format(name)
    return card

def makeCardBoostedXblr(name, basecats):
    card = Datacard()

    suffix = ""
    if "_sj" in name:
        suffix += "_sj"
    for basecat, var in basecats.items():
        for blr in ["_blrL", "_blrH"]:
            card.basecategories[basecat + "_boosted" + blr] = var + suffix
            card.basecategories[basecat + "_nonboosted" + blr] = var
            card.categories[basecat + "_boosted" + blr] = var + suffix
            card.categories[basecat + "_nonboosted" + blr] = var
            card.shape_uncertainties[basecat + "_boosted" + blr] = copy.deepcopy(card.total_shape_uncert)
            card.shape_uncertainties[basecat + "_nonboosted" + blr] = copy.deepcopy(card.total_shape_uncert)
            card.scale_uncertainties[basecat + "_boosted" + blr] = copy.deepcopy(card.common_scale_uncertainties)
            card.scale_uncertainties[basecat + "_nonboosted" + blr] = copy.deepcopy(card.common_scale_uncertainties)
    card.output_datacardname = "shapes_Cboost_Cblr_{0}.txt".format(name)
    return card

def makeCard(name, basecats):
    card = Datacard()

    suffix = ""
    if "_sj" in name:
        suffix += "_sj"

    for basecat, var in basecats.items():
        card.basecategories[basecat] = var + suffix
        card.categories[basecat] = var + suffix
        card.shape_uncertainties[basecat] = copy.deepcopy(card.total_shape_uncert)
        card.scale_uncertainties[basecat] = copy.deepcopy(card.common_scale_uncertainties)

    card.output_datacardname = "shapes_{0}.txt".format(name)
    return card

def makeCardWMass(name, basecats):
    card = Datacard()

    suffix = ""
    if "_sj" in name:
        suffix += "_sj"
    for basecat, var in basecats.items():
        for c in ["_Wmass60_100", "_nonWmass60_100"]:
            card.basecategories[basecat + c] = var + suffix
            card.shape_uncertainties[basecat + c] = copy.deepcopy(card.total_shape_uncert)
            card.scale_uncertainties[basecat + c] = copy.deepcopy(card.common_scale_uncertainties)
    card.categories = copy.deepcopy(card.basecategories)
    card.output_datacardname = "shapes_CWmass_{0}.txt".format(name)
    return card
