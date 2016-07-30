import ROOT, json, sys, os
ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.gSystem.Load("libTTHMEIntegratorStandalone.so")
from ROOT import MEM
from ROOT import TLorentzVector
import math
import pickle
import numpy as np
import copy

def configure_transfer_function(cfg):
    for nb in [0, 1]:
        for fl1, fl2 in [('b', MEM.TFType.bLost), ('l', MEM.TFType.qLost)]:
            tf = tf_matrix[fl1][nb].Make_CDF()
            #set pt cut for efficiency function
            tf.SetParameter(0, 30)
            tf.SetNpx(10000)
            tf.SetRange(0, 500)
            cfg.set_tf_global(fl2, nb, tf)

def normalize_proba(vec):
    proba_vec = np.array(vec)
    proba_vec[proba_vec <= 1E-100] = 1E-100
    ret = np.array(np.log10(proba_vec), dtype="float64")
    return ret

def attach_jet_transfer_function(pt, eta):
    """
    Attaches transfer functions to the supplied jet based on the jet eta bin.
    """
    jet_eta_bin = 0
    if abs(eta)>1.0:
        jet_eta_bin = 1
    tf_b = tf_matrix['b'][jet_eta_bin].Make_Formula(False)
    tf_l = tf_matrix['l'][jet_eta_bin].Make_Formula(False)
    
    tf_b.SetNpx(10000)
    tf_b.SetRange(0, 500)
    tf_l.SetNpx(10000)
    tf_l.SetRange(0, 500)
    
    return tf_b, tf_l

def get_results(mem_res):
    res = {}
    res["p"] = mem_res.p
    res["p_err"] = mem_res.p_err
    res["time"] = mem_res.time/1000.0
    res["nperm"] = mem_res.num_perm

    for iperm in range(mem_res.num_perm):
        perms = mem_res.permutation_indexes[iperm]
        res["perm_{0}_perms".format(iperm)] = [p for p in perms] 
        v_p = normalize_proba([v for v in mem_res.permutation_probas[iperm]])
        res["perm_{0}_p_mean".format(iperm)] = np.mean(v_p)
        res["perm_{0}_p_std".format(iperm)] = np.std(v_p)

        v_p_tf = normalize_proba([v for v in mem_res.permutation_probas_transfer[iperm]])
        res["perm_{0}_p_tf_mean".format(iperm)] = np.mean(v_p_tf)
        res["perm_{0}_p_tf_std".format(iperm)] = np.std(v_p_tf)

        v_p_me = normalize_proba([v for v in mem_res.permutation_probas_me[iperm]])
        res["perm_{0}_p_me_mean".format(iperm)] = np.mean(v_p_me)
        res["perm_{0}_p_me_std".format(iperm)] = np.std(v_p_me)
        
        if len(mem_res.permutation_sum)>0:
            res["perm_{0}_sum".format(iperm)] = mem_res.permutation_sum[iperm]
    return res

def add_obj(mem, typ, **kwargs):

    if kwargs.has_key("p4s"):
        pt, eta, phi, mass = kwargs.pop("p4s")
        v = TLorentzVector()
        v.SetPtEtaPhiM(pt, eta, phi, mass);
    elif kwargs.has_key("p4c"):
        v = TLorentzVector(*kwargs.pop("p4c"))
    obsdict = kwargs.pop("obsdict", {})

    o = MEM.Object(v, typ)
    if typ == MEM.ObjectType.Jet:
        tb, tl = attach_jet_transfer_function(v.Pt(), v.Eta()) 
        o.addTransferFunction(MEM.TFType.qReco, tl)
        o.addTransferFunction(MEM.TFType.bReco, tb)
    
    for k, v in obsdict.items():
        o.addObs(k, v)
    mem.push_back_object(o)

if __name__ == "__main__":

    outfile = open("out.json", "w")

    FILE_NAMES = os.environ["FILE_NAMES"].split()
    SKIP_EVENTS = int(os.environ["SKIP_EVENTS"])
    MAX_EVENTS = int(os.environ["MAX_EVENTS"])

    inlines = []
    nline = 0
    for fn in FILE_NAMES:
        fi = open(fn)
        for line in fi.readlines():
            nline += 1
            if nline <= SKIP_EVENTS:
                continue
            if len(inlines) >= MAX_EVENTS:
                break
            inlines += [line]
        fi.close()
    
    print "processing {0} events".format(len(inlines))
    CvectorPermutations = getattr(ROOT, "std::vector<MEM::Permutations::Permutations>")
    CvectorPSVar = getattr(ROOT, "std::vector<MEM::PSVar::PSVar>")
    
    pvec = CvectorPermutations()
    pvec.push_back(MEM.Permutations.BTagged)
    pvec.push_back(MEM.Permutations.QUntagged)
    pvec.push_back(MEM.Permutations.QQbarBBbarSymmetry)
    
    cfg1 = ROOT.MEM.MEMConfig()
    cfg1.name = "CASE1"
    cfg1.defaultCfg()
    cfg1.points = 2000
    cfg1.save_permutations = True
    cfg1.vars_to_integrate = CvectorPSVar()
    cfg1.vars_to_marginalize = CvectorPSVar()
    cfg1.transfer_function_method = MEM.TFMethod.External
    cfg1.perm_pruning = pvec
    cfg1.do_add_jet = lambda pt, btag: True
    cfg1.do_calculate = lambda njet, nlep: njet>=6 and nlep==1
    cfg1.final_state = MEM.FinalState.LH
    
    
    cfg2 = ROOT.MEM.MEMConfig()
    cfg2.name = "CASE2"
    cfg2.defaultCfg()
    cfg2.points = 2000
    cfg2.save_permutations = True
    cfg2.vars_to_integrate = CvectorPSVar()
    cfg2.vars_to_marginalize = CvectorPSVar()
    cfg2.transfer_function_method = MEM.TFMethod.External
    cfg2.perm_pruning = pvec
    cfg2.perm_int = 1
    cfg2.do_add_jet = lambda pt, btag: True
    cfg2.do_calculate = lambda njet, nlep: njet>=6 and nlep==1
    cfg2.final_state = MEM.FinalState.LH
    
    cfg3 = ROOT.MEM.MEMConfig()
    cfg3.name = "CASE3"
    cfg3.defaultCfg()
    cfg3.points = 2000
    cfg3.save_permutations = True
    cfg3.vars_to_integrate = CvectorPSVar()
    cfg3.vars_to_marginalize = CvectorPSVar()
    cfg3.transfer_function_method = MEM.TFMethod.External
    cfg3.perm_pruning = pvec
    cfg3.perm_int = 1
    cfg3.do_add_jet = lambda pt, btag: True
    cfg3.do_calculate = lambda njet, nlep: njet>=6 and nlep==1
    cfg3.final_state = MEM.FinalState.LH
    cfg3.int_code = MEM.IntegrandType.Constant + MEM.IntegrandType.Jacobian + MEM.IntegrandType.Transfer + MEM.IntegrandType.DecayAmpl
    confs = [cfg1, cfg2, cfg3]
   
    #Load transfer functions
    import TTH.MEAnalysis.TFClasses as TFClasses
    sys.modules["TFClasses"] = TFClasses
    pi_file = open(os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/transfer_functions.pickle" , 'rb')
    tf_matrix = pickle.load(pi_file)
    pi_file.close()

    #set transfer functions on config objects
    map(configure_transfer_function, confs)

    events = map(json.loads, inlines)
    
    for jsev in events:
        results_d = {}
        results_d["evt"] = jsev["input"]["evt"]
        results_d["run"] = jsev["input"]["run"]
        results_d["lumi"] = jsev["input"]["lumi"]

        for cfg in confs:
            mem = MEM.Integrand(
                MEM.output,
                cfg
            )
            jets_p4 = jsev["input"]["selectedJetsP4"]
            jets_csv = jsev["input"]["selectedJetsCSV"]
            jets_btag = jsev["input"]["selectedJetsBTag"]
    
            njet = 0
            nlep = 0
            for p4, btag in zip(jets_p4, jets_btag):
                if cfg.do_add_jet(p4, btag):
                    add_obj(mem,
                        MEM.ObjectType.Jet,
                        p4s=p4,
                        obsdict={MEM.Observable.BTAG: btag},
                    )
                    njet += 1
            
            leps_p4 = jsev["input"]["selectedLeptonsP4"]
            leps_charge = jsev["input"]["selectedLeptonsCharge"]
            for p4, charge in zip(leps_p4, leps_charge):
                nlep += 1
                add_obj(mem,
                    MEM.ObjectType.Lepton,
                    p4s=p4,
                    obsdict={MEM.Observable.CHARGE: charge},
                )
    
            print "event with {0} jets, {1} leptons".format(njet, len(leps_p4))
    
            add_obj(mem,
                MEM.ObjectType.MET,
                p4s=(jsev["input"]["metP4"][0], 0, jsev["input"]["metP4"][1], 0),
            )
            if cfg.do_calculate(njet, nlep):
                r1 = mem.run(cfg.final_state, MEM.Hypothesis.TTH, cfg.vars_to_integrate, cfg.vars_to_marginalize, cfg.points)
                r2 = mem.run(cfg.final_state, MEM.Hypothesis.TTBB, cfg.vars_to_integrate, cfg.vars_to_marginalize, cfg.points)
               
                for (res, hypo) in [(r1, "tth"), (r2, "ttbb")]:
                    _resd = get_results(res)
                    kpref = "{0}_{1}_".format(cfg.name, hypo)
                    results_d.update({kpref+k: v for (k,v) in _resd.items()})
            mem.next_event()
        outfile.write(json.dumps(results_d) +"\n")
    outfile.close()
