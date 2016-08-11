#!/usr/bin/env python
"""
Thomas:

This program creates cfg_outputtree.dat, which contains a dictionary of all
relevant input and parameters for outputtree-strict.py.

"""

########################################
# Imports
########################################

import pickle, json
import os
import shutil
import sys

import time
import datetime

import TTH.MEAnalysis.samples as samples
import TTH.MEAnalysis.samples_base as samples_base

########################################
# Main
########################################

def Make_config(do_subjets=False):

    config = {}

    ########################################
    # Information concerning this config file
    ########################################

    ts = time.time()
    config['date'] = datetime.datetime.fromtimestamp(ts).strftime(
        '%Y-%m-%d %H:%M:%S')

    config['info'] = '*** Information on this config.dat ***\n'\
    'This config file contains the configuration data used for outputtree.py,'\
    ' which translates a VHBB Ntuple to a format readable by readtree.py. \n\n'\
    'This config.dat was created on: {0}'.format(config['date'])


    ########################################
    # I/O information
    ########################################

    config['input_tree_name'] = 'vhbb/tree'

    #the path to the root files
    config["root_file_base"] = samples_base.site_prefix

    # The config file will be copied to 'runs/{config['run_name']}'
    config['run_name'] = "Jul13_pilot_v1"
    if do_subjets:
        config['run_name'] += "_subjet"
    else:
        config['run_name'] += "_resolved"

    config['output_root_file_name'] = 'out.root'


    ########################################
    # Program parameters
    ########################################

    # Use only a part of the input root file
    config['Use_limited_entries'] = False

    # Specify the number of entries if only a limited number of entries is used
    #   This number is not used if Use_limited_entries is set to False
    config['n_entries_limited'] = 10000

    # Specify whether the program should attempt to find MC branches for the jets
    config['Get_MC_for_jets'] = False

    # Specify whether the program should link with quarks.
    #   If this is set to True, the program will not save any quark data, and the
    #   the user should calculate TFs with the MC values of the jets. Make sure
    #   config['Get_MC_for_jets'] is set to True if this is set to True.
    config['Dont_Link_Just_Jets'] = False

    # Specify whether the program should look for a closely matched second quark.
    #   If two quarks could both be matched to a jet, it usually better to remove 
    #   these quarks and this jet altogether, in order to prevent faulty matching.
    config['Remove_double_match'] = True


    ########################################
    # Branch info
    ########################################

    # Specify the names of the particles of with pt, eta, phi and m should be
    # extracted. 
    #   - pt, eta, phi and mass are extracted by default. A branch E is created by
    #     default - it is calculated with the use of pt, eta, phi and mass.
    #   - Since the notation '_pt' is common but not *standard*, it is necessary to
    #     to add underscores where necessary manually.

    config['quarktypes'] = ['GenBQuarkFromTop_', 'GenBQuarkFromH_', 'GenWZQuark_' ]
    
    #enable this for resolved jets
    if not do_subjets:
        config['jettypes'] = [ 'Jet_' ]
    else: 
        config['jettypes'] = [ 'httCandidates_sjW1', 'httCandidates_sjW2',
            'httCandidates_sjNonW'
        ]

    # Specify which branches *other* than pt, eta, phi, mass and E should be 
    # extracted.
    #   - This should be FULL branch names, e.g. httCandidates_fW
    #   - If the extra variable is particle-specific, write '{particle}' in front
    #     it. For example: '(a quark)pdgId' can be written as '{particle}pdgId'

    config['quark_extra_vars'] = [
        '{particle}pdgId',
        #'{particle}charge',
        #'{particle}status',
        ]
    
    if not do_subjets:
        config['jet_extra_vars'] = [
            '{particle}hadronFlavour',
            '{particle}btagCSV',
            '{particle}btagBDT',
        ]
    else:
        config['jet_extra_vars'] = [
             'httCandidates_pt',
             'httCandidates_eta',
             'httCandidates_phi',
             'httCandidates_mass',
             'httCandidates_fRec',
        ]
    
    ########################################
    # Cutoff criteria
    ########################################

    # format of 1 cutoff criterium: ( varname, operator sign, cutoff value )
    #   Note: Only defined variable names can be used here!


    config['jet_cutoff_list'] = [
        ( '{particle}pt'       , '>' , 30.0 ),
        #( 'httCandidates_pt'   , '>' , 200.0 ),
        #( 'httCandidates_mass' , '>' , 120.0 ),
        #( 'httCandidates_mass' , '<' , 220.0 ),
        #( 'httCandidates_fW'   , '<' , 0.175 ),
        ]

    config['quark_cutoff_list'] = [
        ( '{particle}pt'       , '>' , 30.0 ) ]


    #matching dR between gen and reco
    config['max_link_delR'] = 0.3
    
    # Only used if config['Remove_double_match'] is set to True
    # if another match closer than dR, remove entire jet
    config['max_sec_delR'] = 0.5


    ########################################
    # Write configuration to file:
    ########################################

    f = open( 'cfg_outputtree.dat', 'wb' )
    json.dump( config , f, indent=2, encoding="ascii", ensure_ascii=True)
    f.close()
    
    
    if not os.path.isdir( 'runs/{0}'.format(config['run_name'] ) ):
        os.makedirs('runs/{0}'.format(config['run_name'] ))
        
    shutil.copyfile( 'cfg_outputtree.dat',
        'runs/{0}/cfg_outputtree.dat'.format( config['run_name'] ) )
    
    shutil.copyfile( 'cfg_outputtree.py',
        'runs/{0}/cfg_outputtree.py'.format( config['run_name'] ) )
    
    print "cfg_outputtree.dat created"



########################################
# End of Main
########################################
def main():
    Make_config(do_subjets=True)
    Make_config(do_subjets=False)

if __name__ == "__main__":
  main()
