import TTH.MEAnalysis.TFClasses as TFClasses
from TTH.MEAnalysis.MEAnalysis_cfg_heppy_local import Conf
import pickle
import ROOT
ROOT.gROOT.SetBatch(False)

conf = Conf()
#Load transfer functions from pickle file
pi_file = open(conf.general["transferFunctionsPickle"] , 'rb')
conf.tf_matrix = pickle.load(pi_file)

f = conf.tf_matrix["b"][1].Make_Formula(False)
f.SetParameter(0, 60)
f.SetRange(0, 120)
print f.GetTitle()
f.SetTitle("gen pt 60")
c = ROOT.TCanvas()
f.Draw()
c.Print("tf.pdf")


f = conf.tf_matrix["b"][1].Make_CDF()
f.SetParameter(0, 30) #lower limit
f.SetRange(0, 100)
f.SetTitle("gen pt 30")
c = ROOT.TCanvas()
f.Draw()
c.Print("cdf.pdf")
