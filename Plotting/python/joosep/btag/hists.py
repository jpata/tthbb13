import ROOT, sys
ROOT.gROOT.SetBatch(True)
ROOT.TH1.SetDefaultSumw2(True)
ROOT.TH1.AddDirectory(False)

INFILES = sys.argv[2:]
OUTFILE = sys.argv[1]

tt = ROOT.TChain("vhbb/tree")
for inf in INFILES:
    tt.AddFile(inf)

def hist(of, x, disc, low=0, high=1):
    h = ROOT.TH1D(x, x, 100, low, high)
    h.GetXaxis().SetTitle(disc + " b-discriminator")
    of.Add(h)
    return h
    
def hist3d(of, x, disc, low=0, high=1):
    h = ROOT.TH3D(x, x, 6, 20, 400, 6, 0, 4.5, 100, low, high)
    h.GetXaxis().SetTitle("Jet pt")
    h.GetYaxis().SetTitle("Jet |eta|")
    h.GetZaxis().SetTitle(disc + " b-discriminator")
    of.Add(h)
    return h

of = ROOT.TFile(OUTFILE, "RECREATE")
of.cd()

def makeControlPlots(discname, functoplot, low, high):
    hists = {
        "b": {
            "Bin0": hist(of, "{0}_b_Bin0__rec".format(discname), discname, low, high),
            "Bin1": hist(of, "{0}_b_Bin1__rec".format(discname), discname, low, high),
            "pt_eta": hist3d(of, "{0}_b_pt_eta".format(discname), discname, low, high)
        },
        "c": {
            "Bin0": hist(of, "{0}_c_Bin0__rec".format(discname), discname, low, high),
            "Bin1": hist(of, "{0}_c_Bin1__rec".format(discname), discname, low, high),
            "pt_eta": hist3d(of, "{0}_c_pt_eta".format(discname), discname, low, high)
        },
        "l": {
            "Bin0": hist(of, "{0}_l_Bin0__rec".format(discname), discname, low, high),
            "Bin1": hist(of, "{0}_l_Bin1__rec".format(discname), discname, low, high),
            "pt_eta": hist3d(of, "{0}_l_pt_eta".format(discname), discname, low, high)
        }
    }
    
    tt.Draw("{1} >> {0}_b_Bin0__rec".format(discname, functoplot), "abs(Jet_eta)<=1.0 && abs(Jet_hadronFlavour)==5")
    tt.Draw("{1} >> {0}_b_Bin1__rec".format(discname, functoplot), "abs(Jet_eta)>1.0 && abs(Jet_hadronFlavour)==5")

    tt.Draw("{1} >> {0}_c_Bin0__rec".format(discname, functoplot), "abs(Jet_eta)<=1.0 && abs(Jet_hadronFlavour)==4")
    tt.Draw("{1} >> {0}_c_Bin1__rec".format(discname, functoplot), "abs(Jet_eta)>1.0 && abs(Jet_hadronFlavour)==4")

    tt.Draw("{1} >> {0}_l_Bin0__rec".format(discname, functoplot), "abs(Jet_eta)<=1.0 && abs(Jet_hadronFlavour)!=4 && abs(Jet_hadronFlavour)!=5")
    tt.Draw("{1} >> {0}_l_Bin1__rec".format(discname, functoplot), "abs(Jet_eta)>1.0 && abs(Jet_hadronFlavour)!=4 && abs(Jet_hadronFlavour)!=5")


    tt.Draw("{1}:abs(Jet_eta):Jet_pt >> {0}_b_pt_eta".format(discname, functoplot), "abs(Jet_hadronFlavour)==5")
    tt.Draw("{1}:abs(Jet_eta):Jet_pt >> {0}_c_pt_eta".format(discname, functoplot), "abs(Jet_hadronFlavour)==4")
    tt.Draw("{1}:abs(Jet_eta):Jet_pt >> {0}_l_pt_eta".format(discname, functoplot), "abs(Jet_hadronFlavour)!=4 && abs(Jet_hadronFlavour)!=5")

    #normalize 1D distributions
    for k in hists.keys():
        for k2 in hists[k].keys():
            hists[k][k2].Scale(1.0 / hists[k][k2].Integral())

    #normalize 3D distributions
    for h3 in [hists[fl]["pt_eta"] for fl in ["b", "c", "l"]]:
        nbinsX = h3.GetNbinsX() #X -> pt distribution
        nbinsY = h3.GetNbinsY() #Y -> eta distribution
        nbinsZ = h3.GetNbinsZ() #Z -> CSV distribution
        for i in range(0, nbinsX+2):
            for j in range(0, nbinsY+2):

                #find integral of csv distribution in this pt/eta bin
                #int_ij = 0.
                #for k in range(0, nbinsZ + 2):
                #    int_ij += h3.GetBinContent(i,j,k)
                int_ij = float(h3.ProjectionZ("asd", i, i, j, j).Integral())
                #normalize csv histogram
                for k in range(0, nbinsZ + 2):
                    unnorm = float(h3.GetBinContent(i,j,k))
                    if int_ij > 0.0:
                        unnorm = unnorm / int_ij
                    h3.SetBinContent(i, j, k, unnorm)
                #print i, j, h3.ProjectionZ("", i, i, j, j).Integral()

makeControlPlots("btagCSV", "Jet_btagCSV", 0.0, 1.0)
makeControlPlots("btagBDT", "Jet_btagBDT", -1.0, 1.0)

of.Write()
of.Close()
