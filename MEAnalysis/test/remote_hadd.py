import ROOT, os
import subprocess as sub

server = "storage01.lcg.cscs.ch"

def xrootd_listdir(server, directory):
    p = sub.Popen(['xrdfs', server, 'ls', '-l', directory], stdout=sub.PIPE, stderr=sub.PIPE)
    output, errors = p.communicate()
    outputs = output.strip().split("\n")
    dirs = []
    files = []
    for o in outputs:
        spl = o.strip().split()
        mode = spl[0]
        is_dir = mode.startswith("d")
        if is_dir:
            dirs += [spl[4]]
        else:
            files += [spl[4]]
    return (dirs, files)

def xrootd_walk(server, directory):
    dirs, files = xrootd_listdir(server, directory)
    total_files = []
    for d in dirs:
        total_files += xrootd_walk(server, d)
    total_files += files 
    return total_files

def xrootd_hadd(server, directory, match, outfile):
    files = xrootd_walk(server, directory)
    good_files = filter(match, files)

    files_with_path = ["root://" + server + "//" + fi for fi in good_files]
    complete_files = [] 
    for fi in files_with_path:
        tf = ROOT.TFile.Open(fi)
        if not tf or tf.IsZombie():
            continue
        complete_files += [fi]
        tf.Close()

    print "merging {0} files".format(len(complete_files))

    merger = ROOT.TFileMerger(False, False)
    merger.OutputFile(outfile) 
    for fi in complete_files:
        merger.AddFile(fi)
    ret = merger.Merge(False)
    if not ret:
        raise Exception("Could not merge file")
    print "Merged output in {0}, {1:.2f} MB".format(outfile, os.path.getsize(outfile)/1024.0/1024.0)
    return outfile

if __name__ == "__main__":

    #configurations go here
    filters = {
        "default": lambda x: ".root" in x and not "failed" in x
    }

    import argparse
    parser = argparse.ArgumentParser(description='Mergers files on a remote SE via XRootD')
    parser.add_argument('--server', action="store", help="XRootD server", default="storage01.lcg.cscs.ch")
    parser.add_argument('--filter', action="store", help="Good file filter function", default="default", choices=sorted(filters.keys()))
    parser.add_argument('--path', action="store", help="Remote path on server")
    parser.add_argument('--outfile', action="store", help="Output file", required=True)
    args = parser.parse_args()
    xrootd_hadd(args.server, args.path, filters[args.filter], args.outfile)
