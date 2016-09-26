import ROOT, sys

tf = ROOT.TFile(sys.argv[1])

if len(sys.argv) == 2:
    syst = "nominal"
else:
    syst = sys.argv[2]

tt = tf.Get("tree")

compare_basic = True
compare_extra = False
compare_dl    = False
compare_boost = True
compare_boost1 = True


def getVar(tt, var, syst):
    if syst == "nominal":
        return getattr(tt, var)
    else:
        return getattr(tt, var + "_" + syst)

def trig_fun(tt):
    # TODO: Update
    trig = False
    if tt.is_sl:
        trig = (
            #tt.HLT_BIT_HLT_Ele27_WP85_Gsf_v or
            tt.HLT_Ele27_WPLoose_Gsf_v or 
            #tt.HLT_BIT_HLT_IsoMu17_eta2p1_v
            tt.HLT_BIT_HLT_IsoMu18_v
        )
    elif tt.is_dl:
        for tr in [
            "HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v",
            "HLT_BIT_HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v",
            "HLT_BIT_HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v",
            "HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v",
            "HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v",
        ]:
            trig = trig or getattr(tt, tr)            
    return trig
 
 
def mll_pass_fun(tt):

    mll_passed = True

    if tt.is_dl:

        mll = tt.ll_mass
        
        if not mll > 20:
            mll_passed = False
        if (abs(tt.leps_pdgId[0])==abs(tt.leps_pdgId[1]) and (tt.ll_mass > 76 and tt.ll_mass < 106)):
            mll_passed = False

    return mll_passed



variables = [    
    ["run",                  compare_basic,  lambda tt: int(tt.run)],
    ["lumi",                 compare_basic,  lambda tt: int(tt.lumi)],
    ["event",                compare_basic,  lambda tt: int(tt.evt)],
    ["trig",                 compare_extra,  trig_fun],
    ["is_SL",                compare_basic,  lambda tt: int(tt.is_sl)],
    ["is_DL",                compare_dl,     lambda tt: int(tt.is_dl)],
    ["lep1_pt",              compare_basic,  lambda tt: tt.leps_pt[0]],
    ["lep1_eta",             compare_basic,  lambda tt: tt.leps_eta[0]],
    ["lep1_phi",             compare_basic,  lambda tt: tt.leps_phi[0]],
    ["lep1_iso",             compare_basic,  lambda tt: tt.leps_relIso03[0] if abs(tt.leps_pdgId[0]) == 11 else tt.leps_relIso04[0]],
    ["lep1_pdgId",           compare_basic,  lambda tt: int(tt.leps_pdgId[0])],                                                            
    ["lep2_pt",              compare_dl,     lambda tt: (tt.leps_pt[1]) if tt.is_dl else 0.],
    ["lep2_eta",             compare_dl,     lambda tt: (tt.leps_eta[1]) if tt.is_dl else 0.],
    ["lep2_phi",             compare_dl,     lambda tt: (tt.leps_phi[1]) if tt.is_dl else 0.],
    ["lep2_iso",             compare_dl,     lambda tt: (tt.leps_relIso03[1] if abs(tt.leps_pdgId[1]) == 11 else tt.leps_relIso04[1]) if tt.is_dl else 0.],
    ["lep2_pdgId",           compare_dl,     lambda tt: int((tt.leps_pdgId[1])) if tt.is_dl else 0.],
    ["mll",                  compare_dl,     lambda tt: tt.ll_mass if tt.is_dl else 0.],
    ["mll_passed",           compare_dl,     mll_pass_fun],
    ["n_jets",               compare_basic,  lambda tt: getVar(tt, "numJets", syst)],
    ["n_btags",              compare_basic,  lambda tt: getVar(tt, "nBCSVM", syst)],
    ["jet1_pt",              compare_basic,  lambda tt: tt.jets_pt[0] if tt.numJets >= 1 else 0.],
    ["jet2_pt",              compare_basic,  lambda tt: tt.jets_pt[1] if tt.numJets >= 2 else 0.],
    ["jet3_pt",              compare_basic,  lambda tt: tt.jets_pt[2] if tt.numJets >= 3 else 0.],
    ["jet4_pt",              compare_basic,  lambda tt: tt.jets_pt[3] if tt.numJets >= 4 else 0.],
    ["jet1_CSVv2",           compare_basic,  lambda tt: tt.jets_btagCSV[0] if tt.numJets >= 1 else 0.],
    ["jet2_CSVv2",           compare_basic,  lambda tt: tt.jets_btagCSV[1] if tt.numJets >= 2 else 0.],
    ["jet3_CSVv2",           compare_basic,  lambda tt: tt.jets_btagCSV[2] if tt.numJets >= 3 else 0.],
    ["jet4_CSVv2",           compare_basic,  lambda tt: tt.jets_btagCSV[3] if tt.numJets >= 4 else 0.],
    ["jet1_JesSF",           compare_extra],
    ["jet2_JesSF",           compare_extra],
    ["jet3_JesSF",           compare_extra],
    ["jet4_JesSF",           compare_extra],
    ["jet1_JerSF",           compare_extra],
    ["jet2_JerSF",           compare_extra],
    ["jet3_JerSF",           compare_extra],
    ["jet4_JerSF",           compare_extra],
    ["MET_pt",               compare_extra],
    ["MET_phi",              compare_extra],
    ["met_passed",           compare_extra],
    ["bWeight",              compare_extra],
    ["ttHFCategory",         compare_extra],
    ["finalDiscriminant1",   compare_extra],
    ["finalDiscriminant2",   compare_extra],
    ["higgstag_fatjet_1",    compare_extra],
    ["higgstag_fatjet_2",    compare_extra],
    ["n_fatjets",            compare_boost, lambda tt: tt.nfatjets],
    ["pt_fatjet_1",          compare_boost, lambda tt: tt.fatjets_pt[0] if tt.nfatjets >= 1 else 0.],
    ["pt_fatjet_2",          compare_boost, lambda tt: tt.fatjets_pt[1] if tt.nfatjets >= 2 else 0.],
    ["eta_fatjet_1",         compare_boost, lambda tt: tt.fatjets_eta[0] if tt.nfatjets >= 1 else 0.],
    ["eta_fatjet_2",         compare_boost, lambda tt: tt.fatjets_eta[1] if tt.nfatjets >= 2 else 0.],
    ["pt_nonW_1",            compare_boost, lambda tt: tt.topCandidatesSync_sjNonWptcal[0] if tt.ntopCandidatesSync >= 1 else 0.],
    ["pt_nonW_2",            compare_boost, lambda tt: tt.topCandidatesSync_sjNonWptcal[1] if tt.ntopCandidatesSync >= 2 else 0.],
    ["pt_W1_1",              compare_boost, lambda tt: tt.topCandidatesSync_sjW1ptcal[0] if tt.ntopCandidatesSync >= 1 else 0.],
    ["pt_W1_2",              compare_boost, lambda tt: tt.topCandidatesSync_sjW1ptcal[1] if tt.ntopCandidatesSync >= 2 else 0.],
    ["pt_W2_1",              compare_boost, lambda tt: tt.topCandidatesSync_sjW2ptcal[0] if tt.ntopCandidatesSync >= 1 else 0.],
    ["pt_W2_2",              compare_boost, lambda tt: tt.topCandidatesSync_sjW2ptcal[1] if tt.ntopCandidatesSync >= 2 else 0.],   
    ["csv_nonW_1",           compare_boost1, lambda tt: tt.topCandidatesSync_sjNonWbtag[0] if tt.ntopCandidatesSync >= 1 else 0.], 
    ["csv_nonW_2",           compare_boost1, lambda tt: tt.topCandidatesSync_sjNonWbtag[1] if tt.ntopCandidatesSync >= 2 else 0.], 
    ["csv_W1_1",             compare_boost1, lambda tt: tt.topCandidatesSync_sjW1btag[0] if tt.ntopCandidatesSync >= 1 else 0.],   
    ["csv_W1_2",             compare_boost1, lambda tt: tt.topCandidatesSync_sjW1btag[1] if tt.ntopCandidatesSync >= 2 else 0.],   
    ["csv_W2_1",             compare_boost1, lambda tt: tt.topCandidatesSync_sjW2btag[0] if tt.ntopCandidatesSync >= 1 else 0.],   
    ["csv_W2_2",             compare_boost1, lambda tt: tt.topCandidatesSync_sjW2btag[1] if tt.ntopCandidatesSync >= 2 else 0.],   
    ["pt_top_1",              compare_boost, lambda tt: tt.topCandidatesSync_ptcal[0] if tt.ntopCandidatesSync >= 1 else 0.],   
    ["pt_top_2",              compare_boost, lambda tt: tt.topCandidatesSync_ptcal[1] if tt.ntopCandidatesSync >= 2 else 0.],   
    ["eta_top_1",              compare_boost, lambda tt: tt.topCandidatesSync_etacal[0] if tt.ntopCandidatesSync >= 1 else 0.],   
    ["eta_top_2",              compare_boost, lambda tt: tt.topCandidatesSync_etacal[1] if tt.ntopCandidatesSync >= 2 else 0.],   
    ["m_top_1",              compare_boost, lambda tt: tt.topCandidatesSync_masscal[0] if tt.ntopCandidatesSync >= 1 else 0.],   
    ["m_top_2",              compare_boost, lambda tt: tt.topCandidatesSync_masscal[1] if tt.ntopCandidatesSync >= 2 else 0.],   
    ["pt_sf_filterjet1_1",   compare_boost, lambda tt: float(tt.higgsCandidate_sj1pt_subjetfiltered[0]) if tt.nhiggsCandidate >= 1 else 0.],
    ["pt_sf_filterjet1_2",   compare_boost, lambda tt: float(tt.higgsCandidate_sj1pt_subjetfiltered[1]) if tt.nhiggsCandidate >= 2 else 0.],
    ["pt_sf_filterjet2_1",   compare_boost, lambda tt: float(tt.higgsCandidate_sj2pt_subjetfiltered[0]) if tt.nhiggsCandidate >= 1 else 0.],
    ["pt_sf_filterjet2_2",   compare_boost, lambda tt:  float(tt.higgsCandidate_sj2pt_subjetfiltered[1]) if tt.nhiggsCandidate >= 2 else 0.],
    ["pt_sf_filterjet3_1",   compare_boost, lambda tt: float(tt.higgsCandidate_sj3pt_subjetfiltered[0])  if tt.nhiggsCandidate >= 1 else 0.],
    ["pt_sf_filterjet3_2",   compare_boost, lambda tt: float(tt.higgsCandidate_sj3pt_subjetfiltered[1])  if tt.nhiggsCandidate >= 2 else 0.],
    ["csv_sf_filterjet1_1",  compare_boost, lambda tt: tt.higgsCandidate_sj1btag_subjetfiltered[0] if tt.nhiggsCandidate >= 1 else 0.],
    ["csv_sf_filterjet1_2",  compare_boost, lambda tt: tt.higgsCandidate_sj1btag_subjetfiltered[1] if tt.nhiggsCandidate >= 2 else 0.],
    ["csv_sf_filterjet2_1",  compare_boost, lambda tt: tt.higgsCandidate_sj2btag_subjetfiltered[0] if tt.nhiggsCandidate >= 1 else 0.],
    ["csv_sf_filterjet2_2",  compare_boost, lambda tt: tt.higgsCandidate_sj2btag_subjetfiltered[1] if tt.nhiggsCandidate >= 2 else 0.],
    ["csv_sf_filterjet3_1",  compare_boost, lambda tt: tt.higgsCandidate_sj3btag_subjetfiltered[0]  if tt.nhiggsCandidate >= 1 else 0.],
    ["csv_sf_filterjet3_2",  compare_boost, lambda tt: tt.higgsCandidate_sj3btag_subjetfiltered[1]  if tt.nhiggsCandidate >= 2 else 0.],
    ["pt_pruned_subjet1_1",  compare_boost, lambda tt: tt.higgsCandidate_sj1pt_pruned[0] if tt.nhiggsCandidate >= 1 else 0.],   
    ["pt_pruned_subjet1_2",  compare_boost, lambda tt: tt.higgsCandidate_sj1pt_pruned[1] if tt.nhiggsCandidate >= 2 else 0.],   
    ["pt_pruned_subjet2_1",  compare_boost, lambda tt: tt.higgsCandidate_sj2pt_pruned[0] if tt.nhiggsCandidate >= 1 else 0.],   
    ["pt_pruned_subjet2_2",  compare_boost, lambda tt: tt.higgsCandidate_sj2pt_pruned[1] if tt.nhiggsCandidate >= 2 else 0.],   
    ["csv_pruned_subjet1_1", compare_boost, lambda tt: tt.higgsCandidate_sj1btag_pruned[0] if tt.nhiggsCandidate >= 1 else 0.], 
    ["csv_pruned_subjet1_2", compare_boost, lambda tt: tt.higgsCandidate_sj1btag_pruned[1] if tt.nhiggsCandidate >= 2 else 0.], 
    ["csv_pruned_subjet2_1", compare_boost, lambda tt: tt.higgsCandidate_sj2btag_pruned[0] if tt.nhiggsCandidate >= 1 else 0.], 
    ["csv_pruned_subjet2_2", compare_boost, lambda tt: tt.higgsCandidate_sj2btag_pruned[1] if tt.nhiggsCandidate >= 2 else 0.], 
    ["pt_sd_subjet1_1",      compare_boost, lambda tt: tt.higgsCandidate_sj1pt_softdrop[0] if tt.nhiggsCandidate >= 1 else 0.],  
    ["pt_sd_subjet1_2",      compare_boost, lambda tt: tt.higgsCandidate_sj1pt_softdrop[1] if tt.nhiggsCandidate >= 2 else 0.],  
    ["pt_sd_subjet2_1",      compare_boost, lambda tt: tt.higgsCandidate_sj2pt_softdrop[0] if tt.nhiggsCandidate >= 1 else 0.],  
    ["pt_sd_subjet2_2",      compare_boost, lambda tt: tt.higgsCandidate_sj2pt_softdrop[1] if tt.nhiggsCandidate >= 2 else 0.],  
    ["csv_sd_subjet1_1",     compare_boost, lambda tt: tt.higgsCandidate_sj1btag_softdrop[0] if tt.nhiggsCandidate >= 1 else 0.],
    ["csv_sd_subjet1_2",     compare_boost, lambda tt: tt.higgsCandidate_sj1btag_softdrop[1] if tt.nhiggsCandidate >= 2 else 0.],
    ["csv_sd_subjet2_1",     compare_boost, lambda tt: tt.higgsCandidate_sj2btag_softdrop[0] if tt.nhiggsCandidate >= 1 else 0.],
    ["csv_sd_subjet2_2",     compare_boost, lambda tt: tt.higgsCandidate_sj2btag_softdrop[1] if tt.nhiggsCandidate >= 2 else 0.],
    ["pt_sdz2b1_subjet1_1",  compare_boost, lambda tt: tt.higgsCandidate_sj1pt_softdropz2b1[0] if tt.nhiggsCandidate >= 1 else 0.],  
    ["pt_sdz2b1_subjet1_2",  compare_boost, lambda tt: tt.higgsCandidate_sj1pt_softdropz2b1[1] if tt.nhiggsCandidate >= 2 else 0.],  
    ["pt_sdz2b1_subjet2_1",  compare_boost, lambda tt: tt.higgsCandidate_sj2pt_softdropz2b1[0] if tt.nhiggsCandidate >= 1 else 0.],  
    ["pt_sdz2b1_subjet2_2",  compare_boost, lambda tt: tt.higgsCandidate_sj2pt_softdropz2b1[1] if tt.nhiggsCandidate >= 2 else 0.],  
    ["csv_sdz2b1_subjet1_1", compare_boost, lambda tt: tt.higgsCandidate_sj1btag_softdropz2b1[0] if tt.nhiggsCandidate >= 1 else 0.],
    ["csv_sdz2b1_subjet1_2", compare_boost, lambda tt: tt.higgsCandidate_sj1btag_softdropz2b1[1] if tt.nhiggsCandidate >= 2 else 0.],
    ["csv_sdz2b1_subjet2_1", compare_boost, lambda tt: tt.higgsCandidate_sj2btag_softdropz2b1[0] if tt.nhiggsCandidate >= 1 else 0.],
    ["csv_sdz2b1_subjet2_2", compare_boost, lambda tt: tt.higgsCandidate_sj2btag_softdropz2b1[1] if tt.nhiggsCandidate >= 2 else 0.],
]    



lines = []
for ev in range(tt.GetEntries()):

    tt.GetEntry(ev)
   
  
    if not (tt.passPV):
        continue

    if not (tt.is_sl or tt.is_dl):
        continue

    if tt.is_sl and (getVar(tt, "numJets", syst) < 4 or  getVar(tt, "nBCSVM", syst)< 2):
        continue
        
    # TODO: update DL preselection
    #if tt.is_dl and (nj < 3 or nt < 1):
    #    continue
    
    # TODO: add as function
    if tt.is_dl:
        if (abs(tt.leps_pdgId[0])==abs(tt.leps_pdgId[1]) and not (tt.met_pt > 40)):
            met_passed = False

    # TODO: reimplement trigger requirement
    #if not trig:
    #    continue
    
    #ntop1 = tt.ntopCandidate
    #ntop2 = tt.nothertopCandidate
    #nonwpt1 = -99
    #nonwpt2 = -99
    #w1pt1 = -99
    #w1pt2 = -99
    #w2pt1 = -99
    #w2pt2 = -99
    #m1 = -99
    #m2 = -99
    #
    #if ntop1 >= 1:
    #    nonwpt1 = tt.topCandidate_sjNonWpt[0]
    #    w1pt1 = tt.topCandidate_sjW1pt[0]
    #    w2pt1 = tt.topCandidate_sjW2pt[0]
    #    m1 = tt.topCandidate_mass[0]
    #if ntop2 >= 1:
    #    nonwpt2 = tt.othertopCandidate_sjNonWpt[0]
    #    w1pt2 = tt.othertopCandidate_sjW1pt[0]
    #    w2pt2 = tt.othertopCandidate_sjW2pt[0]
    #    m2 = tt.othertopCandidate_mass[0]
    #
    #fdisc1 = 0
    #fdisc2 = 0
    #arr = [
    #    int(tt.run), int(tt.lumi), int(tt.evt),
    #    int(trig),
    #    int(tt.is_sl), int(tt.is_dl),
    #    lep0_pt, lep0_eta, lep0_phi, lep0_iso, lep0_id,
    #    lep1_pt, lep1_eta, lep1_phi, lep1_iso, lep1_id,
    #    float(mll), int(mll_passed),
    #    jet0_pt, jet1_pt, jet2_pt, jet3_pt,
    #    jet0_csv, jet1_csv, jet2_csv, jet3_csv,
    #    0, 0, 0, 0,
    #    0, 0, 0, 0,
    #    #jet0_JesSF, jet1_JesSF, jet2_JesSF, jet3_JesSF,
    #    #jet0_JerSF, jet1_JerSF, jet2_JerSF, jet3_JerSF,
    #    tt.met_pt, tt.met_phi,
    #    int(met_passed),
    #    int(nj), int(nt),
    #    getattr(tt, "bTagWeight", 0.0),
    #    int(getattr(tt, "ttCls", 0)),
    #    float(fdisc1),
    #    float(fdisc2),
    #    int(0),                         #n_fatjets,\
    #    float(0), float(0),             #pt_fatjet_1,pt_fatjet_2,\
    #    nonwpt1, nonwpt2,
    #    w1pt1, w1pt2,
    #    w2pt1, w2pt2,
    #    m1, m2,
    #    float(0), float(0)              #higgstag_fatjet_1,higgstag_fatjet_2"
    #]

    s = ""
    for var in variables:
        if var[1]:            
            res = var[2](tt)
            
            # Map dummy -9999 to zero
            if res == -9999:
                res =0.
            
            if not isinstance(res, int):
                s += "{0:.4f}".format(res) + ","
            else:
                s += str(res) + ","
    lines += [(int(tt.evt), s[:-1])]

# List of all variable names
print ",".join([var[0] for var in variables if var[1]])

lines = sorted(lines, key=lambda x: x[0])
for line in lines:
    print line[1]
