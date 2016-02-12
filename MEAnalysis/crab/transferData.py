
import glob
repl1 = "/store/user/jpata/VHBBHeppyV16pre/"
repl2 = "/store/group/phys_higgs/hbb/ntuples/V16_tth_moriond/"
src_pref = "srm://ganymede.hep.kbfi.ee:8888/hdfs/cms"
dst_pref = "srm://srm-eoscms.cern.ch:8443/eos/cms"

#repl1 = "/store/user/jpata/VHBBHeppyV16pre/"
#repl2 = repl1
#src_pref = "srm://ganymede.hep.kbfi.ee:8888/hdfs/cms"
#dst_pref = "srm://t3se01.psi.ch:8443/pnfs/psi.ch/cms/trivcat/"

dsname_repl = [
    (repl1, repl2),
    ("ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1", "ST_tW_tbar"),
    ("ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1", "ST_tW_t"),
    ("ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1", "ST_s"),
    ("ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1", "ST_tbar"),
    ("ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1", "ST_t"),
    ("TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8", "ttw_wlnu"),
    ("TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8", "ttw_wqq"),
    ("TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8", "ttz_zllnunu"),
    ("TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8", "ttz_zqq"),
    ("RunIISpring15MiniAODv2-74X_mcRun2", "maodv2")
]

def parseDataFile(infile):
    curname = None
    datasets = {}
    for line in open(infile).readlines():
        line = line.strip()
        if line.startswith("#"):
            continue
        if line.startswith("["):
            if curname:
                datasets[curname] = datafiles
            datafiles = []
            curname = line[1:-1]
        elif "root" in line:
            l0, l1 = line.split("=") 
            datafiles += [(l0.strip(), int(l1.strip()))]
    #add last dataset
    datasets[curname] = datafiles
    
    return datasets

if __name__ == "__main__":
    infiles = glob.glob("../gc/datasets/V16_newjec/*.dat")
    for inf in infiles:
        datasets = parseDataFile(inf)
        for dataset in datasets.keys():
            for fi, nfi in datasets[dataset]:
                dstfi = fi
                for repls in dsname_repl:
                    dstfi = dstfi.replace(repls[0], repls[1])
                print src_pref+fi, dst_pref + dstfi
