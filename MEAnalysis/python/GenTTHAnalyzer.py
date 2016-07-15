import copy, math

from TTH.MEAnalysis.vhbb_utils import lvec, MET, autolog
from TTH.MEAnalysis.Analyzer import FilterAnalyzer
from TTH.MEAnalysis.JetAnalyzer import attach_jet_transfer_function

class GenTTHAnalyzer(FilterAnalyzer):
    """
    Analyzes the ttbar (and Higgs) system on gen level.
    Identifies leptonic and hadronic gen top quarks. 
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        self.conf = cfg_ana._conf
        super(GenTTHAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

    def beginLoop(self, setup):
        super(GenTTHAnalyzer, self).beginLoop(setup)

    def pass_jet_selection(self, quark):
        return quark.pt > 30 and abs(quark.eta) < 2.5

    def process(self, event):
        for (syst, event_syst) in event.systResults.items():
            if event_syst.passes_btag:
                res = self._process(event_syst)
                event.systResults[syst] = res
        return True

    def _process(self, event):

        if not self.cfg_comp.isMC:
            return event 

        if "debug" in self.conf.general["verbosity"]:
            autolog("GenTTHAnalyzer started")

        #Get light quarks from W/Z
        event.l_quarks_w = event.GenWZQuark

        #Get b quarks from top
        event.b_quarks_t = event.GenBQuarkFromTop

        #Get b-quarks from H
        event.b_quarks_h = event.GenBQuarkFromH

        #Get leptonic top children
        #note that the tau lepton might be missing
        event.lep_top = event.GenLepFromTop
        event.nu_top = event.GenNuFromTop
        
        #cat_gen - a string specifying the ttbar decay mode
        event.cat_gen = None
        #cat_gen_n - a numerical value corresponding to the string
        event.cat_gen_n = -1

        #all leptonic and hadronic gen tops
        event.genTopLep = []
        event.genTopHad = []


        #Only run top algos
        if len(event.GenTop) == 2:
        
            #Gen tops might be in random order
            gt1 = event.GenTop[0]
            gt2 = event.GenTop[1]
            dm1 = getattr(gt1, "decayMode", -1)
            dm2 = getattr(gt2, "decayMode", -1)
            #single-leptonic
            if ((dm1 == 0 and dm2==1) or (dm2==0 and dm1==1)):
                
                #First top is leptonic
                if dm1 == 0:
                    event.genTopLep = [gt1]
                    event.genTopHad = [gt2]
                #Second top is leptonic
                else:
                    event.genTopLep = [gt2]
                    event.genTopHad = [gt1]
                        
                event.cat_gen = "sl"
                event.cat_gen_n = 0
            elif (dm1 == 0 and dm2 == 0):
                event.cat_gen = "dl"
                event.cat_gen_n = 1
                event.genTopLep = [gt1, gt2]
                event.genTopHad = []
            elif (dm1 == 1 and dm2 == 1):
                event.cat_gen = "fh"
                event.cat_gen_n = 2
                event.genTopHad = [gt1, gt2]
                event.genTopLep = []
            else:
                event.genTopLep = []
                event.genTopHad = []

        #these are the quarks that would pass selection
        event.l_quarks_gen = []
        event.b_quarks_gen_t = []
        event.b_quarks_gen_h = []

        nq = 0
        #Find the light quarks from W that would pass jet selection
        #associate them with a transfer function
        for q in event.l_quarks_w:
            nq += 1
            if self.pass_jet_selection(q):
                q.btagFlag = 0.0
                q.tth_match_label = "wq"
                q.tth_match_index = nq
                attach_jet_transfer_function(q, self.conf)
                event.l_quarks_gen += [q]

        #Find the b quarks from top that would pass jet selection
        #associate them with a transfer function
        for q in event.b_quarks_t:
            nq += 1
            if self.pass_jet_selection(q):
                q.btagFlag = 1.0
                q.tth_match_label = "tb"
                q.tth_match_index = nq
                attach_jet_transfer_function(q, self.conf)
                event.b_quarks_gen_t += [q]

        #Find the b quarks from Higgs that would pass jet selection
        #associate them with a transfer function
        for q in event.b_quarks_h:
            nq += 1
            if self.pass_jet_selection(q):
                q.btagFlag = 1.0
                q.tth_match_label = "hb"
                q.tth_match_index = nq
                attach_jet_transfer_function(q, self.conf)
                event.b_quarks_gen_h += [q]
        
        #Number of reco jets matched to quarks from W, top, higgs
        event.nSelected_wq = len(event.l_quarks_gen)
        event.nSelected_tb = len(event.b_quarks_gen_t)
        event.nSelected_hb = len(event.b_quarks_gen_h)

        #Get the total MET from the neutrinos
        spx = 0
        spy = 0
        for nu in event.nu_top:
            p4 = lvec(nu)
            spx += p4.Px()
            spy += p4.Py()
        event.MET_tt = MET(px=spx, py=spy)

        #Get the total ttH visible pt at gen level
        spx = 0
        spy = 0
        for p in (event.l_quarks_w + event.b_quarks_t +
            event.b_quarks_h + event.lep_top):
            p4 = lvec(p)
            spx += p4.Px()
            spy += p4.Py()
        event.tth_px_gen = spx
        event.tth_py_gen = spy

        #Calculate tth recoil
        #rho = -met - tth_matched
        event.tth_rho_px_gen = -event.MET_gen.px - event.tth_px_gen
        event.tth_rho_py_gen = -event.MET_gen.py - event.tth_py_gen

        if "gen" in self.conf.general["verbosity"]:
            for j in event.l_quarks_w:
                autolog("gen q(W)", j.pt, j.eta, j.phi, j.mass, j.pdgId)
            for j in event.b_quarks_t:
                autolog("gen b(t)", j.pt, j.eta, j.phi, j.mass, j.pdgId)
            for j in event.lep_top:
                autolog("gen l(t)", j.pt, j.eta, j.phi, j.mass, j.pdgId)
            for j in event.nu_top:
                autolog("gen n(t)", j.pt, j.eta, j.phi, j.mass, j.pdgId)
            for j in event.b_quarks_h:
                autolog("gen b(h)", j.pt, j.eta, j.phi, j.mass, j.pdgId)
            autolog("gen cat", event.cat_gen, event.cat_gen_n)


        # In semi-leptonic events we need to figure out which top b is from
        if event.cat_gen == "sl":
                    
            # If b pdgId has same sign as hadronic top pdgId, it's the one
            if event.b_quarks_t[0].pdgId * event.genTopHad[0].pdgId > 0:
                event.b_quarks_t[0].from_had_t = 1
                event.b_quarks_t[1].from_had_t = 0
            else:
                event.b_quarks_t[0].from_had_t = 0
                event.b_quarks_t[1].from_had_t = 1

        # In Di leptonic events no b quarks come from hadronic top
        elif event.cat_gen == "dl":
            for b in event.b_quarks_t:
                b.from_had_t = 0
                            
        # In All hadronic events both b quarks come from hadronic top
        elif event.cat_gen == "fh":
            for b in event.b_quarks_t:
                b.from_had_t = 1
        else:
            for b in event.b_quarks_t:
                b.from_had_t = -1
            

        #Store for each jet, specified by it's index in the jet
        #vector, if it is matched to any gen-level quarks
        matched_pairs = {}

        def match_jets_to_quarks(jetcoll, quarkcoll, label, label_numeric):
            for ij, j in enumerate(jetcoll):        
                for iq, q in enumerate(quarkcoll):

                    # Set to 1 for bs from hadronic top
                    # Set to 0 for bs from hadronic top
                    # Set to -1 for other stuff
                    if label == "tb":
                        if q.from_had_t == 1:
                            numeric_b_from_had_t = 1
                        elif q.from_had_t == 0:
                            numeric_b_from_had_t = 0
                        else:
                            numeric_b_from_had_t = -1
                    else:
                        numeric_b_from_had_t = -1

                    #find DeltaR between jet and quark
                    l1 = lvec(q)
                    l2 = lvec(j)
                    dr = l1.DeltaR(l2)
                    if dr < 0.3:
                        #Jet already had a match: take the one with smaller dR
                        if not matched_pairs.has_key(ij):
                            matched_pairs[ij] = []
                        matched_pairs[ij] += [(label, iq, dr, label_numeric, numeric_b_from_had_t)]

        #Find the best possible match for each individual jet

        #light-quarks from W
        match_jets_to_quarks(event.good_jets, event.l_quarks_gen, "wq", 0)
        #b-quarks from top
        match_jets_to_quarks(event.good_jets, event.b_quarks_gen_t, "tb", 1)
        #b-quarks from Higgs
        match_jets_to_quarks(event.good_jets, event.b_quarks_gen_h, "hb", 2)
        #gluons from top
        match_jets_to_quarks(event.good_jets, event.GenGluonFromTop, "tg", 3)
        #gluons from b
        match_jets_to_quarks(event.good_jets, event.GenGluonFromB, "bg", 4)

        #Number of reco jets matched to quarks from W, top, higgs
        event.nMatch_wq = 0
        event.nMatch_tb = 0
        event.nMatch_hb = 0
        #As above, but also required to be tagged/untagged for b/light respectively.
        event.nMatch_wq_btag = 0
        event.nMatch_tb_btag = 0
        event.nMatch_hb_btag = 0
        
        #Now check what each jet was matched to
        for ij, jet in enumerate(event.good_jets):

            jet.tth_match_label = None
            jet.tth_match_index = -1
            jet.tth_match_dr = -1
            jet.tth_match_label_numeric = -1

            #Jet did not have a match (no jet index in matched_pairs)
            if not matched_pairs.has_key(ij):
                continue #continue jet loop

            #mlabel - string label of quark collection, e.g. "wq"
            #midx - index of quark in vector that the jet was matched to
            #mdr - delta R between jet and matched quark
            #mlabel_num - numeric label of quark collection, e.g. 0
            #mlabel_num_bfromhadt - numeric label if the b is from hadronic top
            #                         -1 if not b or not from top
            #                          0 if from leptonic top
            #                          1 if from hadronic top
            matches = matched_pairs[ij]
            if len(matches) == 1:
                mlabel, midx, mdr, mlabel_num, mlabel_num_bfromhadt = matches[0]
            else:
                #select dR-ordered matches from W, t, b
                matches_hard = filter(lambda x: x[0] in ["wq", "tb", "hb"], matches)
                matches_hard = sorted(matches_hard, key=lambda x: x[2])
                if len(matches_hard) >= 1:
                    mlabel, midx, mdr, mlabel_num, mlabel_num_bfromhadt = matches_hard[0]
                else:
                    matches_soft = filter(lambda x: x[0] in ["tg", "bg"], matches)
                    matches_soft = sorted(matches_soft, key=lambda x: x[2])
                    mlabel, midx, mdr, mlabel_num, mlabel_num_bfromhadt = matches_soft[0]

            jet.tth_match_label = mlabel
            jet.tth_match_index = midx
            jet.tth_match_dr = mdr
            jet.tth_match_label_numeric = mlabel_num
            jet.tth_match_label_bfromhadt = mlabel_num_bfromhadt
            
            if mlabel == "wq":
                event.nMatch_wq += 1

                #If this jet is considered to be un-tagged
                if jet.btagFlag == 0.0:
                    event.nMatch_wq_btag += 1
            elif mlabel == "tb":
                event.nMatch_tb += 1

                #If this jet is considered to be b-tagged
                if jet.btagFlag == 1.0:
                    event.nMatch_tb_btag += 1

            elif mlabel == "hb":
                event.nMatch_hb += 1
                if jet.btagFlag == 1.0:
                    event.nMatch_hb_btag += 1

        if "debug" in self.conf.general["verbosity"]:
            autolog("nSel {0}_{1}_{2} nMatch {3}_{4}_{5} nMatch_btag {6}_{7}_{8}".format(
                event.nSelected_wq,
                event.nSelected_tb,
                event.nSelected_hb,
                event.nMatch_wq,
                event.nMatch_tb,
                event.nMatch_hb,
                event.nMatch_wq_btag,
                event.nMatch_tb_btag,
                event.nMatch_hb_btag,
            ))
        
        if "matching" in self.conf.general["verbosity"]:
            matches = {"wq":event.l_quarks_w, "tb": event.b_quarks_t, "hb":event.b_quarks_h}

            for ij, jet in enumerate(event.good_jets):
                if not matched_pairs.has_key(ij):
                    continue
                mlabel, midx, mdr, mlabel_num = matched_pairs[ij]
                autolog("jet match", ij, mlabel, midx, mdr, jet.pt, matches[mlabel][midx].pt)

        #reco-level tth-matched system
        spx = 0.0
        spy = 0.0
        for jet in event.good_jets:
            if not (jet.tth_match_label is None):
                p4 = lvec(jet)
                spx += p4.Px()
                spy += p4.Py()
        for lep in event.good_leptons:
            p4 = lvec(lep)
            match = False
            for glep in event.lep_top:
                p4g = lvec(glep)
                if p4g.DeltaR(p4) < 0.3:
                    match = True
                    break
            if match:
                spx += p4.Px()
                spy += p4.Py()

        event.tth_px_reco = spx
        event.tth_py_reco = spy

        #Calculate tth recoil
        #rho = -met - tth_matched
        event.tth_rho_px_reco = -event.MET.px - event.tth_px_reco
        event.tth_rho_py_reco = -event.MET.py - event.tth_py_reco

        #print out gen-level quarks
        if "input" in self.conf.general["verbosity"]:
            print "gen Q"
            for q in event.l_quarks_gen:
                print q.pt, q.eta, q.phi, q.mass, q.pdgId
            print "gen B"
            for q in event.b_quarks_gen:
                print q.pt, q.eta, q.phi, q.mass, q.pdgId

        return event
