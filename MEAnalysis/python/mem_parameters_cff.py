import FWCore.ParameterSet.Config as cms

############################################### Run
###############################################

# path to file
#pathToFile = '/pnfs/psi.ch/cms/trivcat/store//user/bianchi/HBB_EDMNtuple/AllHDiJetPt'
pathToFile = '/hdfs/cms/store/user/jpata/tth/v1/'
ordering   = ''

# luminosity
lumi = 1.0

from TTH.MEAnalysis.samples_v1 import samples

# 0 = all events between evLow and evHigh will be considered
# 1 = process (evHigh-evLow) events of the desired type starting from the beginning
#
fixNumEvJob = 0

# run on all events
evLimits = cms.vint32(0, -1),

# ntuplize all events ?
ntuplizeAll = 0

# print intermediate steps
printout    = 1

# verbosity [0,1,2,3]
debug       = 0

# systematics
#systematics = cms.vint32(0,3,4,5,6)
#
systematics = cms.vint32(0)

############################################### Object definition
###############################################

# use b-energy regression
useRegression      = 0

# read the (statistical error on the trigger/id scale factors
triggerErrors      = 1

# use gen-jets or reco-jets
doGenLevelAnalysis = 0

# smear jets by TF_smear
smearJets          = 0

# use DG parametrization for b-jets TF
doubleGaussianB    = 1

# use csv
useBtag            = 1

# use MVA b-tagging
useCMVA            = 0

# use the csv calibration from BDT
useCSVcalibration  = 1

# toss csv values untill the event passes the cut
enhanceMC          = 0

# maximum number of trials (if enhanceMC)
max_n_trials       = 200000

############################################### Event selection
###############################################

# jet preselection
jetMultLoose   = 0
jetPtLoose     = 40.
jetPtThreshold = 30.

# lepton selection cut thresholds
lepPtLoose   = 20.
lepPtTight   = 30.
lepIsoLoose  = 0.20
lepIsoTight  = 0.12
elEta        = 2.5
muEtaTight   = 2.1
muEtaLoose   = 2.4

# btag-thresholds
csv_WP_L = 0.244
csv_WP_M = 0.679
csv_WP_T = 0.898

# select by btag_LR
#0 -> choose fixed num of tags
#1 -> choose by LR cut
selectByBTagShape  = 1

# cut values to select events
btag_prob_cut_6jets = 0.960
btag_prob_cut_5jets = 0.970
btag_prob_cut_4jets = 0.850

############################################### Category definition
###############################################

# needed for category classification
MwL          = 60.
MwH          = 100.
MhL          = 110.
MhH          = 140.
MwLType3     = 72.
MwHType3     = 92.

# recover the <4 btag bin
recoverTopBTagBin  = 1

# test SLw1j hypothesis on type3 events
testSLw1jType3     = 1

# test hypo SLw1j on up to nMaxJetsSLw1jType3 untagged jets
nMaxJetsSLw1jType3 = 4


############################################### ME configuration
###############################################

# central mass values
MH          = 125.00
MT          = 173.50

# whuch mass values to scan
#massesH     = cms.vdouble( 125. )
#massesT     = cms.vdouble(174.3)
massesH     = cms.vdouble( MH )
massesT     = cms.vdouble( MT )

# an extra name for the output files
extraoutname = ""
if len(massesH)>1:
    extraoutname = "MHscan_"
if len(massesT)>1:
    extraoutname = "MTscan_"

# normalize weight by xsec (default 0)
norm                 = 0

# use ME in weight calculation
useME                = 1

# use jacobians in weight calculation
useJac               = 1

# use MET TF in weight calculation
useMET               = 1

# use jet TF in weight calculation
useTF                = 1

# use gg PDF in weight calculation
usePDF               = 1

# use analytical t decay amplitude in weight calculation
useAnalyticalFormula = 1

# use dynamical state when evaluating ttbb prob.
useDynamicalScale    = 1

# chi2-optimization
integralOption0      = 0
maxChi2              = 2.5

# permutation pruning
integralOption1      = 0

# integration speed-up
integralOption2           = 1
integralOption2_stage     = 1
integralOption2_niter     = 1
integralOption2_nevalfact = 1.0

# switch off ME calculation
speedup              = 0

# switch off OL calculation
switchoffOL          = 0
