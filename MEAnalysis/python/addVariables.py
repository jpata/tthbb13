import ROOT
import numpy as np

from TTH.CommonClassifier.db import ClassifierDB

def main(infile, outfile, cls_db_path):
    tf1 = ROOT.TFile(infile)
    tt1 = tf1.Get("tree")
    tf2 = ROOT.TFile(outfile, "RECREATE")
    tt2 = ROOT.TTree("cc_tree", "CommonClassifier tree")
    
    cls_db = ClassifierDB(filename=cls_db_path)

    branches = {
        "common_mem": np.zeros(1, dtype=np.float64),
        "common_mem_sig": np.zeros(1, dtype=np.float64),
        "common_mem_bkg": np.zeros(1, dtype=np.float64),
        "common_bdt": np.zeros(1, dtype=np.float64)
    }
    
    for br in branches.keys():
        tt2.Branch(br, branches[br], "{0}/D".format(br))

    tt1.SetBranchStatus("*", False)
    for br in ["run", "lumi", "evt"]:
        tt1.SetBranchStatus(br, True)



    for iEv, ev in enumerate(tt1):
        run = ev.run
        lumi = ev.lumi
        event = ev.evt

        branches["common_mem"][0] = 0
        branches["common_mem_sig"][0] = 0
        branches["common_mem_bkg"][0] = 0
        branches["common_bdt"][0] = 0

        key = (run, lumi, event, 0)
        if cls_db.data.has_key(key):
            classifiers = cls_db.get(key)
            if classifiers.mem_p_sig > 0:
                branches["common_mem_sig"][0] = classifiers.mem_p_sig
                branches["common_mem_bkg"][0] = classifiers.mem_p_bkg
                branches["common_mem"][0] = classifiers.mem_p_sig / (classifiers.mem_p_sig + 0.2*classifiers.mem_p_bkg)
            branches["common_bdt"][0] = classifiers.bdt

        tt2.Fill()
    tf2.Write()
    tf2.Close()


if __name__ == "__main__":
        
    import argparse
    parser = argparse.ArgumentParser(
        description='Creates friend trees with classifier data and other variables'
    )
    parser.add_argument(
        '--config',
        action="store",
        help="Analysis configuration",
        type=str,
        required = True
    )
    
    from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
    args = parser.parse_args()
    an_name, analysis = analysisFromConfig(args.config)
    
    for sample in analysis.samples:
        outfile = sample.skim_file.replace(".root", "_variables.root")
        main(sample.skim_file, outfile, sample.classifier_db_path)

