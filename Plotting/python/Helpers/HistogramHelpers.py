#!/usr/bin/env python
"""
Helpers to deal with variables/ROOT histograms
"""

########################################
# Imports and configs
########################################

import ROOT

# Global variable to count drawn histograms for unique naming
h_draw = 0 


########################################
# Count
########################################

def Count(tree, cut):
    """ Count the number of events passing a given cut string. If the
    cut contains a wait then take it into account.  This means looking
    at the integral and not at GetEntries """

    global h_draw

    # Set a new for the new histogram
    tmp_name = "helpertmp{0}".format(h_draw)
    h_draw += 1
    
    # Draw and get histogram
    tree.Draw("(1)>>"+tmp_name, cut)
    h = getattr(ROOT, tmp_name).Clone()
    
    return h.Integral()
# End Count
                                         
