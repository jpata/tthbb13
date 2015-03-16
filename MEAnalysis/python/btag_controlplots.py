import ROOT, sys, rootpy

ROOT.TH1.SetDefaultSumw2(True)

tf2 = ROOT.TFile("/Users/joosep/Documents/tth/data/ntp/ttjets.root")
tt = tf2.Get("tree")
tt.SetBranchStatus("*", False)
tt.SetBranchStatus("njets", True)
tt.SetBranchStatus("jets_*", True)

def hist(x):
    h = rootpy.asrootpy(ROOT.TH1D(x, x, 100, 0, 1))
    h.GetXaxis().SetTitle("CSVv2 discriminator")
    return h
    
def hist3d(x):
    h = rootpy.asrootpy(ROOT.TH3D(x, x, 6, 20, 400, 6, 0, 4.5, 100, 0, 1))
    h.GetXaxis().SetTitle("Jet pt")
    h.GetYaxis().SetTitle("Jet |eta|")
    h.GetZaxis().SetTitle("CSVv2 discriminator")
    return h

of = ROOT.TFile("ControlPlotsV6.root", "RECREATE")
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

for iev in range(tt.GetEntries()):
#for iev in range(50000):
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

print ""
for k in hists.keys():
    for k2 in hists[k].keys():
        hists[k][k2].Scale(1.0 / hists[k][k2].Integral())

of.Write("", ROOT.TObject.kOverwrite)
of.Close()
