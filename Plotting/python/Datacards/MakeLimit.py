import ROOT
from TTH.Plotting.Datacards.makeDatacard import MakeDatacard2

class SlimLeaf:
    def __init__(self, **kwargs):
        self.discriminator_axis = kwargs.get("discriminator_axis")

def get_integral(fn, proc, cat):
    fi = ROOT.TFile(fn)
    dir = fi.Get("{0}/{1}".format(proc, cat))
    i = dir.Get("common_bdt").Integral()
    fi.Close()
    return i

class SlimCategorization:
    def __init__(self, **kwargs):
        self.event_counts = {}
        self.categories = kwargs.get("categories", [])
        self.processes = kwargs.get("processes", [])
        self.categories_files = kwargs.get("categories_files", {})

        for proc in self.processes:
            for cat in self.categories:
                try:
                    self.event_counts[proc][cat] = get_integral(
                        self.categories_files[cat], proc, cat
                    )
                except Exception as e:
                    print "Exception", e

    def getCategories(self, ignore_splittings):
        return ["sl_jge6_t3", "sl_jge6_tge4"]

    def getProcesses(self):
        return ["ttH_hbb", "ttbarOther"]

    def getLeafDiscriminators(self, ignore_splittings):
        return {
            "sl_jge6_tge4": "mem_SL_0w2h2t",
            "sl_jge6_t3": "mem_SL_0w2h2t"
        }
    
    def get_leaves(self, ignore_splittings):
        return [
            SlimLeaf(discriminator_axis="mem_SL_0w2h2t")
        ]

sc = SlimCategorization(
    processes=["ttH_hbb"],
    categories=["sl_jge6_tge4"],
    categories_files={
        "sl_jge6_tge4": "./out.root"
    }
)
sc.event_counts["ttH_hbb"] = {}
sc.event_counts["ttbarOther"] = {}
sc.event_counts["ttH_hbb"]["sl_jge6_tge4"] = 1
sc.event_counts["ttH_hbb"]["sl_jge6_t3"] = 2
sc.event_counts["ttbarOther"]["sl_jge6_tge4"] = 10
sc.event_counts["ttbarOther"]["sl_jge6_t3"] = 20

MakeDatacard2(
    sc,
    {
        "sl_jge6_tge4": "./out.root",
        "sl_jge6_t3": "./out.root"
    },
    "shapes.txt"
)
