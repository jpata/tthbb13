
import glob

infiles = glob.glob("../gc/datasets/V16_newjec/*.dat")

#repl1 = "/store/user/jpata/VHBBHeppyV16pre/"
#repl2 = "/store/group/phys_higgs/hbb/ntuples/V16_tth_moriond/"
#src_pref = "srm://ganymede.hep.kbfi.ee:8888/hdfs/cms"
#dst_pref = "srm://srm-eoscms.cern.ch:8443/eos/cms"

repl1 = "/store/user/jpata/VHBBHeppyV16pre/"
repl2 = repl1
src_pref = "srm://ganymede.hep.kbfi.ee:8888/hdfs/cms"
dst_pref = "srm://t3se01.psi.ch:8443/pnfs/psi.ch/cms/trivcat/"

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

for inf in infiles:
    datasets = parseDataFile(inf)
    for dataset in datasets.keys():
        for fi, nfi in datasets[dataset]:
            print src_pref+fi, dst_pref+fi.replace(repl1, repl2)
