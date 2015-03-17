import FWCore.ParameterSet.Config as cms

def configure(pi):
	# luminosity
	pi.lumi = 1.0
	pi.fixNumEvJob = 0
	pi.ntuplizeAll = 1
	pi.printout    = 0
	pi.debug       = 0
	pi.systematics = cms.vint32(0)

	pi.useRegression      = 0
	pi.triggerErrors      = 1
	pi.doGenLevelAnalysis = 0
	pi.smearJets          = 0
	pi.doubleGaussianB    = 1
	pi.useBtag            = 1
	pi.useCMVA            = 0
	pi.useCSVcalibration  = 1
	pi.enhanceMC          = 0
	pi.max_n_trials       = 200000

	pi.jetMultLoose   = 0
	pi.jetPtLoose     = 40.
	pi.jetPtThreshold = 30.

	pi.lepPtLoose   = 20.
	pi.lepPtTight   = 30.
	pi.lepIsoLoose  = 0.20
	pi.lepIsoTight  = 0.12
	pi.elEta        = 2.5
	pi.muEtaTight   = 2.1
	pi.muEtaLoose   = 2.4

	pi.csv_WP_L = 0.244
	pi.csv_WP_M = 0.679
	pi.csv_WP_T = 0.898

	pi.selectByBTagShape  = 1

	pi.btag_prob_cut_6jets = 0.960 #SL cat 1-2, type 0-2
	pi.btag_prob_cut_5jets = 0.970 #SL cat 3: type 3
	pi.btag_prob_cut_4jets = 0.850 #DL: type 6

	pi.MwL          = 60.
	pi.MwH          = 100.
	pi.MhL          = 110.
	pi.MhH          = 140.
	pi.MwLType3     = 72.
	pi.MwHType3     = 92.

	pi.recoverTopBTagBin  = 1

	# test SLw1j hypothesis on type3 events
	pi.testSLw1jType3     = 1

	# test hypo SLw1j on up to nMaxJetsSLw1jType3 untagged jets
	pi.nMaxJetsSLw1jType3 = 4


	############################################### ME configuration
	###############################################

	# central mass values
	MH          = 125.00
	MT          = 173.50

	# whuch mass values to scan
	#massesH     = cms.vdouble( 125. )
	#massesT     = cms.vdouble(174.3)
	pi.massesH     = cms.vdouble( MH )
	pi.massesT     = cms.vdouble( MT )

	# an extra name for the output files
	#extraoutname = ""
	#if len(massesH)>1:
	#    pi.extraoutname = "MHscan_"
	#if len(massesT)>1:
	#    pi.extraoutname = "MTscan_"

	# normalize weight by xsec (default 0)
	pi.norm                 = 0

	# use ME in weight calculation
	pi.useME                = 1

	# use jacobians in weight calculation
	vuseJac               = 1

	# use MET TF in weight calculation
	pi.useMET               = 1

	# use jet TF in weight calculation
	pi.useTF                = 1

	# use gg PDF in weight calculation
	pi.usePDF               = 1

	# use analytical t decay amplitude in weight calculation
	pi.useAnalyticalFormula = 1

	# use dynamical state when evaluating ttbb prob.
	vuseDynamicalScale    = 1

	# chi2-optimization
	pi.integralOption0      = 0
	pi.maxChi2              = 2.5

	# permutation pruning
	pi.integralOption1      = 0

	# integration speed-up
	pi.integralOption2           = 1
	pi.integralOption2_stage     = 1
	pi.integralOption2_niter     = 1
	pi.integralOption2_nevalfact = 1.0

	# switch off ME calculation
	pi.speedup              = 1

	# switch off OL calculation
	pi.switchoffOL          = 0
