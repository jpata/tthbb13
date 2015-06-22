import ROOT
import itertools
from PhysicsTools.HeppyCore.framework.analyzer import Analyzer
import copy
import math
from TTH.MEAnalysis.VHbbTree import *

from TTH.MEAnalysis.WTagAnalyzer import WTagAnalyzer
from TTH.MEAnalysis.GenRadiationModeAnalyzer import GenRadiationModeAnalyzer
from TTH.MEAnalysis.GenTTHAnalyzer import GenTTHAnalyzer
from TTH.MEAnalysis.MEMAnalyzer import MEAnalyzer, MECategoryAnalyzer
from TTH.MEAnalysis.LeptonAnalyzer import LeptonAnalyzer
from TTH.MEAnalysis.JetAnalyzer import JetAnalyzer
from TTH.MEAnalysis.BTagLRAnalyzer import BTagLRAnalyzer
from TTH.MEAnalysis.Analyzer import EventIDFilterAnalyzer, EventWeightAnalyzer, PrimaryVertexAnalyzer
from TTH.MEAnalysis.MVAVarAnalyzer import MVAVarAnalyzer
from TTH.MEAnalysis.TreeVarAnalyzer import TreeVarAnalyzer
