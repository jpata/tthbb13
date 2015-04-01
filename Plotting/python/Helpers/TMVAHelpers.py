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

from xml.dom import minidom

import ROOT

# initializer: simple creation of bag-of-object classes
from Initializer import initializer

# Our support Code
# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.VariableHelpers import variable
    from TTH.Plotting.Helpers.HistogramHelpers import Count
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.VariableHelpers import variable
    from TTH.Plotting.python.Helpers.HistogramHelpers import Count


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
    li_methods       - [list of string objects] TMVA methods to apply
    li_vars          - [list of variable objects] variables to include
    file_name_sig    - [string]: full name of the input signal file
    file_name_bkg     - [string]: full name of the input background file
    tree_name_sig    - [string]: name of the tree with signal events
    tree_name_bkg     - [string]: name of the tree with background events
    fiducial_cut_sig - [string]: fiducial cut signal - define denominator of efficiencies
    fiducial_cut_bkg  - [string]: fiducial cut background - define denominator of efficiencies
    weight_sig       - [string]: weight for signal
    weight_bkg        - [string]: weight for bg
    """

    @initializer    
    def __init__( self, 
                  name,
                  pretty_name,
                  li_methods,
                  li_vars,
                  file_name_sig,
                  file_name_bkg,
                  tree_name_sig    = "tree",
                  tree_name_bkg     = "tree",
                  fiducial_cut_sig = "(1)",
                  fiducial_cut_bkg  = "(1)",
                  weight_sig       = "(1)",
                  weight_bkg        = "(1)",
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
    outputFile    = ROOT.TFile( outfname, 'RECREATE' )
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
    li_cuts = ["(1)"]
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
    [event_counts["n_sig_fiducial"], event_counts["e_sig_fiducial"]] = countEventsAndError(signal, setup.fiducial_cut_sig, setup.weight_sig)
    [event_counts["n_bkg_fiducial"],  event_counts["e_bkg_fiducial"]]  = countEventsAndError(background, setup.fiducial_cut_bkg, setup.weight_bkg)
    [event_counts["n_sig_cuts"],     event_counts["e_sig_cuts"]]     = countEventsAndError(signal, cut_signal, setup.weight_sig)
    [event_counts["n_bkg_cuts"],      event_counts["e_bkg_cuts"]]      = countEventsAndError(background, cut_bkg, setup.weight_bkg)

    pickle.dump(event_counts, outputFilePickle)
    outputFilePickle.close()


    ########################################
    # TMVA starts here
    ########################################

    print cut_signal

    # Create instance of TMVA factory
    factory = ROOT.TMVA.Factory( setup.name, outputFile, 
                            "!V:!Silent:Color:DrawProgressBar:Transformations=I:AnalysisType=Classification" )
    factory.SetVerbose( False )

    # Add variables to factory
    for var in setup.li_vars:
        factory.AddVariable( var.name, 'F' )

    # Global event weights
    signalWeight     = 1.0
    backgroundWeight = 1.0

    # register trees
    factory.AddSignalTree    ( signal,     signalWeight     )
    factory.AddBackgroundTree( background, backgroundWeight )

    mycutSig = ROOT.TCut(cut_signal ) 
    mycutBkg = ROOT.TCut(cut_bkg )


    factory.SetSignalWeightExpression( setup.weight_sig )
    factory.SetBackgroundWeightExpression( setup.weight_bkg)



    # prepare trees
    factory.PrepareTrainingAndTestTree( mycutSig, mycutBkg,
                                        "SplitMode=Random:NormMode=None:!V" )


    ########################################
    # Schedule the Classifiers
    ########################################
    
    if "Cuts" in setup.li_methods:

        sample_size = { 1 :   30000,
                        2 :   80000*4,
                        3 : 10000000}

        factory.BookMethod( ROOT.TMVA.Types.kCuts, 
                            "Cuts",
                            #"PopSize=150:Steps=20",
                            "FitMethod=MC:SampleSize={0}".format(sample_size[len(setup.li_vars)])
        )

    if "Likelihood" in setup.li_methods:
        factory.BookMethod( ROOT.TMVA.Types.kLikelihood, 
                            "Likelihood",
                            "")
                            #"H:!V:TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmoothBkg[1]=10:NSmooth=1:NAvEvtPerBin=50"
                            #"!H:!V:!TransformOutput:PDFInterpol=KDE:KDEtype=Gauss:KDEiter=Adaptive:KDEFineFactor=0.3:KDEborder=None:NAvEvtPerBin=100")

    if "Fisher" in setup.li_methods:
        factory.BookMethod( ROOT.TMVA.Types.kFisher, 
                            "Fisher", 
                            "H:!V" )

    if "MLP" in setup.li_methods:
        factory.BookMethod( ROOT.TMVA.Types.kMLP, 
                            "MLP", 
                            "H:!V:NeuronType=tanh:VarTransform=N:NCycles=1200:HiddenLayers=N+5:TestRate=5:!UseRegulator" )

    if "SVM" in setup.li_methods:
        factory.BookMethod( ROOT.TMVA.Types.kSVM, 
                            "SVM", 
                            "Gamma=0.25:Tol=0.001:VarTransform=Norm" )

    if "BDTG" in setup.li_methods:
        factory.BookMethod( ROOT.TMVA.Types.kBDT, 
                            "BDTG",
        "!H:!V:NTrees=1000:BoostType=Grad:Shrinkage=0.30:UseBaggedGrad:GradBaggingFraction=0.6:SeparationType=GiniIndex:nCuts=20:NNodesMax=5" )

    if "BDT" in setup.li_methods:
        factory.BookMethod( ROOT.TMVA.Types.kBDT, 
                            "BDT",
                            "!H:!V:NTrees=50:MaxDepth=2:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex:nCuts=20:PruneMethod=NoPruning" )

    if "BDTB" in setup.li_methods:
        factory.BookMethod( ROOT.TMVA.Types.kBDT, 
                            "BDTB",
                            "!H:!V:NTrees=400:BoostType=Bagging:SeparationType=GiniIndex:nCuts=20:PruneMethod=NoPruning" )

    if "BDTD" in setup.li_methods:
        factory.BookMethod( ROOT.TMVA.Types.kBDT, 
                            "BDTD",
                            "!H:!V:NTrees=400:nEventsMin=400:MaxDepth=3:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=20:PruneMethod=NoPruning:VarTransform=Decorrelate" )


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


########################################
# plotROCs
########################################

def plotROCs(name, li_setups, view="all"):
    
    li_colors = [ROOT.kRed,      ROOT.kBlue+1,     ROOT.kBlack, 
                 ROOT.kOrange-1, ROOT.kViolet+1,   ROOT.kGreen+1,
                 ROOT.kGray,     ROOT.kYellow]*10

    li_line_styles = [1]*(len(li_colors)/10) + [2]*(len(li_colors)/10) + [3]*(len(li_colors)/10)


    ########################################
    # Extract histograms from files
    ########################################

    li_hs    = []
    li_names = []
    li_pretty_names = []

    di_cut_fracs = {}

    li_grs = []

    # Loop over setyps
    for setup in li_setups: 

        input_filename = "TMVA_{0}.root".format(setup.name)
        
        # We need three things:
        # -the pickle that tells us the efficiency/uncertainty of the preselection cut
        # -the output root file produced by TMVA: so we can evaluate the efficiency on the test-tree
        # -the weights.xml file produced by TMVA: this is where we read the working points from
        
        # First get the cut (preselection, not wp) efficiaency + uncertainty 
        f_pickle = open( input_filename.replace(".root",".dat"), "r")
        event_counts = pickle.load(f_pickle)        
                
        # Get the trees
        f = ROOT.TFile(input_filename, "READ" )        
        testTree = f.FindObjectAny("TestTree")
        trainTree = f.FindObjectAny("TrainTree")

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

        for method in setup.li_methods:
            
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

            # This should be 100 bins with cuts
            binlist = xmldoc.getElementsByTagName('Weights')[0].getElementsByTagName("Bin")

            gr = ROOT.TGraphAsymmErrors(len(binlist))

            for ibin, x in enumerate(binlist):
                
                # We don't need the preselection cuts - they're already applied when making the test tree                
                li_cuts = ["(1)"]

                # Turn the ranges into cuts
                for i_expr, expr in enumerate(expressions):                                        
                    min_val =  x.getElementsByTagName("Cuts")[0].attributes["cutMin_{0}".format(i_expr)].value
                    max_val =  x.getElementsByTagName("Cuts")[0].attributes["cutMax_{0}".format(i_expr)].value

                    li_cuts.append("({0}>{1})".format(expr, min_val))
                    li_cuts.append("({0}<{1})".format(expr, max_val))
                # End of loop over expressions

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
                
                #print "Sig: {0:5<.3f} +{1:5<.3f} -{2:5<.3f}   Bkg: {3:5<.3f} +{4:5<.3f} -{5:5<.3f}".format(eff_total_sig*100,
                #                                                                                           err_total_sig_high*100,
                #                                                                                           err_total_sig_low*100,
                #                                                                                           eff_total_bkg_new*100,
                #                                                                                           err_total_bkg_high*100,
                #                                                                                           err_total_bkg_low*100)

                gr.SetPoint(ibin, eff_total_sig, 1-eff_total_bkg)
                # As we show -e(bg) we have to flip high/low for it 
                gr.SetPointError(ibin, err_total_sig_low, err_total_sig_high,  err_total_bkg_high, err_total_bkg_low) 
                
            # End loop over bins
            li_grs.append(gr)
        # End loop over methods            
    # End loop over infiles


    ########################################
    # And draw them
    ########################################

    c = ROOT.TCanvas( "","", 800, 800)

    legend_origin_x     = 0.21
    legend_origin_y     = 0.18
    legend_size_x       = 0.3
    legend_size_y       = 0.04 * len(li_hs)

    legend = ROOT.TLegend( legend_origin_x, 
                           legend_origin_y,
                           legend_origin_x + legend_size_x,
                           legend_origin_y + legend_size_y )
    legend.SetBorderSize(1) 
    legend.SetFillColor(0)
    legend.SetTextSize(0.03)      
    legend.SetBorderSize(0)

    # Top Tagging
    # High Purity
    if view == "left_top":
        c.SetLogy(0)
        h_bkg = ROOT.TH2F("","",100,0,0.33,100,0.98,1)
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
        h_bkg = ROOT.TH2F("","",100,0,1.,100,0.,1)
    else:
        print "Ivalid view! Exiting.."
        sys.exit()

    h_bkg.GetXaxis().SetTitle( "#varepsilon(S)" )      
    h_bkg.GetYaxis().SetTitle( "1-#varepsilon(B)" )      
    h_bkg.Draw()

    for i_h, h in enumerate(li_hs):
        h.SetLineColor( li_colors[i_h] )
        h.SetFillColor( li_colors[i_h] )
        h.SetLineStyle( li_line_styles[i_h] )
        h.SetLineWidth( 2)    
        legend.AddEntry( h, li_pretty_names[i_h], "L" )

    for gr in li_grs:    
        gr.Draw("SAME 2")
    legend.Draw()

    c.Print("{0}_{1}.png".format(name, view))
    c.Print("{0}_{1}.pdf".format(name, view))
# end of plotROCs


########################################
# plotROCMultiple
########################################

def plotROCMultiple(name, li_setups, tagging_object = "top"):
    """ Call plotROCs multiple times looking at different regions"""
    
    plotROCs(name, li_setups, "all")
    if tagging_object == "top":
        plotROCs(name, li_setups, "left_top")
        plotROCs(name, li_setups, "middle_top")
        plotROCs(name, li_setups, "right_top")
    elif tagging_object == "higgs":
        plotROCs(name, li_setups, "left_higgs")
        plotROCs(name, li_setups, "middle_higgs")
        plotROCs(name, li_setups, "right_higgs")
# end of plotROCMultiple



