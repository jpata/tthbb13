from TTH.MEAnalysis.Analyzer import FilterAnalyzer
import ROOT
import copy

class SubjetAnalyzer(FilterAnalyzer):
    """
    Subjet analyzer by Thomas
    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(SubjetAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf

        self.R_cut = 0.3
        self.top_mass = 172.04

        self.bTagAlgo = self.conf.jets["btagAlgo"]

        if hasattr( self.conf, 'httCandidatecut' ):
            self.Cut_criteria = self.conf.httCandidatecut
            print 'Using httCandidate cut criteria from configuration file'
        else:
            self.Cut_criteria = [
                ( 'pt'  , '>', '200.0' ),
                ( 'mass', '>', '120.0' ),
                ( 'mass', '<', '220.0' ),
                ( 'fW'  , '<', '0.175' ) ]

    def beginLoop(self, setup):
        super(SubjetAnalyzer, self).beginLoop(setup)


    def endLoop(self, setup):
        print 'Running endLoop'


    def process(self, event):

        print 'Printing from SubjetAnalyzer! iEv = {0}'.format(event.iEv)

        # Is set to True only after the event passed all criteria
        setattr( event, 'PassedSubjetAnalyzer', False )

        # Create two new lists for selected_btagged_jets and wquark_candidate_jets
        # Needs to be done here because the lists are needed in the mem config
        setattr( event, 'selected_btagged_jets_sj', [] )
        setattr( event, 'wquark_candidate_jets_sj', [] )


        ########################################
        # Minimal event suitability:
        #  - Needs to be single leptonic
        #  - At least 1 httCandidate
        ########################################

        # Check if the event is single leptonic
        if not event.is_sl:
            return True

        # Keep track of number of httCandidates that passed the cut
        setattr( event, 'nhttCandidate', len( event.httCandidate ) )
        setattr( event, 'nhttCandidate_aftercuts', 0 )

        # Just run normal mem if there is no httCandidate present
        # Check if there is an httCandidate
        if len( event.httCandidate ) == 0:
            return True

        # Apply the cuts on the httCandidate
        tops = []
        for candidate in event.httCandidate:
            if self.Apply_Cut_criteria( candidate ):
                tops.append( copy.deepcopy(candidate) )

        # Keep track of how many httCandidates passed
        event.nhttCandidate_aftercuts = len( tops )

        # Just run normal mem if there is no httCandidate surviving the cuts
        # Check if any candidates survived the cutoff criteria
        if len(tops) == 0:
            return True

        # Calculates the delR with the (single) lepton that was found
        self.Set_DelRwithLepton( event, tops )

        # If exactly 1 survived, simply continue with that candidate
        if len(tops) == 1:
            top = tops[0]
            other_top_present = False

        # If more than 1 candidate survived the cutoff criteria, choose the
        # one whose delR with the lepton was biggest
        else:
            tops = sorted( tops, key=lambda x: -x.delR_lepton )
            other_top_present = True
            top = tops[0]
            other_top = tops[1]

        # Write delRmin to event
        setattr( event, 'httCandidate_delRmin', abs(top.Rmin-top.RminExpected) )
        print 'httCandidate_delRmin = {0}'.format( abs(top.Rmin-top.RminExpected) )

        # event.wquark_candidate_jets is a set instead of a list (not sure why)
        event.wquark_candidate_jets = list( event.wquark_candidate_jets )

        # Check how many of which quarks are present
        # ======================================

        # Necessary to remove duplicates in GenWZQuark branch
        # This step can be removed for V12 samples
        self.CompareWZQuarks( event )

        # Check if event contains the right number of quarks
        # (Only used to do truth-level comparisons)
        genquarks_cat1_present = True
        genhiggs_present = True
        if len(event.GenWZQuark)<2:
            genquarks_cat1_present = False
        if len(event.GenWZQuark)>2:
            genquarks_cat1_present = False
        if len(event.GenBQuarkFromTop)<2:
            genquarks_cat1_present = False
        if len(event.GenBQuarkFromTop)>2:
            genquarks_cat1_present = False
        if len(event.GenBQuarkFromH)<2:
            genhiggs_present = False
        if len(event.GenBQuarkFromH)>2:
            genhiggs_present = False


        ########################################
        # Get the lists of particles: quarks, jets and subjets
        ########################################

        # Create two new lists for selected_btagged_jets and wquark_candidate_jets:
        event.selected_btagged_jets_sj = \
            copy.deepcopy( event.selected_btagged_jets ) )
        event.wquark_candidate_jets_sj = \
            copy.deepcopy( event.wquark_candidate_jets ) )

        if genquarks_cat1_present:
            # Get the hadronic & leptonic b-quark and the two light quarks
            ( tl_HadronicBQuark,
              tl_GenWZQuark1,
              tl_GenWZQuark2,
              tl_LeptonicBQuark )  = self.Get_tl_genquarks( event )

            # Some convenient lists of quarks
            tl_QuarksFromHadrTop = [
                tl_HadronicBQuark, tl_GenWZQuark1, tl_GenWZQuark2 ]
            tl_LightQuarks = [ tl_GenWZQuark1, tl_GenWZQuark2 ]

        if genhiggs_present:
            # Get the 2 b-quarks from Higgs
            tl_BQuarksFromH = []
            for q in event.GenBQuarkFromH:
                tl_q = ROOT.TLorentzVector()
                tl_q.SetPtEtaPhiM( q.pt, q.eta, q.phi, q.mass )
                tl_BQuarksFromH.append( tl_q )

        # Get the subjets from the httCandidate
        # Also sets transfer functions as attributes, and a btagFlag based on kin.
        tl_subjets = self.Get_Subjets( top )
        if other_top_present:
            tl_subjets_other_top = self.Get_Subjets( other_top )

        # Get the list of btagged_jets
        tl_btagged_jets = []
        for jet in event.selected_btagged_jets_sj:
            x = ROOT.TLorentzVector()
            x.SetPtEtaPhiM( jet.pt, jet.eta, jet.phi, jet.mass )
            setattr( x, 'origin_jet', jet )
            tl_btagged_jets.append( x )

        # Get list of wquark_candidate_jets
        tl_wquark_candidate_jets = []
        for jet in event.wquark_candidate_jets_sj:
            x = ROOT.TLorentzVector()
            x.SetPtEtaPhiM( jet.pt, jet.eta, jet.phi, jet.mass )
            setattr( x, 'origin_jet', jet )
            tl_wquark_candidate_jets.append( x )


        ########################################
        # Matching
        ########################################

        # Match subjet to a bjet
        Match_subjet_bjet = self.Match_two_tl_lists(
            tl_subjets, 'subjet',
            tl_btagged_jets, 'bjet' )

        # Match subjet to a ljet
        Match_subjet_ljet = self.Match_two_tl_lists(
            tl_subjets , 'subjet',
            tl_wquark_candidate_jets, 'ljet' )

        # In case of double matching, choose the match with lowest delR
        # (This is not expected to happen often)
        for tl_subjet in tl_subjets:
            if hasattr( tl_subjet, 'bjet_match' ) and \
                hasattr( tl_subjet, 'ljet_match' ) :
                print 'Double match detected'
                if tl_subjet.bjet_match_delR < tl_subjet.ljet_match_delR:
                    del tl_subjet.ljet_match
                    del tl_subjet.ljet_match_delR
                    Match_subjet_ljet -= 1
                else:
                    del tl_subjet.bjet_match
                    del tl_subjet.bjet_match_delR
                    Match_subjet_bjet -= 1


        if genquarks_cat1_present and genhiggs_present:

            # Quark matching
            # ==============

            # Quark matching is only done to compare events to truth level.
            # Events are not selected based on successful quark matching.

            # Matching quarks with subjets

            Match_hadr_bquark_subjet = self.Match_two_tl_lists(
                tl_HadronicBQuark, 'hadr_bquark',
                tl_subjets, 'subjet' )

            Match_lquark1_subjet = self.Match_two_tl_lists(
                tl_GenWZQuark1, 'lquark1',
                tl_subjets, 'subjet' )

            Match_lquark2_subjet = self.Match_two_tl_lists(
                tl_GenWZQuark2, 'lquark2',
                tl_subjets, 'subjet' )

            Match_lept_bquark_subjet = self.Match_two_tl_lists(
                tl_LeptonicBQuark, 'lept_bquark',
                tl_subjets, 'subjet' )

            Match_bquark_higgs1_subjet = self.Match_two_tl_lists(
                tl_BQuarksFromH[0], 'bquark_higgs1',
                tl_subjets, 'subjet' )

            Match_bquark_higgs2_subjet = self.Match_two_tl_lists(
                tl_BQuarksFromH[1], 'bquark_higgs2',
                tl_subjets, 'subjet' )

            # Matching quarks with jets

            Match_hadr_bquark_jet = self.Match_two_tl_lists(
                tl_HadronicBQuark, 'hadr_bquark',
                tl_btagged_jets, 'jet' )

            Match_lquark1_jet = self.Match_two_tl_lists(
                tl_GenWZQuark1, 'lquark1',
                tl_wquark_candidate_jets, 'jet' )

            Match_lquark2_jet = self.Match_two_tl_lists(
                tl_GenWZQuark2, 'lquark2',
                tl_wquark_candidate_jets, 'jet' )

            Match_lept_bquark_jet = self.Match_two_tl_lists(
                tl_LeptonicBQuark, 'lept_bquark',
                tl_btagged_jets, 'jet' )

            Match_bquark_higgs1_jet = self.Match_two_tl_lists(
                tl_BQuarksFromH[0], 'bquark_higgs1',
                tl_btagged_jets, 'jet' )

            Match_bquark_higgs2_jet = self.Match_two_tl_lists(
                tl_BQuarksFromH[1], 'bquark_higgs2',
                tl_btagged_jets, 'jet' )

            setattr( event, 'QMatching_sj_hadr_bquark'  , Match_hadr_bquark_subjet )
            setattr( event, 'QMatching_sj_lquark1'      , Match_lquark1_subjet )
            setattr( event, 'QMatching_sj_lquark2'      , Match_lquark2_subjet )
            setattr( event, 'QMatching_sj_lept_bquark'  , Match_lept_bquark_subjet )
            setattr( event, 'QMatching_sj_bquark_higgs1',
                Match_bquark_higgs1_subjet )
            setattr( event, 'QMatching_sj_bquark_higgs2',
                Match_bquark_higgs2_subjet )

            setattr( event, 'QMatching_jet_hadr_bquark'  , Match_hadr_bquark_jet )
            setattr( event, 'QMatching_jet_lquark1'      , Match_lquark1_jet )
            setattr( event, 'QMatching_jet_lquark2'      , Match_lquark2_jet )
            setattr( event, 'QMatching_jet_lept_bquark'  , Match_lept_bquark_jet )
            setattr( event, 'QMatching_jet_bquark_higgs1', Match_bquark_higgs1_jet )
            setattr( event, 'QMatching_jet_bquark_higgs2', Match_bquark_higgs2_jet )


        ########################################
        # Logic
        ########################################

        # Goal of this section is make sure exactly 1 subjet has btagFlag = 1.0,
        # and exactly 2 subjets have btagFlag = 0.0.

        # Regarding the strategy: a successful match is always prioritized.

        # b | l | Strategy
        # --+---+-------------------------------------------------------------------
        # 0 | 0 | Trust btagFlags based on prefix ('sjNonW'=b) (Strategy 1)
        # 0 | 3 |
        # --+---+-------------------------------------------------------------------
        # 0 | 1 | If the matched subjet was 'sjW1' or 'sjW2', trust the btagFlags
        #   |   | based on prefix. (Strategy 1)
        #   |   | Else, trust the matching, and tag one of the remaining subjets as
        #   |   | the b, based on highest pt (to be tested) (Strategy 2)
        # --+---+-------------------------------------------------------------------
        # 0 | 2 | Tag the remaining unmatched subjet as the b (Strategy 3)
        # --+---+-------------------------------------------------------------------
        # 1 | 0 | Trust the match with the b-jet, and set the other 2 subjets as the
        #   | 1 | l-jets (Strategy 4)
        #   | 2 | 
        # --+---+-------------------------------------------------------------------
        # 2 | 0 | Select the subjet that was matched to a b-jet with the highest
        #   | 1 | b-likelihood as the b, and set the remaining subjets as the l-jets
        # 3 | 0 | (Strategy 5)
        # --+---+-------------------------------------------------------------------

        # For every type of event, store the number of mismatches, the applied
        # strategy and the 'event_type_number' (see documentation, TODO):
        # ( nr_of_mismatches, strategy, event_type_number )

        #Do nothing; trust the btagFlags based on prefix
        if Match_subjet_bjet == 0 and Match_subjet_ljet == 0:
            ( nr_of_mismatches, strategy, event_type_number ) = ( 0, 1, 1 )
        elif Match_subjet_bjet == 0 and Match_subjet_ljet == 3:
            ( nr_of_mismatches, strategy, event_type_number ) = ( 1, 1, 2 )

        elif Match_subjet_bjet == 0 and Match_subjet_ljet == 1:

            # Get the subjet that was matched with a light jet
            tl_l_subjet = [ tl for tl in tl_subjets if hasattr(tl,'ljet_match') ][0]
            # Get the other two subjets
            tl_o_subjets = [ tl for tl in tl_subjets if not hasattr( tl,
                                                                     'ljet_match') ]
            ( nr_of_mismatches, strategy, event_type_number ) = ( 0, 1, 3 )

            if tl_l_subjet.prefix == 'sjNonW':
                # This means the 'sjNonW' subjet was matched with a light jet.
                # Trust the matching. From the remaining subjets, tag the one with
                # highest pt as the b
                ( nr_of_mismatches, strategy, event_type_number ) = ( 0, 2, 4 )
                setattr( tl_l_subjet, 'btagFlag', 0.0 )
                if tl_o_subjets[0].Pt() >  tl_o_subjets[1].Pt():
                    setattr( tl_o_subjets[0], 'btagFlag', 1.0 )
                    setattr( tl_o_subjets[1], 'btagFlag', 0.0 )
                else:
                    setattr( tl_o_subjets[0], 'btagFlag', 0.0 )
                    setattr( tl_o_subjets[1], 'btagFlag', 1.0 )
            # else: Trust btagFlags based on prefix

        elif Match_subjet_bjet == 0 and Match_subjet_ljet == 2:
            for tl in tl_subjets:
                if hasattr( tl, 'ljet_match' ): setattr( tl, 'btagFlag', 0.0 )
                else:                           setattr( tl, 'btagFlag', 1.0 )
            ( nr_of_mismatches, strategy, event_type_number ) = ( 0, 3, 5 )
            
        elif Match_subjet_bjet == 1 and Match_subjet_ljet in [0,1,2]:
            for tl in tl_subjets:
                if hasattr( tl, 'bjet_match' ): setattr( tl, 'btagFlag', 1.0 )
                else:                           setattr( tl, 'btagFlag', 0.0 )
            # Set appropiate ETN for easy accessing later
            if Match_subjet_ljet==0: ETN = 6
            if Match_subjet_ljet==1: ETN = 7
            if Match_subjet_ljet==2: ETN = 8
            ( nr_of_mismatches, strategy, event_type_number ) = ( 0, 4, ETN )

        elif Match_subjet_bjet in [2,3] and Match_subjet_ljet in [0,1]:

            tl_b_subjets = [ tl for tl in tl_subjets if hasattr(tl, 'bjet_match') ]
            tl_b_subjet = sorted(
                tl_b_subjets,
                key=lambda x: -getattr( x.bjet_match.origin_jet, self.bTagAlgo ))[0]

            for tl in tl_subjets:
                if tl == tl_b_subjet:           setattr( tl, 'btagFlag', 1.0 )
                else:                           setattr( tl, 'btagFlag', 0.0 )

            # Set appropiate ETN for easy accessing later
            if Match_subjet_bjet==2 and Match_subjet_ljet==0:
                NOM = 1
                ETN = 9
            if Match_subjet_bjet==2 and Match_subjet_ljet==1:
                NOM = 1
                ETN = 10
            if Match_subjet_bjet==3 and Match_subjet_ljet==0:
                NOM = 2
                ETN = 11
            ( nr_of_mismatches, strategy, event_type_number ) = ( NOM, 5, ETN )

        else:
            print 'Unassigned category! Create a strategy for this case.'
            print 'subjet-b matches: {0}, subjet-l matches = {1}'.format(
                Match_subjet_bjet, Match_subjet_ljet )
            return 0

        """
        # Check up printing - the httCandidate
        print '=====================================\nCheck print'
        for tl_subjet in tl_subjets:
            print '\nSubjet {0}'.format( tl_subjet.prefix )
            print '    btagFlag: {0}'.format( tl_subjet.btagFlag )
            if hasattr( tl_subjet, 'bjet_match' ):
                btag = getattr( tl_subjet.bjet_match.origin_jet, self.bTagAlgo ) 
                print '    original btag of the jet: {0}'.format(btag)
                self.Print_particle_lists(
                    ( [tl_subjet], 'TL', 'subjet'),
                    ( [tl_subjet.bjet_match], 'TL', 'Matching bjet')
                    )
            if hasattr( tl_subjet, 'ljet_match' ):

                self.Print_particle_lists(
                    ( [tl_subjet], 'TL', 'subjet'),
                    ( [tl_subjet.ljet_match], 'TL', 'Matching ljet')
                    )
        print '=====================================\n'

        # Check up printing - the input jets
        print '=====================================\n'
        print 'Input jets:'
        self.Print_particle_lists(
            ( event.selected_btagged_jets_sj, 'Class', 
                'event.selected_btagged_jets_sj'),
            ( event.wquark_candidate_jets_sj, 'Class',
                'event.wquark_candidate_jets_sj'),
            )
        print '=====================================\n'
        """

        # Remove all original instances and replace them with their matched subjets
        # If an original bjet is matched with a subjet that has btagFlag=0.0, the
        # original bjet is removed from the btagged_jets, and the subjet is appended
        # to event.wquark_candidate_jets.
        # (Analogous for original ljet matched with a subjet that has btagFlag=1.0)
        for tl_subjet in tl_subjets:
            if hasattr( tl_subjet, 'ljet_match' ):
                # Get the original ljet
                orig_ljet = tl_subjet.ljet_match.origin_jet
                # Remove it from the ljet list in the event
                event.wquark_candidate_jets_sj.pop(
                    event.wquark_candidate_jets_sj.index( orig_ljet ) )
            if hasattr( tl_subjet, 'bjet_match' ):
                # Get the original bjet
                orig_bjet = tl_subjet.bjet_match.origin_jet
                # Remove it from the bjet list in the event
                event.selected_btagged_jets_sj.pop(
                    event.selected_btagged_jets_sj.index( orig_bjet ) )

            if tl_subjet.btagFlag == 1.0:
                # Append the subjet to btagged_jets list in the event
                event.selected_btagged_jets_sj.append( tl_subjet )
            elif tl_subjet.btagFlag == 0.0:
                # Append the subjet to wquark_candidate_jets list in the event
                event.wquark_candidate_jets_sj.append( tl_subjet )

        """
        # Check up printing - the output jets
        print '=====================================\n'
        print 'Output jets:'
        self.Print_particle_lists(
            ( event.selected_btagged_jets_sj, 'Class', 
                'event.selected_btagged_jets_sj'),
            ( event.wquark_candidate_jets_sj, 'Class',
                'event.wquark_candidate_jets_sj'),
            )
        print '=====================================\n'
        """


        ########################################
        # Categorization
        # Requires work - very quick & dirty at the moment
        ########################################

        if len( event.selected_btagged_jets_sj ) > 4:
            # The last added element is the subjet - keep that one, and the next
            # 3 btagged_jets
            event.selected_btagged_jets_sj = \
                event.selected_btagged_jets_sj[-1:] + \
                event.selected_btagged_jets_sj[:3]
        
        if len( event.selected_btagged_jets_sj ) >= 4:
            event.PassedSubjetAnalyzer = True


        ########################################
        # Write to event
        ########################################

        setattr( event, 'Matching_subjet_bjet', Match_subjet_bjet )
        setattr( event, 'Matching_subjet_ljet', Match_subjet_ljet )

        setattr( event, 'Matching_nr_of_mismatches', nr_of_mismatches )
        setattr( event, 'Matching_strategy', strategy )
        setattr( event, 'Matching_event_type_number', event_type_number )

        # This tells the MEMAnalyzer to run
        print 'Exiting SubjetAnalyzer! event.PassedSubjetAnalyzer = {0}'.format(
            event.PassedSubjetAnalyzer )



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
    # Sorts tops - criterium to be tested
    def Set_DelRwithLepton( self, event, tops ):

        # Get the lepton
        l = event.good_leptons[0]

        # Create TLorentzVector for lepton
        tl_lepton = ROOT.TLorentzVector()
        tl_lepton.SetPtEtaPhiM( l.pt, l.eta, l.phi, l.mass )

        # Create TLorentzVector for tops
        tl_tops = []
        for top in tops:
            tl_top = ROOT.TLorentzVector()
            tl_top.SetPtEtaPhiM( top.pt, top.eta, top.phi, top.mass )
            setattr( top, 'delR_lepton', tl_top.DeltaR(tl_lepton) )
    
    # ==============================================================================
    def Get_Subjets( self, top ):

        tl_subjets = []
        prefixes = [ 'sjW1', 'sjW2', 'sjNonW' ]
        for (i_subjet, prefix) in enumerate( prefixes ):
            x = ROOT.TLorentzVector()
            x.SetPtEtaPhiM(
                getattr( top, prefix + 'pt' ),
                getattr( top, prefix + 'eta' ),
                getattr( top, prefix + 'phi' ),
                getattr( top, prefix + 'mass' ) )
            setattr( x, 'prefix', prefix )

            # Set the btagFlag, based on prefix (only used if there is no other tag)
            if prefix == 'sjNonW':
                setattr( x, 'btagFlag', 1.0 )
            else:
                setattr( x, 'btagFlag', 0.0 )

            # Set pt, eta, phi and mass also as attributes
            # Needed for compatibility with mem
            setattr( x, 'pt', x.Pt() )
            setattr( x, 'eta', x.Eta() )
            setattr( x, 'phi', x.Phi() )
            setattr( x, 'mass', x.M() )

            tl_subjets.append( x )

        #Adding subjet transfer functions
        for subjet in tl_subjets:
            jet_eta_bin = 0
            if abs(subjet.Eta())>1.0:
                jet_eta_bin = 1

            #If True, TF [0] - reco, x - gen
            #If False, TF [0] - gen, x - reco
            eval_gen = False
            setattr( subjet, 'tf_b' ,
                self.conf.tf_sj_matrix['b'][jet_eta_bin].Make_Formula(eval_gen) )
            setattr( subjet, 'tf_l' ,
                self.conf.tf_sj_matrix['l'][jet_eta_bin].Make_Formula(eval_gen) )
            setattr( subjet, 'tf_b_lost' ,
                self.conf.tf_sj_matrix['b'][jet_eta_bin].Make_CDF() )
            setattr( subjet, 'tf_l_lost' ,
                self.conf.tf_sj_matrix['l'][jet_eta_bin].Make_CDF() )

            #Set jet pt threshold for CDF
            subjet.tf_b_lost.SetParameter(0, self.conf.jets["pt"])
            subjet.tf_l_lost.SetParameter(0, self.conf.jets["pt"])

        return tl_subjets

    # ==============================================================================
    # Print a non-predefined number of particle lists
    # Input is a list of tuples: input_args = [ (tuple), (tuple), ... ]
    # Every tuple is structured as follows:
    # (tuple) = ( particle list, TLorentz/Class label, name of the particle )
    def Print_particle_lists( self, *input_args ):

        for ( p_list, mode, name ) in input_args:

            print '\n    Printing {0}:'.format( name )

            if mode == 'TL':

                for q in p_list:
                    print '    [ {0:9s} | {1:9s} | {2:9s} | {3:9s} ]'.format(
                        '{0:.3f}'.format(q.Pt()),
                        '{0:.3f}'.format(q.Eta()),
                        '{0:.3f}'.format(q.Phi()),
                        '{0:.3f}'.format(q.M()) )

            if mode == 'Class':

                for q in p_list:
                    print '    [ {0:9s} | {1:9s} | {2:9s} | {3:9s} ]'.format(
                        '{0:.3f}'.format(q.pt),
                        '{0:.3f}'.format(q.eta),
                        '{0:.3f}'.format(q.phi),
                        '{0:.3f}'.format(q.mass) )

        print ''

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
    # Gets a list of 3 quarks
    #  - The first quark is a Gen B quark. This should be the hadronic B quark.
    #    Which quark is hadronic is determined by adding the light quarks to the
    #    B quarks, and seeing which combined mass comes closer to the top mass
    #  - Output looks like: [ BQuark, lightQuark1, lightQuark2 ], where the list
    #    entries are TLorentzVector objects.
    #  - Output looks like:
    #    ( hadronic_BQuark, lightQuark1, lightQuark2, leptonic_BQuark )
    #    , where the all entries are TLorentzVector objects.
    def Get_tl_genquarks(self, event ):

        # Make list of TLorentzVector objects for the 2 light quarks
        tl_GenWZQuarks = []
        for l in event.GenWZQuark:
            tl_l = ROOT.TLorentzVector()
            tl_l.SetPtEtaPhiM( l.pt, l.eta, l.phi, l.mass )
            tl_GenWZQuarks.append( tl_l )

        # Make list for the 2 B quarks, and a list of B quarks + light quarks
        tl_GenBQuarks = []
        tl_Combined = []
        for (b_i, b) in enumerate(event.GenBQuarkFromTop):

            tl_b = ROOT.TLorentzVector()
            tl_b.SetPtEtaPhiM( b.pt, b.eta, b.phi, b.mass )

            tl_GenBQuarks.append( tl_b )
            tl_Combined.append( tl_b + tl_GenWZQuarks[0] + tl_GenWZQuarks[1] )

        # Calculate mass difference from top mass
        delmass0 = abs(tl_Combined[0].M() - self.top_mass)
        delmass1 = abs(tl_Combined[1].M() - self.top_mass)

        # Save the mass difference with top mass
        setattr( event.GenBQuarkFromTop[0], 'delmass_top', delmass0 )
        setattr( event.GenBQuarkFromTop[1], 'delmass_top', delmass1 )

        # Make sure the B quark with lowest del mass to top mass is at index 0
        # (both for the tl list and in the event)
        if delmass1 < delmass0:

            tl_GenBQuarks = [ tl_GenBQuarks[1], tl_GenBQuarks[0] ]

            event.GenBQuarkFromTop = [
                event.GenBQuarkFromTop[1],
                event.GenBQuarkFromTop[0] ]

        setattr( tl_GenBQuarks[0], 'is_hadr', 1 )
        setattr( event.GenBQuarkFromTop[0], 'is_hadr', 1 )
        setattr( event.GenBQuarkFromTop[1], 'is_hadr', 0 )

        return ( tl_GenBQuarks[0],  # Hadronic
                 tl_GenWZQuarks[0], # Light 1
                 tl_GenWZQuarks[1], # Light 2
                 tl_GenBQuarks[1] ) # Leptonic

    # ==============================================================================
    # Simple algorithm that matches the smallest delta R for two lists of TL vectors
    def Link_smallest_delR( self, tl_quarks, tl_jets ):

        n_jets = len(tl_jets)
        n_quarks = len(tl_quarks)

        Rmat = [[ (tl_quarks[i].DeltaR( tl_jets[j] )) \
            for j in range(n_jets)] for i in range(n_quarks) ]

        Rmin = 9999.0
        
        for (r, row) in enumerate(Rmat):
            for (c, ele) in enumerate(row):
                if ele < Rmin and ele < self.R_cut:
                    Rmin = ele
                    r_min = r
                    c_min = c

        if Rmin == 9999.0: return ( 'No link', 0, 0)

        return (r_min, c_min, Rmin)


    def Match_two_tl_lists( self, tls1_orig, label1, tls2_orig, label2 ):

        # If just a single TLorentzVector object was passed, convert it to a list
        if isinstance( tls1_orig, ROOT.TLorentzVector ):
            tls1_orig = [ tls1_orig ]
        if isinstance( tls2_orig, ROOT.TLorentzVector ):
            tls1_orig = [ tls2_orig ]

        # Create copies of the list, since entries will be popped
        tls1 = copy.deepcopy( tls1_orig )
        tls2 = copy.deepcopy( tls2_orig )

        # Save the original tl as an attribute
        for ( tl1, tl1_orig ) in zip( tls1, tls1_orig ):
            setattr( tl1, 'tl_origin', tl1_orig )
        for ( tl2, tl2_orig ) in zip( tls2, tls2_orig ):
            setattr( tl2, 'tl_origin', tl2_orig )

        # Attempt matching until the shortest list is depleted, or until there are
        # no more matches with delR < delR_cut
        n_matches = min( len(tls1), len(tls2) )

        for i_match in range(n_matches):

            # Attempt a match
            (i1, i2, delR) = self.Link_smallest_delR( tls1, tls2 )

            # Return the attempt number if no more matches could be made
            if i1 == 'No link':
                return i_match

            # Pop the matched tls from the lists for the next iteration
            matched_tl1 = tls1.pop(i1)
            matched_tl2 = tls2.pop(i2)

            # Record the match in the original tls
            setattr( matched_tl1.tl_origin,
                     '{0}_match'.format( label2 ),
                     matched_tl2.tl_origin )
            setattr( matched_tl2.tl_origin,
                     '{0}_match'.format( label1 ),
                     matched_tl1.tl_origin )

            # Record the delR value in the original tls
            setattr( matched_tl1.tl_origin,
                     '{0}_match_delR'.format( label2 ),
                     delR )
            setattr( matched_tl2.tl_origin,
                     '{0}_match_delR'.format( label1 ),
                     delR )

        return n_matches

#==========================END OF SUBJET ANALYZER==========================#
