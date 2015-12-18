########################################
# Imports
########################################

import os
import sys
import glob
import math

import ROOT

import TTH.TTHNtupleAnalyzer.AccessHelpers as AH

########################################
# deltaR
########################################

def deltaR(eta1, phi1, eta2, phi2):
    """ Helper function to calculate delta R"""
    tlv1 = ROOT.TLorentzVector()
    tlv2 = ROOT.TLorentzVector()
    
    tlv1.SetPtEtaPhiM(1, eta1, phi1, 0)
    tlv2.SetPtEtaPhiM(1, eta2, phi2, 0)

    dphi = abs(abs(abs(phi1-phi2)-math.pi)-math.pi)
    deta = eta1 - eta2

    return math.sqrt(pow(dphi,2) + pow(deta,2))


def deltaRAlt(eta1, phi1, eta2, phi2):
    """ Helper function to calculate delta R
    Alternative version using TLorentzVector    
    """
    tlv1 = ROOT.TLorentzVector()
    tlv2 = ROOT.TLorentzVector()
    
    tlv1.SetPtEtaPhiM(1, eta1, phi1, 0)
    tlv2.SetPtEtaPhiM(1, eta2, phi2, 0)

    return tlv1.DeltaR(tlv2)



########################################
# Configuration
########################################

DEF_VAL_FLOAT = -9999.0

infile_name = "/scratch/gregor/VHBB_HEPPY_preV12_G08_tth_13tev_spring15dr74_asympt25ns/tree_10.root"


########################################
# Prepare input/output
########################################

infile = ROOT.TFile(infile_name)
intree = infile.Get('tree')
n_entries = intree.GetEntries()

########################################
# Event loop
########################################

print "Will process {0} events".format(n_entries)

h_all = ROOT.TH1F("", "", 50, -1, 1) 
h_cls = ROOT.TH1F("", "", 50, -1, 1) 

for i_event in range(n_entries):

    # Progress
    if not i_event % 1000:
        print "{0:.1f}%".format( 100.*i_event /n_entries)

    intree.GetEntry( i_event )    

    # True Higgs
    h_pt    = AH.getter(intree, "GenHiggsBoson_pt")
    h_eta   = AH.getter(intree, "GenHiggsBoson_eta")
    h_phi   = AH.getter(intree, "GenHiggsBoson_phi")
    h_mass  = AH.getter(intree, "GenHiggsBoson_mass")

    higgs = []

    for pt, eta, phi, mass in zip(h_pt, h_eta, h_phi, h_mass):
        tlv = ROOT.TLorentzVector()
        tlv.SetPtEtaPhiM(pt, eta, phi, mass)
        higgs.append(tlv)

    # Fat Jets
    fj_pt    = AH.getter(intree, "FatjetCA15ungroomed_pt")
    fj_eta   = AH.getter(intree, "FatjetCA15ungroomed_eta")
    fj_phi   = AH.getter(intree, "FatjetCA15ungroomed_phi")
    fj_mass  = AH.getter(intree, "FatjetCA15ungroomed_mass")
    fj_bb    = AH.getter(intree, "FatjetCA15ungroomed_bbtag")

    fjs = []

    for pt, eta, phi, mass, bb in zip(fj_pt, fj_eta, fj_phi, fj_mass, fj_bb):
        tlv = ROOT.TLorentzVector()
        tlv.SetPtEtaPhiM(pt, eta, phi, mass)
        tlv.bb = bb
        fjs.append(tlv)

        
    for fj in fjs:
        h_all.Fill(fj.bb)

        delta_rs = [fj.DeltaR(x) for x in higgs if x.Pt()>200]
        if delta_rs and min(delta_rs) < 0.6:
            h_cls.Fill(fj.bb)

    

h_all.SetLineColor(ROOT.kRed)
h_all.SetLineWidth(2)
h_cls.SetLineWidth(2)
        

h_all.Draw()
h_cls.Draw("SAME")

ROOT.c1.Print("foo.pdf")

# End of Event Loop
