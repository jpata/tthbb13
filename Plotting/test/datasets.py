import ROOT

data = {
    "sparse": [
        "root://t3se01.psi.ch///store/user/jpata/tth/histograms/March2016D/sparse_Mar29.root",
        "http://hep.kbfi.ee/~joosep/tth/histograms/March2016D/sparse_Mar29.root"
    ]
}

def open_data(fns):
    tf = None
    for fn in fns:
        tf = ROOT.TFile.Open(fn)
        if tf:
            if not tf.IsZombie():
                return tf
    raise Exception("Could not open any file")
