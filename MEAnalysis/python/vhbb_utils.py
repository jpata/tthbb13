import ROOT, math

def lvec(self):
    """
    Converts an object with pt, eta, phi, mass to a TLorentzVector
    """
    lv = ROOT.TLorentzVector()
    lv.SetPtEtaPhiM(self.pt, self.eta, self.phi, self.mass)
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
        self.__dict__.update(event.__dict__)
