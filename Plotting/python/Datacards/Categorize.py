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
from multiprocessing import Pool

import ROOT

from Axis import axis
from CombineHelper import get_limit
from makeDatacard import MakeDatacard

ROOT.TH1.AddDirectory(0)


########################################
# Configuration
########################################

input_file = "/shome/jpata/tth//datacards/Oct7_sparse/ControlPlots.root"

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
# Cut
########################################

class Cut(object):
    """ Helper class: simple cut that knows the number of the axis
    (wrt/ to the static axes list) and the low (lo) and high (hi) bin
    to include.
    """
    
    axes = None

    def __init__(self, axis=-1, lo=-1, hi=-1):            
        self.axis = axis
        self.lo = lo
        self.hi = hi
        
    def __nonzero__(self):
        if self.axis == -1:
            return False
        else:
            return True

    def __repr__(self):

        if self.axis >= 0:
            axis = self.axes[self.axis]            
            binsize = (axis.xmax - axis.xmin)/(1.*axis.nbins)
            lower = axis.xmin + (self.lo-1)*binsize
            upper = axis.xmin + (self.hi)*binsize
            
            # Binsize of 1 means we have integer bins 
            if binsize==1.:
                lower = int(lower)
                upper = int(upper)
            
            return "{0}__{1}__{2}".format(axis.name, lower, upper).replace(".","_").replace("-","m")
                
        else:
            return ""


        
        
########################################
# Categorization
########################################

class Categorization(object):

    """ Categorization: class for finding analysis categories.

    Associated static objects:
    h_sig, h_bkg: Dictionaries of signal/background sparse histograms
        (THN objects): key = sample
    h_sig_sys, h_bkg_sys: Nested Dictionaries of signal/background
        sparse histograms (THN objects) keys = sample, syst
    axes: A list of axis objects

    The cutflow is implemented as a binary tree. The cut member is the
    additional cut to perform for a given node (Cut type object).  The
    total cut for a node is the sum of it's own cut and the cuts on
    all it's ancestors. The root node will not have any cut associated
    to it.

    Children are always created in pairs (d'uh - it's a binary tree) -
    one with a cut, the other one with it's inversion.
    """
        
    h_sig = None
    h_bkg = None

    h_sig_sys = None
    h_bkg_sys = None

    axes = None

    pool = Pool(10)

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
            if c and c.axis == iaxis:

                if c.lo > leftmost_of_left_bins:
                    leftmost_of_left_bins = c.lo
                if c.lo > rightmost_of_left_bins:
                    rightmost_of_left_bins = c.lo

                if c.hi < leftmost_of_right_bins:
                    leftmost_of_right_bins = c.hi
                if c.hi < rightmost_of_right_bins:
                    rightmost_of_right_bins = c.hi
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
        child_pass = Categorization(Cut(iaxis, leftmost_of_left_bins, rightmost_of_left_bins), parent=self)
        child_fail = Categorization(Cut(iaxis, leftmost_of_right_bins, rightmost_of_right_bins), parent=self)
        self.children = [child_pass, child_fail]


    def print_tree(self, depth=0):    
        """ Print the node and all it's children recursively in a pretty way """

        S,B = self.get_sb()
        print "   " * depth, self.cut, "S={0:.1f}, B={1:.1f}, S/sqrt(S+B)={2:.2f}".format(S,B,S/math.sqrt(S+B))
        for c in self.children:
            c.print_tree(depth+1)


    def get_sb(self):
        """ Get the total signal and background counts after applying
        the cuts (+ancestors) for all the associated THNs.

        Return a tuple of numbers: signal and background counts
        """

        self.prepare_nominal_thns()        
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

    def get_root(self):
        """ Return the root node of the tree"""

        if self.parent is not None:
            return self.parent.get_root()
        else:
            return self


    def all_parents(self):        
        """ Return a list of parents of the node. The higher up, the
        earlier they come in the list. Returns an empty list for the
        root Node."""

        if self.parent is not None:
            return self.parent.all_parents() + [self.parent] 
        else:
            return []
        

    def prepare_nominal_thns(self):
        """ Prime nominal (no systematics) THNs for projection """
        thns = h_sig.values() + h_bkg.values()
        self.prepare_thns(thns)


    def prepare_all_thns(self):
        """ Prime nominal and systematic variation THNs for projection """
        
        # Nominal
        thns = h_sig.values() + h_bkg.values() 
        
        # Systematic variations
        # (these nested dictionaries)
        for v in h_sig_sys.values() + h_bkg_sys.values():
            thns.extend(v.values())

        self.prepare_thns(thns)


    def prepare_thns(self, thns):
        """ Prime THNs so a Projection call return the the
        histogram after all cuts (and all ancestors cuts) have been
        applied """
    
        # Get the list of all cuts to apply (own cuts + ancestors)
        # Order matters here. We want to execute  the oldest cuts first.
        # Otherwise SetRange could widen the selection again
        all_cuts = [p.cut for p in self.all_parents()] + [self.cut]

        # Loop over all histograms
        for thn in thns:

            # First cut on the axes but ignore the overflow bin
            for iaxis, axis in enumerate(self.axes):            
                thn.GetAxis(iaxis).SetRange(1, axis.nbins)
                thn.GetAxis(iaxis).SetBit(ROOT.TAxis.kAxisRange)
            # end of loop over axes
        
            # Loop over cuts
            for c in all_cuts:
                if c: # this is just to handle the ROOT node
                    # And restirct the axis range
                    thn.GetAxis(c.axis).SetRange(c.lo, c.hi)
        # End of loop over histograms


    def merge(self):
        """ Undo a splitting. Opposite of split"""
        self.children = []

        
    def eval(self):
        """ Calculate the cost function of the tree. Squared sum of
        S/sqrt(S+B) over all leaves that are children/grand-children
        of this node """
        SBs = [l.get_sb() for l in self.get_leaves()]

        # Make sure the denominators are all >0
        if any([sum(SB)==0 for SB in SBs]):
            return -1000

        sig  = math.sqrt(sum([math.pow(x[0],2)/(x[0]+x[1]) for x in SBs]))
        return sig

    
    def find_categories(self, n=6):
        """Define binning, maximizing eval() at each step """

        for i_iter in range(n):
            print "Doing iteration", i_iter

            best_sig = self.eval()        
            best_split = None
            second_best_sig = None

            # Loop over axes
            for iaxis, axis in enumerate(self.axes):

                print "Testing axis", iaxis

                # We don't want to split by the MEM variable
                if iaxis==0:
                    continue

                # Loop over bins on the axis
                # (ROOT Histogram bin counting starts at 1)
                for split_bin in range(1, axis.nbins):

                    # Loop over all leaves - these are the categories that we
                    # could split further
                    for l in self.get_leaves():

                        # The split function executes the split
                        # If it failed (return value of -1) - for example because the requested range is already excluded
                        # we go to the next one
                        if l.split(iaxis, split_bin)==-1:
                            continue

                        # Test if the splitting increased the significance
                        # Store if it helped
                        sig = self.eval()
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
            self.print_tree()
        # End of loop over iterations


    def find_categories_async(self, n, limit_fun):

        for i_iter in range(n):
            print "Doing iteration", i_iter

            splittings = {}
            i_splitting = 0

            # Loop over axes
            for iaxis, axis in enumerate(self.axes):

                print "Testing axis", iaxis

                # We don't want to split by the MEM variable
                if iaxis==0 or iaxis>3:
                    continue

                # Loop over bins on the axis
                # (ROOT Histogram bin counting starts at 1)
                for split_bin in range(1, axis.nbins):

                    # Loop over all leaves - these are the categories that we
                    # could split further
                    for l in self.get_leaves():

                        # The split function executes the split
                        # If it failed (return value of -1) - for example because the requested range is already excluded
                        # we go to the next one
                        if l.split(iaxis, split_bin)==-1:
                            continue
                            
                        splitting_name = "iter_{0}_cats_{1}".format(i_iter, i_splitting)
                            
                        # make the datacard here
                        # create control plots creates the control plots for the whole tree 
                        control_plots_filename = "/scratch/gregor/foobar/ControlPlots_{0}.root".format(splitting_name)
                        shapes_root_filename   = "/scratch/gregor/foobar/shapes_{0}.txt".format(splitting_name)
                        shapes_txt_filename    = "/scratch/gregor/foobar/shapes_{0}.root".format(splitting_name)

                        l.create_control_plots(control_plots_filename)
                        
                        print "Make datacard"

                        MakeDatacard(control_plots_filename, 
                                     shapes_root_filename,
                                     shapes_txt_filename,
                                     do_stat_variations=True)

                        print "done making datacard"
                            
                        splittings[shapes_txt_filename] = [l, iaxis, split_bin]
      
                        # Undo the split
                        l.merge()

                    # End of loop over leaves
                # End of loop over histogram bins
            # End of loop over axes

            # Extract a list todo and pass them to the limit calculation
            li_splittings = splittings.keys()
            li_limits = self.pool.map(limit_fun, li_splittings)
            
            # build a list of tuples with limit name and numerical value
            li_name_limits = [(name,limit) for name,limit in zip(li_splittings, li_limits)]
            # sort by limit and take the lowest/best one
            best_splitting_name, best_limit = sorted(li_name_limits, key = lambda x:x[1])[0]
            best_split = splittings[best_splitting_name]

            print "New Split:", best_limit
            best_split[0].split(best_split[1],best_split[2])
            self.print_tree()
        # End of loop over iterations



    def __repr__(self):
        """Printing a category returns its name. The name is built
        from the cuts of this category and its ancestors"""
        
        all_cuts = [p.cut for p in self.all_parents()] + [self.cut]
        
        # The name of a bin is the sum of all cuts
        # -we want the axes in the order the cutflow goes
        # -BUT only list the tightest cut
        
        # First just extract the order of axes
        axes_order = [c.axis for c in all_cuts if c]
        unique_axes = []
        for ia, a in enumerate(axes_order):
            if not a in axes_order[:ia]:
                unique_axes.append(a)
        
        unique_cuts = []
        for a in unique_axes:
            unique_cuts.append( [c for c in all_cuts if c.axis == a][-1])
        
        return "__".join([c.__repr__() for c in unique_cuts])


    def create_control_plots(self, name):

        print "Entering create.."

        of = ROOT.TFile(name, "RECREATE")

        root = self.get_root()

        dirs = {}
        
        print "Projecting"
        
        # Loop over categories
        for l in root.get_leaves():

            print l
            l.prepare_all_thns()

            # Nominal
            for process, thn in self.h_sig.items() + self.h_bkg.items():        

                # Get the output directory (inside the TFile)
                outdir_str = "{0}/{1}".format(process, l)
                if not outdir_str in dirs.keys():
                    dirs[outdir_str] = []
                
                h = thn.Projection(0).Clone()
                h.SetName(axes[0].name)
                dirs[outdir_str].append(h)                
            # End of loop over processes

            # Systematic Variations
            for process, hs in self.h_sig_sys.items() + self.h_bkg_sys.items():

                # Get the output directory (inside the TFile)
                outdir_str = "{0}/{1}".format(process, l)
                if not outdir_str in dirs.keys():
                    dirs[outdir_str] = []

                for sys_name, thn in hs.items():
                    h = thn.Projection(0).Clone()
                    h.SetName(axes[0].name + "_" + sys_name)
                    dirs[outdir_str].append(h)

                # End of loop over systematics
            # End of loop over processes
        # End of loop over categories
        
        print "Storing"

        for outdir_str, hs in dirs.iteritems():
                        
            of.mkdir(outdir_str)
            outdir = of.Get(outdir_str)

            for h in hs:
                h.SetDirectory(outdir)
            outdir.Write("", ROOT.TObject.kOverwrite)
        of.Close()

        print "Done storing histos"    
        
########################################
# Get All Sparse Histograms
########################################

f = ROOT.TFile(input_file)

h_sig = {}
h_bkg = {}
h_sig_sys = {}
h_bkg_sys = {}

for processes, h, h_sys in zip( [signals,   backgrounds],
                                [h_sig,     h_bkg],
                                [h_sig_sys, h_bkg_sys] ):
    for process in processes:

        # Nominal Histograms
        h[process] = f.Get("{0}/sl/sparse".format(process))
        print process, h[process].GetEntries()

        # Systematic Variations
        h_sys[process] = {}     
        for key in f.Get("{0}/sl".format(process)).GetListOfKeys():

            if not "sparse_" in key.GetName():
                continue
             
            syst_name = key.GetName().replace("sparse_", "")
            h_sys[process][syst_name] = f.Get("{0}/sl/{1}".format(process, key.GetName()))

        # End loop over keys
    # End loop over processes
# End Signal/Background loop
            

########################################
# Extract axes from a histogram
########################################

axes = []
n_dim = h_sig["ttH_hbb"].GetNdimensions()
print "We have", n_dim, "dimensions"
for i_axis in range(n_dim):
    a = h_sig["ttH_hbb"].GetAxis(i_axis)
    new_axis = axis(a.GetName(), a.GetNbins(), a.GetXmin(), a.GetXmax())
    axes.append(new_axis)
    print i_axis, new_axis


########################################
# Categorization
########################################

Cut.axes = axes
Categorization.axes = axes
Categorization.h_sig = h_sig
Categorization.h_bkg = h_bkg
Categorization.h_sig_sys = h_sig_sys
Categorization.h_bkg_sys = h_bkg_sys

r = Categorization(Cut())
r.find_categories_async(3, get_limit)

#r.split(4, 15)
#r.children[0].split(1,1)
#r.children[1].split(1,1)


