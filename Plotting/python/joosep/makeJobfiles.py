import samples, ROOT, json

sampstorun = [
    "ttHTobb_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
    "ttHToNonbb_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
    # #"TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9", #inclusive
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_tt2b",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttbb",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttb",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttcc",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttll",
    "TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
    "TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
    "TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
    "TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
]

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

ijob = 0
for samp in sampstorun:
    s = samples.samples_dict[samp]
    tf = ROOT.TChain("tree")
    for fn in s.fileNamesS2:
        tf.AddFile(fn)
    nEntries = tf.GetEntries()
    for ch in chunks(range(nEntries), 500000):
        ret = {
            "filenames": s.fileNamesS2,
            "lumi": 10000.0,
            "process": s.name,
            "outputFile": "ControlPlots_{0}.root".format(ijob),
            "firstEntry": ch[0],
            "numEntries": len(ch),
            "printEvery": 0,
            "btagLRCuts": {
                "dl:j3_t2": 0.2,
                "dl:jge3_tge3": 4.4,
                "dl:jge4_t2": 0.5,
                "dl:jge4_tge4": 8.9,
                "sl:j4_t3": 4.1,
                "sl:j4_t4": 9.8,
                "sl:j5_t3": 4.4,
                "sl:j5_tge4": 8.9,
                "sl:jge6_t2": 0.8,
                "sl:jge6_t3": 4.4,
                "sl:jge6_tge4": 8.3
            }
        }
        of = open("job_{0}.json".format(ijob), "w")
        of.write(json.dumps(ret, indent=2))
        of.close()
        ijob += 1
