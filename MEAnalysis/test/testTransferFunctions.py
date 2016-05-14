import TTH.MEAnalysis.TFClasses as TFClasses
from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf
import pickle
import ROOT, sys
sys.modules["TFClasses"] = TFClasses
ROOT.gROOT.SetBatch(False)

outfile = ROOT.TFile("transfer.root", "RECREATE")

pickle_fn    = sys.argv[1] # Resolved
pickle_fn_sj = sys.argv[2] # Subjets
 
for prefix, fn in zip(["",        "sj"],
                      [pickle_fn, pickle_fn_sj]):


    #Load transfer functions from pickle file
    pi_file = open(fn , 'rb')
    tf_matrix = pickle.load(pi_file)


    #configures if gen or reco is the TF x argument
    #     If True, TF [0] - reco, x - gen
    #     If False, TF [0] - gen, x - reco
    eval_gen = False

    for fl in ["b", "l"]:
        for etabin in [0,1]:
            f = tf_matrix[fl][etabin].Make_Formula(eval_gen)
            #f.SetNpx(10000)
            #f.SetRange(0, 500)
            f.SetName("tf_{0}{1}_etabin{2}".format(prefix, fl, etabin))
            #f.SetParameter(0, 100)
            outfile.Add(f)

            #make cumulative transfer function (reco efficiency)
            f2 = tf_matrix[fl][etabin].Make_CDF()
            #f2.SetNpx(10000)
            #f2.SetRange(0, 500)
            f2.SetName("tf_{0}{1}eff_etabin{2}".format(prefix, fl, etabin))
            #Jet pt cut
            #f2.SetParameter(0, 20)
            outfile.Add(f2)

outfile.Write()
outfile.Close()
