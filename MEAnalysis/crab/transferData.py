import glob, sys, os

import glob
repl1 = "/store/user/arizzi/VHBBHeppyV20/"
#repl2 = "/store/group/phys_higgs/hbb/ntuples/VHBBHeppyV20/"
repl2 = "/store/user/jpata/VHBBHeppyV20/"
#src_pref = "srm://ganymede.hep.kbfi.ee:8888/hdfs/cms"
src_pref = "srm://stormfe1.pi.infn.it:8444/cms"
#dst_pref = "srm://srm-eoscms.cern.ch:8443/eos/cms"
dst_pref = "srm://ganymede.hep.kbfi.ee:8888/hdfs/cms"
das = "/home/joosep/util/das_cli.py"

dsname_repl = [
    (repl1, repl2),
#    ("ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1", "ST_tW_tbar"),
#    ("ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1", "ST_tW_t"),
#    ("ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1", "ST_s"),
#    ("ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1", "ST_tbar"),
#    ("ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1", "ST_t"),
#    ("TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8", "ttw_wlnu"),
#    ("TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8", "ttw_wqq"),
#    ("TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8", "ttz_zllnunu"),
#    ("TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8", "ttz_zqq"),
#    ("RunIISpring15MiniAODv2-74X_mcRun2", "maodv2")
]

def cleanList(l):
    l = [w.strip() for w in l]
    l = filter(lambda x: len(x)>0, l)
    return l

def getFiles(dataset):
    files = os.popen('python {0} --query=\"file dataset={1} instance=prod/phys03\" --limit=0'.format(das, dataset)).read().split("\n")
    return sorted(cleanList(files))

if __name__ == "__main__":
    outfile = open("copyjob", "w")
    datasets = open("datasets").readlines()
    datasets = cleanList(datasets)

    for dataset in datasets:
        files = getFiles(dataset)
        dsname = dataset.split("/")[1]
        outfile_ds = open("{0}.dat".format(dsname), "w")
        outfile_ds.write("[{0}]\n".format(dsname))
        for fi in files:
            dstfi = fi
            for repls in dsname_repl:
                dstfi = dstfi.replace(repls[0], repls[1])
            outfile.write("{0} {1}\n".format(src_pref + fi, dst_pref + dstfi))
            outfile_ds.write(dstfi + "\n")
        outfile_ds.close()
    outfile.close()
