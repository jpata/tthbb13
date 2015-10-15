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
from Cut import Cut
from CombineHelper import LimitGetter
from makeDatacard import MakeDatacard

ROOT.TH1.AddDirectory(0)


########################################
# Configuration
########################################


input_file = "/home/gregor/dev-747/CMSSW/src/TTH/Plotting/ControlPlotsSparse.root"
output_path = "/scratch/gregor/foobar"

n_proc = 40
n_iter = 6


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

    pool = None
    output_path = None

    lg = None

    verbose = 0

    def __init__(self, cut, parent=None, discriminator_axis=0):
        """ Create a new node """        
        self.parent = parent
        self.children = []
        self.cut = cut
        self.discriminator_axis = discriminator_axis
        
    # Allow directly accessing the children
    def __getitem__(self, key):
        return self.children[key]

    def split(self, 
              iaxis, 
              rightmost_of_left_bins, 
              discriminator_axis_child_0 = 0,
              discriminator_axis_child_1 = 0):        
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
            if self.verbose:
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
            if self.verbose:
                print "leftmost_of_right_bins <= rightmost_of_left_bins"
            return -1
        if leftmost_of_right_bins > self.axes[iaxis].nbins:
            if self.verbose:
                print "Invalid subdivision, leftmost_of_right_bins > self.axes[iaxis].nbins"
            return -1


        # Sanity check if the requested discriminator variable is defined for both children
        # First get all the cuts, including the one we would apply for the children
        all_cuts_child_0 = all_previous_cuts + [Cut(iaxis, leftmost_of_left_bins, rightmost_of_left_bins)  ]
        all_cuts_child_1 = all_previous_cuts + [Cut(iaxis, leftmost_of_right_bins, rightmost_of_right_bins)]

        # Get the prerequisites for the requested discriminators
        prereqs_for_child_0 = self.axes[discriminator_axis_child_0].discPrereq
        prereqs_for_child_1 = self.axes[discriminator_axis_child_1].discPrereq

        # We want for ALL prerequisits that at LEAST ONE is as tight as the prerequiste
        # all([]) returns True - so this also works if there are no prerequs        
        if not all([any([c.is_subset_of(p) for c in all_cuts_child_0]) for p in prereqs_for_child_0]):
            return -1
        if not all([any([c.is_subset_of(p) for c in all_cuts_child_1]) for p in prereqs_for_child_1]):
            return -1
                
        # And finally: actually spawn two new children and add the Nodes to the tree
        child_pass = Categorization(Cut(iaxis, leftmost_of_left_bins, rightmost_of_left_bins), 
                                    parent = self,
                                    discriminator_axis = discriminator_axis_child_0)
        child_fail = Categorization(Cut(iaxis, leftmost_of_right_bins, rightmost_of_right_bins), 
                                    parent = self,
                                    discriminator_axis = discriminator_axis_child_1)
        self.children = [child_pass, child_fail]
        

    def print_tree(self, depth=0, of=None):    
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

        string = "   " * depth + " {0} Discr={1} S={2:.1f}, B={3:.1f}, S/sqrt(S+B)={4:.2f}".format(self.cut, self.discriminator_axis, S, B, SsqrtB)

        if of is None:
            print string
        else:
            of.write(string + "\n")
            
        for c in self.children:
            c.print_tree(depth+1, of)


    def print_tree_latex(self, depth=0):    
        """  """

        S,B = self.get_sb()

        ret = ""        
        
        if depth == 0:
            ret += self.latex_preamble() + "["

        ret += "{" 
        ret += self.cut.latex_string() + r"\\"
        ret += "S={0:.1f}".format(S) + r"\\"
        ret += "B={0:.1f}".format(B) 

        ret += r"\\"
        ret += "Discr: "
        ret += self.axes[self.discriminator_axis].name.replace("_", " ")

        if depth == 0:
            ret += r"\\"
            ret += r"$\mu_{Comb.} = " + "{0}$".format(self.eval_limit(str(self)))

        if not self.children: 
            ret += r"\\"
            ret += r"$\mu = " + "{0}$".format(self.eval_limit(str(self)))

        ret += "}"

        for c in self.children:
            
            # Ignore pruned away leaves
            if len(c.children)==0 and c.discriminator_axis == -1:
                continue

            ret += "[\n"
            ret += c.print_tree_latex(depth+1)
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
        if self.discriminator_axis ==-1:
            projection_axis = 0
        else:
            projection_axis = self.discriminator_axis

        for k in keys:

            if k in self.h_sig.keys():
                thn = self.h_sig[k]
            else:
                thn = self.h_bkg[k]
            
            yields[k] = thn.Projection(projection_axis).Integral()

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
            "numJets__4__5__nBCSVM__2__3__discr_-1"	: "t2j4",
            "numJets__4__5__nBCSVM__3__4__discr_2"	: "t3j4",
            "numJets__4__5__nBCSVM__4__5__discr_2"	: "t4j4",
            "numJets__5__6__nBCSVM__2__3__discr_-1"	: "t2j5",
            "numJets__5__6__nBCSVM__3__4__discr_2"	: "t3j5",
            "numJets__5__6__nBCSVM__4__5__discr_2"	: "t4j5",
            "numJets__6__7__nBCSVM__2__3__discr_2"	: "t2j6",
            "numJets__6__7__nBCSVM__3__4__discr_2"	: "t3j6",
            "numJets__6__7__nBCSVM__4__5__discr_2"      : "t4j6",
        }

        print "\t\t" + "\t".join(names[str(l)] for l in self.get_leaves() if not l.discriminator_axis ==-1)

        for sample in samples:
            print sample + "\t" + "\t".join(["{0:.1f}".format(yield_table[str(l)][sample]) for l in self.get_leaves() if not l.discriminator_axis ==-1])
                        

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

    def eval_limit(self, name):
        
        control_plots_filename = "{0}/ControlPlots_{1}.root".format(self.output_path, name)
        shapes_txt_filename    = "{0}/shapes_{1}.txt".format(self.output_path, name)
        shapes_root_filename   = "{0}/shapes_{1}.root".format(self.output_path, name)
        
        self.create_control_plots(control_plots_filename)                        
        MakeDatacard(control_plots_filename, 
                     shapes_root_filename,
                     shapes_txt_filename,
                     do_stat_variations=False)
        
        return self.lg(shapes_txt_filename)

    def find_categories_async(self, 
                              n, 
                              cut_axes, 
                              discriminator_axes):

        # Start by calculating the limit without splitting
        last_limit = self.eval_limit("whole")
        
        for i_iter in range(n):
            print "Doing iteration", i_iter

            splittings = {}
            i_splitting = 0

            # Loop over axes
            for iaxis in cut_axes:
                
                axis = self.axes[iaxis]

                print "Preparing axis", iaxis

                # Loop over bins on the axis
                # (ROOT Histogram bin counting starts at 1)
                for split_bin in range(1, axis.nbins):

                    # Loop over all leaves - these are the categories that we
                    # could split further
                    for l in self.get_leaves():
                            
                        for discriminator_axis_for_child_0  in discriminator_axes:
                            for discriminator_axis_for_child_1 in discriminator_axes:

                                # The split function executes the split
                                # If it failed (return value of -1) - for example because the requested range is already excluded
                                # we go to the next one
                                if l.split(iaxis, 
                                           split_bin,
                                           discriminator_axis_for_child_0,
                                           discriminator_axis_for_child_1)==-1:
                                    continue
                        
                                splitting_name = "iter_{0}_cats_{1}".format(i_iter, i_splitting)

                                # create control plots creates the control plots for the whole tree 
                                control_plots_filename = "{0}/ControlPlots_{1}.root".format(self.output_path, splitting_name)
                                shapes_txt_filename    = "{0}/shapes_{1}.txt".format(self.output_path, splitting_name)
                                shapes_root_filename   = "{0}/shapes_{1}.root".format(self.output_path, splitting_name)

                                # Here always evaluate the full tree!
                                root = self.get_root()
                                root.create_control_plots(control_plots_filename)                        
                                MakeDatacard(control_plots_filename, 
                                             shapes_root_filename,
                                             shapes_txt_filename,
                                             do_stat_variations=False)

                                splittings[shapes_txt_filename] = [l, 
                                                                   iaxis, 
                                                                   split_bin,
                                                                   discriminator_axis_for_child_0,
                                                                   discriminator_axis_for_child_1]
                                i_splitting += 1

                                # Undo the split
                                l.merge()

                    # End of loop over leaves
                # End of loop over histogram bins
            # End of loop over axes

            # Extract a list todo and pass them to the limit calculation
            li_splittings = splittings.keys()        


            li_limits = self.pool.map(self.lg, li_splittings)
            
            # build a list of tuples with limit name and numerical value
            li_name_limits = [(name,limit) for name,limit in zip(li_splittings, li_limits)]
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
            self.print_tree()
            
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

        total_limit = self.eval_limit("prune_whole")
        
        n_pruned_away = 0

        for l in self.get_leaves():
                        
            # Store the discriminator axis
            original_discriminator = l.discriminator_axis
            # Deactivate for now
            l.discriminator_axis = -1
            
            # Important - eval the limit starting from the node under
            # study - not just the leave limit
            limit = self.eval_limit("prune_" + str(l))
            
            # Deactivating this category is too costly so we turn it
            # back on
            if (limit-total_limit)/total_limit > threshold:
                l.discriminator_axis = original_discriminator
            else:
                n_pruned_away += 1
        # End of loop over leaves
        
        print "Pruned away", n_pruned_away, "leaves"
        self.print_tree()


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


    def create_control_plots(self, name):
        
        of = ROOT.TFile(name, "RECREATE")

        dirs = {}
                
        # Loop over categories
        for l in self.get_leaves():

            if  l.discriminator_axis == -1:
                continue

            l.prepare_all_thns()

            # Nominal
            for process, thn in self.h_sig.items() + self.h_bkg.items():        

                # Get the output directory (inside the TFile)
                outdir_str = "{0}/{1}".format(process, l)
                if not outdir_str in dirs.keys():
                    dirs[outdir_str] = []
                
                h = thn.Projection(l.discriminator_axis).Clone()
                h.SetName(axes[l.discriminator_axis].name)
                dirs[outdir_str].append(h)                
            # End of loop over processes

            # Systematic Variations
            for process, hs in self.h_sig_sys.items() + self.h_bkg_sys.items():

                # Get the output directory (inside the TFile)
                outdir_str = "{0}/{1}".format(process, l)
                if not outdir_str in dirs.keys():
                    dirs[outdir_str] = []

                for sys_name, thn in hs.items():
                    
                    if "jDown" in sys_name or "jUp" in sys_name:
                        continue

                    h = thn.Projection(l.discriminator_axis).Clone()
                    h.SetName(axes[l.discriminator_axis].name + "_" + sys_name)
                    dirs[outdir_str].append(h)

                # End of loop over systematics
            # End of loop over processes
        # End of loop over categories

        for outdir_str, hs in dirs.iteritems():
                        
            of.mkdir(outdir_str)
            outdir = of.Get(outdir_str)

            for h in hs:
                h.SetDirectory(outdir)
            outdir.Write("", ROOT.TObject.kOverwrite)
        of.Close()

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
        line = line[1:]
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
            discriminator = int(cut_string.split("=")[1])
            last_node.discriminator_axis = discriminator
            continue

        # Otherwise the discriminator will be the second item
        discriminator = int(line_atoms[1].split("=")[1])

        # Build the cut object from the string
        cut = Cut(cut_string)

        # Here the real fun starts
        # - if the depth icreased by one, we do a splitting
        if depth > last_depth:
            last_node.split(cut.axis, cut.hi)
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
            
    # End of loop over lines
    
    return r

# End of CategorizationFromString




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

Categorization.output_path = output_path
Categorization.pool = Pool(n_proc)

Categorization.lg = LimitGetter(output_path)
    

old = """
  Discr=2
    numJets__4__5 Discr=2 
       nBCSVM__2__4 Discr=2
          nBCSVM__2__3 Discr=-1
          nBCSVM__3__4 Discr=2
       nBCSVM__4__5 Discr=2
    numJets__5__7 Discr=2
       numJets__5__6 Discr=2
          nBCSVM__2__4 Discr=2
             nBCSVM__2__3 Discr=-1
             nBCSVM__3__4 Discr=2
          nBCSVM__4__5 Discr=2
       numJets__6__7 Discr=2
          nBCSVM__2__4 Discr=2
             nBCSVM__2__3 Discr=2
             nBCSVM__3__4 Discr=2
          nBCSVM__4__5 Discr=2
"""


if __name__ == "__main__":

    r = Categorization(Cut(), discriminator_axis=2)

    #r = CategorizationFromString(old)
    #r.print_tree() 
    #r.print_yield_table()     
    #print r.eval_limit("test")   
    

    # TODO: something clever for boosted prereq - it can be
    # conditional on mass or other variables... For now we just
    # evaluate it for more events than we should - costs a bit in
    # computing but should be safe physics wise
    axes[0].discPrereq = [Cut(3,3,3)]
    axes[1].discPrereq = [Cut(3,3,3)]

    cut_axes = range(4,14)
    discriminator_axes = [0,1,2,3]
    
    r.find_categories_async(n_iter, 
                            cut_axes, 
                            discriminator_axes)    





