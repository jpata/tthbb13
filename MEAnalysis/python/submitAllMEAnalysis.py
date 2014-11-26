#!/usr/bin/env python


import commands
import re
import os
import ROOT

import sys
sys.path.append('./')

import FWCore.ParameterSet.Config as cms

from TTH.MEAnalysis.mem_parameters_cff import *


###########################################
###########################################


#file which contains scheduler commands to submit jobs
tosubmit = open("submit.sh", "w")
tosubmit.write("#!/bin/bash\n")
os.system('chmod +x submit.sh')

DOMEMCATEGORIES = 1
PSI			 = 0

address1 = ''
address2 = ''
subcommand	 = ''

if PSI==1:
	address1		= 'gsidcap://t3se01.psi.ch:22128/'
	address2		= 'dcap://t3se01.psi.ch:22125/'
	subcommand			= 'subcommand -V -cwd -l h_vmem=2G -q all.q'
else:
	address2		= ''
	address1		= ''
	subcommand			= 'sbatch -p main'
	tempOutPath = "/scratch/" + os.environ["USER"] + "/"
	finalOutPath = "/home/" + os.environ["USER"] + "/tth/{0}/".format(processing_tag)

if not os.path.exists(finalOutPath):
	os.makedirs(finalOutPath)

###########################################
###########################################


def getSplitting(path, sample, numjobs, treeName="tthNtupleAnalyzer/events"):

	print "getSplitting for", path, sample, numjobs
	sampleName = None

	for sam in samples:
		if sam.nickName == sample:
			sampleName = (sam.name).value()

	fn = address1+path+sampleName+'.root'
	if os.path.isfile(fn):

		f = ROOT.TFile.Open(fn, 'read')
		if f != None :
			t = f.Get(treeName)
			if t != None and not t.IsZombie():
				entries = t.GetEntries()
				entries_per_job = (entries/numjobs + 1)
			else:
				raise Exception("Cannot open tree %s in file %s" % (treeName, fn))
			print "\033[94mProcessing..... %s jobs will run on (%.2fK ev/job) * (%.0f job) = %.0f events (%.1f%% of %s)\033[0m" % (numjobs, float(entries_per_job)/1000., numjobs, entries_per_job*numjobs, float(entries_per_job*numjobs)/float(entries)*100, sample)
			f.Close()

			if numjobs==1:
				return -1
			else:
				return int(entries_per_job)
		else:
			raise Exception('Cannot open file %s' % fn)
			#print 'Cannot open file %s' % fn
			#return -2
	else:
		raise Exception('Cannot find file %s' % fn)
		#print 'Cannot find file %s in %s' % (sample, path)
		#return -2


###########################################
###########################################


def submitMEAnalysis(script,
							sample,
							version,
							evLow,evHigh):

	#print "Overload meAnalysisNew_all.py..."
	os.system('cp $CMSSW_BASE/src/TTH/MEAnalysis/python/MEAnalysis_cfg.py ./')

	from MEAnalysis_cfg import process

	#print "Creating the shell file for the batch..."
	scriptName = 'job_'+script+'.sh'
	jobName	= 'job_'+script

	process.fwliteInput.samples  = samples

	numOfMatches = 0
	isMC = 1
	for sam in process.fwliteInput.samples:
		if sam.nickName != sample:
			sam.skip = cms.bool(True)
		else:
			numOfMatches += 1
			sam.skip = cms.bool(False)
			if (re.search("Run2012",sam.name.value())!=None):
				isMC = 0

	if numOfMatches==0:
		raise Exception("Sample %s does not match any of those available...return" % sample)
	elif numOfMatches>1:
		raise Exception("Sample %s matches multiple of those available, check the names...return" % sample)
	else:
		#print "Sample \033[94m%s\033[0m matched (isMC=%d)" % (sample,isMC)
		pass

	process.fwliteInput.outFileName		= cms.string(tempOutPath + 'MEAnalysis_'+extraoutname+script+'.root')
	finalOutFilename						= finalOutPath + 'MEAnalysis_'+extraoutname+script+'.root'
	process.fwliteInput.pathToFile		= cms.string(address2 + pathToFile+version + '/' )
	process.fwliteInput.ordering		= cms.string(ordering)


	if useRegression:
		process.fwliteInput.pathToTF		 = cms.string('./root/transferFunctionsTEST_reg.root')
		process.fwliteInput.pathToCP		 = cms.string('./root/ControlPlotsTEST_reg.root')
		process.fwliteInput.pathToCP_smear   = cms.string("./root/ControlPlotsTEST_reg_gen.root")
	else:
		process.fwliteInput.pathToTF		 = cms.string('./root/transferFunctionsTEST.root')
		process.fwliteInput.pathToCP		 = cms.string('./root/ControlPlotsTEST.root')
		process.fwliteInput.pathToCP_smear   = cms.string("./root/ControlPlotsTEST_std_gen.root")

	process.fwliteInput.norm			 = cms.untracked.int32(norm)
	process.fwliteInput.useME			= cms.untracked.int32(useME)
	process.fwliteInput.useJac		   = cms.untracked.int32(useJac)
	process.fwliteInput.useMET		   = cms.untracked.int32(useMET)
	process.fwliteInput.useTF			= cms.untracked.int32(useTF)
	process.fwliteInput.usePDF		   = cms.untracked.int32(usePDF)
	process.fwliteInput.useAnalyticalFormula = cms.untracked.int32(useAnalyticalFormula)
	process.fwliteInput.useDynamicalScale	= cms.untracked.int32(useDynamicalScale)

	process.fwliteInput.integralOption0  = cms.untracked.int32( integralOption0 )
	process.fwliteInput.integralOption1  = cms.untracked.int32( integralOption1 )
	process.fwliteInput.integralOption2  = cms.untracked.int32( integralOption2 )
	process.fwliteInput.speedup		  = cms.untracked.int32(speedup)
	process.fwliteInput.integralOption2_stage	 = cms.untracked.int32(integralOption2_stage)
	process.fwliteInput.integralOption2_niter	 = cms.untracked.int32(integralOption2_niter)
	process.fwliteInput.integralOption2_nevalfact = cms.untracked.double(integralOption2_nevalfact)
	process.fwliteInput.switchoffOL			   = cms.untracked.int32(switchoffOL)

	process.fwliteInput.doubleGaussianB	= cms.untracked.int32(doubleGaussianB)
	process.fwliteInput.useBtag			= cms.untracked.int32(useBtag)
	process.fwliteInput.useCMVA			= cms.untracked.int32(useCMVA)
	process.fwliteInput.selectByBTagShape  = cms.untracked.int32(selectByBTagShape)
	process.fwliteInput.useCSVcalibration  = cms.untracked.int32(useCSVcalibration)

	process.fwliteInput.enhanceMC		  = cms.untracked.int32(enhanceMC)
	process.fwliteInput.max_n_trials	   = cms.untracked.int32(max_n_trials)

	process.fwliteInput.recoverTopBTagBin  = cms.untracked.int32(recoverTopBTagBin)

	process.fwliteInput.testSLw1jType3	 = cms.untracked.int32(testSLw1jType3)
	process.fwliteInput.nMaxJetsSLw1jType3 = cms.untracked.int32(nMaxJetsSLw1jType3)

	process.fwliteInput.jetMultLoose	   = cms.untracked.int32(jetMultLoose)
	process.fwliteInput.jetPtLoose		 = cms.untracked.double(jetPtLoose)
	process.fwliteInput.jetPtThreshold	 = cms.untracked.double(jetPtThreshold)

	if DOMEMCATEGORIES:
		process.fwliteInput.doType0			= cms.untracked.int32(not selectByBTagShape)
		process.fwliteInput.doType1			= cms.untracked.int32(not selectByBTagShape)
		process.fwliteInput.doType2			= cms.untracked.int32(not selectByBTagShape)
		process.fwliteInput.doType3			= cms.untracked.int32(not selectByBTagShape)
		process.fwliteInput.doType6			= cms.untracked.int32(not selectByBTagShape)
		process.fwliteInput.doType7			= cms.untracked.int32(0)
		process.fwliteInput.doType0ByBTagShape = cms.untracked.int32(selectByBTagShape)
		process.fwliteInput.doType1ByBTagShape = cms.untracked.int32(selectByBTagShape)
		process.fwliteInput.doType2ByBTagShape = cms.untracked.int32(selectByBTagShape)
		process.fwliteInput.doType3ByBTagShape = cms.untracked.int32(selectByBTagShape)
		process.fwliteInput.doType6ByBTagShape = cms.untracked.int32(selectByBTagShape)
		process.fwliteInput.doTypeBTag6		= cms.untracked.int32(0)
		process.fwliteInput.doTypeBTag5		= cms.untracked.int32(0)
		process.fwliteInput.doTypeBTag4		= cms.untracked.int32(0)
	else:
		process.fwliteInput.doType0			= cms.untracked.int32(0)
		process.fwliteInput.doType1			= cms.untracked.int32(0)
		process.fwliteInput.doType2			= cms.untracked.int32(0)
		process.fwliteInput.doType3			= cms.untracked.int32(0)
		process.fwliteInput.doType6			= cms.untracked.int32(0)
		process.fwliteInput.doType7			= cms.untracked.int32(0)
		process.fwliteInput.doType0ByBTagShape = cms.untracked.int32(0)
		process.fwliteInput.doType1ByBTagShape = cms.untracked.int32(0)
		process.fwliteInput.doType2ByBTagShape = cms.untracked.int32(0)
		process.fwliteInput.doType3ByBTagShape = cms.untracked.int32(0)
		process.fwliteInput.doType6ByBTagShape = cms.untracked.int32(0)
		process.fwliteInput.doTypeBTag6		= cms.untracked.int32(1)
		process.fwliteInput.doTypeBTag5		= cms.untracked.int32(1)
		process.fwliteInput.doTypeBTag4		= cms.untracked.int32(1)

	process.fwliteInput.btag_prob_cut_6jets = cms.untracked.double(btag_prob_cut_6jets)
	process.fwliteInput.btag_prob_cut_5jets = cms.untracked.double(btag_prob_cut_5jets)
	process.fwliteInput.btag_prob_cut_4jets = cms.untracked.double(btag_prob_cut_4jets)

	process.fwliteInput.csv_WP_L			=  cms.untracked.double(csv_WP_L)
	process.fwliteInput.csv_WP_M			=  cms.untracked.double(csv_WP_M)
	process.fwliteInput.csv_WP_T			=  cms.untracked.double(csv_WP_T)

	process.fwliteInput.useRegression	   = cms.untracked.int32(useRegression)
	process.fwliteInput.triggerErrors	   = cms.untracked.int32(triggerErrors)

	process.fwliteInput.massesH			 = massesH
	process.fwliteInput.massesT			 = massesT
	process.fwliteInput.MH				  = cms.untracked.double(MH)
	process.fwliteInput.MT				  = cms.untracked.double(MT)

	process.fwliteInput.lepPtLoose   = cms.untracked.double(lepPtLoose)
	process.fwliteInput.lepPtTight   = cms.untracked.double(lepPtTight)
	process.fwliteInput.lepIsoLoose  = cms.untracked.double(lepIsoLoose)
	process.fwliteInput.lepIsoTight  = cms.untracked.double(lepIsoTight)
	process.fwliteInput.elEta		= cms.untracked.double(elEta)
	process.fwliteInput.muEtaTight   = cms.untracked.double(muEtaTight)
	process.fwliteInput.muEtaLoose   = cms.untracked.double(muEtaLoose)

	process.fwliteInput.MwL		  = cms.untracked.double(MwL)
	process.fwliteInput.MwH		  = cms.untracked.double(MwH)
	process.fwliteInput.MhL		  = cms.untracked.double(MhL)
	process.fwliteInput.MhH		  = cms.untracked.double(MhH)
	process.fwliteInput.MwLType3	 = cms.untracked.double(MwLType3)
	process.fwliteInput.MwHType3	 = cms.untracked.double(MwHType3)

	process.fwliteInput.fixNumEvJob		 = cms.untracked.int32(fixNumEvJob)
	process.fwliteInput.evLimits			= cms.vint32(evLow,evHigh)

	process.fwliteInput.lumi				= cms.untracked.double(lumi)

	process.fwliteInput.printout			= cms.untracked.int32(printout)
	process.fwliteInput.debug			   = cms.untracked.int32(debug)

	process.fwliteInput.doGenLevelAnalysis  = cms.untracked.int32(doGenLevelAnalysis)
	process.fwliteInput.smearJets		   = cms.untracked.int32(smearJets)

	process.fwliteInput.ntuplizeAll		 = cms.untracked.int32(ntuplizeAll)

	process.fwliteInput.systematics		 = systematics
	if isMC==0:
		process.fwliteInput.systematics	 = cms.vint32(0)

	out = open(jobName+'.py','w')
	out.write(process.dumpPython())
	out.close()

	f = open(scriptName,'w')
	f.write('#!/bin/bash\n\n')
	f.write('set -e\n')
	f.write('echo "SCRIPT '+scriptName+'"\n')
	f.write('cd ${CMSSW_BASE}/src/TTH/MEAnalysis/\n')
	f.write('export SCRAM_ARCH="slc6_amd64_gcc481"\n')
	f.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
	f.write('eval `scramv1 runtime -sh`\n')
	f.write('\n\n')

	#call script with absolute path
	d = os.getcwd()
	f.write('time MEAnalysis ' + d + "/" + jobName+'.py\n')

	#remove output from final location and copy
	f.write('rm -f %s\n' % (finalOutFilename))
	f.write('rsync %s %s\n' % (process.fwliteInput.outFileName.value(), finalOutFilename))
	f.write('rm -f %s\n' % process.fwliteInput.outFileName.value())
	f.write('echo "JOB DONE"\n')

	f.close()
	os.system('chmod +x '+scriptName)

	submitToQueue = subcommand+' -N job'+sample+' '+scriptName
	tosubmit.write(submitToQueue + "\n")
	#print submitToQueue
	#os.system(submitToQueue)

	#print "\n@@@@@ END JOB @@@@@@@@@@@@@@@"
	#os.system('rm testME_tmp.py')

###########################################
###########################################

def submitFullMEAnalysis( analysis ):
	print "Running full analysis for %s" %  (analysis)

	toBeRun = []
	total_jobs = 0

	if PSI:
		toBeRun = [
			['TTH125',		 50,'_V4/'],
			#['TTJetsSemiLept', 50,'_V4/'],
			#['TTJetsFullLept', 50,'_V4/'],
			#['TTJetsFullHad',   5,'_V4/'],
			#['DYJets10to50',	1,'_V4/'],
			#['DYJets50',		1,'_V4/'],
			#['WJets',		   1,'_V4/'],
			#['TtW',			 1,'_V4/'],
			#['Tt',			  1,'_V4/'],
			#['Ts',			  1,'_V4/'],
			#['TbartW',		  1,'_V4/'],
			#['Tbart',		   1,'_V4/'],
			#['Tbars',		   1,'_V4/'],
			#['WW',			  1,'_V4/'],
			#['WZ',			  1,'_V4/'],
			#['ZZ',			  1,'_V4/'],
			#['TTZ',			20,'_V4/'],
			#['TTW',			5,'_V4/'],
			#['Run2012_DoubleElectron_Run2012A-13Jul2012-v1_ProcFIXED',				1, '_V4/'],
			#['Run2012_DoubleElectron_Run2012A-recover-06Aug2012-v1_ProcV2',		   1, '_V4/'],
			#['Run2012_DoubleElectron_Run2012B-13Jul2012-v1_ProcFIXED',			   12, '_V4/'],
			#['Run2012_DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV1', 4, '_V4/'],
			#['Run2012_DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV2', 4, '_V4/'],
			#['Run2012_DoubleElectronRun2012C-EcalRecover_11Dec2012-v1_v2',			1, '_V4/'],
			#['Run2012_DoubleElectronRun2012CAug24RerecoEdmV42',					   4, '_V4/'],
			#['Run2012_DoubleElectronRun2012D',										6, '_V4/'],
			#['Run2012_SingleElectronRun2012AAug06EdmV42',							 1, '_V4/'],
			#['Run2012_SingleElectronRun2012AJul13EdmV42b',							1, '_V4/'],
			#['Run2012_SingleElectronRun2012BJul13EdmV42',							18, '_V4/'],
			#['Run2012_SingleElectronRun2012C-EcalRecover_11Dec2012-v1_v2',			1, '_V4/'],
			#['Run2012_SingleElectronRun2012CAug24RerecoEdmV42',					   4, '_V4/'],
			#['Run2012_SingleElectronRun2012CPromptv2EdmV42',						  8, '_V4/'],
			#['Run2012_SingleElectronRun2012CPromptV2TopUpEdmV42',					 8, '_V4/'],
			#['Run2012_SingleElectronRun2012D-PromptReco-v1_v3',					  40, '_V4/'],
			#['Run2012_SingleMuRun2012AAug06',										 1, '_V4/'],
			#['Run2012_SingleMuRun2012AJul13',										 1, '_V4/'],
			#['Run2012_SingleMuRun2012BJul13',										18, '_V4/'],
			#['Run2012_SingleMuRun2012C-EcalRecover_11Dec2012-v1_v2',				  1, '_V4/'],
			#['Run2012_SingleMuRun2012CAug24Rereco',								   4, '_V4/'],
			#['Run2012_SingleMuRun2012CPromptv2',									  8, '_V4/'],
			#['Run2012_SingleMuRun2012CPromptV2TopUp',								 8, '_V4/'],
			#['Run2012_SingleMuRun2012D-PromptReco-v1',							   40, '_V4/'],
			]
	else:
		toBeRun = [
			["TTJets", 1000, ''],
			["TTHBB125", 100, '']
			#['TTH125',		  50, ''], #499
			#['TTJetsSemiLept',  50,''], #499
			#['TTJetsFullLept',  50,''], #499
			#['TTJetsFullHad',   5,''],
			#['DYJets10to50',	1,''],
			#['DYJets50',		1,''], # 1
			#['WJets',		   1,''],
			#['TtW',			 2,''],
			#['Tt',			  1,''],
			#['Ts',			  1,''],
			#['TbartW',		  2,''],
			#['Tbart',		   1,''],
			#['Tbars',		   1,''],
			#['WW',			  1,''], #  1
			#['WZ',			  1,''], #  1
			#['ZZ',			  5,''], #  1
			#['TTZ',			40,''], # 40
			#['TTW',			10,''], # 10
			#['Run2012_DoubleElectron_Run2012A-13Jul2012-v1_ProcFIXED',				1, ''],
			#['Run2012_DoubleElectron_Run2012A-recover-06Aug2012-v1_ProcV2',		   1, ''],
			#['Run2012_DoubleElectron_Run2012B-13Jul2012-v1_ProcFIXED',			   12, ''],
			#['Run2012_DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV1', 4, ''],
			#['Run2012_DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV2', 4, ''],
			#['Run2012_DoubleElectronRun2012C-EcalRecover_11Dec2012-v1_v2',			1, ''],
			#['Run2012_DoubleElectronRun2012CAug24RerecoEdmV42',					   4, ''],
			#['Run2012_DoubleElectronRun2012D',										6, ''],
			#['Run2012_SingleElectronRun2012AAug06EdmV42',							 1, ''],
			#['Run2012_SingleElectronRun2012AJul13EdmV42b',							1, ''],
			#['Run2012_SingleElectronRun2012BJul13EdmV42',							18, ''],
			#['Run2012_SingleElectronRun2012C-EcalRecover_11Dec2012-v1_v2',			1, ''],
			#['Run2012_SingleElectronRun2012CAug24RerecoEdmV42',					   4, ''],
			#['Run2012_SingleElectronRun2012CPromptv2EdmV42',						  8, ''],
			#['Run2012_SingleElectronRun2012CPromptV2TopUpEdmV42',					 8, ''],
			#['Run2012_SingleElectronRun2012D-PromptReco-v1_v3',					  40, ''],  #40
			#['Run2012_SingleMuRun2012AAug06',										 1, ''],
			#['Run2012_SingleMuRun2012AJul13',										 1, ''],
			#['Run2012_SingleMuRun2012BJul13',										18, ''],
			#['Run2012_SingleMuRun2012C-EcalRecover_11Dec2012-v1_v2',				  1, ''],
			#['Run2012_SingleMuRun2012CAug24Rereco',								   4, ''],
			#['Run2012_SingleMuRun2012CPromptv2',									  8, ''],
			#['Run2012_SingleMuRun2012CPromptV2TopUp',								 8, ''],
			#['Run2012_SingleMuRun2012D-PromptReco-v1',							   40, ''], #40

#			['QCD_Pt-30To50_bEnriched',												1, ''],
#			['QCD_Pt-50To150_bEnriched',											   1, ''],
#			['QCD_Pt-150_bEnriched',												   1, ''],

#			['QCD_Pt_80_170_BCtoE',													1, ''],
#			['QCD_Pt_170_250_BCtoE',												   1, ''],
#			['QCD_Pt_250_350_BCtoE',												   1, ''],
#			['QCD_Pt_350_BCtoE',													   1, ''],
			]

	for run in toBeRun:
		print "running", run
		counter	= 0
		sample= run[0]
		num_of_jobs = run[1]
		version	= run[2]
		evs_per_job = getSplitting(pathToFile+version+ordering , sample, num_of_jobs )
		if evs_per_job==-2:
			print "Error in getSplitting.. please check again."
			continue
		for i in range(num_of_jobs):
			counter = counter + 1
			submitMEAnalysis(analysis+'_'+sample+'_p'+str(counter), sample,  version,  i*evs_per_job, (i+1)*evs_per_job )
			total_jobs += 1

	print "Total jobs submitted.....%d" % total_jobs

###########################################
###########################################

analyses = ['all']
#analyses = ['all_ntuplizeAll_v3']

for analysis in analyses:
	if doGenLevelAnalysis:
		analysis = analysis+'_gen'
	else:
		analysis = analysis+'_rec'
	if useRegression:
		analysis = analysis+'_reg'
	else:
		analysis = analysis+'_std'
	submitFullMEAnalysis( analysis)

###########################################
###########################################
