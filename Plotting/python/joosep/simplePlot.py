import sys
sys.path.append("../Datacards/")
from MakeCategory import apply_rules
from sparse import save_hdict
import rootpy
import rootpy.io
import matplotlib.pyplot as plt
import plotlib

var = "[('mem_SL_2w2h2t', 1)]"
cut = "[('numJets', 6, 8), ('nBCSVM', 4, 8)]"
lumi = 10.0

rules = [
  {
    "project": var, 
    "input": "ttHTobb_M125_13TeV_powheg_pythia8/ttH_hbb/sl/sparse", 
    "output": "ttH_hbb/sl_jge6_tge4/jet0_pt", 
    "cuts": cut,
    "xs_weight": lumi* 1.0
  },
  {
    "project": var, 
    "input": "TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ttbarOther/sl/sparse", 
    "output": "ttbarOther/sl_jge6_tge4/jet0_pt", 
    "cuts": cut,
    "xs_weight": lumi*0.5
  },
  {
    "project": var, 
    "input": "TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ttbarOther/sl/sparse", 
    "output": "ttbarOther/sl_jge6_tge4/jet0_pt", 
    "cuts": cut,
    "xs_weight": lumi*0.5
  },
  {
    "project": var, 
    "input": "TTTo2L2Nu_13TeV-powheg/ttbarOther/sl/sparse", 
    "output": "ttbarOther/sl_jge6_tge4/jet0_pt", 
    "cuts": cut,
    "xs_weight": lumi*1.0
  },


  {
    "project": var, 
    "input": "TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ttbarPlusBBbar/sl/sparse", 
    "output": "ttbarPlusBBbar/sl_jge6_tge4/jet0_pt", 
    "cuts": cut,
    "xs_weight": lumi*0.5
  },
  {
    "project": var, 
    "input": "TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ttbarPlusBBbar/sl/sparse", 
    "output": "ttbarPlusBBbar/sl_jge6_tge4/jet0_pt", 
    "cuts": cut,
    "xs_weight": lumi*0.5
  },
  {
    "project": var, 
    "input": "TTTo2L2Nu_13TeV-powheg/ttbarPlusBBbar/sl/sparse", 
    "output": "ttbarPlusBBbar/sl_jge6_tge4/jet0_pt", 
    "cuts": cut,
    "xs_weight": lumi*1.0
  },

  {
    "project": var, 
    "input": "TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ttbarPlus2B/sl/sparse", 
    "output": "ttbarPlus2B/sl_jge6_tge4/jet0_pt", 
    "cuts": cut,
    "xs_weight": lumi*0.5
  },
  {
    "project": var, 
    "input": "TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ttbarPlus2B/sl/sparse", 
    "output": "ttbarPlus2B/sl_jge6_tge4/jet0_pt", 
    "cuts": cut,
    "xs_weight": lumi*0.5
  },
  {
    "project": var, 
    "input": "TTTo2L2Nu_13TeV-powheg/ttbarPlus2B/sl/sparse", 
    "output": "ttbarPlus2B/sl_jge6_tge4/jet0_pt", 
    "cuts": cut,
    "xs_weight": lumi*1.0
  },

  {
    "project": var, 
    "input": "TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ttbarPlusB/sl/sparse", 
    "output": "ttbarPlusB/sl_jge6_tge4/jet0_pt", 
    "cuts": cut,
    "xs_weight": lumi*0.5
  },
  {
    "project": var, 
    "input": "TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ttbarPlusB/sl/sparse", 
    "output": "ttbarPlusB/sl_jge6_tge4/jet0_pt", 
    "cuts": cut,
    "xs_weight": lumi*0.5
  },
  {
    "project": var, 
    "input": "TTTo2L2Nu_13TeV-powheg/ttbarPlusB/sl/sparse", 
    "output": "ttbarPlusB/sl_jge6_tge4/jet0_pt", 
    "cuts": cut,
    "xs_weight": lumi*1.0
  },

  {
    "project": var, 
    "input": "TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ttbarPlusCCbar/sl/sparse", 
    "output": "ttbarPlusCCbar/sl_jge6_tge4/jet0_pt", 
    "cuts": cut,
    "xs_weight": lumi*0.5
  },
  {
    "project": var, 
    "input": "TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ttbarPlusCCbar/sl/sparse", 
    "output": "ttbarPlusCCbar/sl_jge6_tge4/jet0_pt", 
    "cuts": cut,
    "xs_weight": lumi*0.5
  },
  {
    "project": var, 
    "input": "TTTo2L2Nu_13TeV-powheg/ttbarPlusCCbar/sl/sparse", 
    "output": "ttbarPlusCCbar/sl_jge6_tge4/jet0_pt", 
    "cuts": cut,
    "xs_weight": lumi*1.0
  }

]

ret = apply_rules(("/Users/joosep/Documents/tth/data/histograms/ControlPlots.root", rules))
print ret
for (k, v) in ret.items():
    print k, v.Integral()
save_hdict("out.root", ret)


inf = rootpy.io.File("out.root")
procs = ["ttH_hbb", "ttbarPlusBBbar", "ttbarPlus2B", "ttbarPlusB", "ttbarPlusCCbar", "ttbarOther"]

fig = plt.figure(figsize=(6,6))
r = plotlib.draw_data_mc(
    inf,
    "sl_jge6_tge4/jet0_pt",
    [(p, p.replace("_", "")) for p in procs],
    dataname=[],
    xlabel="Jet pt",
    xunit="",
    legend_fontsize=10, legend_loc="best",
    rebin=6,
    colors=[plotlib.colors.get(p) for p in procs],
    do_legend=True,
    show_overflow=True,
    title_extended=r"$,\ \mathcal{{L}}=2.6,\ \mathrm{{fb}}^{-1}$",
    systematics=[],
    #blindFunc=blind,
    #do_pseudodata=True
)
plt.savefig("out.pdf")
