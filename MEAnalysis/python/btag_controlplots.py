import ROOT, sys

ROOT.TH1.SetDefaultSumw2(True)

tt = ROOT.TChain("tree")
tt.AddFile("/home/joosep/tth/gc/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ext3-v1.root")
tt.AddFile("/home/joosep/tth/gc/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2.root")
print tt.GetEntries()
first = int(sys.argv[1])
last = first + int(sys.argv[2])
nfile = int(sys.argv[3])

tt.SetBranchStatus("*", False)
tt.SetBranchStatus("njets", True)
for br in ["pt", "eta", "mcFlavour", "btagCSV"]:
    tt.SetBranchStatus("jets_"+br, True)

def hist(x):
    h = ROOT.TH1D(x, x, 100, 0, 1)
    h.GetXaxis().SetTitle("CSVv2 discriminator")
    return h
    
def hist3d(x):
    h = ROOT.TH3D(x, x, 6, 20, 400, 6, 0, 4.5, 100, 0, 1)
    h.GetXaxis().SetTitle("Jet pt")
    h.GetYaxis().SetTitle("Jet |eta|")
    h.GetZaxis().SetTitle("CSVv2 discriminator")
    return h

of = ROOT.TFile("ControlPlots.root.{0}".format(nfile), "RECREATE")
of.cd()
hists = {
    "b": {
        "Bin0": hist("csv_b_Bin0__csv_rec"),
        "Bin1": hist("csv_b_Bin1__csv_rec"),
        "pt_eta": hist3d("csv_b_pt_eta")
    },
    "c": {
        "Bin0": hist("csv_c_Bin0__csv_rec"),
        "Bin1": hist("csv_c_Bin1__csv_rec"),
        "pt_eta": hist3d("csv_c_pt_eta")
    },
    "l": {
        "Bin0": hist("csv_l_Bin0__csv_rec"),
        "Bin1": hist("csv_l_Bin1__csv_rec"),
        "pt_eta": hist3d("csv_l_pt_eta")
    }
}

#for iev in range(tt.GetEntries()):
for iev in xrange(first, min(last, tt.GetEntries())):
    tt.GetEntry(iev)
    ev = tt
    if iev%10000 == 0:
        sys.stdout.write(".")
        sys.stdout.flush()
    for ji in range(ev.njets):
        pt, eta, csv, fl = ev.jets_pt[ji], ev.jets_eta[ji], ev.jets_btagCSV[ji], ev.jets_mcFlavour[ji]
        flavour = "l"
        if abs(fl) == 5:
            flavour = "b"
        elif abs(fl) == 4:
            flavour = "c"
        if abs(eta)>1.0:
            b = "Bin1"
        else:
            b = "Bin0"
        hists[flavour]["pt_eta"].Fill(pt, abs(eta), csv)
        hists[flavour][b].Fill(csv)

#print ""
for k in hists.keys():
    for k2 in hists[k].keys():
        hists[k][k2].Scale(1.0 / hists[k][k2].Integral())

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
            #print i, j, h3.ProjectionZ("asd", i, i, j, j).Integral()

of.Write("", ROOT.TObject.kOverwrite)
of.Close()
