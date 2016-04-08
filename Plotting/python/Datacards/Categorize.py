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
import copy
import numpy as np

from collections import OrderedDict

import ROOT

from Axis import axis
from Cut import Cut

from makeDatacard import MakeDatacard2
from datacardCombiner import makeStatVariations, fakeData

ROOT.TH1.AddDirectory(0)
ROOT.TH1.SetDefaultSumw2(True)
        
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
    pool: A pool of workers (multiprocessing module)
    output_path: Pathname where to store temporary files
    lg: LimitGetter object (takes care of calling combine)
    verbose: Verbosity level (int)


    The cutflow is implemented as a binary tree. The cut member is the
    additional cut to perform for a given node (Cut type object).  The
    total cut for a node is the sum of it's own cut and the cuts on
    all it's ancestors. The root node will not have any cut associated
    to it.

    Children are always created in pairs (d'uh - it's a binary tree) -
    one with a cut, the other one with it's inversion. However we can
    set the discriminator variable to -1 so the node is not evaluated
    """
        
    h_sig = None
    h_bkg = None

    h_sig_sys = None
    h_bkg_sys = None

    #OrderedDict
    axes = None

    pool = None
    output_path = None

    lg = None

    verbose = 0

    #Cache of all projected histograms
    allhists = {}    
    leaf_files = {}
    event_counts = {}

    #scale all histograms by this factor
    scaling = 1.0

    def __init__(self, cut, parent=None, discriminator_axis=0):
        """ Create a new node """        
        self.parent = parent
        self.children = []
        self.cut = cut
        self.discriminator_axis = discriminator_axis
        self.rebin_discriminator = 0
        self.iteration_results = []
    # Allow directly accessing the children
    def __getitem__(self, key):
        return self.children[key]

    def split(self, 
              axis_name, 
              rightmost_of_left_bins, 
              discriminator_axis_child_0,
              discriminator_axis_child_1):        
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
        if leftmost_of_right_bins > self.axes[axis_name].nbins:
            if self.verbose:
                print "Invalid subdivision, leftmost_of_right_bins > self.axes[axis_name].nbins"
            return -1    
        rightmost_of_right_bins =  self.axes[axis_name].nbins

        # Get the list of all previous cuts on the ancestors
        # the order here is imporant - we have to execute the cuts from
        # TOP to BOTTOM
        # so the TIGHTEST cut on a given axis comes LAST
        all_previous_cuts = [p.cut for p in self.all_parents()] + [self.cut]

        
        # Loop over cuts to apply previous constraints
        for c in all_previous_cuts:
            # Make sure the cut is defined (ignore the root node) and
            # modifies the axis we are testing right now
            if c and c.axis.name == axis_name:

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
            if self.verbose:
                print "leftmost_of_right_bins <= rightmost_of_left_bins"
            return -1
        if leftmost_of_right_bins > self.axes[axis_name].nbins:
            if self.verbose:
                print "Invalid subdivision, leftmost_of_right_bins > self.axes[axis_name].nbins"
            return -1


        # Sanity check if the requested discriminator variable is defined for both children
        # First get all the cuts, including the one we would apply for the children
        all_cuts_child_0 = all_previous_cuts + [Cut(axis_name, leftmost_of_left_bins, rightmost_of_left_bins)  ]
        all_cuts_child_1 = all_previous_cuts + [Cut(axis_name, leftmost_of_right_bins, rightmost_of_right_bins)]
        
        # Get the prerequisites for the requested discriminators
        if not discriminator_axis_child_0 is None:
            prereqs_for_child_0 = self.axes[discriminator_axis_child_0].discPrereq
            if not all([any([c.is_subset_of(p) for c in all_cuts_child_0]) for p in prereqs_for_child_0]):
                return -1
        if not discriminator_axis_child_1 is None:
            prereqs_for_child_1 = self.axes[discriminator_axis_child_1].discPrereq
            if not all([any([c.is_subset_of(p) for c in all_cuts_child_1]) for p in prereqs_for_child_1]):
                return -1

        # We want for ALL prerequisits that at LEAST ONE is as tight as the prerequiste
        # all([]) returns True - so this also works if there are no prerequs        
                
        # And finally: actually spawn two new children and add the Nodes to the tree
        child_pass = Categorization(Cut(axis_name, leftmost_of_left_bins, rightmost_of_left_bins), 
                                    parent = self,
                                    discriminator_axis = discriminator_axis_child_0)
        child_fail = Categorization(Cut(axis_name, leftmost_of_right_bins, rightmost_of_right_bins), 
                                    parent = self,
                                    discriminator_axis = discriminator_axis_child_1)

        self.children = [child_pass, child_fail]
        

    def print_tree(self, depth=0, of=None, verbose=False):    
        """ Print the node and all it's children recursively in a pretty way.
        depth tells us the level of the node we're currently at (root=0)
        of is the output file. Either a file object or None. If None,
        we just print the tree to the terminal.        
        """

        S,B = self.get_sb()        
        if S+B>0:
            SsqrtB = S/math.sqrt(S+B)
        else:
            SsqrtB = -1

        if verbose:
            string = "   " * depth + " {0} Discr={1} S={2:.1f}, B={3:.1f}, S/sqrt(S+B)={4:.2f}".format(self.cut, self.discriminator_axis, S, B, SsqrtB)
        else:
            string = "   " * depth + " {0} Discr={1}".format(self.cut, self.discriminator_axis)

        if of is None:
            print string
        else:
            of.write(string + "\n")
            
        for c in self.children:
            c.print_tree(depth+1, of, verbose)


    def print_tree_latex(self, depth=0, limits = {}, also_calc_unsplit = False):    
        """  """

        S,B = self.get_sb()

        # Pre-calculate all the limits so we can paralellize
        if depth == 0:
                                    
            nodes_to_eval = [n for n in self.get_offspring() if not n.discriminator_axis is None]
            filenames = []

            i_split = 0
                        
            if also_calc_unsplit:
                ignore_splittings_list = [True, False]
            else:
                ignore_splittings_list = [False]

            for ignore_splittings in ignore_splittings_list:

                for node in nodes_to_eval:
                    shapes_txt_filename    = "{0}/shapes_tree_{1}_{2}_NS{3}.txt".format(node.output_path, str(node), i_split, ignore_splittings)
                    filenames.append(shapes_txt_filename)
                    if ignore_splittings:
                        node.shapes_txt_filename_self = shapes_txt_filename
                        node.i_split_self = i_split
                    else:
                        node.shapes_txt_filename_comb = shapes_txt_filename
                        node.i_split_comb = i_split

                    node.create_control_plots(self.output_path, ignore_splittings = ignore_splittings)
                    MakeDatacard2(
                        node,
                        self.leaf_files,
                        shapes_txt_filename,
                        do_stat_variations = self.do_stat_variations,
                        ignore_splittings = ignore_splittings
                    )
                    i_split += 1
                #end of loop over nodes
            #end of loop over split/not split
            print "running limits", [f for f in filenames]

            li_limits = self.pool.map(self.lg, [f for f in filenames])
            self.li_limits = copy.deepcopy(li_limits)

            for n in nodes_to_eval:
                n.limits_comb = li_limits[n.i_split_comb]
                if also_calc_unsplit:
                    n.limits_self = li_limits[n.i_split_self]

            limits = {}
            for ignore_splitting in ignore_splittings_list:
                for n in nodes_to_eval:
                    _limits, _quantiles = li_limits.pop(0)
                    l = _limits[2]
                    limits[str(n)+str(ignore_splitting)] = l
        ret = ""
        print str(self), depth
        if self.discriminator_axis is None:
            return "{}"
        
        if depth == 0:
            ret += self.latex_preamble() + "["

        ret += "{" 
        ret += self.cut.latex_string() + r"\\"
        ret += "S={0:.1f}".format(S) + r"\\"
        ret += "B={0:.1f}".format(B) 
        
        if self.children:
            
            ret += r"\\"
            ret += r"$\mu_{Comb.} = " + "{0:.2f}$".format(limits[str(self)+str(False)])

            if also_calc_unsplit:
                ret += r"\\"
                ret += r"$\mu_{Self} = " + "{0:.2f}$".format(limits.get(str(self)+str(True), -1))
        else:
            ret += r"\\"
            ret += r"$\mu_{Self} = " + "{0:.2f}$".format(limits.get(str(self)+str(False), -1))


        ret += "}"

        for c in self.children:
            
            # Ignore pruned away leaves
            if len(c.children)==0 and c.discriminator_axis is None:
                print "Ignoring leaf", c
                continue

            ret += "[\n"
            ret += c.print_tree_latex(depth+1, limits)
            ret += "\n]"

        if depth == 0:
            ret += "]" + self.latex_postamble()

        return ret

    def get_yields(self):
        """ Return a dictionary of yields for this node.
        Keys: sample names (same as in h_sig and h_bkg
        Values: yields        
        """
        
        yields = {}
        keys = self.h_sig.keys() + self.h_bkg.keys()

        self.prepare_nominal_thns()

        # For the yield we don't really care which axis is used - the
        # projections should all be the same.
        # Just make sure we don't try to project unto -1..
        if self.discriminator_axis is None:
            projection_axis = 0
        else:
            projection_axis = self.discriminator_axis

        for k in keys:

            if k in self.h_sig.keys():
                thn = self.h_sig[k]
            else:
                thn = self.h_bkg[k]
            
            yields[k] = thn.Projection(self.axes.keys().index(projection_axis)).Integral()
            yields[k] = yields[k] * self.scaling
        return yields
                        
        
    def print_yield_table(self):
        """ Print a breakdown of yields for all leaves below this node
        - or for this node if it is a leaf itself"""

        # Nested dic: key1 = category name, key2 = sample name

        yield_table = {}
        for l in self.get_leaves():
            yield_table[str(l)] = l.get_yields()
        
        # Get the list of all sample names
        samples = yield_table.values()[0].keys()


        names = {
            "numJets__4__5__nBCSVM__2__3__discr_None"	: "t2j4",
            "numJets__4__5__nBCSVM__3__4__discr_2"	: "t3j4",
            "numJets__4__5__nBCSVM__4__5__discr_2"	: "t4j4",
            "numJets__5__6__nBCSVM__2__3__discr_None"	: "t2j5",
            "numJets__5__6__nBCSVM__3__4__discr_2"	: "t3j5",
            "numJets__5__6__nBCSVM__4__5__discr_2"	: "t4j5",
            "numJets__6__7__nBCSVM__2__3__discr_2"	: "t2j6",
            "numJets__6__7__nBCSVM__3__4__discr_2"	: "t3j6",
            "numJets__6__7__nBCSVM__4__5__discr_2"  : "t4j6",
        }

        print "\t\t" + "\t".join(names[str(l)] for l in self.get_leaves() if not l.discriminator_axis is None)

        for sample in samples:
            print sample + "\t" + "\t".join(["{0:.1f}".format(yield_table[str(l)][sample]) for l in self.get_leaves() if not l.discriminator_axis is None])
                        

    def get_sb(self):
        """ Get the total signal and background counts after applying
        the cuts (+ancestors) for all the associated THNs.

        Return a tuple of numbers: signal and background counts
        """

        self.prepare_nominal_thns()        
        S = sum([x.Projection(0).Integral() for x in self.h_sig.values()])
        S = S * self.scaling
        B = sum([x.Projection(0).Integral() for x in self.h_bkg.values()])        
        B = B * self.scaling

        return S,B


    def get_sb_entries(self):
        """ Get the effective signal and background entries after applying
        the cuts (+ancestors) for all the associated THNs.

        Return a tuple of numbers: signal and background counts
        """

        self.prepare_nominal_thns()        
        S_entries = sum([x.Projection(0).GetEntries() for x in self.h_sig.values()])
        B_entries = sum([x.Projection(0).GetEntries() for x in self.h_bkg.values()])
                
        return S_entries, B_entries


    def get_leaves(self, ignore_splittings=False):
        """ Return a list of leaves at or below the current node"""

        leaves = []
        if ignore_splittings:
            return [self]

        if self.children:
            for c in self.children:
                leaves.extend(c.get_leaves())
        else:
            leaves.append(self)
            
        return leaves


    def get_offspring(self):
        """ Return a list of all nodes below and including the current one. """

        offspring = []
        if self.children:
            for c in self.children:
                offspring.extend(c.get_offspring())

        offspring.append(self)
            
        return offspring

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
        thns = self.h_sig.values() + self.h_bkg.values()
        self.prepare_thns(thns)


    def prepare_all_thns(self):
        """ Prime nominal and systematic variation THNs for projection """
        
        # Nominal
        thns = self.h_sig.values() + self.h_bkg.values() + self.h_data.values()
        
        # Systematic variations
        # (these nested dictionaries)
        for v in self.h_sig_sys.values() + self.h_bkg_sys.values():
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
            for iaxis, (axis_name, axis) in enumerate(self.axes.items()):            
                thn.GetAxis(iaxis).SetRange(1, axis.nbins)
                thn.GetAxis(iaxis).SetBit(ROOT.TAxis.kAxisRange)
            # end of loop over axes
        
            # Loop over cuts
            for c in all_cuts:
                if c: # this is just to handle the ROOT node
                    # And restirct the axis range
                    thn.GetAxis(c.iaxis).SetRange(c.lo, c.hi)
                                        
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

    def eval_limit(self, name):

        control_plots_filename = "{0}/ControlPlots_{1}.root".format(self.output_path, name)
        shapes_txt_filename    = "{0}/shapes_{1}.txt".format(self.output_path, name)
        shapes_root_filename   = "{0}/shapes_{1}.root".format(self.output_path, name)
        
        self.create_control_plots(self.output_path)
        MakeDatacard2(
            self,
            self.leaf_files,
            shapes_txt_filename,
            do_stat_variations=self.do_stat_variations
        )
        return self.lg(shapes_txt_filename)

    def find_categories_async(self,
                              n,
                              cut_axes,
                              discriminator_axes):

        # Start by calculating the limit without splitting
        last_limit = self.eval_limit("whole")[0][2]

        min_eff_entries_per_bin = 40
        
        for i_iter in range(n):
            print "Doing iteration", i_iter

            splittings = {}
            i_splitting = 0


            # Loop over all leaves - these are the categories that we
            # could split further
            for ileaf, leaf in enumerate(self.get_leaves()):

                # Can we split this leave at all?
                entries_sig, entries_bkg   = leaf.get_sb_entries()
                if min(entries_sig, entries_bkg) < 2*min_eff_entries_per_bin:
                    print "Do not attempt to split", leaf, entries_sig, entries_bkg
                    continue


                # Loop over axes
                for axis_name in cut_axes:

                    axis = self.axes[axis_name]
                    #print "Preparing axis", axis_name

                    # Loop over bins on the axis
                    # (ROOT Histogram bin counting starts at 1)
                    for split_bin in range(1, axis.nbins):

                            
                        for idisc1, discriminator_axis_for_child_0 in enumerate(getattr(leaf, "disc_axes_child_left", discriminator_axes)):
                            for idisc2, discriminator_axis_for_child_1 in enumerate(getattr(leaf, "disc_axes_child_right", discriminator_axes)):
                                

                                # The split function executes the split
                                # If it failed (return value of -1) - for example because the requested range is already excluded
                                # we go to the next one
                                if leaf.split(axis_name, 
                                           split_bin,
                                           discriminator_axis_for_child_0,
                                           discriminator_axis_for_child_1)==-1:
                                    continue

                                splitting_name = "iter_{0}_leaf_{1}_bin_{2}_dl_{3}_dr_{4}".format(i_iter, ileaf, split_bin, idisc1, idisc2)
                        
                                # Make sure we have sufficient stat power in both children
                                entries_sig_child_left, entries_bkg_child_left   = leaf.children[0].get_sb_entries()
                                entries_sig_child_right, entries_bkg_child_right = leaf.children[1].get_sb_entries()
                                if min(entries_sig_child_left, entries_bkg_child_left, entries_sig_child_right, entries_bkg_child_right) < min_eff_entries_per_bin:
                                    print "Vetoing", splitting_name, "due to insufficient stats!", entries_sig_child_left, entries_bkg_child_left, entries_sig_child_right, entries_bkg_child_right
                                    leaf.merge()
                                    continue
                                


                                control_plots_filename = "{0}/ControlPlots_{1}.root".format(self.output_path, splitting_name)
                                shapes_txt_filename    = "{0}/shapes_{1}.txt".format(self.output_path, splitting_name)
                                shapes_root_filename   = "{0}/shapes_{1}.root".format(self.output_path, splitting_name)

                                # Here always evaluate the full tree!
                                root = self.get_root()
                                root.create_control_plots(self.output_path)
                                MakeDatacard2(
                                    root,
                                    self.leaf_files,
                                    shapes_txt_filename,
                                    do_stat_variations=self.do_stat_variations
                                )

                                splittings[shapes_txt_filename] = [
                                    leaf,
                                    axis_name,
                                    split_bin,
                                    discriminator_axis_for_child_0,
                                    discriminator_axis_for_child_1
                                ]
                                i_splitting += 1

                                # Undo the split
                                leaf.merge()

                    # End of loop over leaves
                # End of loop over histogram bins
            # End of loop over axes

            if len(splittings) == 0:
                print "NO MORE SPLITTINGS POSSIBLE!"
                print self.print_tree(verbose=True)
                break
            
            # Extract a list todo and pass them to the limit calculation
            li_splittings = splittings.keys()
            print "evaluating limit over {0} trials".format(len(li_splittings))
            li_limits = self.pool.map(self.lg, li_splittings)

            # build a list of tuples with limit name and numerical value
            li_name_limits = [(name, limit[0][2]) for name, limit in zip(li_splittings, li_limits)]
           
            split_limits = {}
            for (spl_filename, spl), lim in zip(splittings.items(), li_limits):
                spl = tuple(spl)
                ax = self.axes[spl[1]]
                bins = np.linspace(ax.xmin, ax.xmax, ax.nbins+1)
                bin_x = bins[spl[2]]
                split_limits[spl] = (bin_x, lim[0])

          
            #store x-y coordinates of all split optimizations
            li_plots = {}
            for spl in sorted(split_limits.keys()):
                li_plots[(spl[0], spl[1], spl[3], spl[4])] = []

            for spl in sorted(split_limits.keys()):
                li_plots[(spl[0], spl[1], spl[3], spl[4])] += [split_limits[spl]]
            self.iteration_results += [li_plots]

            # sort by limit and take the lowest/best one
            best_splitting_name, best_limit = sorted(li_name_limits, key = lambda x:x[1])[0]
            best_split = splittings[best_splitting_name]

            print "New Split:", best_limit, "(previous best was {0})".format(last_limit)
            print "(File: ", best_splitting_name, ")"
            split_retval = best_split[0].split(best_split[1], # iaxis
                                               best_split[2], # split_bin
                                               best_split[3], # discriminator_axis_for_child_0
                                               best_split[4]) # discriminator_axis_for_child_1
            if split_retval == -1:
                raise Exception('SplittingError', 'Invalid splitting selected as best splitting')

            last_limit = best_limit
            self.print_tree(verbose=True)
            
            # Also write the latest tree to disk
            of = open("best_tree_iter_{0}.txt".format(i_iter), "w")
            self.print_tree(of=of)
            of.close()
            
        # End of loop over iterations

    def prune(self, threshold = 0.02):
        """Go through all leave nodes. If not including this leave in
        the total limit only makes the limit worse within the
        threshold then deactivate the node. The node is not removed
        but rather the discriminator for this node is set to -1"""


        limits, quantiles = self.eval_limit("prune_whole")
        total_limit = limits[2]

        n_pruned_away = 0

        for l in self.get_leaves():
                        
            # Store the discriminator axis
            original_discriminator = l.discriminator_axis
            # Deactivate for now
            l.discriminator_axis = None
            
            # Important - eval the limit starting from the node under
            # study - not just the leave limit
            limits, quantiles = self.eval_limit("prune_" + str(l))
            limit = limits[2]

            # Deactivating this category is too costly so we turn it
            # back on
            if (limit-total_limit)/total_limit > threshold:
                l.discriminator_axis = original_discriminator
            else:
                n_pruned_away += 1
        # End of loop over leaves
        
        print "Pruned away", n_pruned_away, "leaves"
        self.print_tree(verbose=True)


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

        name = "__".join([c.__repr__() for c in unique_cuts])
        if not name:
            name = "Whole"
        
        name += "__discr_" + str(self.discriminator_axis)

        return name

    def latex_string(self):
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

        name = ", ".join([c.latex_string() for c in unique_cuts])
        if not name:
            name = "Whole"

        #name += "__discr_" + str(self.discriminator_axis)

        return name


    def create_control_plots(self, path, ignore_splittings = False):
        """
        Creates the root files containing the 1D templates for this categorization.
        Each category will be saved into a separate file. If a control plot for a category
        has already been created, it is not recreated and is instead read from self.leaf_files

        path (string) - output path, e.g. /scratch/$USER
        ignore_splittings (bool) - if True, nodes will be merged (FIXME).

        returns: nothing
        """
        if ignore_splittings:
            leaves = [self]
        else:
            leaves = self.get_leaves()
        event_counts = {}

        # Loop over categories
        for leaf in leaves:
            dirs = {}

            leaf_fname = path + "/" + leaf.__repr__() + ".root"
            
            #leaf already created
            if self.leaf_files.has_key(leaf.__repr__()):
                continue

            #This leaf is specified to be removed from the fit
            if leaf.discriminator_axis is None:
                continue
            print leaf_fname

            of = ROOT.TFile(leaf_fname, "RECREATE")
            self.leaf_files[leaf.__repr__()] = leaf_fname

            leaf.prepare_all_thns()
            
            processes = []
            # Nominal
            for process, thn in self.h_sig.items() + self.h_bkg.items():

                # Get the output directory (inside the TFile)
                outdir_str = "{0}/{1}".format(process, leaf)
                if not outdir_str in dirs.keys():
                    dirs[outdir_str] = []
                
                hname = self.axes[leaf.discriminator_axis].name
                k = (process, leaf.__repr__(), hname)
                if self.allhists.has_key(k):
                    h = self.allhists[k]
                else:
                    h = thn.Projection(self.axes.keys().index(leaf.discriminator_axis), "E")                    
                    h.Scale(self.scaling) 
                    if leaf.rebin_discriminator:
                        h.Rebin(leaf.rebin_discriminator)                    

                    h.SetName(hname)
                    self.allhists[k] = h.Clone()

                if not self.event_counts.has_key(process):
                    self.event_counts[process] = {}
                self.event_counts[process][leaf.__repr__()] = h.Integral()

                dirs[outdir_str].append(h)
                processes += [process]
            # End of loop over processes

            # Systematic Variations
            for process, hs in self.h_sig_sys.items() + self.h_bkg_sys.items():

                # Get the output directory (inside the TFile)
                outdir_str = "{0}/{1}".format(process, leaf)
                if not outdir_str in dirs.keys():
                    dirs[outdir_str] = []

                for sys_name, thn in hs.items():
                   
                    hname = self.axes[leaf.discriminator_axis].name + "_" + sys_name
                    k = (process, leaf.__repr__(), hname)
                    if self.allhists.has_key(k):
                        h = self.allhists[k]
                    else:
                        h = thn.Projection(self.axes.keys().index(leaf.discriminator_axis), "E")
                        h.Scale(self.scaling) 
                        if leaf.rebin_discriminator:
                            h.Rebin(leaf.rebin_discriminator)                    

                        h.SetName(hname)
                        self.allhists[k] = h.Clone()
                    dirs[outdir_str].append(h)

            # End of loop over systematics
            # End of loop over processes
            for outdir_str, hs in dirs.iteritems():

                of.mkdir(outdir_str)
                outdir = of.Get(outdir_str)

                for h in hs:
                    h.SetDirectory(outdir)
                outdir.Write("", ROOT.TObject.kOverwrite)
            if self.do_stat_variations:
                makeStatVariations(of, of, [leaf.discriminator_axis], [leaf.__repr__()], processes)
            fakeData(of, of, [leaf.discriminator_axis], [leaf.__repr__()], processes)
            of.Close()
        # End of loop over categories
    #end of create_control_plots

    def getProcesses(self):
        return self.h_sig.keys() + self.h_bkg.keys()

    def getCategories(self, ignore_splittings):
        return [l.__repr__() for l in self.get_leaves(ignore_splittings)]   

    def getLeafDiscriminators(self, ignore_splittings):
        ret = {}
        for leaf in self.get_leaves(ignore_splittings):
            ret[leaf.__repr__()] = leaf.discriminator_axis
        return ret

    def latex_preamble(self):
        return r"""\documentclass[border=5pt]{standalone}
        \usepackage{forest}

        \begin{document}
        
        \begin{forest}
        for tree={
        draw,
        minimum height=2cm,
        anchor=north,
        align=center,
        child anchor=north
        },
        """
    
    def latex_postamble(self):
        return r"""\end{forest}
        \end{document}
        """
    
    #save per-leaf control plots in a root file
    def SaveControlPlots(self, name):
        rof = ROOT.TFile(name + ".root", "RECREATE")
        for k, v in self.allhists.items():
            outdir_str = "/".join(k[:-1])
            if rof.Get(outdir_str) == None:
                rof.mkdir(outdir_str)
            outdir = rof.Get(outdir_str)
            v = v.Clone()
            v.SetDirectory(outdir)
            outdir.Write("", ROOT.TObject.kOverwrite)
        rof.Close()

#End of Categorization

########################################
# CategorizationFromString
########################################

def CategorizationFromString(string):
    """Build the whole cutflow tree from a string and return the root
    node. Works with the output of print_tree.    
    """

    r = Categorization(Cut())

    last_depth = 0
    last_node = r

    for line in string.split("\n"):

        # remove the first character - it's usually a space (we count
        # the depth by how indented the line is and one space is extra
        # offset)
        line = line[1:].rstrip()
        depth = line.count("   ")

        # Now split by spaces, if nothing remains, ignore this line
        line_atoms = [x for x in line.split(' ') if x]
        if not line_atoms:
            continue

        # Take the first piece of the text - this should now be the cutstring
        cut_string = line_atoms[0]

        # For the first entry we don't have a cutstring
        # just set the discriminator variable of the ROOT node correctly
        if "Discr" in cut_string:
            discriminator = cut_string.split("=")[1]
            last_node.discriminator_axis = discriminator
            continue

        # Otherwise the discriminator will be the second item
        discriminator = line_atoms[1].split("=")[1]
        if discriminator == "None":
            discriminator = None

        # If we also have a rebinning prescription
        if len(line_atoms) > 2:            
            rebin = int(line_atoms[2].split("=")[1])
        else:
            rebin = 0
        
        # Build the cut object from the string
        cut = Cut(cut_string)

        # Here the real fun starts
        # - if the depth icreased by one, we do a splitting
        if depth > last_depth:
            last_node.split(cut.axis.name, cut.hi, discriminator, discriminator)
            last_node = last_node[0]
            last_depth = depth
        # - if the depth stayed the same we go to the other child
        elif depth == last_depth:
            last_node = last_node.parent[1]
        # - and if the depth decreased
        #     we first go out the appropriate amount
        #     and then switch to the other child
        elif depth < last_depth:
            for _ in range(last_depth-depth):
                last_node = last_node.parent
            last_node = last_node.parent[1]
            last_depth = depth
        last_node.discriminator_axis = discriminator            
        last_node.rebin_discriminator = rebin

    # End of loop over lines
    
    return r

# End of CategorizationFromString


########################################
# GetSparseHistograms
########################################

def GetSparseHistograms(input_file,
        signals, backgrounds, category="sl", data=[]):
    """
    Given an input file containing histograms in the structure
    {process}/{category}/sparse{_syst[Up,Down]}
    where process is any signal or background process, category
    a subfolder denoting the analysis category (e.g. sl) and syst[Up,Down]
    any systematic variation, returns the per-process dictionaries of the
    nominal signal and background histograms as well as the systematic variations.
    The histograms are not copied to memory and the file will be kept open by PyROOT (?).
    

    input_file (string): path to TFile which contains the aforementioned structure.
    signals (list of strings): list of all signal processes
    backgrounds (list of strings): list of all background processes
    category (string): name of the category, default "sl"

    returns: tuple of dicts h_sig, h_bkg, h_sig_sys, h_bkg_sys
        h_[sig,bkg]: a d[process]->histogram dictionary
        h_[sig,bkg]_sys: a double dictionary d[process][syst_name]->histogram 
    """

    f = ROOT.TFile(input_file)

    h_sig = {}
    h_bkg = {}
    h_sig_sys = {}
    h_bkg_sys = {}
    h_data = {}

    for processes, h, h_sys in zip( [signals,   backgrounds],
                                    [h_sig,     h_bkg],
                                    [h_sig_sys, h_bkg_sys] ):
        for process in processes:

            basedir = "{0}/{1}".format(process, category)
            base = basedir + "/sparse"
            # Nominal Histograms
            h[process] = f.Get(base)

            # Systematic Variations
            h_sys[process] = {}     
            for key in f.Get(basedir).GetListOfKeys():

                if not "sparse_" in key.GetName():
                    continue

                syst_name = key.GetName().replace("sparse_", "")
                h_sys[process][syst_name] = f.Get("{0}/{1}/{2}".format(
                    process, category, key.GetName()
                ))

            # End loop over keys
        # End loop over processes
    # End Signal/Background loop
    for dname in data:
        h_data[dname] = f.Get("{0}/{1}/sparse".format(dname, category))
    return h_sig, h_bkg, h_sig_sys, h_bkg_sys, h_data
# End of GetSparseHistograms
   

########################################
# GetAxes
########################################

def GetAxes(h):
    """ Extract axes from a sparse histogram"""
    axes = OrderedDict()
    n_dim = h.GetNdimensions()
    for i_axis in range(n_dim):
        a = h.GetAxis(i_axis)
        new_axis = axis(a.GetName(), a.GetNbins(), a.GetXmin(), a.GetXmax())
        axes[new_axis.name] = new_axis 
    return axes


def Recurse(categorization, depth=0, leaves=[], nodes=[]):
    """
    Recursively iterate over all the nodes of a Categorization.
    Returns all the leaves and nodes.
    """
    categorization.depth = depth
    if len(categorization.children) == 0:
        leaves += [categorization]
    nodes += [categorization]
    categorization.name = categorization.__repr__()
    for ch in categorization.children:
        Recurse(ch, depth+1, leaves, nodes)

def control_plots_leaves(of, leaves, do_stat_variations, use_cache):
    # Loop over categories
    for leaf in leaves:
        dirs = {}

        leaf.prepare_all_thns()

        processes = []
        # Nominal
        for process, thn in leaf.h_sig.items() + leaf.h_bkg.items() + leaf.h_data.items():

            # Get the output directory (inside the TFile)
            outdir_str = "{0}/{1}".format(process, leaf)
            if not outdir_str in dirs.keys():
                dirs[outdir_str] = []

            hname = leaf.axes[leaf.discriminator_axis].name
            k = (process, leaf.__repr__(), hname)
            if use_cache and leaf.allhists.has_key(k):
                h = leaf.allhists[k]
            else:
                h = thn.Projection(leaf.axes.keys().index(leaf.discriminator_axis), "E")                    
                h.Scale(leaf.scaling) 
                if leaf.rebin_discriminator:
                    h.Rebin(leaf.rebin_discriminator)                    

                h.SetName(hname)
                leaf.allhists[k] = h.Clone()

            if not leaf.event_counts.has_key(process):
                leaf.event_counts[process] = {}
            leaf.event_counts[process][leaf.__repr__()] = h.Integral()

            dirs[outdir_str].append(h)
            processes += [process]
        # End of loop over processes

        # Systematic Variations
        for process, hs in leaf.h_sig_sys.items() + leaf.h_bkg_sys.items():

            # Get the output directory (inside the TFile)
            outdir_str = "{0}/{1}".format(process, leaf)
            if not outdir_str in dirs.keys():
                dirs[outdir_str] = []

            for sys_name, thn in hs.items():

                hname = leaf.axes[leaf.discriminator_axis].name + "_" + sys_name
                k = (process, leaf.__repr__(), hname)
                if use_cache and leaf.allhists.has_key(k):
                    h = leaf.allhists[k]
                else:
                    h = thn.Projection(leaf.axes.keys().index(leaf.discriminator_axis), "E")
                    h.Scale(leaf.scaling) 
                    if leaf.rebin_discriminator:
                        h.Rebin(leaf.rebin_discriminator)                    

                    h.SetName(hname)
                    leaf.allhists[k] = h.Clone()
                dirs[outdir_str].append(h)

        # End of loop over systematics
        # End of loop over processes
        for outdir_str, hs in dirs.iteritems():

            of.mkdir(outdir_str)
            outdir = of.Get(outdir_str)

            for h in hs:
                h.SetDirectory(outdir)
            outdir.Write("", ROOT.TObject.kOverwrite)
        if do_stat_variations:
            makeStatVariations(of, of, [leaf.discriminator_axis], [leaf.__repr__()], processes)
        #fakeData(of, of, [leaf.discriminator_axis], [leaf.__repr__()], processes)

def leaves_cplots(categorization, of):
    nodes_to_eval = []
    for c in categorization.get_offspring():
        if len(c.children) == 0 and not (c.discriminator_axis is None):
            nodes_to_eval += [c]
    control_plots_leaves(of, nodes_to_eval, False, False)
