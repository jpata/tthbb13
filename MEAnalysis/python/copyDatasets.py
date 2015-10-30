import sys,os,shutil,ROOT

# TO BE CUSTOMIZED
indir = 'gsiftp://stormgf2.pi.infn.it/gpfs/ddn/srm/cms/store/user/arizzi/VHBBHeppyV15/'
outdir = 'gsiftp://t3se01.psi.ch/pnfs/psi.ch/cms/trivcat/store/t3groups/ethz-higgs/run2/VHBBHeppyV15/'
localfiledir = outdir.replace("gsiftp://t3se01.psi.ch", "")
das = "/shome/jpata/util/das_cli.py"

def replacerule(x):
    return x.replace("/store/user/arizzi", "/store/t3groups/ethz-higgs/run2")

datasets = open("datasets").readlines()
datasets = datasets

def cleanList(l):
    l = [w.strip() for w in l]
    l = filter(lambda x: len(x)>0, l)
    return l

datasets = cleanList(datasets)

def getFiles(dataset):
    files = os.popen('python {0} --query=\"file dataset={1} instance=prod/phys03\" --limit=0'.format(das, dataset)).read().split("\n")
    return sorted(cleanList(files))

def getCopyDump(inpath, outpath):
    os.popen(
        "globus-url-copy -dump-only ./to_be_copied.txt -continue-on-error -rst -nodcau -fast -vb -v -cd -r {0} {1}".format(inpath, outpath)
    )
    l = open("to_be_copied.txt").readlines()
    l = filter(lambda x: "root" in x, l)
    return sorted(cleanList(l))

def getExistingFiles(path):
    l = os.popen(
        "find {0} -name '*.root'".format(path)
    ).readlines()
    return sorted(cleanList(l))

#get list of files from DAS
allfiles = []
for dataset in datasets:
    files = getFiles(dataset)
    allfiles += files
of = open("files_das", "w")
allfiles = sorted(allfiles)
of.write("\n".join(allfiles))
of.close()

#get files from dump
srcFiles = getCopyDump(indir, outdir)
of = open("files_src", "w")
of.write("\n".join(srcFiles))
of.close()

existingFiles = getExistingFiles(localfiledir)
of = open("files_dst", "w")
of.write("\n".join(existingFiles))
of.close()

copy_f = open("tocopy", "w")
missing_f = open("files_src_missing", "w")
removed = []
for inf in allfiles:
    exists = False
    toremove = ""
    for ex in existingFiles:

        #DAS file exists on target
        if replacerule(inf) in ex:
            exists = True
            toremove = ex
            break
    if exists:
        existingFiles.remove(toremove)
    else:
        atsource = False
        for src in srcFiles:
            if inf in src:
                spl = src.split()
                copy_f.write('echo globus-url-copy -sync -sync-level 3 -continue-on-error -rst -nodcau -fast -vb -v -cd -r {0} {1} | qsub -cwd -q long.q ; sleep 1\n'.format(
                        spl[0][1:-1], spl[1][1:-1] 
                ))
                atsource = True
                break
        if not atsource:
            missing_f.write(inf + "\n")

of = open("files_dst_todel", "w")
of.write("\n".join(existingFiles))
of.close()

copy_f.close()
missing_f.close()
