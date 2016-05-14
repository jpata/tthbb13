import subprocess


basepath = "srm://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat//store/user/jpata/tth/VHBBHeppyV21_tthbbV9_May12/TT_TuneCUETP8M1_13TeV-powheg-pythia8/VHBBHeppyV21_tthbbV9_May12/160512_183419/"

def gfal_ls(path):
    proc = subprocess.Popen(["gfal-ls", "--color", "never", path], stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    return out.split()

def gfal_download(fn1, fn2):
    proc = subprocess.Popen(["gfal-copy", fn1, fn2], stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    return out.split()

dirs = gfal_ls(basepath)

bad_logs = []
good_logs = []
for d in dirs:
    fpath = "{0}/{1}/failed/log".format(basepath, d)
    try:
        logs = gfal_ls(fpath)
        logs = map(lambda x: fpath + "/" + x, logs)
        bad_logs += logs
    except Exception as e:
        print e
    
    fpath = "{0}/{1}/log".format(basepath, d)
    try:
        logs = gfal_ls(fpath)
        logs = map(lambda x: fpath + "/" + x, logs)
        good_logs += logs
    except Exception as e:
        print e

for log in bad_logs[:100]:
    fn1 = log
    fn2 = "file:///scratch/joosep/badlogs/" + log.split("/")[-1]
    print fn1, fn2
    gfal_download(fn1, fn2)

for log in good_logs[:100]:
    fn1 = log
    fn2 = "file:///scratch/joosep/goodlogs/" + log.split("/")[-1]
    print fn1, fn2
    gfal_download(fn1, fn2)
