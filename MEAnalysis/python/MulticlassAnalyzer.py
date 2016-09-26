from TTH.MEAnalysis.Analyzer import FilterAnalyzer
import ROOT
import copy
import sys
import numpy as np
import sklearn
import pandas
import pickle
import math
from TTH.MEAnalysis.vhbb_utils import lvec, autolog

import TTH.MEAnalysis.MakeTaggingNtuple as maketuple

import pdb

class MulticlassAnalyzer(FilterAnalyzer):
    """
    MVA based event classification
    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(MulticlassAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf

        self.pickle_filename = self.conf.multiclass["bdtPickleFile"]
        
        # Load the BDT
        pickle_file = open(self.pickle_filename, "r")
        self.model = pickle.load(pickle_file)

    def beginLoop(self, setup):
        super(MulticlassAnalyzer, self).beginLoop(setup)


    def endLoop(self, setup):
        if "multiclass" in self.conf.general["verbosity"]:
            print 'Running endLoop'


    def process(self, event):
        #Process event with variated systematics
        for (syst, event_syst) in event.systResults.items():
            res = self._process(event_syst)
            event.systResults[syst] = res
        return np.any([v.passes_multiclass for v in event.systResults.values()])

    def _process(self, event):
        event.passes_multiclass = True
        setattr( event, 'PassedMulticlassAnalyzer', True )

        if "debug" in self.conf.general["verbosity"]:
            autolog("MulticlassAnalyzer started")

        if "multiclass" in self.conf.general["verbosity"]:
            print 'Printing from MulticlassAnalyzer! iEv = {0}'.format(event.iEv)
                    
        if event.is_sl and event.numJets >= 6 and event.nBCSVM >= 2:
            # Calculate the input variables for the MVA
            var_dic = maketuple.calc_vars(event, "event")
            input_var_names = [                                
                "j0_pt", "j0_eta",  "j0_mass",     "j0_btagCSV",     
                "j1_pt", "j1_eta",  "j1_mass",     "j1_btagCSV",     
                "j2_pt", "j2_eta",  "j2_mass",     "j2_btagCSV",     
                "j3_pt", "j3_eta",  "j3_mass",     "j3_btagCSV",     
                "j4_pt", "j4_eta",  "j4_mass",     "j4_btagCSV",     
                "j5_pt", "j5_eta",  "j5_mass",     "j5_btagCSV",     
            ]        
            input_list = [var_dic[v] for v in input_var_names]
            input_arr = np.array(input_list)
            input_arr = input_arr.reshape(1,-1)

            # Run the MVA
            pred_class = self.model.predict(input_arr)[0]
            pred_probas = self.model.predict_proba(input_arr)

            # And store in event
            event.multiclass_class           = pred_class
            event.multiclass_proba_ttb       = pred_probas[0][0]
            event.multiclass_proba_tt2bAndBb = pred_probas[0][1]                    
            event.multiclass_proba_ttcc      = pred_probas[0][2]
            event.multiclass_proba_ttll      = pred_probas[0][3]
        
        if "multiclass" in self.conf.general["verbosity"]:
            print '[MulticlassAnalyzer] Exiting MulticlassAnalyzer! event.PassedMulticlassAnalyzer = {0}'.format(
                event.PassedMulticlassAnalyzer
            )

        return event 

