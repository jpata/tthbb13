from TTH.MEAnalysis.Analyzer import FilterAnalyzer
import ROOT
import copy
import sys
import numpy as np

class Jet_container:
    def __init__(self, pt, eta, phi, mass):
        self.pt = pt
        self.eta = eta
        self.phi = phi
        self.mass = mass


class SubjetAnalyzer(FilterAnalyzer):
    """
    Subjet analyzer by Thomas
    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(SubjetAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf

        self.R_cut = 0.3

        self.R_cut_fatjets = 1.0

        self.top_mass = 172.04

        self.btagAlgo = self.conf.jets["btagAlgo"]

        self.Cut_criteria = [
            ( 'pt'  , '>', '200.0' ),
            ( 'mass', '>', '120.0' ),
            ( 'mass', '<', '180.0' ),
            ( 'fRec'  , '<', '0.45' ),
            ]

        self.n_subjettiness_cut = 0.97

        self.bbtag_cut = 0.1


    def beginLoop(self, setup):
        super(SubjetAnalyzer, self).beginLoop(setup)


    def endLoop(self, setup):
        if "subjet" in self.conf.general["verbosity"]:
            print 'Running endLoop'


    def process(self, event):
        for (syst, event_syst) in event.systResults.items():
            if event_syst.passes_btag:
                res = self._process(event_syst)
                event.systResults[syst] = res
            else:
                event.systResults[syst].passes_subjet = False
        return np.any([v.passes_subjet for v in event.systResults.values()])

    def _process(self, event):
        event.passes_subjet = True

        if "subjet" in self.conf.general["verbosity"]:
            print 'Printing from SubjetAnalyzer! iEv = {0}'.format(event.iEv)

        # Is set to True only after the event passed all criteria
        setattr( event, 'PassedSubjetAnalyzer', False )

        # Create two new lists for selected_btagged_jets and wquark_candidate_jets
        # Needs to be done here because the lists are needed in the mem config
        setattr( event, 'boosted_bjets', [] )
        setattr( event, 'boosted_ljets', [] )
        setattr( event, 'topCandidate', [] )
        setattr( event, 'othertopCandidate', [] )
        setattr( event, 'higgsCandidate', [] )

        event.n_bjets = len( event.selected_btagged_jets_high )
        event.n_ljets = len( list( event.wquark_candidate_jets ) )

        ########################################
        # Minimal event suitability:
        #  - Needs to be single leptonic
        #  - At least 1 httCandidate
        ########################################

        # Check if the event is single leptonic
        if not event.is_sl:
            return event

        # Get the top candidates
        # ======================================

        # Keep track of number of httCandidates that passed the cut
        setattr( event, 'nhttCandidate', len( event.httCandidate ) )
        setattr( event, 'nhttCandidate_aftercuts', 0 )

        # Just run normal mem if there is no httCandidate present
        # Check if there is an httCandidate
        if len( event.httCandidate ) == 0:
            return event

        # Apply the cuts on the httCandidate
        tops = []
        for candidate in event.httCandidate:
            if self.Apply_Cut_criteria( candidate ):
                tops.append( copy.deepcopy(candidate) )

        # Match the top to a fat jet
        #  - Copies bbtag and tau_N, calculates n_subjettiness
        #  - Applies the n_subjettiness cut
        #  - Calculates delR with the single lepton
        tops = self.Match_top_to_fatjet( event, tops )
        other_tops = []

        # Calculate delR with the lepton for all tops that survived the cut
        for top in tops:
            setattr( top, 'delR_lepton' ,
                self.Get_DeltaR_two_objects( top, event.good_leptons[0] ) )

        # Keep track of how many httCandidates passed
        event.nhttCandidate_aftercuts = len( tops )

        # Just run normal mem if there is no httCandidate surviving the cuts
        # Check if any candidates survived the cutoff criteria
        if len(tops) == 0:
            return event
        # If exactly 1 survived, simply continue with that candidate
        elif len(tops) == 1:
            top = tops[0]
            other_top_present = False
        # If more than 1 candidate survived the cutoff criteria, choose the
        # one whose delR with the lepton was biggest
        else:
            tops = sorted( tops, key=lambda x: -x.delR_lepton )
            other_top_present = True
            top = tops[0]
            other_tops = tops[1:]

        # Get a Higgs candidate
        # ======================================

        higgs_present = False

        higgsCandidates = []
        for fatjet in event.FatjetCA15ungroomed:

            # Check if bbtag is not too low
            #if fatjet.bbtag < self.bbtag_cut:
            #    continue

            # Check if the fatjet is not already matched to the chosen top
            if hasattr(fatjet, 'matched_top') and fatjet == top.matched_fatjet:
                continue

            fatjet.n_subjettiness = fatjet.tau2 / fatjet.tau1

            higgsCandidates.append( fatjet )
            higgs_present = True

        # Sort by decreasing bbtag
        higgsCandidates = sorted( higgsCandidates, key=lambda x: -x.bbtag )


        ########################################
        # Get the lists of particles: quarks, jets and subjets
        ########################################

        # Get the subjets from the httCandidate
        #  - Also sets transfer functions as attributes
        #  - Returns subjets ordered by decreasing btag
        #  - First subjet has btagFlag==1.0, the other two btagFlag==0.0
        top_subjets = self.Get_Subjets( top )
        if "subjet" in self.conf.general["verbosity"]:
            print "subjets"
            for subjet in top_subjets:
                print subjet

        if other_top_present:
            for top in other_tops: self.Get_Subjets( top )

        # Set 'PDGID' to 1 for light, and to 5 for b
        for subjet in top_subjets:
            if subjet.btagFlag == 1.0: setattr( subjet, 'PDGID', 5 )
            if subjet.btagFlag == 0.0: setattr( subjet, 'PDGID', 1 )

        # Create two new lists for btagged_jets and wquark_candidate_jets in the
        # original events
        reco_btagged_jets = copy.deepcopy( event.selected_btagged_jets_high )
        reco_ltagged_jets = copy.deepcopy( list( event.wquark_candidate_jets ) )

        for jet in reco_btagged_jets:
            setattr( jet, 'btag', getattr(jet,self.btagAlgo) )
            setattr( jet, 'btagFlag', 1.0 )
            setattr( jet, 'PDGID', 0 )

        for jet in reco_ltagged_jets:
            setattr( jet, 'btag', getattr(jet,self.btagAlgo) )
            setattr( jet, 'btagFlag', 0.0 )
            setattr( jet, 'PDGID', 0 )


        ########################################
        # Matching
        ########################################

        # Whenever a subjet has a 'match' (dR < dR_cut), the matched object should
        # excluded from the event

        # Match subjet to a bjet
        n_excluded_bjets = self.Match_two_lists(
            top_subjets, 'top_subjet',
            reco_btagged_jets, 'bjet' )

        # Match subjet to a ljet
        n_excluded_ljets = self.Match_two_lists(
            top_subjets , 'top_subjet',
            reco_ltagged_jets, 'ljet' )
        if "subjet" in self.conf.general["verbosity"]:
            print "subjet nMatchB={0} nMatchL={1}".format(n_excluded_bjets, n_excluded_ljets)


        # In case of double matching, choose the match with lowest delR
        # (This is not expected to happen often)
        for subjet in top_subjets:
            if hasattr( subjet, 'matched_bjet' ) and \
                hasattr( subjet, 'matched_ljet' ) :
                print 'Double match detected'
                if subjet.matched_bjet_delR < subjet.matched_ljet_delR:
                    del subjet.matched_ljet
                    del subjet.matched_ljet_delR
                    n_excluded_bjets -= 1
                else:
                    del subjet.matched_bjet
                    del subjet.matched_bjet_delR
                    n_excluded_ljets -= 1


        ########################################
        # Modifying the bjets and ljets lists
        ########################################

        boosted_bjets = []
        boosted_ljets = []

        if n_excluded_bjets <= 1:
            if "subjet" in self.conf.general["verbosity"]:
                print "subjet replacing"
            # Add the subjets to the final output lists first
            for subjet in top_subjets:
                if subjet.btagFlag == 1.0: boosted_bjets.append( subjet )
                if subjet.btagFlag == 0.0: boosted_ljets.append( subjet )

            # Sort tl btagged jets by decreasing btag (to be sure, but should 
            # already be done in previous analyzer)
            reco_btagged_jets = sorted( reco_btagged_jets, key=lambda x: -x.btag )

            # Add up to 4 reco btagged jets to the output lists
            for bjet in reco_btagged_jets:
                # Check if the b-jet is not excluded
                if not hasattr( bjet, 'matched_top_subjet' ):
                    boosted_bjets.append( bjet )

                # Stop adding after 4 b-jets
                if len(boosted_bjets) == 4: break
            event.PassedSubjetAnalyzer = True

        # If too many events are excluded, just run the default hypothesis
        else:
            if "subjet" in self.conf.general["verbosity"]:
                print "subjet has too many overlaps, using reco"
            boosted_bjets = reco_btagged_jets
            boosted_ljets = reco_ltagged_jets
            event.PassedSubjetAnalyzer = False



        ########################################
        # Write to event
        ########################################

        # Store output lists in event
        event.topCandidate = [ top ]
        event.othertopCandidate = other_tops
        event.higgsCandidate = higgsCandidates
        event.boosted_bjets = boosted_bjets
        event.boosted_ljets = boosted_ljets

        # Also declared at beginning of analyzer, but overwrite just in case
        event.n_bjets = len( reco_btagged_jets )
        event.n_ljets = len( reco_ltagged_jets )

        event.n_boosted_bjets = len( boosted_bjets )
        event.n_boosted_ljets = len( boosted_ljets )

        event.n_excluded_bjets = n_excluded_bjets
        event.n_excluded_ljets = n_excluded_ljets

        if "subjet" in self.conf.general["verbosity"]:
            print 'Exiting SubjetAnalyzer! event.PassedSubjetAnalyzer = {0}'.format(
                event.PassedSubjetAnalyzer
            )
        return event


        ########################################
        # Printing particle lists
        ########################################

        """
        print '\n====================================='
        print 'tops (first one = chosen):'
        self.Print_objs( tops, extra_attrs=['bbtag'] )
        print 'higgsCandidates:'
        self.Print_objs( higgsCandidates, extra_attrs=['bbtag'] )
        print '====================================='
        print 'reco_btagged_jets:'
        self.Print_objs( reco_btagged_jets, ['btag'] )
        print 'reco_ltagged_jets:'
        self.Print_objs( reco_ltagged_jets, ['btag'] )
        print '====================================='
        print 'top_subjets:'
        for subjet in top_subjets:
            self.Print_objs( subjet, ['btag'] )
            if hasattr( subjet, 'matched_bjet'):
                print '        Matched with bjet, delR = {0}'.format(
                    subjet.matched_bjet_delR )
                self.Print_objs( subjet.matched_bjet, ['btag'], tab=True )
            if hasattr( subjet, 'matched_ljet'):
                print '        Matched with ljet, delR = {0}'.format(
                    subjet.matched_ljet_delR )
                self.Print_objs( subjet.matched_ljet, ['btag'], tab=True )
        print '====================================='
        print 'boosted_bjets:'
        self.Print_objs( boosted_bjets, ['btag'] )
        print 'boosted_ljets:'
        self.Print_objs( boosted_ljets, ['btag'] )
        print '====================================='
        """

        ########################################
        # Quark Matching
        ########################################

        # This section is only useful for truth-level comparison, and can be turned
        # off if this is not needed.
        # Do_Quark_Matching( event ) sets number of matches with quarks as branches
        # in the event, but these branches do not have to be filled (they will be
        # automatically set to -1 in the final output root file).

        self.Do_Quark_Matching( event )


    ########################################
    # Functions
    ########################################

    # ==============================================================================
    # Applies the cut criteria - returns True (survived) or False (did not survive)
    def Apply_Cut_criteria( self, candidate ):
        for ( attr, operator, cut_off ) in self.Cut_criteria:
            if not eval( '{0}{1}{2}'.format(
                getattr( candidate, attr ),
                operator,
                cut_off ) ):
                return False
        return True

    # ==============================================================================
    # Additional httCandidate cut: n-subjetiness
    # Takes a list of tops, returns a (reduced) list of tops with an n_subjettiness
    def Match_top_to_fatjet( self, event, tops ):

        # Loosely match the fatjets to the tops
        n_matched_httcand_fatjet = self.Match_two_lists(
            tops, 'top',
            event.FatjetCA15ungroomed, 'fatjet',
            R_cut = self.R_cut_fatjets )

        # New list of tops after n_subjettiness cut is applied
        tops_after_nsub_cut = []

        for top in tops:

            # Skip unmatched tops
            if not hasattr( top, 'matched_fatjet' ):
                print 'Warning: httCandidate unmatchable to fatjet!'
                continue

            fatjet = top.matched_fatjet

            # Get n_subjettiness from the matched fatjet
            n_subjettiness = fatjet.tau3 / fatjet.tau2

            # Try next top if n_subjettiness exceeds the cut
            if n_subjettiness > self.n_subjettiness_cut: continue

            # Set n_subjettiness, tau_N and the bbtag
            setattr( top , 'n_subjettiness', n_subjettiness )
            setattr( top , 'tau1', fatjet.tau1 )
            setattr( top , 'tau2', fatjet.tau2 )
            setattr( top , 'tau3', fatjet.tau3 )
            setattr( top , 'bbtag', fatjet.bbtag )

            # Calculate delRopt
            setattr( top, 'delRopt', top.Ropt - top.RoptCalc )

            # Append the httCandidate class to the list
            tops_after_nsub_cut.append( top )

        return tops_after_nsub_cut

    # ==============================================================================
    def Get_Subjets( self, top ):

        top_subjets = []
        for prefix in [ 'sjW1', 'sjW2', 'sjNonW' ]:
            x = Jet_container(
                getattr( top, prefix + 'pt' ),
                getattr( top, prefix + 'eta' ),
                getattr( top, prefix + 'phi' ),
                getattr( top, prefix + 'mass' ) )
            setattr( x, 'prefix', prefix )
            setattr( x, 'btag'  , getattr( top, prefix + 'btag' ) )

            top_subjets.append( x )

        # Set the btagFlags; order by decreasing btag, highest btag gets btagFlag=1.0
        top_subjets = sorted( top_subjets, key = lambda x: -x.btag )
        setattr( top_subjets[0], 'btagFlag', 1.0 )
        setattr( top_subjets[1], 'btagFlag', 0.0 )
        setattr( top_subjets[2], 'btagFlag', 0.0 )

        # Adding subjet transfer functions
        for subjet in top_subjets:
            jet_eta_bin = 0
            if abs(subjet.eta)>1.0:
                jet_eta_bin = 1

            # If True, TF [0] - reco, x - gen
            # If False, TF [0] - gen, x - reco
            eval_gen = False
            setattr( subjet, 'tf_b' ,
                self.conf.tf_sj_matrix['b'][jet_eta_bin].Make_Formula(eval_gen) )
            setattr( subjet, 'tf_l' ,
                self.conf.tf_sj_matrix['l'][jet_eta_bin].Make_Formula(eval_gen) )
            setattr( subjet, 'tf_b_lost' ,
                self.conf.tf_sj_matrix['b'][jet_eta_bin].Make_CDF() )
            setattr( subjet, 'tf_l_lost' ,
                self.conf.tf_sj_matrix['l'][jet_eta_bin].Make_CDF() )

            # Set jet pt threshold for CDF
            subjet.tf_b_lost.SetParameter(0, self.conf.jets["pt"])
            subjet.tf_l_lost.SetParameter(0, self.conf.jets["pt"])

        # Create a pointer in the top to its subjets
        setattr( top, 'subjets', top_subjets )

        return top_subjets

    # ==============================================================================
    # Calculates angular distance between two objects (needs eta and phi as attr.)
    def Get_DeltaR_two_objects( self, obj1, obj2 ):

        for obj in [ obj1, obj2 ]:
            if not ( hasattr( obj, 'phi' ) or hasattr( obj, 'eta' ) ):
                print "Can't calculate Delta R: objects don't have right attributes"
                return 0

        pi = 3.1415926535897932

        del_phi = abs( obj1.phi - obj2.phi )
        if del_phi > pi: del_phi = 2*pi - del_phi

        delR = pow( pow(obj1.eta-obj2.eta,2) + pow(del_phi,2) , 0.5 )

        return delR

    # ==============================================================================
    # Simple algorithm that matches the smallest delta R for two lists of objects
    def Get_min_delR( self, objs1, objs2, R_cut = 'def' ):

        # Use self.R_cut if R_cut is not specified
        if R_cut == 'def':
            R_cut = self.R_cut

        n_objs1 = len(objs1)
        n_objs2 = len(objs2)

        Rmat = [[ self.Get_DeltaR_two_objects(objs1[i], objs2[j]) \
            for j in range(n_objs2)] for i in range(n_objs1) ]

        Rmin = 9999.0
        
        for i in range(n_objs1):
            for j in range(n_objs2):
                if Rmat[i][j] < Rmin and Rmat[i][j] < R_cut:
                    Rmin = Rmat[i][j]
                    i_min = i
                    j_min = j

        if Rmin == 9999.0: return ( 'No link', 0, 0)

        return (i_min, j_min, Rmin)

    # ==============================================================================
    def Match_two_lists( self,
                         objs1_orig, label1,
                         objs2_orig, label2,
                         R_cut = 'def' ):

        # Check if object is not a list; if so, convert it to a list
        # (This allows to conveniently pass single objects to the function as well)
        if hasattr( objs1_orig, 'eta' ) and hasattr( objs1_orig, 'phi' ):
            objs1_orig = [ objs1_orig ]
        if hasattr( objs2_orig, 'eta' ) and hasattr( objs2_orig, 'phi' ):
            objs2_orig = [ objs2_orig ]
    
        # Create copies of the list, since entries will be popped
        objs1 = copy.deepcopy( objs1_orig )
        objs2 = copy.deepcopy( objs2_orig )

        # Save the original objecs as attributes of the workable objects
        for ( obj1, obj1_orig ) in zip( objs1, objs1_orig ):
            setattr( obj1, 'orig_obj', obj1_orig )
        for ( obj2, obj2_orig ) in zip( objs2, objs2_orig ):
            setattr( obj2, 'orig_obj', obj2_orig )

        # Attempt matching until the shortest list is depleted, or until there are
        # no more matches with delR < delR_cut
        n_matches = min( len(objs1), len(objs2) )

        for i_match in range(n_matches):

            # Attempt a match
            (i1, i2, delR) = self.Get_min_delR( objs1, objs2, R_cut )

            # Return the attempt number if no more matches could be made
            if i1 == 'No link':
                return i_match

            # Pop the matched objs from the lists for the next iteration
            matched_obj1 = objs1.pop(i1)
            matched_obj2 = objs2.pop(i2)

            # Record the match in the original objs
            setattr( matched_obj1.orig_obj,
                     'matched_{0}'.format( label2 ),
                     matched_obj2.orig_obj )
            setattr( matched_obj2.orig_obj,
                     'matched_{0}'.format( label1 ),
                     matched_obj1.orig_obj )

            # Record the delR value in the original objs
            setattr( matched_obj1.orig_obj,
                     'matched_{0}_delR'.format( label2 ),
                     delR )
            setattr( matched_obj2.orig_obj,
                     'matched_{0}_delR'.format( label1 ),
                     delR )

        return n_matches

    # ==============================================================================
    # Print exactly 1 particle

    def Print_one_obj( self, q, extra_attrs=[], tab=False ):

        pt = '{0:.2f}'.format(q.pt)
        eta = '{0:.2f}'.format(q.eta)
        phi = '{0:.2f}'.format(q.phi)
        mass = '{0:.2f}'.format(q.mass)

        p4_str = '    [ pt: {0:6s} | eta: {1:5s} | phi: {2:5s} | mass: {3:6s} '.format( pt, eta, phi, mass )
    
        for a in extra_attrs:
            if hasattr( q, a ):
                value = getattr(q,a)
                if isinstance( value, float ): value = '{0:.2f}'.format(value)
                p4_str += '| {0}: {1} '.format( a, value )

        p4_str += ']'

        if tab: p4_str = '    ' + p4_str
        print p4_str

    # ==============================================================================
    # Print object or list of objects
    def Print_objs( self, objs, extra_attrs=[], tab=False ):

        # Check if only 1 object was passed; if so, convert to list
        if ( hasattr( objs, 'pt' ) and hasattr( objs, 'eta' ) and
             hasattr( objs, 'phi' ) and hasattr( objs, 'mass' ) ):
            objs = [ objs ]
        
        for obj in objs: self.Print_one_obj( obj, extra_attrs, tab )

    # ==============================================================================
    # Deletes duplicate WZ Quarks
    def CompareWZQuarks(self, event ):

        if len(event.GenWZQuark) < 4:
            return 0

        quarks = event.GenWZQuark

        Is_Duplicate = ( quarks[-1].pt==quarks[1].pt and \
            quarks[-2].pt==quarks[0].pt )

        if Is_Duplicate:
            event.GenWZQuark = event.GenWZQuark[0:-2]

        return 0

    # ==============================================================================
    # Tag one of the bquarks as hadronic, based on mass difference with top
    def Tag_GenB_as_hadronic(self, event ):

        # Make list of TLorentzVector objects for the 2 light quarks
        tl_GenWZQuarks = []
        for l in event.GenWZQuark:
            tl_l = ROOT.TLorentzVector()
            tl_l.SetPtEtaPhiM( l.pt, l.eta, l.phi, l.mass )
            tl_GenWZQuarks.append( tl_l )

        tl_Combined = []
        for (b_i, b) in enumerate(event.GenBQuarkFromTop):
            tl_b = ROOT.TLorentzVector()
            tl_b.SetPtEtaPhiM( b.pt, b.eta, b.phi, b.mass )
            tl_Combined.append( tl_b + tl_GenWZQuarks[0] + tl_GenWZQuarks[1] )

        # Calculate mass difference from top mass
        delmass0 = abs(tl_Combined[0].M() - self.top_mass)
        delmass1 = abs(tl_Combined[1].M() - self.top_mass)

        # Make sure the B quark with lowest del mass to top mass is at index 0
        if delmass0 < delmass1:
            setattr( event.GenBQuarkFromTop[0], 'is_hadr', 1 )
            setattr( event.GenBQuarkFromTop[1], 'is_hadr', 0 )
        else:
            setattr( event.GenBQuarkFromTop[1], 'is_hadr', 1 )
            setattr( event.GenBQuarkFromTop[0], 'is_hadr', 0 )

        event.GenBQuarkFromTop = sorted( event.GenBQuarkFromTop,
                                         key=lambda x: -x.is_hadr )

    # ==============================================================================
    # Writes matching statistics to event for matching (sub)jets to quarks
    def Do_Quark_Matching( self, event ):

        # Necessary to remove duplicates in GenWZQuark branch
        # This step can be removed for V12 samples <---- Check dit
        self.CompareWZQuarks( event )

        # Check if event contains the right number of quarks
        # (Only used to do truth-level comparisons)
        genquarks_top_present = False
        if len(event.GenWZQuark)==2 and len(event.GenBQuarkFromTop)==2:
            genquarks_top_present = True
        genquarks_higgs_present = False
        if len(event.GenBQuarkFromH)==2:
            genquarks_higgs_present = True

        # Convenient list names
        if genquarks_top_present:
            # Sorts event.GenBQuarkFromTop
            self.Tag_GenB_as_hadronic(event)
            # Get the hadronic & leptonic b-quark and the two light quarks
            hadr_bquark = event.GenBQuarkFromTop[0]
            lept_bquark = event.GenBQuarkFromTop[1]
            lquarks = event.GenWZQuark
        if genquarks_higgs_present:
            higgs_bquarks = event.GenBQuarkFromH

        reco_btagged_jets = event.selected_btagged_jets_high
        reco_ltagged_jets = list( event.wquark_candidate_jets )

        top = event.topCandidate[0]
        other_tops = event.othertopCandidate


        # Quark matching
        # ==============

        # Quark matching is only done to compare events to truth level.
        # Events are not selected based on successful quark matching.
        # This entire part can be commented out if so desired.

        # Matching GenBQuarkFromTop and GenWZQuark
        if genquarks_top_present:

            # To reco_btagged_jets
            n_hadr_bquark_matched_to_bjet = self.Match_two_lists(
                hadr_bquark, 'hadr_bquark',
                reco_btagged_jets, 'bjet' )

            n_lept_bquark_matched_to_bjet = self.Match_two_lists(
                lept_bquark, 'lept_bquark',
                reco_btagged_jets, 'bjet' )

            n_lquarks_matched_to_bjet = self.Match_two_lists(
                lquarks, 'lquark',
                reco_btagged_jets, 'bjet' )

            # To reco_ltagged_jets
            n_hadr_bquark_matched_to_ljet = self.Match_two_lists(
                hadr_bquark, 'hadr_bquark',
                reco_ltagged_jets, 'ljet' )

            n_lept_bquark_matched_to_ljet = self.Match_two_lists(
                lept_bquark, 'lept_bquark',
                reco_ltagged_jets, 'ljet' )

            n_lquarks_matched_to_ljet = self.Match_two_lists(
                lquarks, 'lquark',
                reco_ltagged_jets, 'ljet' )

            # To subjets from chosen top
            n_hadr_bquark_matched_to_top_subjet = self.Match_two_lists(
                hadr_bquark, 'hadr_bquark',
                top.subjets, 'top_subjet' )

            n_lept_bquark_matched_to_top_subjet = self.Match_two_lists(
                lept_bquark, 'lept_bquark',
                top.subjets, 'top_subjet' )

            n_lquarks_matched_to_top_subjet = self.Match_two_lists(
                lquarks, 'lquark',
                top.subjets, 'top_subjet' )

            # To subjets from other top
            if len(other_tops) == 0:
                n_hadr_bquark_matched_to_otop_subjet = -1
                n_lept_bquark_matched_to_otop_subjet = -1
                n_lquarks_matched_to_otop_subjet = -1
            else:
                n_hadr_bquark_matched_to_otop_subjet = 0
                n_lept_bquark_matched_to_otop_subjet = 0
                n_lquarks_matched_to_otop_subjet = 0
                for top in other_tops:

                    n_hadr_bquark_matched_to_otop_subjet += self.Match_two_lists(
                        hadr_bquark, 'hadr_bquark',
                        top.subjets, 'other_top_subjet' )

                    n_lept_bquark_matched_to_otop_subjet += self.Match_two_lists(
                        lept_bquark, 'lept_bquark',
                        top.subjets, 'other_top_subjet' )

                    n_lquarks_matched_to_otop_subjet += self.Match_two_lists(
                        lquarks, 'lquark',
                        top.subjets, 'other_top_subjet' )


        if genquarks_higgs_present:

            # To reco_btagged_jets
            n_higgs_bquarks_matched_to_bjet = self.Match_two_lists(
                higgs_bquarks, 'higgs_bquark',
                reco_btagged_jets, 'bjet' )

            # To reco_ltagged_jets
            n_higgs_bquarks_matched_to_ljet = self.Match_two_lists(
                higgs_bquarks, 'higgs_bquark',
                reco_ltagged_jets, 'ljet' )

            # To subjets from chosen top
            n_higgs_bquarks_matched_to_top_subjet = self.Match_two_lists(
                higgs_bquarks, 'higgs_bquark',
                top.subjets, 'top_subjet' )

            # To subjets from other top
            if len(other_tops) == 0:
                n_higgs_bquarks_matched_to_otop_subjet = -1
            else:
                n_higgs_bquarks_matched_to_otop_subjet = 0
                for top in other_tops:
                    n_higgs_bquarks_matched_to_otop_subjet += self.Match_two_lists(
                        higgs_bquarks, 'higgs_bquark',
                        top.subjets, 'other_top_subjet' )


        # Write to event
        # ==============

        setattr( event, 'QMatching_t_attempted', genquarks_top_present )
        setattr( event, 'QMatching_H_attempted', genquarks_higgs_present )

        if genquarks_top_present:

            event.QMatching_n_hadr_bquark_matched_to_bjet = \
                n_hadr_bquark_matched_to_bjet
            event.QMatching_n_lept_bquark_matched_to_bjet = \
                n_lept_bquark_matched_to_bjet
            event.QMatching_n_lquarks_matched_to_bjet = \
                n_lquarks_matched_to_bjet

            event.QMatching_n_hadr_bquark_matched_to_ljet = \
                n_hadr_bquark_matched_to_ljet
            event.QMatching_n_lept_bquark_matched_to_ljet = \
                n_lept_bquark_matched_to_ljet
            event.QMatching_n_lquarks_matched_to_ljet = \
                n_lquarks_matched_to_ljet

            event.QMatching_n_hadr_bquark_matched_to_top_subjet = \
                n_hadr_bquark_matched_to_top_subjet
            event.QMatching_n_lept_bquark_matched_to_top_subjet = \
                n_lept_bquark_matched_to_top_subjet
            event.QMatching_n_lquarks_matched_to_top_subjet = \
                n_lquarks_matched_to_top_subjet

            event.QMatching_n_hadr_bquark_matched_to_otop_subjet = \
                n_hadr_bquark_matched_to_otop_subjet
            event.QMatching_n_lept_bquark_matched_to_otop_subjet = \
                n_lept_bquark_matched_to_otop_subjet
            event.QMatching_n_lquarks_matched_to_otop_subjet = \
                n_lquarks_matched_to_otop_subjet

        if genquarks_higgs_present:

            event.QMatching_n_higgs_bquarks_matched_to_bjet = \
                n_higgs_bquarks_matched_to_bjet
            event.QMatching_n_higgs_bquarks_matched_to_ljet = \
                n_higgs_bquarks_matched_to_ljet
            event.QMatching_n_higgs_bquarks_matched_to_top_subjet = \
                n_higgs_bquarks_matched_to_top_subjet
            event.QMatching_n_higgs_bquarks_matched_to_otop_subjet = \
                n_higgs_bquarks_matched_to_otop_subjet

#==========================END OF SUBJET ANALYZER==========================#
