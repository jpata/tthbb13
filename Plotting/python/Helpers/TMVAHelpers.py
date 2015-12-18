
#!/usr/bin/env python
"""
Helper script for the evaluation of different methods/variables using TMVA.
"""

########################################
# Imports and Macros
########################################

import os
import sys
import math
import pickle
import array
import multiprocessing as mp

from xml.dom import minidom

import ROOT

# initializer: simple creation of bag-of-object classes
from Initializer import initializer

# Our support Code
# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.VariableHelpers import variable
    from TTH.Plotting.Helpers.HistogramHelpers import Count
    from TTH.Plotting.Helpers.PrepareRootStyle import myStyle
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.VariableHelpers import variable
    from TTH.Plotting.python.Helpers.HistogramHelpers import Count
    from TTH.Plotting.python.Helpers.PrepareRootStyle import myStyle


myStyle.SetPadLeftMargin(0.15)
myStyle.SetPadTopMargin(0.12)

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()

########################################
# Definitions
########################################

li_colors = [ROOT.kRed,      ROOT.kBlue+1,     ROOT.kBlack, 
             ROOT.kOrange-1, ROOT.kViolet+1,   ROOT.kGreen+1,
             ROOT.kGray,     ROOT.kBlue-7]*20

li_marker_styles = [20]*4+[21]*4+[22]*4+[23]*4+[24,25,26,27]*100

tmp = [1]*(len(li_colors)/20) + [2]*(len(li_colors)/20) + [3]*(len(li_colors)/20)
li_line_styles = tmp*20

########################################
# Helper: CalcEffAndError
########################################

def calcEffAndError(n_pass, e_pass, n_total, e_total):

    h_pass = ROOT.TH1D("","",1,0.5,1.5)
    h_pass.SetBinContent(1, n_pass)
    h_pass.SetBinError(1, e_pass)

    h_total = ROOT.TH1D("","",1,0.5,1.5)
    h_total.SetBinContent(1, n_total)
    h_total.SetBinError(1, e_total)
    
    gr = ROOT.TGraphAsymmErrors(1)
    gr.BayesDivide( h_pass, h_total)

    px = ROOT.Double(0)
    py = ROOT.Double(0)
    
    gr.GetPoint(0, px, py)

    return py, gr.GetErrorYlow(0), gr.GetErrorYhigh(0)


########################################
# Helper: CountEventsAndError
########################################
    
ROOT.TH1.SetDefaultSumw2()

def countEventsAndError(tree, cut, weight):

    # Draw events into a dummy histogram so we don't have to calculate
    # the uncertainty on a bunch of weigthed events ourselved
    tree.Draw("1>>h_tmp(1,0.5,1.5)", "({0})*{1}".format(cut, weight))
    h_tmp = ROOT.gDirectory.Get("h_tmp").Clone()
    return h_tmp.GetBinContent(1), h_tmp.GetBinError(1)


def countEventsAndErrorClassifier(tree, cut, weight):

    # Draw events into a dummy histogram so we don't have to calculate
    # the uncertainty on a bunch of weigthed events ourselved
    tree.Draw("1>>h_tmp(1,0.5,1.5)", "({0})*{1}".format(cut, weight))
    h_tmp = ROOT.gDirectory.Get("h_tmp").Clone()
    return h_tmp.GetBinContent(1), h_tmp.GetBinError(1)
    

########################################
# class TMVASetup
########################################

class TMVASetup:
    """Helper class to store options for running TMVA.

    - Each variable can have an allowed range as well as an extra cut
    - We need to record the efficiency of these cuts with respect to the ficucial selection
        -> N(fiducual && per-variable-cuts) / N(fiducial)
    - These numbers are written to a pickle file so the ROC curves can be correctly     
    - Then all the TMVA methods are run on the set of variables

    Arguments:
    name             - [string]: will be used for naming the output files
    pretty_name      - [string]: used for labelling
    li_methods       - [list of list of string objects]: TMVA method and (optional) options. Example: [["Cuts", "FitMethod=MC:SampleSize=200000"], ["BDT"]]
    li_vars          - [list of variable objects] variables to include
    li_spectators    - [list of variable objects] spectator variables to include
    file_name_sig    - [string]: full name of the input signal file
    file_name_bkg    - [string]: full name of the input background file
    tree_name_sig    - [string]: name of the tree with signal events
    tree_name_bkg    - [string]: name of the tree with background events
    fiducial_cut_sig - [string]: fiducial cut signal - define denominator of efficiencies
    fiducial_cut_bkg - [string]: fiducial cut background - define denominator of efficiencies
    extra_cut        - [string]: extra cut - on part with per-variable cuts (not fiducial, only numerator, same for sig and bg)
    weight_sig       - [string]: weight for signal
    weight_bkg       - [string]: weight for bg
    draw_roc         - [bool]: draw the ROC curves
    draw_wps         - [bool]: draw the working points (extract from file)
    draw_manual_wps  - [bool]: draw the working points (given as cuts)
    output_dir       - [string]: output directory
    """

    @initializer    
    def __init__( self, 
                  name,
                  pretty_name,
                  li_methods,
                  li_vars,
                  li_spectators,
                  file_name_sig,
                  file_name_bkg,
                  tree_name_sig    = "tree",
                  tree_name_bkg    = "tree",
                  fiducial_cut_sig = "(1)",
                  fiducial_cut_bkg = "(1)",
                  extra_cut        = "(1)",
                  weight_sig       = "(1)",
                  weight_bkg       = "(1)",
                  working_points   = [],
                  manual_working_points   = [],
                  draw_roc         = True,
                  draw_wps         = True,
                  draw_manual_wps  = True,
                  output_dir = "/shome/gregor/new_results/ClassifyTaggers/",
              ):
        pass

# end of TMVASetup class


########################################
# doTMVA
########################################

def doTMVA(setup):
        
    # Open Files
    # Output
    outfname = "TMVA_{0}.root".format(setup.name)
    # add path
    outfname = os.path.join(setup.output_dir, outfname)

    outputFile    = ROOT.TFile(outfname, 'RECREATE' )
    outputFilePickle = open( outfname.replace(".root",".dat"), "w")

    # Input
    inputFileSig  = ROOT.TFile.Open( setup.file_name_sig )
    inputFileBkg  = ROOT.TFile.Open( setup.file_name_bkg )

    # Get the signal and background trees for training
    signal      = inputFileSig.Get( setup.tree_name_sig )
    background  = inputFileBkg.Get( setup.tree_name_bkg )


    ########################################
    # Create cuts and calculate efficiency
    ########################################

    # Combine all the cuts associated to variables
    li_cuts = [setup.extra_cut]
    for var in setup.li_vars:        
        if var.extra_cut:
            li_cuts.append(var.extra_cut)
            
        li_cuts.append( "({0}>={1})".format(var.name, var.range_min))
        li_cuts.append( "({0}<={1})".format(var.name, var.range_max))
                
    # The final cut is:
    #  - the && of per-variable cuts 
    #  - && the per-sample fidcucial cuts
    cut_signal = "&&".join(li_cuts + [setup.fiducial_cut_sig])
    cut_bkg     = "&&".join(li_cuts + [setup.fiducial_cut_bkg])

    # Store the event counts after fiducial and after
    # fiducial+additional cuts for future reference. As we use
    # weighted events, store also the related uncertainty.
    event_counts = {}
    [event_counts["n_sig_fiducial"], event_counts["e_sig_fiducial"]]   = countEventsAndError(signal, setup.fiducial_cut_sig, setup.weight_sig)
    [event_counts["n_bkg_fiducial"],  event_counts["e_bkg_fiducial"]]  = countEventsAndError(background, setup.fiducial_cut_bkg, setup.weight_bkg)
    
    pickle.dump(event_counts, outputFilePickle)
    outputFilePickle.close()

    # Count unweighted events 
    n_sig_cuts_noweight = countEventsAndError(signal, cut_signal, "1")[0]
    n_bkg_cuts_noweight = countEventsAndError(background, cut_bkg, "1")[0]
    
    n_training_events = int(min(n_sig_cuts_noweight, n_bkg_cuts_noweight)/2.)

    print "Number of events for training: ", n_training_events

    ########################################
    # TMVA starts here
    ########################################

    print cut_signal

    # Create instance of TMVA factory
    factory = ROOT.TMVA.Factory( setup.name, outputFile, 
                            "!V:!Silent:Color:DrawProgressBar:Transformations=I:AnalysisType=Classification:" )
    factory.SetVerbose( False )

    # Add variables to factory
    for var in setup.li_vars:
        factory.AddVariable( var.name)

    for var in setup.li_spectators:
        factory.AddSpectator( var.name, 'F' )

    # Global event weights
    signalWeight     = 1.0
    backgroundWeight = 1.0

    # register trees
    factory.AddSignalTree    ( signal,     signalWeight     )
    factory.AddBackgroundTree( background, backgroundWeight )

    mycutSig = ROOT.TCut(cut_signal) 
    mycutBkg = ROOT.TCut(cut_bkg )


    factory.SetSignalWeightExpression( setup.weight_sig )
    factory.SetBackgroundWeightExpression( setup.weight_bkg)



    # prepare trees
    # :nTrain_Background=250000
    factory.PrepareTrainingAndTestTree( mycutSig, mycutBkg,
                                        "SplitMode=Random:NormMode=None:!V:nTrain_Signal={0}:nTrain_Background={1}".format(n_training_events, 2*n_training_events) )


    ########################################
    # Schedule the Classifiers
    ########################################

    method_types = {
        "Cuts"       : ROOT.TMVA.Types.kCuts,
        "Likelihood" : ROOT.TMVA.Types.kLikelihood, 
        "Fisher"     : ROOT.TMVA.Types.kFisher, 
        "MLP"        : ROOT.TMVA.Types.kMLP, 
        "SVM"        : ROOT.TMVA.Types.kSVM, 
        "BDT"        : ROOT.TMVA.Types.kBDT,         
    }

    default_options = {
        "Cuts"       : "FitMethod=MC:SampleSize=100000",
        "Likelihood" : "",
        "Fisher"     : "H:!V",
        "MLP"        : "H:!V:NeuronType=tanh:VarTransform=N:NCycles=1200:HiddenLayers=N+5:TestRate=5:!UseRegulator", 
        "SVM"        : "Gamma=0.25:Tol=0.001:VarTransform=Norm",
        "BDT"        : "!H:!V:NTrees=50:MaxDepth=2:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex:nCuts=20:PruneMethod=NoPruning",
    }
    
    for method_and_options in setup.li_methods:
        # Only name, use default options
        if len(method_and_options)==1:
            method_name = method_and_options[0]
            factory.BookMethod(method_types[method_name],
                               method_name, 
                               default_options[method_name])
        elif len(method_and_options)==2:
            method_name = method_and_options[0]
            method_options = method_and_options[1]
            factory.BookMethod(method_types[method_name],
                               method_name, 
                               method_options)            
    

    ########################################
    # Do actual training&testing work
    ########################################

    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()    

    outputFile.Close()
    inputFileSig.Close()
    inputFileBkg.Close()
# end of doTMVA


def doROCandWP(setup):
    
    # Initialize to-return object
    ret = {
        "grs"      : [],
        "gr_names" : [],
        "wps"      : [],
        "wp_names" : [],
    }

    
    ########################################
    # Extract information from files
    ########################################


    input_filename = os.path.join(setup.output_dir, "TMVA_{0}.root".format(setup.name))

    print "input_filename=", input_filename

    # We need three things:
    # -the pickle that tells us the efficiency/uncertainty of the preselection cut
    # -the output root file produced by TMVA: so we can evaluate the efficiency on the test-tree
    # -the weights.xml file produced by TMVA: this is where we read the working points from

    # First get the cut (preselection, not wp) efficiaency + uncertainty 
    f_pickle = open( input_filename.replace(".root",".dat"), "r")
    try:
        event_counts = pickle.load(f_pickle)        
    except EOFError:
        print "WTF:", input_filename
        sys.exit()

    f_pickle.close()

    # Get the trees
    if os.path.isfile(input_filename):     
        f = ROOT.TFile(input_filename, "READ" )        
        testTree= f.FindObjectAny("TestTree")
        trainTree = f.FindObjectAny("TrainTree")
    else:
        print "File: ", input_filename, "does not exist"
        print "Skipping..."
        return ret

    try:
        testTree.GetEntries()
    except AttributeError:
        print "Tree does not exist in: ", input_filename
        print "Skipping..."
        return ret
        

 
    if (testTree.GetEntries()==0) or (trainTree.GetEntries()==0):
        print "Empty tree for ", input_filename
        print "Skipping"
        return ret

    # Retrieve correct assignment of the signal/background flag
    testTree.Draw("className>>h_clsname_id0", "classID==0")
    classname_id0 = ROOT.gDirectory.Get("h_clsname_id0").GetXaxis().GetBinLabel(1)
    if classname_id0 == "Signal":
        classid_sig = 0
        classid_bkg = 1
    elif classname_id0 == "Background":
        classid_sig = 1
        classid_bkg = 0
    else:
        print "Invalid class name: ", classname_id0
        print "Exiting.."
        sys.exit()

    # Lengthy explanation why we need these numbers is below where
    # eff_total_sig/bkg and the related uncertainties are calculated

    # Count the signal/background events (+error) in the test tree
    [n_test_sig, e_test_sig] = countEventsAndError(testTree, "(classID=={0})".format(classid_sig), "weight")
    [n_test_bkg, e_test_bkg] = countEventsAndError(testTree, "(classID=={0})".format(classid_bkg), "weight")

    # Count the signal/background events (+error) in the training tree
    trainTree = f.FindObjectAny("TrainTree")
    [n_train_sig, e_train_sig] = countEventsAndError(trainTree, "(classID=={0})".format(classid_sig), "weight")
    [n_train_bkg, e_train_bkg] = countEventsAndError(trainTree, "(classID=={0})".format(classid_bkg), "weight")

    test_frac_sig = 1.0 * n_test_sig/(n_test_sig+n_train_sig)
    test_frac_bkg = 1.0 * n_test_bkg/(n_test_bkg+n_train_bkg)

    # Loop over different methods
    # (for example to compare a neural networks and BDTs)
    for method_and_options in setup.li_methods:

        method = method_and_options[0]

        if setup.draw_roc:
            


            # The xml file contains the list of cuts
            xmldoc = minidom.parse("weights/{0}_{1}.weights.xml".format(setup.name, method))
            varlist = xmldoc.getElementsByTagName('Variables')[0].getElementsByTagName("Variable")
            epxression_and_index = []
            for var in varlist:
                epxression_and_index.append([str(var.attributes['Expression'].value),
                                             int(var.attributes['VarIndex'].value)])

            epxression_and_index.sort(key = lambda x:x[1])
            expressions = [x[0] for x in epxression_and_index]
            # There is some string mangling done when stroing the variables for the test tree!
            # Convert ( and ) to _
            expressions = [x.replace("(","_").replace(")","_") for x in expressions]
            expressions = [x.replace("/","_D_") for x in expressions]
            expressions = [x.replace("-","_M_") for x in expressions]

            
            if method == "Cuts":
                # This should be 100 bins with cuts
                binlist = xmldoc.getElementsByTagName('Weights')[0].getElementsByTagName("Bin")

            elif method in ["BDT", "Likelihood"] :

                binlist = []

                for target_es in [0.29, 0.3, 0.31]:
                
                    x = 0
                    delta = 0.1

                    repeats = 0

                    # Get intial efficiency
                    cuts_sig = "(({0} > {1}) && (classID=={2}))".format(method, x,classid_sig)
                    [n_pass_sig, e_pass_sig] = countEventsAndError(testTree, cuts_sig, "weight")
                    last_es = calcEffAndError(n_pass_sig, e_pass_sig, event_counts["n_sig_fiducial"]*test_frac_sig, event_counts["e_sig_fiducial"]*math.sqrt(test_frac_sig))[0]

                    while True:

                        print "Searching for", target_es, ":", x, delta, last_es

                        # Efficiency too small, make cut looser
                        if last_es < target_es:                        
                            x -= delta
                        # Efficiency too large, make cut tighter
                        else:
                            x += delta

                        # Recalculate efficiency
                        cuts_sig = "(({0} > {1}) && (classID=={2}))".format(method, x,classid_sig)
                        [n_pass_sig, e_pass_sig] = countEventsAndError(testTree, cuts_sig, "weight")
                        es = calcEffAndError(n_pass_sig, e_pass_sig, event_counts["n_sig_fiducial"]*test_frac_sig, event_counts["e_sig_fiducial"]*math.sqrt(test_frac_sig))[0]

                        # If we switched to the other side of target es, half the step-width
                        if (es < target_es and last_es > target_es) or (es > target_es and last_es < target_es):
                            delta /= 2.
                        
                        if es==last_es:
                            repeats += 1
                        else:
                            repeats = 0
                            
                        # We found it
                        if abs(last_es - target_es) < 0.001 or repeats == 10: 
                            binlist.extend([x-2*delta, x-delta, x-delta/2, x, x+delta/2, x + delta, x+2*delta])
                            print "Done here!"
                            break

                        # Update last efficiency
                        last_es = es
                    # 
                # End loop over target_es
                binlist = list(set(binlist))

            gr = ROOT.TGraphAsymmErrors()

            # Interesting points: Look for a WP with bgk efficiency closest to nominal and store the cuts
            interesting_points = [
                #{"nominal_bkg" : 0.001, "actual_bkg":-1000, "actual_sig":-1000, "cuts" : "(1)"},
                #{"nominal_bkg" : 0.003, "actual_bkg":-1000, "actual_sig":-1000, "cuts" : "(1)"},
                #{"nominal_bkg" : 0.01,  "actual_bkg":-1000, "actual_sig":-1000, "cuts" : "(1)"},
                #{"nominal_bkg" : 0.03,  "actual_bkg":-1000, "actual_sig":-1000, "cuts" : "(1)"},
                #{"nominal_bkg" : 0.1,   "actual_bkg":-1000, "actual_sig":-1000, "cuts" : "(1)"},
            ]


            last_eff_bkg = -1
            for ibin, x in enumerate(binlist):

                # We don't need the preselection cuts - they're already applied when making the test tree                
                li_cuts = ["(1)"]

                # Turn the ranges into cuts
                if method == "Cuts":
                    for i_expr, expr in enumerate(expressions):                                        
                        min_val =  x.getElementsByTagName("Cuts")[0].attributes["cutMin_{0}".format(i_expr)].value
                        max_val =  x.getElementsByTagName("Cuts")[0].attributes["cutMax_{0}".format(i_expr)].value

                        li_cuts.append("({0}>{1})".format(expr, min_val))
                        li_cuts.append("({0}<{1})".format(expr, max_val))
                    # End of loop over expressions
                elif method in ["Likelihood", "BDT"]:
                    li_cuts.append("({0} > {1})".format(method, x))



                # We need one additional cut to distinguish signal
                # from background (these are mixed in the test tree)
                li_cuts_sig = li_cuts + ["(classID=={0})".format(classid_sig)]
                li_cuts_bkg = li_cuts + ["(classID=={0})".format(classid_bkg)]

                cuts_sig = "&&".join(li_cuts_sig)
                cuts_bkg = "&&".join(li_cuts_bkg)

                [n_pass_sig, e_pass_sig] = countEventsAndError(testTree, cuts_sig, "weight")
                [n_pass_bkg, e_pass_bkg] = countEventsAndError(testTree, cuts_bkg, "weight")

                # We want to calculate the total efficiency with respect to the fiducial selection
                # So eff(fiducial passes preselection) * eff(preselection passes per-bin cut)
                # However there is a problem: events that pass preselection are split into test and training
                # The simplest way to deal with this is to pretend we
                # only had proportionally as many event in the
                # fiducial selection as go into the test tree (because
                # that's where we want to evaluate our uncertainty)
                # So we calculate:
                # pass cut and preselection / (fidicual * fraction of fiducial that made it into test tree)
                #
                # To be on the safe side we actually "scale up" the uncertainty on the event count in the fiducial region
                # So we divide be sqrt(X) instead of full X. This
                # takes into account that the efficiency is only
                # evaluated on a smaller set of events                
                eff_total_sig, err_total_sig_low, err_total_sig_high = calcEffAndError(n_pass_sig, e_pass_sig, event_counts["n_sig_fiducial"]*test_frac_sig, event_counts["e_sig_fiducial"]*math.sqrt(test_frac_sig))
                eff_total_bkg, err_total_bkg_low, err_total_bkg_high = calcEffAndError(n_pass_bkg, e_pass_bkg, event_counts["n_bkg_fiducial"]*test_frac_bkg, event_counts["e_bkg_fiducial"]*math.sqrt(test_frac_bkg))

                print x, eff_total_sig, eff_total_bkg

                #print "Sig: {0:5<.3f} +{1:5<.3f} -{2:5<.3f}   Bkg: {3:5<.3f} +{4:5<.3f} -{5:5<.3f}".format(eff_total_sig*100,
                #                                                                                           err_total_sig_high*100,
                #                                                                                           err_total_sig_low*100,
                #                                                                                           eff_total_bkg_new*100,
                #                                                                                           err_total_bkg_high*100,
                #                                                                                           err_total_bkg_low*100)

                if eff_total_sig > 0.0 and eff_total_bkg > last_eff_bkg:
                    
                    last_eff_bkg = eff_total_bkg

                    i = gr.GetN()

                    gr.SetPoint(i, eff_total_sig, eff_total_bkg)
                    gr.SetPointError(i, err_total_sig_low, err_total_sig_high,  err_total_bkg_low, err_total_bkg_high) 

                    # Look for working points
                    for point in interesting_points:
                        # If this point is closer to the BG rejection we want than what we had before: update
                        if abs(point["nominal_bkg"] - eff_total_bkg) < abs(point["nominal_bkg"] - point["actual_bkg"]):
                            point["actual_bkg"] = eff_total_bkg
                            point["actual_sig"] = eff_total_sig
                            point["cuts"]       = cuts_sig

            # End loop over bins

            for point in interesting_points:
                print "---WP---", setup.name, point

            ret["grs"].append(gr)
            ret["gr_names"].append(setup.pretty_name)

        if setup.draw_wps:

            for wp in setup.working_points:

                # The xml file contains the list of cuts
                xmldoc = minidom.parse("weights/{0}.weights.xml".format(wp["file_name"]).replace("TMVA_",""))
                varlist = xmldoc.getElementsByTagName('Variables')[0].getElementsByTagName("Variable")
                epxression_and_index = []
                for var in varlist:
                    epxression_and_index.append([str(var.attributes['Expression'].value),
                                                 int(var.attributes['VarIndex'].value)])

                epxression_and_index.sort(key = lambda x:x[1])
                expressions = [x[0] for x in epxression_and_index]
                # There is some string mangling done when stroing the variables for the test tree!
                # Convert ( and ) to _
                expressions = [x.replace("(","_").replace(")","_") for x in expressions]
                expressions = [x.replace("/","_D_") for x in expressions]
                expressions = [x.replace("-","_M_") for x in expressions]


                other_filename = "TMVA_{0}.dat".format("_".join(wp["file_name"].split("_")[:-1]))                    
                f_other_pickle = open( other_filename, "r")
                other_event_counts = pickle.load(f_other_pickle)        
                f_other_pickle.close()


                # We want the X% total efficiency working point
                # However the TMVA xml file only stores efficiency after preselection
                # Correct for this when looking for the correct entry (bin) in the file
                eff_preselection = other_event_counts["n_sig_cuts"]/other_event_counts["n_sig_fiducial"]
                if eff_preselection>0:
                    bin_number = int((100*wp["eff"]/eff_preselection)) + 1
                    print wp['file_name'], bin_number
                    if bin_number > 99:
                        bin_number = 99
                else:
                    bin_number = 99

                # This should be 100 bins with cuts

                binlist = xmldoc.getElementsByTagName('Weights')[0].getElementsByTagName("Bin")
                the_bin = binlist[bin_number]

                wp_gr = ROOT.TGraphAsymmErrors(1)


                # We don't need the preselection cuts - they're already applied when making the test tree                
                li_cuts = ["(1)"]

                # Turn the ranges into cuts
                for i_expr, expr in enumerate(expressions):                                        
                    min_val =  the_bin.getElementsByTagName("Cuts")[0].attributes["cutMin_{0}".format(i_expr)].value
                    max_val =  the_bin.getElementsByTagName("Cuts")[0].attributes["cutMax_{0}".format(i_expr)].value

                    li_cuts.append("({0}>{1})".format(expr, min_val))
                    li_cuts.append("({0}<{1})".format(expr, max_val))
                # End of loop over expressions

                print "Cuts (wo/ fiducial and presel) for", wp["name"].replace("[name]", setup.pretty_name)
                for cut in [setup.extra_cut] +  li_cuts:
                    print "\t", cut
                for var in setup.li_vars:        
                    if var.extra_cut:
                        print "\t",  var.extra_cut
                print "-----\n\n"


                # We need one additional cut to distinguish signal
                # from background (these are mixed in the test tree)
                li_cuts_sig = li_cuts + ["(classID=={0})".format(classid_sig)]
                li_cuts_bkg = li_cuts + ["(classID=={0})".format(classid_bkg)]

                cuts_sig = "&&".join(li_cuts_sig)
                cuts_bkg = "&&".join(li_cuts_bkg)

                [n_pass_sig, e_pass_sig] = countEventsAndError(testTree, cuts_sig, "weight")
                [n_pass_bkg, e_pass_bkg] = countEventsAndError(testTree, cuts_bkg, "weight")


                eff_total_sig, err_total_sig_low, err_total_sig_high = calcEffAndError(n_pass_sig, e_pass_sig, event_counts["n_sig_fiducial"]*test_frac_sig, event_counts["e_sig_fiducial"]*math.sqrt(test_frac_sig))
                eff_total_bkg, err_total_bkg_low, err_total_bkg_high = calcEffAndError(n_pass_bkg, e_pass_bkg, event_counts["n_bkg_fiducial"]*test_frac_bkg, event_counts["e_bkg_fiducial"]*math.sqrt(test_frac_bkg))

                wp_gr.SetPoint(0, eff_total_sig, eff_total_bkg)
                wp_gr.SetPointError(0, err_total_sig_low, err_total_sig_high, err_total_bkg_low, err_total_bkg_high) 

                ret["wps"].append(wp_gr)
                ret["wp_names"].append(wp["name"].replace("[name]", setup.pretty_name))

            # End loop over working points
        # End draw_wps


        if setup.draw_manual_wps:

            for wp in setup.manual_working_points:
                
                wp_gr = ROOT.TGraphAsymmErrors(1)

                cuts_sig = "( ({0}) && (classID=={1}) )".format(wp["cuts"], classid_sig)
                cuts_bkg = "( ({0}) && (classID=={1}) )".format(wp["cuts"], classid_bkg)

                [n_pass_sig, e_pass_sig] = countEventsAndError(testTree, cuts_sig, "weight")
                [n_pass_bkg, e_pass_bkg] = countEventsAndError(testTree, cuts_bkg, "weight")

                eff_total_sig, err_total_sig_low, err_total_sig_high = calcEffAndError(n_pass_sig, e_pass_sig, event_counts["n_sig_fiducial"]*test_frac_sig, event_counts["e_sig_fiducial"]*math.sqrt(test_frac_sig))
                eff_total_bkg, err_total_bkg_low, err_total_bkg_high = calcEffAndError(n_pass_bkg, e_pass_bkg, event_counts["n_bkg_fiducial"]*test_frac_bkg, event_counts["e_bkg_fiducial"]*math.sqrt(test_frac_bkg))


                wp_gr.SetPoint(0, eff_total_sig, eff_total_bkg)
                wp_gr.SetPointError(0, err_total_sig_low, err_total_sig_high, err_total_bkg_low, err_total_bkg_high) 

                ret["wps"].append(wp_gr)
                ret["wp_names"].append(wp["name"].replace("[name]", setup.pretty_name))

            # End loop over working points
        # End draw_manual_wps

    # End of loop over methods

    return ret

# End of doROCandWP


########################################
# plotROCs
########################################

def plotROCs(name, 
             li_setups, 
             extra_text = [""], 
             x_label = "#varepsilon_{S}",
             error_band = True,
):

    # Loop over setups
    pool = mp.Pool(processes=10)  
    outputs = pool.map(doROCandWP, li_setups)
    
    # Extract the outputs
    li_grs = []
    li_gr_names = []
    li_wps = []
    li_wp_names = []

    for output in outputs:
        for gr in output["grs"]:
            li_grs.append(gr)
        for gr_name in output["gr_names"]:
            li_gr_names.append(gr_name)
        for wp in output["wps"]:
            li_wps.append(wp)
        for wp_name in output["wp_names"]:
            li_wp_names.append(wp_name)
            
    ########################################
    # And draw them
    ########################################

    c = ROOT.TCanvas( "","", 800, 800)

    legend_origin_x     = 0.21
    legend_origin_y     = 0.18
    legend_size_x       = 0.25
    legend_size_y       = 0.03 * (len(li_grs)+len(li_wps))


    for view in [
            #"left_top", "all", "weak_left_top", "weak_all", 
            "log", 
            "log2",
            "log3",  
            "loglow", 
            "loglow2", 
            "loglow3", 
            "loglow4", 
            "loglow5", 
            "loglow6", 
            #"logpuppi"
    ]:

        x_extra_text = 0.22
        y_extra_text =  0.8


        # Top Tagging
        # High Purity
        if view == "log":
            legend_origin_y = 0.15
            legend_origin_x = 0.48
            c.SetLogy(1)
            h_bkg = ROOT.TH2F("","",100,0,1.1,100,0.0001,0.1)
        elif view == "log2":
            legend_origin_y = 0.15
            legend_origin_x = 0.44
            c.SetLogy(1)
            h_bkg = ROOT.TH2F("","",100,0,1.1,100,0.0001,0.1)
        elif view == "log3":
            legend_origin_y = 0.155
            legend_origin_x = 0.48
            x_extra_text = 0.214
            y_extra_text =  0.823
            c.SetLogy(1)
            h_bkg = ROOT.TH2F("","",100,0,1.1,100,0.0001,0.1)
        elif view == "loglow":
            legend_origin_y = 0.16
            legend_origin_x = 0.48
            c.SetLogy(1)
            h_bkg = ROOT.TH2F("","",100,0,1.,100,0.0001,0.1)
        elif view == "loglow2":
            legend_origin_y = 0.16
            legend_origin_x = 0.52
            c.SetLogy(1)
            h_bkg = ROOT.TH2F("","",100,0,1.,100,0.0001,0.3)
        elif view == "loglow3":
            legend_origin_y = 0.15
            legend_origin_x = 0.59
            y_extra_text =  0.83
            c.SetLogy(1)
            h_bkg = ROOT.TH2F("","",100,0,1.,100,0.0001,0.8)
        elif view == "loglow4":
            legend_origin_y = 0.16
            legend_origin_x = 0.33
            c.SetLogy(1)
            h_bkg = ROOT.TH2F("","",100,0,1.,100,0.0001,0.3)
        elif view == "loglow5":
            legend_origin_y = 0.16
            legend_origin_x = 0.33
            c.SetLogy(1)
            h_bkg = ROOT.TH2F("","",100,0,1.,100,0.0001,1.2)
        elif view == "loglow6":
            legend_origin_y = 0.145
            legend_origin_x = 0.605
            y_extra_text =  0.83
            c.SetLogy(1)
            h_bkg = ROOT.TH2F("","",100,0,1.,100,0.0001,0.8)
        elif view == "logpuppi":
            legend_origin_y = 0.15
            legend_origin_x = 0.32
            c.SetLogy(1)
            h_bkg = ROOT.TH2F("","",100,0,1.,100,0.0001,0.1)
        elif view == "left_top":
            c.SetLogy(0)
            h_bkg = ROOT.TH2F("","",100,0,.4,100,0.99,1)
        elif view == "weak_left_top":
            c.SetLogy(0)
            h_bkg = ROOT.TH2F("","",100,0,.4,100,0.95,1)
        # Top Tagging
        # Medium
        elif view == "middle_top":
            c.SetLogy(0)
            h_bkg = ROOT.TH2F("","",100,0.33,0.66,100,0.8,1)
        # Top Tagging
        # High Efficiency
        elif view == "right_top":
            c.SetLogy(0)
            h_bkg = ROOT.TH2F("","",100,0.66,1.,100,0.4,1)
        # Higgs Tagging
        # High Purity
        elif view == "left_higgs":
            c.SetLogy(0)
            h_bkg = ROOT.TH2F("","",100,0,0.33,100,0.85,1)
        # Higgs Tagging
        # Middle
        elif view == "middle_higgs":
            c.SetLogy(0)
            h_bkg = ROOT.TH2F("","",100,0.33,0.66,100,0.5,.95)
        # Middle Tagging
        # High Efficiency
        elif view == "right_higgs":
            c.SetLogy(0)
            h_bkg = ROOT.TH2F("","",100,0.66,1.,100,0.0,.6)
        # All
        elif view == "all":
            c.SetLogy(0)
            h_bkg = ROOT.TH2F("","",100,0,1.,100,0.9,1)
        elif view == "weak_all":
            c.SetLogy(0)
            h_bkg = ROOT.TH2F("","",100,0,1.,100,0.6,1)
        else:
            print "Invalid view! Exiting.."
            sys.exit()

        legend = ROOT.TLegend( legend_origin_x, 
                               legend_origin_y,
                               legend_origin_x + legend_size_x,
                               legend_origin_y + legend_size_y )
        legend.SetBorderSize(1) 
        legend.SetFillColor(0)
        legend.SetTextSize(0.025)      
        legend.SetBorderSize(0)


        h_bkg.GetXaxis().SetTitle( x_label  )      
        h_bkg.GetXaxis().SetNdivisions(508)
        h_bkg.GetYaxis().SetTitle( "#varepsilon_{B}" )      
        h_bkg.Draw()

        
        txt = ROOT.TText()
        txt.SetTextFont(61)
        txt.SetTextSize(0.05)
        txt.DrawTextNDC(0.20, 0.94, "CMS")

        txt.SetTextFont(52)
        txt.SetTextSize(0.04)
        txt.DrawTextNDC(0.20, 0.90, "Simulation Preliminary")

        txt.SetTextFont(41)
        txt.DrawTextNDC(0.83, 0.90, "13 TeV")
        
        


        gr_and_name = [(a,b) for a,b in zip(li_grs, li_gr_names)]
        gr_and_name.sort(key = lambda x:x[1])


        f_out_gr = open(name + "_out_gr.dat","wb")
        pickle.dump(gr_and_name, f_out_gr)
        f_out_gr.close()

        for i_gr, gr_and_name in enumerate(gr_and_name):    
                        
            gr = gr_and_name[0]

            gr.SetLineColor( li_colors[i_gr] )
            gr.SetFillColor( li_colors[i_gr] )
            gr.SetLineStyle( li_line_styles[i_gr] )
            gr.SetLineWidth( 2)    
            legend.AddEntry( gr, gr_and_name[1], "L" )
            

            if error_band:
                gr.Draw("SAME E3")
            else:
                gr.Draw("SAME")


        for i_wp, wp in enumerate(li_wps):
            wp.SetLineColor( li_colors[i_wp] )
            wp.SetMarkerColor( li_colors[i_wp] )
            wp.SetMarkerStyle( li_marker_styles[i_wp] )
            wp.SetFillColor( li_colors[i_wp] )
            wp.SetLineStyle( li_line_styles[i_wp] )
            wp.SetLineWidth( 2)    
            wp.SetMarkerSize(2)    
            legend.AddEntry( wp, li_wp_names[i_wp], "LP" )
            wp.Draw("E3 SAME")

        l_txt = ROOT.TLatex()    
        l_txt.SetTextSize(0.04)

        for line in extra_text:
            l_txt.DrawLatexNDC(x_extra_text, y_extra_text, line)
            y_extra_text -= 0.06

        legend.Draw()

        c.Print("{0}_{1}.png".format(name, view))
        c.Print("{0}_{1}.pdf".format(name, view))
# end of plotROCs



