import ROOT

if ROOT.gROOT.GetVersion().startswith("5."):
    ROOT.gSystem.Load("libCintex")
    ROOT.gROOT.ProcessLine('ROOT::Cintex::Cintex::Enable();')
ROOT.gSystem.Load("libTTHMEIntegratorStandalone")
from ROOT import MEM
import inspect

def ROOT_MEMConfig_str(self):
    s = "ROOT.MEM.MEMConfig(\n"
    for k, v in self.__dict__.items():
        s += "  {0}: {1},\n".format(k, v)
    s += ")"
    return s
ROOT.MEM.MEMConfig.__str__ = ROOT_MEMConfig_str
ROOT.MEM.MEMConfig.__repr__ = ROOT_MEMConfig_str

class MEMConfig:
    def __init__(self):
        self.cfg = MEM.MEMConfig()
        self.cfg.defaultCfg()
        self.b_quark_candidates = lambda event: event.selected_btagged_jets_high
        self.l_quark_candidates = lambda event: event.wquark_candidate_jets
        self.lepton_candidates = lambda event: event.good_leptons
        self.met_candidates = lambda event: event.MET
        self.transfer_function_method = MEM.TFMethod.External

        self.do_calculate = lambda event, config: False
        self.mem_assumptions = set([])
        self.enabled = True
        self.maxJets = 4
        self.maxlJets = 5 #DS
        self.btagMethod = "btagCSV"

    def __str__(self):
        s = "MEMConfig(\n"
        for k, v in self.__dict__.items():
            if callable(v):
                v = inspect.getsource(v).strip()
            s += "  {0}: {1},\n".format(k, v)
        s += ")"
        return s
    def __repr__(self):
        return str(self)
    def configure_btag_pdf(self, conf):
        """
        Add the jet b-tag discriminator distributions to the MEM::MEMConfig object.
        The distributions are 3D in (pt, |eta|, CSV).
        """
        #btag_map = CmapDistributionTypeTH1F()

        for x,y in [
            ("b", MEM.DistributionType.csv_b),
            ("c", MEM.DistributionType.csv_c),
            ("l", MEM.DistributionType.csv_l),
        ]:
            self.cfg.add_distribution_global(
                y,
                conf.BTagLRAnalyzer.csv_pdfs[(x, "pt_eta")]
            )

    def configure_transfer_function(self, conf):
        for nb in [0, 1]:
            for fl1, fl2 in [('b', MEM.TFType.bLost), ('l', MEM.TFType.qLost)]:
                tf = conf.tf_matrix[fl1][nb].Make_CDF()
                #set pt cut for efficiency function
                tf.SetParameter(0, conf.jets["pt"])
                tf.SetNpx(10000)
                tf.SetRange(0, 500)
                self.cfg.set_tf_global(fl2, nb, tf)

    def configure_minimize(self, orig_mem):
        self.cfg.do_minimize = 1

    def configure_sudakov(self, orig_mem):
        self.cfg.int_code |= MEM.IntegrandType.Sudakov
        njets = 6
        if "dl" in orig_mem.mem_assumptions:
            njets = 4
        if "1qW" in orig_mem.mem_assumptions:
            njets -= 1
        self.do_calculate = lambda event, conf, njets=njets: (
            orig_mem.do_calculate(event, conf) and
            len(event.good_jets) == njets
        )

    def configure_newtf(self, orig_mem):
        self.cfg.transfer_function_method = MEM.TFMethod.External

    def configure_recoil(self, orig_mem):
        self.cfg.int_code |= MEM.IntegrandType.Recoil
