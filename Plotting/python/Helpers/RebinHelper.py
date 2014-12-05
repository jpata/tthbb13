#!/usr/bin/env python
"""
Helper script to rebin ROOT TH1 histograms
"""

########################################
# Imports
########################################

import array
import sys


########################################
# rebinHistos
########################################

# Count the newly created histograms
rebin_cnt = 0

def rebinHistos( hs, combine_bins):
    """ Rebin Histograms.
    Arguments:
    hs: either one TH1 or a list of TH1s
    combine_bins: list of bins to merge. 

    Important: the content is re-scaled! So if two bins are merged the content
      and the error are divided by two.

    Explanation:
      If we have a histogram with 50 bins of 1 GeV width. Then
      50*[1] will leave it unchanged
      25*[2] will gives use 25 bins, each a merge two->one
      and
      20*[2]+2*[5] will merge the first 40 two->one, and the remaining 10 five->one
      We sum of products always have to be the initial number of bins

    The return value will always be a list of new histograms (the
    passed histograms should not be changed). If only one histogram is
    given instead of a list then still a list is returned (but with
    only one element).    
   """

    # Allow treating individual histograms and lists of hisograms in
    #  the same way
    if not isinstance(hs,list):
        hs = [hs]

    # check if we have the correct number of bins
    if not sum(combine_bins) == hs[0].GetNbinsX():
        print hs[0].GetName()
        print "The bins dont match! Have: ", hs[0].GetNbinsX(), " but list for ", sum(combine_bins)
        print "-> Exit.."
        sys.exit()
    else:
        # The array rebin function creates new histograms. We use this global
        #  counter to give them unique names
        global rebin_cnt

        # translate bin numbers to combine into boundaries
        width   = hs[0].GetXaxis().GetBinWidth(4)
        minimum = hs[0].GetXaxis().GetXmin()

        boundaries = []
        boundaries.append( minimum )
        for x in combine_bins:
            boundaries.append( minimum+x*width )
            minimum += x*width

        # convert the list into an array
        bound_array = array.array( 'd', boundaries )

        # rebin and create new histograms
        hs_new = [x.Rebin( len(combine_bins), "rebin"+str(rebin_cnt), bound_array) for x in hs]
        rebin_cnt += 1

        # give them the same names as the old histograms
        [ hs_new[i].SetName(hs[i].GetName()) for i in range(len(hs)) ]

        # rescale content and error
        for h in hs_new:
            for i, factor in enumerate( combine_bins ):
                cont = h.GetBinContent(i+1 )
                err  = h.GetBinError(i+1 )
                if cont:
                    h.SetBinContent( i+1, 1.*cont/factor )
                    h.SetBinError( i+1, 1.*err/factor )
            # end of loop over bins
        # end of loop over histograms

        return hs_new

    # end of else for not sum(combine_bins) == hs[0].GetNbinsX():
# end of rebinHistos
