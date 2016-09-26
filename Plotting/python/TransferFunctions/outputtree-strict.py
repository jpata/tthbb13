#!/usr/bin/env python
"""
Thomas:
Reads VHBB Ntuple, outputs events with 1 quark and 1 jet which had minimal delR

"""


########################################
# Imports
########################################

import ROOT
import os
import pickle, json
import time
import datetime
try: 
    import AccessHelpers as AH
except:
    import TTH.MEAnalysis.AccessHelpers as AH


########################################
# Functions
########################################

def Get_min_2D( Mat ):

    # Mat should be a list of lists: [ [...], [...], ...]

    if len(Mat)==0: print "Mat is empty!"

    Min = Mat[0][0]
    i_index = 0
    j_index = 0

    # Loop over matrix to find minimum
    for i in range( len(Mat) ):
        for j in range( len(Mat[0]) ):
            if Mat[i][j] < Min:
                Min = Mat[i][j]
                i_index = i
                j_index = j

    # Set sec_min > Mat[0][0], in case the minimum is actually Mat[0][0]
    sec_Min = Mat[0][0]+10
    sec_i_index = 0
    sec_j_index = 0

    # Loop a second time to find the second closest mininum
    for i in range( len(Mat) ):
        for j in range( len(Mat[0]) ):
            if Mat[i][j] < sec_Min and (not (i==i_index and j==j_index)):
                sec_Min = Mat[i][j]
                sec_i_index = i
                sec_j_index = j

    return [ Min , i_index , j_index , sec_Min, sec_i_index, sec_j_index]


def LinkJettoQuark( tl_jets, tl_quarks, config ):

    # General method:
    #  - Compute matrix of delR values (rows = jets, columns = quarks)
    #  - Loop until out of quarks or jets:
    #    - Find minimum
    #    - Write the corresponding jet, quark and delR value to lists
    #    - Delete the row and column from the matrix
    #    - Repeat

    links = []
    tl_quarks_out = []
    tl_jets_out = []
    delR = []

    # Computing matrix of delR values
    Rmat = [[ (tl_jets[i].DeltaR( tl_quarks[j] )) \
        for j in range(len(tl_quarks))] for i in range(len(tl_jets)) ]

    # Find the links
    #for k in range(number_of_links):
    while len(tl_quarks)>0 and len(tl_jets)>0:

        # Find minimum and indices of minimum in delR matrix
        [ Rmin, Jet_min_index, Quark_min_index,
        sec_Rmin, sec_Jet_min_index, sec_Quark_min_index ] = Get_min_2D( Rmat )

        # Don't use del R values > 0.3
        if Rmin > config['max_link_delR']:
            break

        if config['Remove_double_match']:
            # Check if there is no second quark very closely matched to the jet
            if (sec_Jet_min_index == Jet_min_index and \
                sec_Rmin < config['max_sec_delR']):

                #print '-------------------'
                #print 'Rmat before removal:'
                #for row in Rmat:
                #    print row
                
                # If a second quark is too close to the jet, both quarks and the jet
                # are removed from the list.

                # Printing the removals
                if False:
                    print '\nClose second match: {0} ~ {1}'.format( Rmin, sec_Rmin )
                    print 'Removing jet {0}:'.format(Jet_min_index)
                    print [tl_jets[Jet_min_index].Pt(),
                        tl_jets[Jet_min_index].Eta(),
                        tl_jets[Jet_min_index].Phi(),
                        tl_jets[Jet_min_index].M()]
                    print 'Removing closest quark {0}:'.format(Quark_min_index)
                    print [tl_quarks[Quark_min_index].Pt(),
                        tl_quarks[Quark_min_index].Eta(),
                        tl_quarks[Quark_min_index].Phi(),
                        tl_quarks[Quark_min_index].M()]
                    print 'Removing second closest quark {0}:'.format(
                        sec_Quark_min_index)
                    print [tl_quarks[sec_Quark_min_index].Pt(),
                        tl_quarks[sec_Quark_min_index].Eta(),
                        tl_quarks[sec_Quark_min_index].Phi(),
                        tl_quarks[sec_Quark_min_index].M()]
                    print ''

                # .pop() should be done first on the higher index (otherwise i 
                # shifts)
                i_first_rm = max( Quark_min_index, sec_Quark_min_index )
                i_second_rm = min( Quark_min_index, sec_Quark_min_index )

                # Remove the jet, quarks, and entries from Rmat
                tl_jets.pop(Jet_min_index)            
                tl_quarks.pop(i_first_rm)
                tl_quarks.pop(i_second_rm)

                Rmat.pop(Jet_min_index)
                for row in Rmat:
                    row.pop(i_first_rm)
                    row.pop(i_second_rm)

                #print 'Rmat after removal:'
                #for row in Rmat:
                #    print row
                #print '-------------------'

                continue

        # Printing
        if False:
            # Print which quarks got linked to which jets
            print 'Minimum delR:', Rmin
            print 'linked Jet:'
            print [tl_jets[Jet_min_index].Pt(),
                tl_jets[Jet_min_index].Eta(),
                tl_jets[Jet_min_index].Phi(),
                tl_jets[Jet_min_index].M()]
            print 'to Quark:'
            print [tl_quarks[Quark_min_index].Pt(),
                tl_quarks[Quark_min_index].Eta(),
                tl_quarks[Quark_min_index].Phi(),
                tl_quarks[Quark_min_index].M()]
            print ''

        # Write corresponding jet, quark and delR-value to lists.
        # Also deletes these jets and quarks from the input lists, which is necessary
        # to find the right minimum indices.
        tl_jets_out.append( tl_jets.pop(Jet_min_index) )
        tl_quarks_out.append( tl_quarks.pop(Quark_min_index) )
        delR.append( Rmat[ Jet_min_index ][ Quark_min_index ] )
        
        # Delete jet and quark from delR matrix
        Rmat.pop(Jet_min_index)
        for row in Rmat:
            row.pop(Quark_min_index)

    return [tl_jets_out, tl_quarks_out, delR]


def Get_TLorentz( particle, input_tree, config):

    if particle in config['jettypes']:
        Is_jet = True
        extra_vars = config['jet_extra_vars']
    elif particle in config['quarktypes']:
        Is_jet = False
        extra_vars = config['quark_extra_vars']
    else:
        print 'Error in Get_TLorentz: given particle is not specified in'\
            'configuration'
        return 0

    # List of the branchnames for the extra vars (where to look up in original root)
    extra_vars_branchnames = [ var.format(particle=particle) for var in extra_vars ]

    # Remove {particle} from extra vars (most sensible attribute name)
    extra_vars = [ var.format(particle='') for var in extra_vars ]


    tl_output = []
    
    # Get the variables for the TLorentz vector
    Pt =  AH.getter(input_tree, particle + 'pt')
    Eta =  AH.getter(input_tree, particle + 'eta')
    Phi =  AH.getter(input_tree, particle + 'phi')
    Mass =  AH.getter(input_tree, particle + 'mass')


    # Get the variables to also construct the TLorentz vector for the MC values
    #   - This is only needed to compute mcE, which is not in the input root file.
    #   - Only works for jets; quarks have no specifief MC values.
    if Is_jet and config['Get_MC_for_jets']:
        mcPt =  AH.getter(input_tree, particletype + 'mcPt')
        mcEta =  AH.getter(input_tree, particletype + 'mcEta')
        mcPhi =  AH.getter(input_tree, particletype + 'mcPhi')
        mcM =  AH.getter(input_tree, particletype + 'mcM')


    # Get the values for the extra variables (beyond what is necessary for TLorentz)
    #   - Every entry of the dict will then contain a list!
    #   - Particle specifics will be stored without particle reference, e.g.:
    #     '{particle}pdgId' is stored as 'pdgId'
    extra_vars_vals_dict = {}
    for (var, var_branch) in zip(extra_vars, extra_vars_branchnames):
        extra_vars_vals_dict[var] = AH.getter(input_tree, var_branch)

    # Remove duplicates: 2 particles are often repeated in the WZQuark entries
    removedupl = 0
    if len(Pt)>2:
        if Pt[0]==Pt[ len(Pt)-2 ] and Pt[1]==Pt[ len(Pt)-1 ]:
            removedupl = 2


    vars_val_dict = {}

    for i in range( len(Pt) - removedupl ):
        
        # Construct the vars_val_dict, the dict with values for only this i

        # Regular vars
        vars_val_dict[particle+'pt'] = Pt[i]
        vars_val_dict[particle+'phi'] = Phi[i]
        vars_val_dict[particle+'eta'] = Eta[i]
        vars_val_dict[particle+'mass'] = Mass[i]

        # Extra vars
        for key in extra_vars_vals_dict:
            vars_val_dict[key] = extra_vars_vals_dict[key][i]

        if Evaluate_Cutoff( particle, Is_jet, vars_val_dict, config ):

            y = ROOT.TLorentzVector()
            y.SetPtEtaPhiM( Pt[i] , Eta[i] , Phi[i] , Mass[i] )

            # Fill in the extra variables
            for var in extra_vars:
                setattr(y, var, vars_val_dict[var])

            # Fill in mcE (only for jets, and if Get_MC==True in configuration)
            if Is_jet and config['Get_MC_for_jets']:
                x = ROOT.TLorentzVector()
                x.SetPtEtaPhiM( mcPt[i] , mcEta[i] , mcPhi[i] , mcM[i] )
                setattr(y, 'mcE', x.E() )

            tl_output.append( y )
            
    return tl_output



def Evaluate_Cutoff( particle, Is_jet, vars_val_dict, config ):

    # Select the right list of cutoff criteria
    if Is_jet:
        cutoff_list = config['jet_cutoff_list']
    else:
        cutoff_list = config['quark_cutoff_list']

    # format of a criterium: ( varname, operator, value )
    #   To convert varname into a value that can be compared with, first format all
    #   instances of {particle} to the particle at hand, and then look that key up
    #   in vars_val_dict. This is the left hand side (LHS) of the equation.

    for crit in cutoff_list:

        LHS = vars_val_dict[ crit[0].format(particle=particle) ]

        eval_str = '{0}{1}{2}'.format( LHS, crit[1], crit[2] )

        if not eval(eval_str):
            return False

    return True


    


########################################
# Main
########################################

def main():
    
    ROOT.gROOT.SetBatch(True)

    ########################################
    # Get the configuration file
    ########################################

    if not os.path.isfile('cfg_outputtree.dat'):
        print "Error: Can't find configuration file cfg_outputtree.dat"
        return 0

    print 'Importing configuration data'
    
    try:
        infile = open( 'cfg_outputtree.dat', 'rb' )
        config = json.load( infile)
        infile.close()
    except Exception as e:
        print "Unable to open cfg_outputtree.dat", e
        print "Please create using cfg_outputtree.py"
        return

    print 'Imported configuration data'

    output_root_file_name = config['output_root_file_name'].encode("ASCII")


    # Linking switch: If Just_Jets=True, .root file will simply contain (unlinked)
    # jets.
    Just_Jets = False

    quarktypes = config['quarktypes']
    jettypes = config['jettypes']

    standard_vars = [ 'pt', 'eta', 'phi', 'mass', 'E' ]

    quark_extra_vars = config['quark_extra_vars']
    jet_extra_vars = config['jet_extra_vars']

    # Only for output purposes
    separate_vars = ['delR' ]

    if config['Get_MC_for_jets']:
        seperate_vars.append( 'Jet_mcE' )

    ########################################
    # Setup I/O
    ########################################

    print 'Setting up IO'

    # Input (environment set by grid control)
    if "FILE_NAMES" in os.environ.keys() and os.environ["FILE_NAMES"]:
        config['input_root_file_list'] = os.environ["FILE_NAMES"].split(" ")
    else:
        print "No files received. Quitting..."
        return()

    # Output tree
    output_root_file = ROOT.TFile(output_root_file_name,'RECREATE')
    output_tree = ROOT.TTree('tree','My test tree')

    # Define branches in output tree
    branches = []

    branches.extend( [ 'Jet_' + var for var in standard_vars ] )
    branches.extend( [ 'Jet_' + str(var.format(particle='')) for var in jet_extra_vars ] )

    branches.extend( [ 'Quark_' + var for var in standard_vars ] )
    branches.extend( [ 'Quark_' + str(var.format(particle='')) \
        for var in quark_extra_vars ] )

    branches.extend( [ var for var in separate_vars ] )



    # Create dictionaries to hold the information that will be
    # written as new branches
    variables      = {}
    variable_types = {}

    # Setup the output branches for the true object
    AH.addScalarBranches(variables,
                         variable_types,
                         output_tree,
                         branches,
                         datatype = 'float')


    ########################################
    # Event loop
    ########################################

    for input_root_file_name in config['input_root_file_list']:

        root_file_base = config["root_file_base"]

        # Input tree
        print root_file_base+input_root_file_name
        input_root_file = ROOT.TFile.Open(root_file_base+input_root_file_name)
        print input_root_file
        input_tree = input_root_file.Get(config['input_tree_name'].encode("ASCII"))
        print 'Processing {0}'.format(input_root_file_name)
        
        n_entries = input_tree.GetEntries()

        if config['Use_limited_entries']:
            n_processed = config['n_entries_limited']
        else:
            n_processed = n_entries
        print "Processing {0} events (out of {1} events)".format(n_processed, n_entries)

        for i_event in range(n_processed):

            if not i_event % int(0.05*n_processed+1):
                
                print "{0:.1f}% ({1} out of {2})".format(100.*i_event /n_processed, i_event, n_processed )

            input_tree.GetEntry( i_event )


            # Get quark and jet data - extra vars will be set as attributes

            tl_quarks = []

            for quarktype in quarktypes:
                tl_quarks.extend( Get_TLorentz( quarktype, input_tree, config ) )
                                
            tl_jets = []

            for jettype in jettypes:
                tl_jets.extend( Get_TLorentz( jettype, input_tree, config ) )


            ########################################
            # delR combinatorics
            ########################################

            if Just_Jets == True:
                # Don't perform linking if 'Just_Jets' parameter is true
                # In that case, just write all found jet data
                for jet in tl_jets:

                    variables['Jet_pt'][0] = jet.Pt()
                    variables['Jet_eta'][0] = jet.Eta()
                    variables['Jet_phi'][0] = jet.Phi()
                    variables['Jet_mass'][0] = jet.M()

                    variables['Jet_E'][0] = jet.E()
                    variables['Jet_mcE'][0] = jet.mcE

                    # Retrieve the extra variables from set attributes
                    for var in extra_jet_vars:
                        variables['Jet_'+var][0] = getattr( jet, var )

                    output_tree.Fill()
                continue
            
            # Otherwise, proceed with linking quarks and jets    
            [linked_jets, linked_quarks, delRs] = LinkJettoQuark(
                tl_jets, tl_quarks, config )

            # linked_jets and linked_quarks are (ordered) lists of TLorentzVectors. 
            # The extra variables are contained in attributes.


            ########################################
            # Write to file
            ########################################

            for jet, quark, delR in zip( linked_jets, linked_quarks, delRs):

                variables['Jet_pt'][0] = jet.Pt()
                variables['Jet_eta'][0] = jet.Eta()
                variables['Jet_phi'][0] = jet.Phi()
                variables['Jet_mass'][0] = jet.M()

                variables['Jet_E'][0] = jet.E()

                if config['Get_MC_for_jets']:
                    variables['Jet_mcE'][0] = jet.mcE

                variables['Quark_pt'][0] = quark.Pt()
                variables['Quark_eta'][0] = quark.Eta()
                variables['Quark_phi'][0] = quark.Phi()
                variables['Quark_mass'][0] = quark.M()

                variables['Quark_E'][0] = quark.E()

                variables['delR'][0] = delR

                # Retrieve the extra variables from set attributes
                for var in quark_extra_vars:
                    var = var.format(particle='')
                    variables[ 'Quark_'+ var ][0] = getattr( quark, var )
                    
                for var in jet_extra_vars:
                    var = var.format(particle='')
                    variables[ 'Jet_'+var ][0] = getattr( jet, var )

                output_tree.Fill()

        # Otherwise memory overflows!
        input_root_file.Close()


    output_root_file.Write()
    output_root_file.Close()

    ts = time.time()
    end_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    print config['info']
    print 'Analysis end time:              {0}'.format(end_date)
    print '.root file: {0}'.format( config['output_root_file_name'] )




########################################
# End of main
########################################   


if __name__ == "__main__":
    main()
