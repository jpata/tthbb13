#!/usr/bin/env python
"""
Helper script for the evaluation of different methods/variables using TMVA.
"""

########################################
# Imports and Macros
########################################

import sys
import pickle

from ROOT import TFile, TTree, TCut, TMVA



########################################
# doTMVA
########################################

def doTMVA( infnameSig, infnameBkg,
            outfname,
            li_methods,
            li_vars,
            treeNameSig  = "tree",
            treeNameBkg  = "tree",
        ):
        
    ########################################
    # Prepare IO & TMVA
    ########################################

    # Open Files
    outputFile    = TFile( outfname, 'RECREATE' )
    outputFilePickle = open( outfname.replace(".root",".dat"), "w")
    inputFileSig  = TFile.Open( infnameSig )
    inputFileBkg  = TFile.Open( infnameBkg )

    # Create instance of TMVA factory
    factory = TMVA.Factory( "TMVAClassification", outputFile, 
                            "!V:!Silent:Color:DrawProgressBar:Transformations=I:AnalysisType=Classification" )
    factory.SetVerbose( False )

    # Add variables to factory
    li_cuts = ["(1)"]
    for var in li_vars:
        factory.AddVariable( var[0], 'F' )
        li_cuts.append( "({0}>={1})".format(var[0],var[1]))
        li_cuts.append( "({0}<={1})".format(var[0],var[2]))

    # Apply additional cuts on the signal and background sample. 
    cut = "&&".join(li_cuts)
    
    # Get the signal and background trees for training
    signal      = inputFileSig.Get( treeNameSig )
    background  = inputFileBkg.Get( treeNameBkg )

    n_sig = signal.Draw("(1)","(1)")
    n_sig_cut = signal.Draw("(1)", cut)

    n_bg = background.Draw("(1)","(1)")
    n_bg_cut = background.Draw("(1)", cut)

    cut_frac = {}
    cut_frac["sig"] = (1. * n_sig_cut / n_sig)
    cut_frac["bg"]  = (1. * n_bg_cut /  n_bg)
    
    pickle.dump(cut_frac, outputFilePickle)
    outputFilePickle.close()

    # Global event weights
    signalWeight     = 1.0
    backgroundWeight = 1.0

    # register trees
    factory.AddSignalTree    ( signal,     signalWeight     )
    factory.AddBackgroundTree( background, backgroundWeight )


    mycutSig = TCut( cut ) 
    mycutBkg = TCut( cut ) 

    # prepare trees
    factory.PrepareTrainingAndTestTree( mycutSig, mycutBkg,
                                        "nTrain_Signal=0:nTrain_Background=0:nTest_Signal=0:nTest_Background=0:SplitMode=Random:NormMode=NumEvents:!V" )


    ########################################
    # Schedule the Classifiers
    ########################################
    
    # Cut optimisation
    if "Cuts" in li_methods:
        factory.BookMethod( TMVA.Types.kCuts, 
                            "Cuts",
                            "FitMethod=SA" )

    if "Likelihood" in li_methods:
        factory.BookMethod( TMVA.Types.kLikelihood, 
                            "Likelihood",
                            "" )

    if "Fisher" in li_methods:
        factory.BookMethod( TMVA.Types.kFisher, 
                            "Fisher", 
                            "H:!V:Fisher:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10" )

    if "MLP" in li_methods:
        factory.BookMethod( TMVA.Types.kMLP, 
                            "MLP", 
                            "H:!V:NeuronType=tanh:VarTransform=N:NCycles=1200:HiddenLayers=N+5:TestRate=5:!UseRegulator" )

    if "SVM" in li_methods:
        factory.BookMethod( TMVA.Types.kSVM, 
                            "SVM", 
                            "Gamma=0.25:Tol=0.001:VarTransform=Norm" )

    if "BDTG" in li_methods:
        factory.BookMethod( TMVA.Types.kBDT, 
                            "BDTG",
        "!H:!V:NTrees=1000:BoostType=Grad:Shrinkage=0.30:UseBaggedGrad:GradBaggingFraction=0.6:SeparationType=GiniIndex:nCuts=20:NNodesMax=5" )

    if "BDT" in li_methods:
        factory.BookMethod( TMVA.Types.kBDT, 
                            "BDT",
                            "!H:!V:NTrees=850:nEventsMin=150:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex:nCuts=20:PruneMethod=NoPruning" )

    if "BDTB" in li_methods:
        factory.BookMethod( TMVA.Types.kBDT, 
                            "BDTB",
                            "!H:!V:NTrees=400:BoostType=Bagging:SeparationType=GiniIndex:nCuts=20:PruneMethod=NoPruning" )

    if "BDTD" in li_methods:
        factory.BookMethod( TMVA.Types.kBDT, 
                            "BDTD",
                            "!H:!V:NTrees=400:nEventsMin=400:MaxDepth=3:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=20:PruneMethod=NoPruning:VarTransform=Decorrelate" )


    ########################################
    # Do actual training&testing work
    ########################################

    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()    
    outputFile.Close()

# end of doTMVA
