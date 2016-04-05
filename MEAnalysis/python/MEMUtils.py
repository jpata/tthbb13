import ROOT

if ROOT.gROOT.GetVersion().startswith("5."):
    ROOT.gSystem.Load("libCintex")
    ROOT.gROOT.ProcessLine('ROOT::Cintex::Cintex::Enable();')
ROOT.gSystem.Load("libTTHMEIntegratorStandalone")
from ROOT import MEM

def set_integration_vars(vars_to_integrate, vars_to_marginalize, mem_assumptions):
    if "1qW" in mem_assumptions:
        vars_to_integrate.push_back(MEM.PSVar.cos_qbar1)
        vars_to_integrate.push_back(MEM.PSVar.phi_qbar1)
    if "0qW" in mem_assumptions:
        vars_to_integrate.push_back(MEM.PSVar.cos_q1)
        vars_to_integrate.push_back(MEM.PSVar.phi_q1)
        vars_to_integrate.push_back(MEM.PSVar.cos_qbar1)
        vars_to_integrate.push_back(MEM.PSVar.phi_qbar1)
    if "1bT" in mem_assumptions:
        vars_to_integrate.push_back(MEM.PSVar.cos_b1)
        vars_to_integrate.push_back(MEM.PSVar.phi_b1)
    if "1bTbar" in mem_assumptions:
        vars_to_integrate.push_back(MEM.PSVar.cos_b2)
        vars_to_integrate.push_back(MEM.PSVar.phi_b2)
    if "1bH" in mem_assumptions:
        vars_to_integrate.push_back(MEM.PSVar.cos_bbar)
        vars_to_integrate.push_back(MEM.PSVar.phi_bbar)

    if "1w2h2t" in mem_assumptions:
        vars_to_marginalize.push_back(MEM.PSVar.cos_qbar1)
        vars_to_marginalize.push_back(MEM.PSVar.phi_qbar1)

    if "2w2h1t_h" in mem_assumptions:
        vars_to_marginalize.push_back(MEM.PSVar.cos_b1)
        vars_to_marginalize.push_back(MEM.PSVar.phi_b1)

    if "2w2h1t_l" in mem_assumptions:
        vars_to_marginalize.push_back(MEM.PSVar.cos_b2)
        vars_to_marginalize.push_back(MEM.PSVar.phi_b2)

    # if "0w2h2t" in mem_assumptions:
    #     vars_to_marginalize.push_back(MEM.PSVar.cos_q1)
    #     vars_to_marginalize.push_back(MEM.PSVar.phi_q1)
    #     vars_to_marginalize.push_back(MEM.PSVar.cos_qbar1)
    #     vars_to_marginalize.push_back(MEM.PSVar.phi_qbar1)

    if "1w2h1t_h" in mem_assumptions:
        vars_to_marginalize.push_back(MEM.PSVar.cos_qbar1)
        vars_to_marginalize.push_back(MEM.PSVar.phi_qbar1)
        vars_to_marginalize.push_back(MEM.PSVar.cos_b1)
        vars_to_marginalize.push_back(MEM.PSVar.phi_b1)

    if "1w2h1t_l" in mem_assumptions:
        vars_to_marginalize.push_back(MEM.PSVar.cos_qbar1)
        vars_to_marginalize.push_back(MEM.PSVar.phi_qbar1)
        vars_to_marginalize.push_back(MEM.PSVar.cos_b2)
        vars_to_marginalize.push_back(MEM.PSVar.phi_b2)

    if "3w2h2t" in mem_assumptions:  #DS
        vars_to_marginalize.push_back(MEM.PSVar.cos_qbar1)
        vars_to_marginalize.push_back(MEM.PSVar.phi_qbar1)

    if "4w2h1t" in mem_assumptions:  #DS
        vars_to_marginalize.push_back(MEM.PSVar.cos_b1)
        vars_to_marginalize.push_back(MEM.PSVar.phi_b1)

    if "0w2h2t" in mem_assumptions:  #DS
        vars_to_marginalize.push_back(MEM.PSVar.cos_q1)
        vars_to_marginalize.push_back(MEM.PSVar.phi_q1)
        vars_to_marginalize.push_back(MEM.PSVar.cos_qbar1)
        vars_to_marginalize.push_back(MEM.PSVar.phi_qbar1) #overwrite SL case above
        vars_to_marginalize.push_back(MEM.PSVar.cos_q2)
        vars_to_marginalize.push_back(MEM.PSVar.phi_q2)
        vars_to_marginalize.push_back(MEM.PSVar.cos_qbar2)
        vars_to_marginalize.push_back(MEM.PSVar.phi_qbar2)
        
    if "0w2h1t" in mem_assumptions:  #DS
        vars_to_marginalize.push_back(MEM.PSVar.cos_q1)
        vars_to_marginalize.push_back(MEM.PSVar.phi_q1)
        vars_to_marginalize.push_back(MEM.PSVar.cos_qbar1)
        vars_to_marginalize.push_back(MEM.PSVar.phi_qbar1)
        vars_to_marginalize.push_back(MEM.PSVar.cos_q2)
        vars_to_marginalize.push_back(MEM.PSVar.phi_q2)
        vars_to_marginalize.push_back(MEM.PSVar.cos_qbar2)
        vars_to_marginalize.push_back(MEM.PSVar.phi_qbar2)
        vars_to_marginalize.push_back(MEM.PSVar.cos_b1)
        vars_to_marginalize.push_back(MEM.PSVar.phi_b1)

    if "0w1h2t" in mem_assumptions:  #DS
        vars_to_marginalize.push_back(MEM.PSVar.cos_q1)
        vars_to_marginalize.push_back(MEM.PSVar.phi_q1)
        vars_to_marginalize.push_back(MEM.PSVar.cos_qbar1)
        vars_to_marginalize.push_back(MEM.PSVar.phi_qbar1)
        vars_to_marginalize.push_back(MEM.PSVar.cos_q2)
        vars_to_marginalize.push_back(MEM.PSVar.phi_q2)
        vars_to_marginalize.push_back(MEM.PSVar.cos_qbar2)
        vars_to_marginalize.push_back(MEM.PSVar.phi_qbar2)
        vars_to_marginalize.push_back(MEM.PSVar.cos_bbar)
        vars_to_marginalize.push_back(MEM.PSVar.phi_bbar)


def add_obj(integrator, objtype, **kwargs):
    """
    Add an event object (jet, lepton, MET) to the ME integrator.

    objtype: specifies the object type
    kwargs: p4s: spherical 4-momentum (pt, eta, phi, M) as a tuple
            obsdict: dict of additional observables to pass to MEM
            tf_dict: Dictionary of MEM.TFType->TF1 of transfer functions
    """
    if kwargs.has_key("p4s"):
        pt, eta, phi, mass = kwargs.pop("p4s")
        v = ROOT.TLorentzVector()
        v.SetPtEtaPhiM(pt, eta, phi, mass);
    elif kwargs.has_key("p4c"):
        v = ROOT.TLorentzVector(*kwargs.pop("p4c"))
    obs_dict = kwargs.pop("obs_dict", {})
    tf_dict = kwargs.pop("tf_dict", {})

    o = MEM.Object(v, objtype)

    #Add observables from observable dictionary
    for k, v in obs_dict.items():
        o.addObs(k, v)
    for k, v in tf_dict.items():
        o.addTransferFunction(k, v)
    integrator.push_back_object(o)
