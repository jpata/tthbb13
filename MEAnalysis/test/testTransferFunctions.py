import TTH.MEAnalysis.TFClasses as TFClasses
from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf
import pickle
import ROOT, sys
sys.modules["TFClasses"] = TFClasses
ROOT.gROOT.SetBatch(False)

pickle_fn = sys.argv[1]
 
#Load transfer functions from pickle file
pi_file = open(pickle_fn , 'rb')
tf_matrix = pickle.load(pi_file)

outfile = ROOT.TFile("transfer.root", "RECREATE")

#configures if gen or reco is the TF x argument
eval_gen = False

for fl in ["b", "l"]:
    for etabin in [0,1]:
        f = tf_matrix[fl][etabin].Make_Formula(eval_gen)
        f.SetNpx(10000)
        f.SetRange(0, 500)
        f.SetName("tf_{0}_etabin{1}".format(fl, etabin))
        f.SetParameter(0, 100)
        outfile.Add(f)

        #make cumulative transfer function (reco efficiency)
        f2 = tf_matrix[fl][etabin].Make_CDF()
        f2.SetNpx(10000)
        f2.SetRange(0, 500)
        f2.SetName("tf_{0}eff_etabin{1}".format(fl, etabin))
        #Jet pt cut
        f2.SetParameter(0, 20)
        outfile.Add(f2)

outfile.Write()
outfile.Close()
