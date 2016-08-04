import ROOT, math
import copy

def lvec(self):
    """
    Converts an object with pt, eta, phi, mass to a TLorentzVector
    """
    lv = ROOT.TLorentzVector()
#    if self.pt < 0 or abs(self.eta) > 6:
#        raise Exception("Invalid values for TLorentzVector")
    lv.SetPtEtaPhiM(self.pt, self.eta, self.phi, self.mass)
#    if abs(lv.Pt()) > 100000 or abs(lv.Eta()) > 100000:
#        raise Exception("Invalid values for TLorentzVector")
    return lv

class MET:
    def __init__(self, **kwargs):
        self.p4 = ROOT.TLorentzVector()

        _px, _py = kwargs.get("px", None), kwargs.get("py", None)
        _pt, _phi = kwargs.get("pt", None), kwargs.get("phi", None)
        tree = kwargs.get("tree", None)
        metobj = kwargs.get("metobj", None)

        self.sumEt = 0
        self.genPt = 0
        self.genPhi = 0

        if not (_px is None or _py is None):
            self.p4.SetPxPyPzE(_px, _py, 0, math.sqrt(_px*_px + _py*_py))
            self.pt = self.p4.Pt()
            self.phi = self.p4.Phi()
            self.px = self.p4.Px()
            self.py = self.p4.Py()
        elif not (_pt is None or _phi is None):
            self.p4.SetPtEtaPhiM(_pt, 0, _phi, 0)
            self.pt = self.p4.Pt()
            self.phi = self.p4.Phi()
            self.px = self.p4.Px()
            self.py = self.p4.Py()
        elif metobj != None:
            for x in ["pt", "eta", "phi", "mass", "sumEt", "genPt", "genPhi"]:
                setattr(self, x, getattr(metobj, x, None))
            self.p4.SetPtEtaPhiM(self.pt, 0, self.phi, 0)
            self.px = self.p4.Px()
            self.py = self.p4.Py()


    @staticmethod
    def make_array(event):
        return [MET(tree=event.input)]

class FakeEvent:
    def __init__(self, event):
        src = copy.deepcopy(event.__dict__)
        self.__dict__.update(src)
        self.input = event.input

from TTH.MEAnalysis.VHbbTree import Jet

jet_keys = ["pt", "eta", "phi", "m", "btagCSV", "chMult", "nhMult"]

def printJet(j):
    s = ""
    for k, v in sorted(j.__dict__.items(), key=lambda x: x[0]):
        if k in jet_keys:
            try:
                v = float(v)
                s += "{0}={1:2.2f} ".format(k, v)
            except TypeError as e:
                pass
    return s
def printJetShort(j):
    s = "<Jet(pt={0:.2f})>".format(j.pt)
    return s

class TreeCache(object):
    """
    This caches a usual PyROOT TTree object such that tree.x does not result
    in an expensive GetEntry operation each time.
    """
    def __init__(self, tree):
        self.tree = tree
        self.branch_cache = {}
        self.branch_cache_values = {}
        self.current_entry = 0

    def __getattr__(self, attr):
        """
        Fetches the branch from the TTree and caches it for future usage.
        attr (string): name of branch or if not existing, TreeCache attribute
        returns: value of branch
        """
        branch_cache = self.__dict__["branch_cache"]
        branch_cache_values = self.__dict__["branch_cache_values"]
        tree = self.__dict__["tree"]

        if not branch_cache.has_key(attr):
            br = tree.GetBranch(attr)
            if not br:
                return object.__getattribute__(self, attr)
            branch_cache[attr] = br
        branch = branch_cache[attr]

        if not branch_cache_values.has_key(branch):
            branch.GetEntry(self.__dict__["current_entry"])
            branch_cache_values[branch] = getattr(tree, attr)
        return branch_cache_values[branch]

    def next_entry(self, ientry):
        self.current_entry = ientry
        self.branch_cache_values = {}

from PhysicsTools.HeppyCore.framework.analyzer import Analyzer
class EventAnalyzer(Analyzer):
    
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(EventAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.cache = None
        self.process_event = cfg_ana.process_event
    def process(self, event):
        if not self.cache:
            self.cache = TreeCache(event.input)
        self.cache.next_entry(event.iEv)
        self.process_event(event, self.cache)

Jet.__str__ = printJet
Jet.__repr__ = printJetShort

def autolog(*args):
    import inspect, logging
    # Get the previous frame in the stack, otherwise it would
    # be this function!!!
    func = inspect.currentframe().f_back.f_code
    message = ", ".join(map(str, args))
    filename_last = func.co_filename.split("/")[-1]
    # Dump the message + the name of this function to the log.
    print "[%s %s:%i]: %s" % (
        func.co_name,
        filename_last,
        func.co_firstlineno,
        message
    )
