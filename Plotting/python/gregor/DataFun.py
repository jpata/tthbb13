
from TTH.Plotting.Helpers.PrepareRootStyle import myStyle
import ROOT

myStyle.SetPadLeftMargin(0.18)
myStyle.SetPadRightMargin(0.04)
myStyle.SetPadTopMargin(0.06)

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()


fns = {
    "data" : "/scratch/gregor/t/foo.root",
    "mc"   : "root://t3dcachedb.psi.ch:1094//pnfs/psi.ch/cms/trivcat/store/user/gregor/VHBBHeppypreT12/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_preT12_TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/150625_084849/0000/tree_568.root"
}


plots = [    
    ["jet_pt"  , "Jet_pt[0]"            , "nselLeptons==1 && abs(selLeptons_pdgId)==13", "(50,0,300)", "Leading AK4 Jet p_{T} [GeV]"],
    
    ["htt_mass", "httCandidates_mass", "nselLeptons==1 && abs(selLeptons_pdgId)==13", "(50,0,300)", "HTT Candidate mass [GeV]"],
    ["htt_frec", "httCandidates_fRec", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && httCandidates_mass > 110", "(20,0,0.5)", "HTT fRec"],

    ["ca15_pt", "FatjetCA15ungroomed_pt[0]", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && httCandidates_mass > 110 && httCandidates_fRec < 0.2", "(40,200,500)",   "Ungroomed CA15 Jet p_{T} [GeV]"],
    ["ca15_mass", "FatjetCA15ungroomed_mass[0]", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && httCandidates_mass > 110 && httCandidates_fRec < 0.2", "(40,0,500)", "Ungroomed CA15 Jet mass [GeV]"],
    ["ca15_eta", "FatjetCA15ungroomed_eta[0]", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && httCandidates_mass > 110 && httCandidates_fRec < 0.2", "(30,-3,3)", "Ungroomed CA15 Jet #eta"],

    ["ca15_tau1", "FatjetCA15ungroomed_tau1[0]", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && fabs(FatjetCA15ungroomed_eta[0])<1.5 && httCandidates_mass > 110 && httCandidates_fRec < 0.2", "(40,0,1.)", "Ungroomed CA15 Jet #tau_{1}"],
    ["ca15_tau2", "FatjetCA15ungroomed_tau2[0]", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && fabs(FatjetCA15ungroomed_eta[0])<1.5 && httCandidates_mass > 110 && httCandidates_fRec < 0.2", "(40,0,.6)", "Ungroomed CA15 Jet #tau_{2}"],
    ["ca15_tau3", "FatjetCA15ungroomed_tau3[0]", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && fabs(FatjetCA15ungroomed_eta[0])<1.5 && httCandidates_mass > 110 && httCandidates_fRec < 0.2", "(40,0,.4)", "Ungroomed CA15 Jet #tau_{3}"],
    ["ca15_tau32", "FatjetCA15ungroomed_tau3[0]/FatjetCA15ungroomed_tau2[0]", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && fabs(FatjetCA15ungroomed_eta[0])<1.5 && httCandidates_mass > 110 && httCandidates_fRec < 0.2 && FatjetCA15ungroomed_tau2[0] > 0", "(40,0,1.)", "Ungroomed CA15 Jet #tau_{3}/#tau_{2}"],

    ["ca15_sdmass", "FatjetCA15softdrop_mass[0]", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && fabs(FatjetCA15ungroomed_eta[0])<1.5 && httCandidates_mass > 110 && httCandidates_fRec < 0.2", "(40,0,400)", "Softdrop (z=0.1, #beta=0) CA15 Jet mass [GeV]"],
    ["ca15_trimmass", "FatjetCA15trimmed_mass[0]", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && fabs(FatjetCA15ungroomed_eta[0])<1.5 && httCandidates_mass > 110 && httCandidates_fRec < 0.2", "(40,0,400)", "Trimmed CA15 Jet mass [GeV]"],
    ["ca15_prunedmass", "FatjetCA15pruned_mass[0]", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && fabs(FatjetCA15ungroomed_eta[0])<1.5 && httCandidates_mass > 110 && httCandidates_fRec < 0.2", "(40,0,400)", "Pruned CA15 Jet mass [GeV]"],


    ["ak08_pt", "FatjetAK08ungroomed_pt[0]", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && httCandidates_mass > 110 && httCandidates_fRec < 0.2", "(40,200,500)",   "Ungroomed AK08 Jet p_{T} [GeV]"],
    ["ak08_mass", "FatjetAK08ungroomed_mass[0]", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && httCandidates_mass > 110 && httCandidates_fRec < 0.2", "(40,0,500)", "Ungroomed AK08 Jet mass [GeV]"],
    ["ak08_eta", "FatjetAK08ungroomed_eta[0]", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && httCandidates_mass > 110 && httCandidates_fRec < 0.2", "(30,-3,3)", "Ungroomed AK08 Jet #eta"],

    ["ak08_tau1", "FatjetAK08ungroomed_tau1[0]", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && fabs(FatjetAK08ungroomed_eta[0]) < 1.5 && httCandidates_mass > 110 && httCandidates_fRec < 0.2", "(40,0,1.)", "Ungroomed AK08 Jet #tau_{1}"],
    ["ak08_tau2", "FatjetAK08ungroomed_tau2[0]", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && fabs(FatjetAK08ungroomed_eta[0]) < 1.5 && httCandidates_mass > 110 && httCandidates_fRec < 0.2", "(40,0,.6)", "Ungroomed AK08 Jet #tau_{2}"],
    ["ak08_tau3", "FatjetAK08ungroomed_tau3[0]", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && fabs(FatjetAK08ungroomed_eta[0]) < 1.5 && httCandidates_mass > 110 && httCandidates_fRec < 0.2", "(40,0,.4)", "Ungroomed AK08 Jet #tau_{3}"],
    ["ak08_tau32", "FatjetAK08ungroomed_tau3[0]/FatjetAK08ungroomed_tau2[0]", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && fabs(FatjetAK08ungroomed_eta[0]) < 1.5 && httCandidates_mass > 110 && httCandidates_fRec < 0.2 && FatjetAK08ungroomed_tau2[0] > 0", "(40,0,1.)", "Ungroomed AK08 Jet #tau_{3}/#tau_{2}"],

    ["ak08_sdmass", "FatjetAK08ungroomed_msoftdrop[0]", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && fabs(FatjetAK08ungroomed_eta[0]) < 1.5 && httCandidates_mass > 110 && httCandidates_fRec < 0.2", "(40,0,400)", "Softdrop (z=0.1, #beta=0) AK08 Jet mass [GeV]"],
    ["ak08_trimmass", "FatjetAK08ungroomed_mtrimmed[0]", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && fabs(FatjetAK08ungroomed_eta[0]) < 1.5 && httCandidates_mass > 110 && httCandidates_fRec < 0.2", "(40,0,400)", "Trimmed AK08 Jet mass [GeV]"],
    ["ak08_prunedmass", "FatjetAK08ungroomed_mpruned[0]", "nselLeptons==1 && abs(selLeptons_pdgId)==13 && fabs(FatjetAK08ungroomed_eta[0]) < 1.5 && httCandidates_mass > 110 && httCandidates_fRec < 0.2", "(40,0,400)", "Pruned AK08 Jet mass [GeV]"],


#    Ropt
#    RoptCalc

]


i_draw =0 

hs = {}

c = ROOT.TCanvas("","",800,800)


for sample, fn in fns.iteritems():
    
    input_file = ROOT.TFile.Open(fn, "READ" )
    input_tree = getattr(input_file, "tree")

    for plot in plots:

        name    = plot[0]
        var     = plot[1]
        cut     = plot[2]
        binning = plot[3]
        title   = plot[4]

        htmp_name = "htmp"+str(i_draw)
        i_draw += 1

        input_tree.Draw(var + ">>{0}{1}".format(htmp_name, binning), cut)
        
        h = ROOT.gDirectory.Get(htmp_name).Clone()
        h.SetDirectory(0)
    
        hs[sample + "_" + name] = h
        
for plot in plots:

    name   = plot[0]
    title  = plot[4]
    
    h_data = hs["data_" + name]
    h_mc   = hs["mc_" + name]

    h_data.GetXaxis().SetTitle(title)
    h_data.GetYaxis().SetTitle("Events")


    h_data.SetLineColor(ROOT.kBlack)
    h_mc.SetLineColor(ROOT.kRed)

    h_data.SetLineWidth(2)
    h_mc.SetLineWidth(2)

    h_mc.Scale( h_data.Integral()/h_mc.Integral() )

    h_data.Draw("P E0")
    h_mc.Draw("HIST SAME")

    
    txt = ROOT.TText()
    txt.SetTextFont(61)
    txt.SetTextSize(0.05)
    txt.DrawTextNDC(0.2, 0.88, "CMS")

    txt.SetTextFont(52)
    txt.SetTextSize(0.04)
    txt.DrawTextNDC(0.2, 0.84, "Work in Progress")
    
    txt.SetTextFont(41)
    txt.DrawTextNDC(0.85, 0.95, "13 TeV")

    
    
    c.Print(name + ".pdf")
