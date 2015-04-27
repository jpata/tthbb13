#!/usr/bin/env python
"""
Thomas: Reading tree for Transfer Function

"""


########################################
# Imports
########################################

import os
import ROOT
import TTH.TTHNtupleAnalyzer.AccessHelpers as AH
import pickle
import copy

from TFClasses import function

########################################
# Functions
########################################

def Make_E_axis( input_tree, eta_axis, n_E_bins, E_bounds, particle, config ):

    # Method:
    #  - Per eta bin, loop:
    #    - Get an E histogram from the input_tree, selected for eta and min/max E
    #    - Loop over the bins and sum up bin content
    #    - Once sum of bin content equals a fraction 1/n_E_bins of the total content,
    #      save the bin number as a boundary, and reset sum to 0
    
    # For this method to work, the content per bin should be << 1/n fraction of total
    # content. This is achieved by choosing a high number of bins (~50000 works well)


    # For convenience:
    n_eta_bins = len(eta_axis)-1

    E_axis = []
    E_values = []

    for i_eta in range(n_eta_bins):

        ########################################
        # Create a draw string and a selection string, and get the histogram
        ########################################
        
        # Selection string; filters for particle and E & eta range of bin
        sel_str = Make_sel_str(
            eta_axis[i_eta], eta_axis[i_eta+1],
            E_bounds[0], E_bounds[1],
            particle,
            config )

        # Histogram names should be unique for solid performance
        hist_name = "H{0}{1}".format( particle, i_eta )

        # The more bins chosen, the more precise the bin boundaries will be
        n_E_hist_bins = 50000

        # Store this number also in config
        config['n_E_hist_bins'] = n_E_hist_bins

        if config['Use_mc_values']: E_var = config['mc_E_str']
        else: E_var = config['quark_E_str']

        draw_str = "{0}>>{1}({2},{3},{4})".format(
            E_var,
            hist_name,
            n_E_hist_bins,
            E_bounds[0], E_bounds[1] )

        # Retrieve the histogram
        input_tree.Draw(draw_str, sel_str)
        E_hist = getattr(ROOT, hist_name).Clone()

        ########################################
        # Determine the bin boundaries
        ########################################

        E_entries = int(E_hist.GetEntries())

        entries_per_E_bin = E_entries / n_E_bins

        # Loop over histogram and determine E bin boundaries
        i = 0
        bin_sum = 0
        E_bin_boundaries = []

        for bin_cnt in range(1, n_E_bins):

            while bin_sum < bin_cnt * entries_per_E_bin:
                bin_sum += E_hist.GetBinContent(i)
                i += 1

            E_bin_boundaries.append( i )

        # Build the E_axis from the bin boundaries
        bin_width = E_hist.GetBinWidth(0)

        E_axis_this_eta = [ E_bounds[0] ]
        E_axis_this_eta.extend( [ E_bounds[0]+i*bin_width for i in E_bin_boundaries ] )
        E_axis_this_eta.append( E_bounds[1] )

        E_axis.append( E_axis_this_eta )

        ########################################
        # Determine the central or mean value of E bin
        ########################################

        # For the transfer function, it is necessary to have 1 single E value.
        # Either use the center of the bin ('c'), or the mean ('m')

        center_or_mean = 'm'

        config['E_value_mean_or_center'] = center_or_mean

        E_values_this_eta = []
        
        if center_or_mean =='m':

            i = 0
            bin_sum = 0
    
            for bin_cnt in range(1, n_E_bins+1):

                mean_sum = 0
                mean_entries = 0

                while bin_sum < bin_cnt * entries_per_E_bin and i < n_E_hist_bins:
                    bin_sum += E_hist.GetBinContent(i)
                    mean_sum += i*E_hist.GetBinContent(i)
                    mean_entries += E_hist.GetBinContent(i)
                    i += 1

                E_values_this_eta.append( 
                    mean_sum / mean_entries * bin_width + E_bounds[0] )

        if center_or_mean == 'c':

            for i in range(n_E_bins):
                E_values_this_eta.append(
                    ( E_axis_this_eta[i+1] + E_axis_this_eta[i] ) / 2 )


        E_values.append( E_values_this_eta )

    return ( E_axis, E_values )
        

def Make_sel_str( left_eta, right_eta, left_E, right_E, particle, config ):

    if config['Use_mc_values']:
        E_var = config['mc_E_str']
        part_var = config['mc_Flavour_str']
        eta_var = config['mc_Eta_str']
    else:
        E_var = config['quark_E_str']
        part_var = config['quark_Flavour_str']
        eta_var = config['quark_Eta_str']

    # Possible to build particle dictionary, so that it's also possible to give for
    # example 't' or 'light' as input.
    if particle in [ 'b', 'bottom' ]:
        part_str = "abs({0})==5 && ".format(part_var)
    elif particle in [ 'o', 'other', 'l', 'light' ]:
        part_str = "abs({0})!=5 && ".format(part_var)
    elif particle in [ 'a', 'all' ]:
        part_str = ''
    else:
        print "Use 'b', 'bottom', 'o', 'other', 'l' or 'light' for particle types"
        return
        
    eta_str = "abs({0})>={1} && abs({0})<={2} && ".format(eta_var, left_eta, right_eta)

    E_str = "abs({0})>={1} && abs({0})<={2}".format( E_var, left_E, right_E )

    if not 'selection_string' in config:
        config['selection_string'] = {}

    config['selection_string'][particle] = part_str + eta_str + E_str

    return part_str + eta_str + E_str


def Make_hist_mat( eta_axis, E_axis, particle, config ):

    n_E_bins = len(E_axis[0])-1
    n_eta_bins = len(eta_axis)-1

    # Initialize matrix
    hist_mat = [[ 0 for j in range(n_E_bins)] for i in range(n_eta_bins) ]

    # Initialize matrix to store number of bins and ranges for config file
    plot_ranges = [[ [0,0] for j in range(n_E_bins)] for i in range(n_eta_bins) ]
    plot_bins = [[ 0 for j in range(n_E_bins)] for i in range(n_eta_bins) ]

    for i_eta in range(n_eta_bins):
        for i_E in range(n_E_bins):

            plottitle = "{4}  |  eta: {0} to {1}  |  {5}: {2} to {3}".format(
                "%.2f" % eta_axis[i_eta], "%.2f" % eta_axis[i_eta+1],
                "%.2f" % E_axis[i_eta][i_E], "%.2f" % E_axis[i_eta][i_E+1],
                particle,
                config['E_or_Pt_str'] )

            number_of_bins = 100
            min_x = 0
            max_x = 2*E_axis[i_eta][i_E+1]

            hist_mat[i_eta][i_E] = ROOT.TH1F(
                '{2}-hist{0}-{1}'.format( i_eta, i_E, particle ),
                plottitle, number_of_bins, min_x, max_x )

            plot_ranges[i_eta][i_E] = [ min_x, max_x ]
            plot_bins[i_eta][i_E] = number_of_bins

    # Write number_of_bins and plot_ranges to the config dict
    if not 'SBF_plot_ranges' in config:
        config['SBF_plot_ranges'] = {}
    if not 'SBF_n_bins' in config:
        config['SBF_n_bins'] = {}

    config['SBF_plot_ranges'][particle] = plot_ranges
    config['SBF_n_bins'][particle] = plot_bins

    return hist_mat


########################################
# Make_Histograms
########################################

def Make_Histograms():

    ########################################
    # Get the configuration file
    ########################################

    if not os.path.isfile('config.dat'):
        print "Error: Can't find configuration file config.dat"
        return 0

    print 'Importing configuration data'
    pickle_f = open( 'config.dat', 'rb' )
    config = pickle.load( pickle_f )
    pickle_f.close()

    ########################################
    # Fill in default values if entries don't exist
    ########################################

    # Specify default input
    default_dict = {}

    default_dict['input_root_file_name'] = 'Just_Jets.root'
    default_dict['input_tree_name'] = 'tree'
    default_dict['outputdir'] = "EtoE-test"
    default_dict['Use_mc_values'] = True
    default_dict['eta_axis'] = [ 0.0 , 1.0 , 2.5 ]
    default_dict['n_E_bins'] = 58
    default_dict['E_bounds'] = [ 30.0, 300.0 ]
    default_dict['particles'] = [ 'b', 'l' ]

    default_dict['bin_functions'] = []
    # Initialize a single Gaussian for every eta bin for every particle by default
    for i_part in range( len( default_dict['particles'] ) ):

        bin_functions_this_part = []

        for i_eta in range( len( default_dict['eta_axis'] )-1 ):

            bin_functions_this_part.append( function(
                "[0]*exp(-0.5*((x-[1])/[2])**2)",
                [ "0", "mean", "rms" ] ) )

        default_dict['bin_functions'].append( bin_functions_this_part )

    # Check if keys of default input exist in config
    for key in default_dict.keys():
        if key not in config:
            print 'Using ',default_dict[key],' for ',key
            config[key] = default_dict[key]

    # Upon initialization, check if function and initialization parameters are
    # properly matched (1 initialization for every parameter in the function)
    for particle in default_dict['particles']:
        for i_eta in range( len( default_dict['eta_axis'] )-1 ):
            if config['bin_functions'][particle][i_eta].Check_function():
                return

    ########################################
    # Program setup
    #  - Read .root file
    #  - Create the directories if necessary
    #  - Setup some objects for the rest of the program
    ########################################

    # Read .root file and setup some root specifics
    input_root_file_name = config['input_root_file_name']
    input_tree_name = config['input_tree_name']

    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")
    ROOT.gStyle.SetOptFit(1011)

    print 'Reading {0}'.format(input_root_file_name)
    input_root_file = ROOT.TFile(input_root_file_name)
    input_tree = input_root_file.Get(input_tree_name)

    outputdir = config['outputdir']

    if not os.path.isdir(outputdir):
        os.makedirs(outputdir)

    # Energy is by default considered the parton energy, Quark_E.
    # With Use_mc_values = True, the mc values are used instead of quark values
    Use_mc_values = config['Use_mc_values']

    # eta_axis: first value is the left bound of the first bin,
    # last value is right bound of the last bin.
    eta_axis = config['eta_axis']

    # number of bins is determined from the given eta_axis
    n_eta_bins = len(eta_axis)-1

    # Set the desired number of E bins; the axis is the dynamically determined
    n_E_bins = config['n_E_bins']
    
    # Fix the left and right bound of the E axis
    E_bounds = config['E_bounds']

    particles = config['particles']

    for particle in particles:

        if not os.path.isdir( outputdir + '/' + particle ):
            os.makedirs( outputdir + '/' + particle )

        if not os.path.isdir( outputdir + '/' + particle + 'png' ):
            os.makedirs( outputdir + '/' + particle + 'png' )

    # List of dicts per particle, in which a matrix of histograms will be stored
    dicts = {}

    for particle in particles:
        
        dic = {}

        dic['type'] = particle
        dic['eta_axis'] = eta_axis
        dic['n_eta_bins'] = n_eta_bins
        dic['n_E_bins'] = n_E_bins
        dic['E_bounds'] = E_bounds

        print 'Creating E_axis for {0}'.format(particle)
        ( dic['E_axis'], dic['E_values'] ) = Make_E_axis(
            input_tree,
            dic['eta_axis'],
            dic['n_E_bins'],
            dic['E_bounds'],
            particle,
            config )

        print 'Creating matrix of histrograms for {0}'.format(particle)
        dic['hist_mat'] = Make_hist_mat(
            dic['eta_axis'], dic['E_axis'], particle, config )

        dicts[particle] = dic
        

    ########################################
    # Event loop
    ########################################
    
    n_entries = input_tree.GetEntries()
    config['n_total_events'] = n_entries
    config['events_used'] = 0

    if config['Use_limited_entries']:
        n_processed = config['n_entries_limited']
    else:
        n_processed = n_entries
    print "Processing {0} events (out of {1} events)".format(n_processed, n_entries)

    for i_event in range(n_processed):

        if not i_event % 5000:
            print "{0:.1f}%".format( 100.*i_event /n_processed)

        input_tree.GetEntry( i_event )

        if Use_mc_values:
            E_event = AH.getter(input_tree, config['mc_E_str'])
            eta_event = AH.getter(input_tree, config['mc_Eta_str'])
            particle_event = AH.getter(input_tree, config['mc_Flavour_str'])
        else:
            E_event = AH.getter(input_tree, config['quark_E_str'])
            eta_event = AH.getter(input_tree, config['quark_Eta_str'])
            particle_event = AH.getter(input_tree, config['quark_Flavour_str'])

        E_reconstructed = AH.getter( input_tree, config['reco_E_str'] )


        if E_event >= E_bounds[0] and E_event <= E_bounds[1] and eta_event >= eta_axis[0] and eta_event <= eta_axis[-1]:

            # Keep track of the number of actually used events in the config dict
            config['events_used'] += 1

            # Select the right dict
            if abs(particle_event) == 5:
                particle = particles[0]
            else:
                particle = particles[1]

            # Get bin numbers
            eta_bin_nr = 0
            while abs(eta_event) > dicts[particle]['eta_axis'][eta_bin_nr+1]:
                eta_bin_nr += 1

            E_bin_nr = 0
            while E_event > dicts[particle]['E_axis'][eta_bin_nr][E_bin_nr+1]:
                E_bin_nr += 1

            # Fill the reconstucted E into the histogram
            dicts[particle]['hist_mat'][eta_bin_nr][E_bin_nr].Fill( E_reconstructed )

    ########## End of event loop ###########


    # Export the dictionary of histrograms to pickle file
    print 'Writing single bin histograms to {0}.dat'.format(
        config['SBF_hists_pickle_filename'] )
    pickle_f = open( config['SBF_hists_pickle_filename'], 'wb' )
    pickle.dump( dicts, pickle_f )
    pickle_f.close()


    ########################################
    # Adding extra info to config.dat
    ########################################   

    print 'Adding single bin fit information to config.dat'
    pickle_f = open( 'config.dat', 'wb' )
    pickle.dump( config, pickle_f )
    pickle_f.close()



########################################
# End of Make_Histograms
########################################   

def main():
    Make_Histograms()

if __name__ == "__main__":
    main()
