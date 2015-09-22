import ROOT, sys

tf = ROOT.TFile(sys.argv[1])
syst = sys.argv[2]
tt = tf.Get("tree")


print "run,lumi,event,\
trig,\
is_SL,is_DL,\
lep1_pt,lep1_eta,lep1_phi,lep1_iso,lep1_pdgId,\
lep2_pt,lep2_eta,lep2_phi,lep2_iso,lep2_pdgId,\
mll,\
jet1_pt,jet2_pt,jet3_pt,jet4_pt,\
jet1_CSVv2,jet2_CSVv2,jet3_CSVv2,jet4_CSVv2,\
jet1_corr,jet2_corr,jet3_corr,jet4_corr,\
jet1_corrUp,jet2_corrUp,jet3_corrUp,jet4_corrUp,\
jet1_corrDown,jet2_corrDown,jet3_corrDown,jet4_corrDown,\
MET_pt,MET_phi,\
n_jets,n_btags,\
bWeight,\
ttHFCategory,\
finalDiscriminant1,\
finalDiscriminant2,\
n_fatjets,\
pt_fatjet_1,pt_fatjet_2,\
pt_nonW_1,pt_nonW_2,\
pt_W1_1,pt_W1_2,\
pt_W2_1,pt_W2_2,\
m_top_1,m_top_2,\
higgstag_fatjet_1,higgstag_fatjet_2"


def getVar(tt, var, syst):
    if syst == "nominal":
        return getattr(tt, var)
    else:
        return getattr(tt, var + "_" + syst)

for ev in range(tt.GetEntries()):
    tt.GetEntry(ev)
   
    nj = getVar(tt, "numJets", syst)
    nt = getVar(tt, "nBCSVM", syst)
  
    if not (tt.passPV):
        continue

    if not (tt.is_sl or tt.is_dl):
        continue

    if tt.is_sl and (nj < 3 or nt < 2):
        continue

    if tt.is_dl and (nj < 2 or nt < 1):
        continue

    nleps = tt.nleps

    leps_pt = tt.leps_pt
    leps_pdgId = tt.leps_pdgId
    leps_eta = tt.leps_eta
    leps_phi = tt.leps_phi
    leps_iso03 = tt.leps_relIso03
    leps_iso04 = tt.leps_relIso04
    
    lep0_pt = leps_pt[0]
    lep0_id = leps_pdgId[0]
    lep0_eta = leps_eta[0]
    lep0_phi = leps_phi[0]
    lep0_iso = 0
    if abs(lep0_id) == 11:
        lep0_iso = leps_iso03[0]
    elif abs(lep0_id) == 13:
        lep0_iso = leps_iso04[0]
    
    mll = 0
    if tt.is_sl:
        trig = tt.HLT_BIT_HLT_Ele27_eta2p1_WP85_Gsf_HT200_v or tt.HLT_BIT_HLT_IsoMu24_eta2p1_v
        lep1_pt = 0
        lep1_id = 0
        lep1_eta = 0
        lep1_phi = 0
        lep1_iso = 0
    elif tt.is_dl:

        trig = False
        for tr in [
            "HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v",
            "HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v",
            "HLT_BIT_HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v",
            "HLT_BIT_HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v",
            "HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v",
        ]:
            trig = trig or getattr(tt, tr)
        lep1_pt = leps_pt[1]
        lep1_id = leps_pdgId[1]
        lep1_eta = leps_eta[1]
        lep1_phi = leps_phi[1]
        lep1_iso = -1
        mll = tt.ll_mass
        if not (lep0_pt > 20 and lep1_pt > 20 and abs(lep0_eta)<2.4 and abs(lep1_eta)<2.4):
            continue
        if not mll > 20:
            continue
        if (abs(lep0_id)==abs(lep1_id) and (tt.ll_mass > 76 and tt.ll_mass < 106)):
            continue
        if not (tt.met_pt > 40):
            continue
        if abs(lep1_id) == 11:
            lep1_iso = leps_iso03[1]
        elif abs(lep1_id) == 13:
            lep1_iso = leps_iso04[1]
    
    #if not trig:
    #    continue
    jet0_pt = 0
    jet0_eta = 0
    jet0_phi = 0
    jet0_csv = 0
    jet0_corr = 0
    jet0_corrUp = 0
    jet0_corrDown = 0
    
    jet1_pt = 0
    jet1_eta = 0
    jet1_phi = 0
    jet1_csv = 0
    jet1_corr = 0
    jet1_corrUp = 0
    jet1_corrDown = 0
    
    jet2_pt = 0
    jet2_eta = 0
    jet2_phi = 0
    jet2_csv = 0
    jet2_corr = 0
    jet2_corrUp = 0
    jet2_corrDown = 0
    
    jet3_pt = 0
    jet3_eta = 0
    jet3_phi = 0
    jet3_csv = 0
    jet3_corr = 0
    jet3_corrUp = 0
    jet3_corrDown = 0

    i = 0
    jet0_pt = tt.jets_pt[i] 
    jet0_eta = tt.jets_eta[i] 
    jet0_phi = tt.jets_phi[i] 
    jet0_csv = tt.jets_btagCSV[i] 
    jet0_corr = tt.jets_corr[i] 
    jet0_corrUp = tt.jets_corr_JESUp[i] 
    jet0_corrDown = tt.jets_corr_JESDown[i] 
    
    i = 1
    jet1_pt = tt.jets_pt[i] 
    jet1_eta = tt.jets_eta[i] 
    jet1_phi = tt.jets_phi[i] 
    jet1_csv = tt.jets_btagCSV[i] 
    jet1_corr = tt.jets_corr[i] 
    jet1_corrUp = tt.jets_corr_JESUp[i] 
    jet1_corrDown = tt.jets_corr_JESDown[i] 
   
    if nj>=3:
        i = 2
        jet2_pt = tt.jets_pt[i] 
        jet2_eta = tt.jets_eta[i] 
        jet2_phi = tt.jets_phi[i] 
        jet2_csv = tt.jets_btagCSV[i] 
        jet2_corr = tt.jets_corr[i] 
        jet2_corrUp = tt.jets_corr_JESUp[i] 
        jet2_corrDown = tt.jets_corr_JESDown[i] 
    
    if nj>=4:
        i = 3
        jet3_pt = tt.jets_pt[i] 
        jet3_eta = tt.jets_eta[i] 
        jet3_phi = tt.jets_phi[i] 
        jet3_csv = tt.jets_btagCSV[i] 
        jet3_corr = tt.jets_corr[i] 
        jet3_corrUp = tt.jets_corr_JESUp[i] 
        jet3_corrDown = tt.jets_corr_JESDown[i] 
    
    if syst == "raw":
        jet0_pt = jet0_pt / jet0_corr
        jet1_pt = jet1_pt / jet1_corr
        jet2_pt = jet2_pt / jet2_corr
        jet3_pt = jet3_pt / jet3_corr
    
    ntop1 = tt.ntopCandidate
    ntop2 = tt.nothertopCandidate
    nonwpt1 = -99
    nonwpt2 = -99
    w1pt1 = -99
    w1pt2 = -99
    w2pt1 = -99
    w2pt2 = -99
    m1 = -99
    m2 = -99
    
    if ntop1 >= 1:
        nonwpt1 = tt.topCandidate_sjNonWpt[0]
        w1pt1 = tt.topCandidate_sjW1pt[0]
        w2pt1 = tt.topCandidate_sjW2pt[0]
        m1 = tt.topCandidate_mass[0]
    if ntop2 >= 1:
        nonwpt2 = tt.othertopCandidate_sjNonWpt[0]
        w1pt2 = tt.othertopCandidate_sjW1pt[0]
        w2pt2 = tt.othertopCandidate_sjW2pt[0]
        m2 = tt.othertopCandidate_mass[0]

    fdisc1 = 0
    fdisc2 = 0
    arr = [
        int(tt.run), int(tt.lumi), int(tt.evt),
        int(trig),
        int(tt.is_sl), int(tt.is_dl),
        lep0_pt, lep0_eta, lep0_phi, lep0_iso, lep0_id,
        lep1_pt, lep1_eta, lep1_phi, lep1_iso, lep1_id,
        float(mll), 
        jet0_pt, jet1_pt, jet2_pt, jet3_pt,
        jet0_csv, jet1_csv, jet2_csv, jet3_csv,
        jet0_corr, jet1_corr, jet2_corr, jet3_corr,
        jet0_corrUp, jet1_corrUp, jet2_corrUp, jet3_corrUp,
        jet0_corrDown, jet1_corrDown, jet2_corrDown, jet3_corrDown,
        tt.met_pt, tt.met_phi,
        int(nj), int(nt),
        tt.bTagWeight,
        int(tt.ttCls),
        float(fdisc1),
        float(fdisc2),
        int(0),                         #n_fatjets,\
        float(0), float(0),             #pt_fatjet_1,pt_fatjet_2,\
        nonwpt1, nonwpt2,
        w1pt1, w1pt2,
        w2pt1, w2pt2,
        m1, m2,
        float(0), float(0)              #higgstag_fatjet_1,higgstag_fatjet_2"
    ]

    s = ""
    for i in range(len(arr)):
        if not isinstance(arr[i], int):
            s += str(round(arr[i], 4)) + ","
        else:
            s += str(arr[i]) + ","
    print s[:-1]
