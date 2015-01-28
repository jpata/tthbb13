#!/usr/bin/env python
import commands
import re
import os
import ROOT
import imp

import sys
sys.path.append('./')

import FWCore.ParameterSet.Config as cms

import argparse
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
default_pars = os.environ["CMSSW_BASE"] + "/python/TTH/MEAnalysis/mem_parameters_cff.py"
parser.add_argument('--pars',
	default=default_pars, type=str,
	help="path to file with MEM parameters"
)
parser.add_argument('--site',
	choices=['T2_EE_Estonia', 'T3_CH_PSI'], type=str,
	default="T3_CH_PSI",
	help="CMS Tier 2/3 site where commands are run"
)

parser.add_argument('--njobs',
	type=int,
	default=100,
	help="Number of jobs for the signal process"
)
parser.add_argument('--verbose', '-v', action='count')
args = parser.parse_args()

#import MEM parameters from specified file
#from TTH.MEAnalysis.mem_parameters_cff import *
if args.verbose > 0:
	print "loading MEM parameters from", args.pars

imp.load_source("mem_parameters", args.pars)
from mem_parameters import *

###########################################
###########################################


#file which contains scheduler commands to submit jobs
tosubmit = open("submit.sh", "w")
tosubmit.write("#!/bin/bash\n")
#os.system('chmod +x submit.sh')

DOMEMCATEGORIES = 1

address1 = ''
address2 = ''
subcommand	 = ''

if args.site=="T3_CH_PSI":
	#address1		= 'gsidcap://t3se01.psi.ch:22128/'
	#address2		= 'dcap://t3se01.psi.ch:22125/'
	address1		= ''
	address2		= ''
	subcommand			= 'qsub -V -cwd -l h_vmem=2G -q all.q'
	#tempOutPath = "/scratch/" + os.environ["USER"] + "/"
	tempOutPath = "$TMPDIR/"
	finalOutPath = "/shome/" + os.environ["USER"] + "/tth/{0}/".format(processing_tag)
elif args.site=="T2_EE_Estonia":
	address2		= ''
	address1		= ''
	subcommand			= 'sbatch -p main'
	tempOutPath = "/scratch/" + os.environ["USER"] + "/"
	finalOutPath = "/home/" + os.environ["USER"] + "/tth/{0}/".format(processing_tag)
else:
	raise ValueError("Unknown site: {0}".format(args.site))

if not os.path.exists(finalOutPath):
	if args.verbose > 0:
		print "creating output directory", finalOutPath
	os.makedirs(finalOutPath)

###########################################
###########################################


def getSplitting(path, sample, numjobs, treeName="tthNtupleAnalyzer/events"):

	if args.verbose > 0:
		print "getSplitting for", path, sample, numjobs
	sampleName = None

	for sam in samples:
		if sam.nickName == sample:
			sampleName = (sam.name).value()

	fn = address1+path+sampleName+'.root'

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

###########################################
###########################################


def submitMEAnalysis(script,
							sample,
							version,
							evLow,evHigh):

	os.system('cp $CMSSW_BASE/src/TTH/MEAnalysis/python/MEAnalysis_cfg.py ./')

	imp.load_source("localME", "./MEAnalysis_cfg.py")
	from localME import process

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
	f.write('source /cvmfs/cms.cern.ch/cmsset_default.sh\n')
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

	if args.site=="T3_CH_PSI":
		toBeRun = [
			["TTJets", 10 * args.njobs, ''],
			["TTHBB125", args.njobs, '']
			]
	elif args.site == "T2_EE_Estonia":
		toBeRun = [
			["TTJets", 10 * args.njobs, ''],
			["TTHBB125", args.njobs, '']
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
