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

        self.shape_uncertainties = kwargs.get("shape_uncertainties", {})
        self.scale_uncertainties = kwargs.get("scale_uncertainties", {})
        self.cuts = kwargs.get("cuts", [])
        self.samples = kwargs.get("samples", [])
        self.processes = list(set([s.output_name for s in self.samples]))

class Analysis:
    def __init__(self, **kwargs):
        self.samples = kwargs.get("samples")
        self.categories = kwargs.get("categories")
        self.groups = kwargs.get("groups")
        self.do_fake_data = kwargs.get("do_fake_data", False)
        self.do_stat_variations = kwargs.get("do_stat_variations", False)
        self.output_directory = kwargs.get("output_directory", "./out")

shape_uncertainties = {
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

scale_uncertainties = {
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
    }
}

base_samples = [
    Sample(
        input_name = "ttHTobb_M125_13TeV_powheg_pythia8/ttH_hbb",
        output_name = "ttH_hbb",
    ),
    Sample(
        input_name = "ttHToNonbb_M125_13TeV_powheg_pythia8/ttH_nonhbb",
        output_name = "ttH_nonhbb",
    ),
]

sl_categories = [
    Category(
        name = "sl_jge6_tge4",
        cuts = [("numJets", 6, 8), ("nBCSVM", 4, 8)],
        samples = base_samples,
        shape_uncertainties = shape_uncertainties,
        discriminator = "mem_SL_0w2h2t",
        src_histogram = "sl/sparse"
    ),
    Category(
        name = "sl_jge6_t3",
        cuts = [("numJets", 6, 8), ("nBCSVM", 3, 4)],
        samples = base_samples,
        shape_uncertainties = shape_uncertainties,
        discriminator = "Wmass",
        rebin=1,
        src_histogram = "sl/sparse"
    )
]

analysis = Analysis(
    samples = base_samples,
    categories = sl_categories,
    groups = {
        "sl": [c.name for c in sl_categories],
    },
    do_fake_data = True,
    do_stat_variations = True
)
