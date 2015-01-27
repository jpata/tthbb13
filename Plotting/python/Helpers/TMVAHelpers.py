#!/usr/bin/env python
"""
Helper script for the evaluation of different methods/variables using TMVA.
"""

########################################
# Imports and Macros
########################################

import sys
import os
import pickle

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
    file_name_bg     - [string]: full name of the input background file
    tree_name_sig    - [string]: name of the tree with signal events
    tree_name_bg     - [string]: name of the tree with background events
    fiducial_cut_sig - [string]: fiducial cut signal - define denominator of efficiencies
    fiducial_cut_bg  - [string]: fiducial cut background - define denominator of efficiencies
    weight_sig       - [string]: weight for signal
    weight_bg        - [string]: weight for bg
    """

    @initializer    
    def __init__( self, 
                  name,
                  pretty_name,
                  li_methods,
                  li_vars,
                  file_name_sig,
                  file_name_bg,
                  tree_name_sig    = "tree",
                  tree_name_bg     = "tree",
                  fiducial_cut_sig = "(1)",
                  fiducial_cut_bg  = "(1)",
                  weight_sig       = "(1)",
                  weight_bg        = "(1)",
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
    inputFileBkg  = ROOT.TFile.Open( setup.file_name_bg )

    # Get the signal and background trees for training
    signal      = inputFileSig.Get( setup.tree_name_sig )
    background  = inputFileBkg.Get( setup.tree_name_bg )


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
    cut_bg     = "&&".join(li_cuts + [setup.fiducial_cut_bg])

    # Calculate cut efficiency and store it in a pickle file
    # This can be used later to properly normalize the ROC curves
    n_sig = Count(signal, "({0})*{1}".format(setup.fiducial_cut_sig, setup.weight_sig))
    n_sig_cut = Count(signal, "({0})*{1}".format(cut_signal, setup.weight_sig))

    n_bg = Count(background, "({0})*{1}".format(setup.fiducial_cut_bg, setup.weight_bg))
    n_bg_cut = Count(background, "({0})*{1}".format(cut_bg, setup.weight_bg))

    cut_frac = {}
    cut_frac["sig"] = (1. * n_sig_cut / n_sig)
    cut_frac["bg"]  = (1. * n_bg_cut /  n_bg)
    
    pickle.dump(cut_frac, outputFilePickle)
    outputFilePickle.close()


    ########################################
    # TMVA starts here
    ########################################

    print cut_signal

    # Create instance of TMVA factory
    factory = ROOT.TMVA.Factory( "TMVAClassification", outputFile, 
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
    mycutBkg = ROOT.TCut(cut_bg )


    factory.SetSignalWeightExpression( setup.weight_sig )
    factory.SetBackgroundWeightExpression( setup.weight_bg)



    # prepare trees
    factory.PrepareTrainingAndTestTree( mycutSig, mycutBkg,
                                        "nTrain_Signal=0:nTrain_Background=0:nTest_Signal=0:nTest_Background=0:SplitMode=Random:NormMode=NumEvents:!V" )


    ########################################
    # Schedule the Classifiers
    ########################################
    
    if "Cuts" in setup.li_methods:

        sample_size = { 1 :   10000,
                        2 :   80000,
                        3 : 4000000}

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

    for setup in li_setups: 
        
        print setup.name

        input_filename = "TMVA_{0}.root".format(setup.name)
        f = ROOT.TFile(input_filename, "READ" )

        for method in setup.li_methods:
            h = f.FindObjectAny("MVA_" + method + "_rejBvsS")
            hc = h.Clone()
            hc.SetDirectory(0)
            li_hs.append( hc )
            li_names.append( setup.name  )
            li_pretty_names.append(setup.pretty_name)

        f_pickle = open( input_filename.replace(".root",".dat"), "r")
        di_cut_fracs[setup.name] = pickle.load(f_pickle)        
    # end loop over infiles


    ########################################
    # And draw them
    ########################################

    c = ROOT.TCanvas( "","", 800, 800)

    legend_origin_x     = 0.17
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
        h_bg = ROOT.TH2F("","",100,0,0.33,100,0.95,1)
    # Top Tagging
    # Medium
    elif view == "middle_top":
        c.SetLogy(0)
        h_bg = ROOT.TH2F("","",100,0.33,0.66,100,0.8,1)
    # Top Tagging
    # High Efficiency
    elif view == "right_top":
        c.SetLogy(0)
        h_bg = ROOT.TH2F("","",100,0.66,1.,100,0.4,1)
    # Higgs Tagging
    # High Purity
    elif view == "left_higgs":
        c.SetLogy(0)
        h_bg = ROOT.TH2F("","",100,0,0.33,100,0.85,1)
    # Higgs Tagging
    # Middle
    elif view == "middle_higgs":
        c.SetLogy(0)
        h_bg = ROOT.TH2F("","",100,0.33,0.66,100,0.5,.95)
    # Middle Tagging
    # High Efficiency
    elif view == "right_higgs":
        c.SetLogy(0)
        h_bg = ROOT.TH2F("","",100,0.66,1.,100,0.0,.6)
    # All
    elif view == "all":
        c.SetLogy(0)
        h_bg = ROOT.TH2F("","",100,0,1.,100,0.,1)
    else:
        print "Ivalid view! Exiting.."
        sys.exit()

    h_bg.GetXaxis().SetTitle( "#varepsilon(S)" )      
    h_bg.GetYaxis().SetTitle( "1-#varepsilon(B)" )      
    h_bg.Draw()

    for i_h, h in enumerate(li_hs):

        cut_fraction_signal = di_cut_fracs[li_names[i_h]]["sig"] 
        cut_fraction_bg = di_cut_fracs[li_names[i_h]]["bg"] 

        print li_names[i_h], cut_fraction_signal, cut_fraction_bg

        h.GetXaxis().SetLimits(0.0,cut_fraction_signal)

        for ibin in range(1, h.GetXaxis().GetNbins()):
            eff_b = 1 - h.GetBinContent(ibin)
            eff_b_new = eff_b * cut_fraction_bg
            h.SetBinContent(ibin, 1-eff_b_new)

        h.SetLineColor( li_colors[i_h] )
        h.SetLineStyle( li_line_styles[i_h] )
        h.SetLineWidth( 2)    
        legend.AddEntry( h, li_pretty_names[i_h], "L" )

    for h in li_hs:    
        h.Draw("SAME ][")
    legend.Draw()

    c.Print("{0}_{1}.png".format(name, view))
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



