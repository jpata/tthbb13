#!/usr/bin/env python
"""

"""

########################################
# Imports
########################################

import os      
import sys     
import math
import pickle

import ROOT

from Axis import axis

ROOT.TH1.AddDirectory(0)

########################################
# Configuration
########################################

#SparseMEM_2015-10-02-1431
input_path = "/scratch/gregor/SparseMEM_2015-10-06-0941/"

signals = [
    "ttH_hbb", 
#    "ttH_nohbb"
]

backgrounds = [
    "ttbarPlus2B",
    "ttbarPlusB",
    "ttbarPlusBBbar",
    "ttbarPlusCCbar",
    "ttbarOther",
#    "ttw_wlnu",       
#    "ttw_wqq",        
#    "ttz_zllnunu",    
#    "ttz_zqq",
]        


########################################
# Categorization
########################################

class Categorization(object):

    """ Categorization: class for finding analysis categories.

    Three associated static objects:
    h_sig, h_bkg: Dictionaries of signal/background sparse histograms (THN objects)
    axes: A list of axis objects

    The cutflow is implemented as a binary tree. The cut member is
    the additional cut to perform for a given node. The total cut for
    a node is the sum of it's own cut and the cuts on all it's
    ancestors. The root node will not have any cut associated to it.

    A cut is a list of three numbers: 
    the axis, the leftmost included bin, the rightmost included bin

    Children are always created in pairs (d'uh - it's a binary tree) -
    one with a cut, the other one with it's inversion.
    """
        
    h_sig = None
    h_bkg = None
    axes = None

    def __init__(self, cut, parent=None):
        """ Create a new node """        
        self.parent = parent
        self.children = []
        self.cut = cut
        

    def split(self, iaxis, rightmost_of_left_bins):        
        """ Split a node using a cut on axis iaxis (index with respect
        to the list of axes: axes) at the bin number
        rightmost_of_left_bins. As the name implies the bin will be
        included in the 'left hand side' of the cut.

        Opposite of merge function
        
        Return nothing on success

        Return -1 if the requested splitting is impossible
        (because it is out of range or because previous cuts on
        ancestors of the node already exclude the requested region)
        """

        # Init all other boundaries with sanity check
        leftmost_of_left_bins = 1
        leftmost_of_right_bins = rightmost_of_left_bins + 1        
        if leftmost_of_right_bins > self.axes[iaxis].nbins:
            print "Invalid subdivision, leftmost_of_right_bins > self.axes[iaxis].nbins"
            return -1    
        rightmost_of_right_bins =  self.axes[iaxis].nbins
        
        # Get the list of all previous cuts on the ancestors
        # the order here is imporant - we have to execute the cuts from
        # TOP to BOTTOM
        # so the TIGHTEST cut on a given axis comes LAST
        all_previous_cuts = [p.cut for p in self.all_parents()] + [self.cut]

        # Loop over cuts to apply previous constraints
        for c in all_previous_cuts:
            # Make sure the cut is defined (ignore the root node) and
            # modifies the axis we are testing right now
            if c and c[0] == iaxis:

                if c[1] > leftmost_of_left_bins:
                    leftmost_of_left_bins = c[1]
                if c[1] > rightmost_of_left_bins:
                    rightmost_of_left_bins = c[1]

                if c[2] < leftmost_of_right_bins:
                    leftmost_of_right_bins = c[2]
                if c[2] < rightmost_of_right_bins:
                    rightmost_of_right_bins = c[2]
        # End of loop over cuts
        
        # Sanity check: make sure our cut is still doable after the
        # preselections have been applied
        if leftmost_of_right_bins <= rightmost_of_left_bins:
            print "leftmost_of_right_bins <= rightmost_of_left_bins"
            return -1
        if leftmost_of_right_bins > self.axes[iaxis].nbins:
            print "Invalid subdivision, leftmost_of_right_bins > self.axes[iaxis].nbins"
            return -1

        # And finally: actually spawn two new children and add the Nodes to the tree
        child_pass = Categorization([iaxis, leftmost_of_left_bins, rightmost_of_left_bins], parent=self)
        child_fail = Categorization([iaxis, leftmost_of_right_bins, rightmost_of_right_bins], parent=self)
        self.children = [child_pass, child_fail]


    def printTree(self, depth=0):    
        """ Print the node and all it's children recursively in a pretty way """

        if self.cut:
            axis = self.axes[self.cut[0]]
            
            binsize = (axis.xmax - axis.xmin)/(1.*axis.nbins)
            lower = axis.xmin + (self.cut[1]-1)*binsize
            upper = axis.xmin + (self.cut[2])*binsize

            print_string = "{0}: {1}..{2}".format(axis.name, lower, upper)
                                                  
        else:
            print_string = ""

        S,B = self.getSB()
        print "  " * depth,  print_string, "\t S={0:.1f}, B={1:.1f}, S/B={2:.2f} S/sqrt(S+B)={3:.2f}".format(S,B,S/B,S/math.sqrt(S+B))
        for c in self.children:
            c.printTree(depth+1)


    def getSB(self):
        """ Get the total signal and background counts after applying the cuts (+ancestors) for all the associated THNs. 

        Return a tuple of numbers: signal and background counts
        """

        self.prepareAllTHNs()        
        S = sum([x.Projection(0).Integral() for x in h_sig.values()])
        B = sum([x.Projection(0).Integral() for x in h_bkg.values()])
        return S,B


    def get_leaves(self):
        """ Return a list of leaves at or below the current node"""

        leaves = []
        if self.children:
            for c in self.children:
                leaves.extend(c.get_leaves())
        else:
            leaves.append(self)
            
        return leaves


    def all_parents(self):        
        """ Return a list of parents of the node. The higher up, the
        earlier they come in the list. Returns an empty list for the
        root Node."""

        if self.parent is not None:
            return self.parent.all_parents() + [self.parent] 
        else:
            return []
        

    def prepareAllTHNs(self):
        """ Prime all THN so a Projection call return the the
        histogram after all cuts (and all ancestors cuts) have been
        applied """
    
        # Get the list of all cuts to apply (own cuts + ancestors)
        # Order matters here. We want to execute  the oldest cuts first.
        # Otherwise SetRange could widen the selection again
        all_cuts = [p.cut for p in self.all_parents()] + [self.cut]

        # Loop over all histograms
        for thn in h_sig.values() + h_bkg.values():

            # First cut on the axes but ignore the overflow bin
            for iaxis, axis in enumerate(self.axes):            
                thn.GetAxis(iaxis).SetRange(1, axis.nbins)
                thn.GetAxis(iaxis).SetBit(ROOT.TAxis.kAxisRange)
            # end of loop over axes
        
            # Loop over cuts
            for c in all_cuts:
                if c: # this is just to handle the ROOT node
                    # And restirct the axis range
                    thn.GetAxis(c[0]).SetRange(c[1], c[2])
        # End of loop over histograms


    def merge(self):
        """ Undo a splitting. Opposite of split"""
        self.children = []

        
    def eval(self):
        """ Calculate the cost function of the tree. Squared sum of
        S/sqrt(S+B) over all leaves that are children/grand-children
        of this node """
        SBs = [l.getSB() for l in self.get_leaves()]

        # Make sure the denominators are all >0
        if any([sum(SB)==0 for SB in SBs]):
            return -1000

        sig  = math.sqrt(sum([math.pow(x[0],2)/(x[0]+x[1]) for x in SBs]))
        return sig

        
########################################
# Get All Sparse Histograms
########################################

h_sig = {}
h_bkg = {}

for signal in signals:
    f = ROOT.TFile(input_path + signal + ".root")
    h_sig[signal] = f.Get("foo")

for background in backgrounds:
    f = ROOT.TFile(input_path + background + ".root")
    h_bkg[background] = f.Get("foo")

for k,v in h_sig.iteritems():
    print k, v.GetEntries()
for k,v in h_bkg.iteritems():
    print k, v.GetEntries()


########################################
# Get the axes
########################################

if_axis = open(input_path + "axes.pickle","rb")
axes = pickle.load(if_axis)
if_axis.close()

for iaxis, axis in enumerate(axes):
    print iaxis, axis


########################################
# Init Categorization
########################################

Categorization.axes = axes
Categorization.h_sig = h_sig
Categorization.h_bkg = h_bkg

r = Categorization([])


########################################
# Do actual work
########################################

for i_iter in range(12):

    print "Doing iteration", i_iter

    best_sig = r.eval()        
    best_split = None
    second_best_sig = None

    # Loop over axes
    for iaxis, axis in enumerate(axes):

        print "Testing axis", iaxis

        # We don't want to split by the MEM variable
        if iaxis==0:
            continue

        # Loop over bins on the axis
        # (ROOT Histogram bin counting starts at 1)
        for split_bin in range(1, axis.nbins):

            # Loop over all leaves - these are the categories that we
            # could split further
            for l in r.get_leaves():

                # The split function executes the split
                # If it failed (return value of -1) - for example because the requested range is already excluded
                # we go to the next one
                if l.split(iaxis, split_bin)==-1:
                    continue

                # Test if the splitting increased the significance
                # Store if it helped
                sig = r.eval()
                if  sig > best_sig:
                    second_best_sig = best_sig
                    best_sig = sig                                        
                    best_split = [l, iaxis, split_bin] # remeber which category to split, on which axis, at which bin 

                # Undo the split
                l.merge()
            
            # End of loop over leaves
        # End of loop over histogram bins
    # End of loop over axes

    print "New Split:", best_sig, second_best_sig
    best_split[0].split(best_split[1],best_split[2])
    r.printTree()
# End if loop over iterations
