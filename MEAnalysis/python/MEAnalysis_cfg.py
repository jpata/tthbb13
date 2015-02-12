import FWCore.ParameterSet.Types  as CfgTypes
import FWCore.ParameterSet.Config as cms
import os

process = cms.Process("MEAnalysisNew")

from TTH.MEAnalysis.samples_v1 import samples, pathToFile, samplePrefix
process.fwliteInput = cms.PSet(

    # output file name
    outFileName   = cms.string("./root/MEAnalysisNewTEST.root"),
    #outFileName   = cms.string("/scratch/bianchi/Trees/MEM/MEAnalysisNewTEST_Sherpa_Had.root"),

    isMC = cms.bool(True),

    # path to the TF root file
    pathToTF      = cms.string("./root/transferFunctionsTEST.root"),

    # path to CVS shapes & TF parameters
    pathToCP      = cms.string("./root/ControlPlotsTEST.root"),

    # path to TF parameters from gen-jets --> reco-jets
    pathToCP_smear= cms.string("./root/ControlPlotsTEST_std_gen.root"),

    # input file directory
    pathToFile    = pathToFile,

    # a name tag for the input files
    ordering      = samplePrefix,

    # the samples
    samples = samples,

    # the target luminosity (used to calculate the 'weight' variable)
    lumi          = cms.untracked.double(19.04),

    # run both S and B hypotheses
    SoB                       = cms.untracked.int32(1),

    # in case SoB=0, run only this hypothesis
    hypo                      = cms.untracked.int32(0),

    # optimization0: re-run integral if bad chi2
    integralOption0           = cms.untracked.int32(0),

    # max chi2 for optimization0
    maxChi2                   = cms.untracked.double(2.5),

    # optimization1: skip combinations loosely compatible with H/t/W mass
    integralOption1           = cms.untracked.int32(0),

    # optimization2: re-run the integral using last VEGAS grid only
    integralOption2           = cms.untracked.int32(1),

    # number of iterations for option2
    integralOption2_stage     = cms.untracked.int32(1),

    # number of iterations for option2
    integralOption2_niter     = cms.untracked.int32(1),

    # increase in evaluations for option2
    integralOption2_nevalfact = cms.untracked.double(1.),

    # divide ME weight by total cross-section
    norm            = cms.untracked.int32(0),

    # formulas for total cross-section
    functions     = cms.vstring(
    '8.95351e+18*TMath::Landau(x, 5.67600e+01,1.01258e+01)',                # incl
    '2.95547e+17*TMath::Landau(x,7.61581e+01 ,1.89245e+01)',                # SL2wj
    '2.98474e+17*TMath::Landau(x,7.40196e+01 ,1.80142e+01)',                # SL1wj
    '6.28300e+16*TMath::Landau(x,8.03060e+01 ,1.81679e+01)',                # SLNoBHad
    'x>150?2.44515e+27*x^(-5.35628e+00):1.24208e+18*exp((-3.63162e-02)*x)', # SLNoHiggs
    'x>=12 ? x^(-2.010e-01)*exp((-1.5785e-02)*x) : 4.184e-02*x'),           # tth Pt

    # switch-off OL
    switchoffOL   = cms.untracked.int32(0), ###### CHECK HERE

    # skip VEGAS call
    speedup       = cms.untracked.int32(0), ###### CHECK HERE

    # select which analysis to run
    # select with 4-6 jets regardless of btagging
    # used for determinging btag_LR cut
    doTypeBTag6   = cms.untracked.int32(0),  #SL 6 jets
    doTypeBTag5   = cms.untracked.int32(0),  #SL 5 jets
    doTypeBTag4   = cms.untracked.int32(0),  #DL 4 jets

    # select by CSVM count
    doType0       = cms.untracked.int32(0),  #SL(4,2)  w/  W-tag
    doType1       = cms.untracked.int32(0),  #SL(4,2)  w/o W-tag
    doType2       = cms.untracked.int32(0),  #SL(4,1)
    doType3       = cms.untracked.int32(0),  #SL(4,3)
    doType4       = cms.untracked.int32(0),  #SL(3,2)
    doType6       = cms.untracked.int32(0),  #DL(4,X)
    doType7       = cms.untracked.int32(0),  #DL(3M+1L,X)
    doType0ByBTagShape = cms.untracked.int32(1),
    doType1ByBTagShape = cms.untracked.int32(1),
    doType2ByBTagShape = cms.untracked.int32(1),
    doType3ByBTagShape = cms.untracked.int32(1),
    doType6ByBTagShape = cms.untracked.int32(1),

    # MEIntegrator options
    useME         = cms.untracked.int32(1),
    useJac        = cms.untracked.int32(1),
    useMET        = cms.untracked.int32(1),
    useTF         = cms.untracked.int32(1),
    usePDF        = cms.untracked.int32(1),
    useAnalyticalFormula = cms.untracked.int32(1),
    useDynamicalScale    = cms.untracked.int32(1),

    # use DG for b-jet TF
    doubleGaussianB  = cms.untracked.int32(1),

    # use jet b-tag information
    useBtag          = cms.untracked.int32(1),
    useCMVA          = cms.untracked.int32(0),

    # select events based on btag LLR
    selectByBTagShape= cms.untracked.int32(1),

    # use CSV tag-and-probe
    useCSVcalibration= cms.untracked.int32(1),

    # recover >4 btag events
    recoverTopBTagBin = cms.untracked.int32(1),

    # test SLw1j hypothesis on type3 events
    testSLw1jType3 = cms.untracked.int32(1),

    # test hypo SLw1j on up to nMaxJetsSLw1jType3 untagged jets
    nMaxJetsSLw1jType3 = cms.untracked.int32(4),

    # b-tag thresholds (for jet counting)
    csv_WP_L         = cms.untracked.double( 0.244 ),
    csv_WP_M         = cms.untracked.double( 0.679 ),
    csv_WP_T         = cms.untracked.double( 0.898 ),

    # if selectByBTagShape, choose cut-value
    #btag_prob_cut_6jets = cms.untracked.double( 0.96675 ),
    btag_prob_cut_6jets = cms.untracked.double( 0.960   ),
    btag_prob_cut_5jets = cms.untracked.double( 0.98225 ),
    btag_prob_cut_4jets = cms.untracked.double( 0.95295 ),

    # apply energy regression on jets
    useRegression    = cms.untracked.int32(0),

    # evaluate trigger errors
    triggerErrors        = cms.untracked.int32(1),
    pathTo_f_Vtype1_id   = cms.string("root/EleRecoId.ScaleFactor.wp95.2012ABCD.root"),
    pathTo_f_Vtype1L1_tr = cms.string("root/DoubleEle17.TrigEff.wp95.2012ABCD.root"),
    pathTo_f_Vtype1L2_tr = cms.string("root/DoubleEle8.TrigEff.wp95.2012ABCD.root"),
    pathTo_f_Vtype2_id   = cms.string("root/MuRecoId.ScaleFactor.2012ABCD.root"),
    pathTo_f_Vtype2_tr   = cms.string("root/SingleMu24OR40.TrigEff.2012ABCD.root"),
    pathTo_f_Vtype3_id   = cms.string("root/EleRecoId.ScaleFactor.wp80.2012ABCD.root"),
    pathTo_f_Vtype3_tr   = cms.string("root/SingleEle.TrigEff.wp80.2012ABCD.root"),

    # print out the integral at run-time
    printout     = cms.untracked.int32(0),

    # various degrees of verbosity
    debug        = cms.untracked.int32(0),

    # extremely verbose
    verbose      = cms.bool(False),

    # the 'nominal' Higgs, top, and W masses
    MH           = cms.untracked.double(125.00),
    MT           = cms.untracked.double(174.30),
    MW           = cms.untracked.double( 80.19),

    # lepton selection cut thresholds
    lepPtLoose   = cms.untracked.double(20),
    lepPtTight   = cms.untracked.double(30),
    lepIsoLoose  = cms.untracked.double(0.2),
    lepIsoTight  = cms.untracked.double(0.12),
    elEta        = cms.untracked.double(2.5),
    muEtaTight   = cms.untracked.double(2.1),
    muEtaLoose   = cms.untracked.double(2.4),

    # jet preselection
    jetMultLoose   = cms.untracked.int32(0),
    jetPtLoose     = cms.untracked.double(40.),
    jetPtThreshold = cms.untracked.double(30.),

    # needed for category classification
    MwL          = cms.untracked.double(60),
    MwH          = cms.untracked.double(100),
    MhL          = cms.untracked.double(110),
    MhH          = cms.untracked.double(140),

    MwLType3     = cms.untracked.double(72.),
    MwHType3     = cms.untracked.double(92.),

    # Reject run range 207883-208307 because of a pixel misalignment problem ( following VHbb )
    reject_pixel_misalign_evts = cms.untracked.int32(0),

    # Higgs and top mass values to be scanned
    massesH      = cms.vdouble(125.),
    #massesH      = cms.vdouble(105.,110.,115.,120.,125.,130.,135.,140.),
    massesT      = cms.vdouble(174.3),
    #massesT      = cms.vdouble(145, 155, 165, 174, 185, 195, 205),

    # if 1, process evLimits[1]-evLimits[0] events passing the selection cuts
    # if 0, process all events in the tree from evLimits[0] to evLimits[1]
    fixNumEvJob    = cms.untracked.int32(0),

    # event limits
    evLimits       = cms.vint32(0, -1),

    # do systematic shifts (dummy)
    doJERbias  = cms.untracked.int32(0),
    doCSVup    = cms.untracked.int32(0),
    doCSVdown  = cms.untracked.int32(0),
    doJECup    = cms.untracked.int32(0),
    doJECdown  = cms.untracked.int32(0),
    doJERup    = cms.untracked.int32(0),
    doJERdown  = cms.untracked.int32(0),

    # choose which systematics to run
    # [0=nominal, 1=CSVup, 2=CSVdown, 3=JECup, 4=JECdown, 5=JERup, 6=JERdown]
    systematics= cms.vint32(0),

    # if 1, gen-jets in the input tree are smeared by the TF
    # if 0, use the reco-jets
    doGenLevelAnalysis  = cms.untracked.int32(0),

    # if 1 and doGenLevelAnalysis, jet energy gets smeared by TF_smear
    smearJets           = cms.untracked.int32(0),

    # toss csv values untill the event passes the cut
    enhanceMC           = cms.untracked.int32(0),

    # maximum number of trials (if enhanceMC)
    max_n_trials        = cms.untracked.int32(50000),

    # if 1, save into the tree all events
    # if 0, save only events passing the analysis cuts
    ntuplizeAll         = cms.untracked.int32(1),

    cutLeptons = cms.untracked.bool(False),
    cutJets = cms.untracked.bool(False),
    cutWMass = cms.untracked.bool(False),
    cutBTagShape = cms.untracked.bool(False),
)
