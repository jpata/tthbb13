import TTH.Plotting.Samples as Samples
import ROOT, json

#these samples will be enabled
sampstorun = [
    "ttHTobb_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
    "ttHToNonbb_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
    # #"TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9", #inclusive
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_tt2b",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttbb",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttb",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttcc",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttll",
#    "TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
#    "TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
#    "TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
#    "TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
]
#entries per job
perjob = 500000

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

ijob = 0
for samp in sampstorun:
    s = Samples.samples_dict[samp]
    tf = ROOT.TChain("tree")
    for fn in s.fileNamesS2:
        tf.AddFile(fn)
    nEntries = tf.GetEntries()
    for ch in chunks(range(nEntries), perjob):

        #default configuration
        ret = {
            "filenames": s.fileNamesS2,
            "lumi": 10000.0,
            "process": s.name,
            "outputFile": "ControlPlots_{0}.root".format(ijob),
            "firstEntry": ch[0],
            "numEntries": len(ch),
            "printEvery": 0,
            "sparseAxes": [
                {
                    "func": "numJets",
                    "xMin": 3,
                    "xMax": 6,
                    "nBins": 3
                },
                {
                    "func": "nBCSVM",
                    "xMin": 2,
                    "xMax": 4,
                    "nBins": 2
                },
                {
                    "func": "nBoosted",
                    "xMin": 0,
                    "xMax": 2,
                    "nBins": 2
                },
                {
                    "func": "btag_LR_4b_2b_logit",
                    "xMin": -20,
                    "xMax": 20,
                    "nBins": 80
                },
                {
                    "func": "mem_SL_0w2h2t",
                    "xMin": 0,
                    "xMax": 1,
                    "nBins": 6
                }
            ]
        }
        of = open("job_{0}.json".format(ijob), "w")
        of.write(json.dumps(ret, indent=2))
        of.close()
        ijob += 1
