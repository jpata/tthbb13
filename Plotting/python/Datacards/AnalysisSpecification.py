class Sample:
    def __init__(self, **kwargs):
        self.input_name = kwargs.get("input_name")
        self.output_name = kwargs.get("output_name")
        self.shape_name = kwargs.get("shape_name", None)
        self.cuts = kwargs.get("cuts", [])

class Category:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.discriminator = kwargs.get("discriminator")
        self.src_histogram = kwargs.get("src_histogram")
        self.rebin = kwargs.get("rebin", 1)

        self.scale_uncertainties = kwargs.get("scale_uncertainties", {})

        self.cuts = kwargs.get("cuts", [])
        self.samples = kwargs.get("samples", [])
        self.signal_processes = kwargs.get("signal_processes", [])
        self.processes = list(set([s.output_name for s in self.samples]))

        #[process][syst]
        self.shape_uncertainties = {}
        self.scale_uncertainties = {}

        #[syst] -> scale factor, common for all processes
        self.common_shape_uncertainties = kwargs.get("common_shape_uncertainties", {})        
        self.common_scale_uncertainties = kwargs.get("common_scale_uncertainties", {})        
        for proc in self.processes:
            self.shape_uncertainties[proc] = {}
            self.scale_uncertainties[proc] = {}
            for systname, systval in self.common_shape_uncertainties.items():
                self.shape_uncertainties[proc][systname] = systval
            for systname, systval in self.common_scale_uncertainties.items():
                self.scale_uncertainties[proc][systname] = systval

        self.proc_shape_uncertainties = kwargs.get("shape_uncertainties", {})
        self.proc_scale_uncertainties = kwargs.get("scale_uncertainties", {})
        
        for k, v in self.proc_shape_uncertainties.items():
            self.shape_uncertainties[k].update(v)

        for k, v in self.proc_scale_uncertainties.items():
            self.scale_uncertainties[k].update(v)

class Analysis:
    def __init__(self, **kwargs):
        self.samples = kwargs.get("samples")
        self.categories = kwargs.get("categories")

        #groups represent calls to combine
        self.groups = kwargs.get("groups")
        self.do_fake_data = kwargs.get("do_fake_data", False)
        self.do_stat_variations = kwargs.get("do_stat_variations", False)
        self.output_directory = kwargs.get("output_directory", "./out")

        #add single-category groups
        for cat in self.categories:
            self.groups[cat.name] = [cat]

common_shape_uncertainties = {
    "CMS_scale_j"           : 1,
    "CMS_ttH_CSVLF"         : 1,
    "CMS_ttH_CSVHF"         : 1,
    "CMS_ttH_CSVcErr1"      : 1,
    "CMS_ttH_CSVcErr2"      : 1,
    "CMS_ttH_CSVHFStats1"   : 1,
    "CMS_ttH_CSVHFStats2"   : 1,
    "CMS_ttH_CSVLFStats1"   : 1,
    "CMS_ttH_CSVLFStats2"   : 1,
}

common_scale_uncertainties = {
    "lumi" : 1.045
}

scale_uncertainties = {
    "ttH_hbb" : {
        "QCDscale_ttH" : 1.133,
        "pdf_gg" : 1.083,
    },
    "ttH_nonhbb" : {
    },
    "ttbarPlus2B" : {
        "bgnorm_ttbarPlus2B" : 1.5,
        "QCDscale_ttbar" : 1.030,
        "pdf_gg" : 1.026,
    },
    "ttbarPlusB" : {
        "bgnorm_ttbarPlusB" : 1.5,
        "QCDscale_ttbar" : 1.030,
        "pdf_gg" : 1.026,
    },
    "ttbarPlusBBbar" : {
        "bgnorm_ttbarPlusBBbar" : 1.5,
        "QCDscale_ttbar" : 1.030,
        "pdf_gg" : 1.026,
    },
    "ttbarPlusCCbar" : {
        "bgnorm_ttbarPlusCCbar" : 1.5,
        "QCDscale_ttbar" : 1.030,
        "pdf_gg" : 1.026,
    },
    "ttbarOther" : {
        "QCDscale_ttbar" : 1.030,
        "pdf_gg" : 1.026,
    }
}


signal_processes = ["ttH_hbb", "ttH_nonhbb"]

base_samples = [
    Sample(
        input_name = "ttHTobb_M125_13TeV_powheg_pythia8/ttH_hbb",
        output_name = "ttH_hbb",
    ),
    Sample(
        input_name = "ttHToNonbb_M125_13TeV_powheg_pythia8/ttH_nonhbb",
        output_name = "ttH_nonhbb",
    ),
    Sample(
        input_name = "TT_TuneCUETP8M1_13TeV-powheg-pythia8/ttbarOther",
        output_name = "ttbarOther",
    ),
    Sample(
        input_name = "TT_TuneCUETP8M1_13TeV-powheg-pythia8/ttbarPlus2B",
        output_name = "ttbarPlus2B",
    ),
    Sample(
        input_name = "TT_TuneCUETP8M1_13TeV-powheg-pythia8/ttbarPlusB",
        output_name = "ttbarPlusB",
    ),
    Sample(
        input_name = "TT_TuneCUETP8M1_13TeV-powheg-pythia8/ttbarPlusBBbar",
        output_name = "ttbarPlusBBbar",
    ),
    Sample(
        input_name = "TT_TuneCUETP8M1_13TeV-powheg-pythia8/ttbarPlusCCbar",
        output_name = "ttbarPlusCCbar",
    ),
]

sl_categories = [
    Category(
        name = "sl_jge6_tge4",
        cuts = [("numJets", 6, 8), ("nBCSVM", 4, 8)],
        samples = base_samples,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_SL_0w2h2t",
        src_histogram = "sl/sparse"
    ),
    Category(
        name = "sl_jge6_t3",
        cuts = [("numJets", 6, 8), ("nBCSVM", 3, 4)],
        samples = base_samples,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_SL_0w2h2t",
        rebin=1,
        src_histogram = "sl/sparse"
    )
]

analysis = Analysis(
    samples = base_samples,
    categories = sl_categories,
    groups = {
        "sl": sl_categories,
    },
    do_fake_data = True,
    do_stat_variations = False
)
