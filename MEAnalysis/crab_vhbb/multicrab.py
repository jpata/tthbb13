import sys, re, shutil
from copy import deepcopy

#Each time you call multicrab.py, you choose to submit jobs from one of these workflows
workflows = [
    "data", #real data
    "leptonic", #ttH with SL/DL decays
    "hadronic", #ttH with FH decays
    "pilot", #ttH sample only, with no MEM
    "testing", #single-lumi jobs, a few samples
    "localtesting", #run combined jobs locally
    "testing_withme" #single-lumi jobs, a few samples
]

import argparse
parser = argparse.ArgumentParser(description='Submits crab jobs')
parser.add_argument('--workflow', action="store", required=True, help="Type of workflow to run", type=str, choices=workflows)
parser.add_argument('--tag', action="store", required=True, help="the version tag for this run, e.g. VHBBHeppyV22_tthbbV10_test1")
args = parser.parse_args()

#list of configurations that we are using, should be in TTH/MEAnalysis/python/
me_cfgs = {
    "default": "MEAnalysis_cfg_heppy.py",
    "nome": "cfg_noME.py",
    "leptonic": "cfg_leptonic.py",
    "hadronic": "cfg_FH.py",
}

sets_data = [
      "/DoubleEG/Run2016B-PromptReco-v1/MINIAOD"
    , "/DoubleEG/Run2016B-PromptReco-v2/MINIAOD"
    , "/DoubleMuon/Run2016B-PromptReco-v1/MINIAOD"
    , "/DoubleMuon/Run2016B-PromptReco-v2/MINIAOD"
    , "/MuonEG/Run2016B-PromptReco-v1/MINIAOD"
    , "/MuonEG/Run2016B-PromptReco-v2/MINIAOD"
    , "/SingleElectron/Run2016B-PromptReco-v1/MINIAOD"
    , "/SingleElectron/Run2016B-PromptReco-v2/MINIAOD"
    , "/SingleMuon/Run2016B-PromptReco-v1/MINIAOD"
    , "/SingleMuon/Run2016B-PromptReco-v2/MINIAOD"
]

#all available datasets.
datasets = {}
for sd in sets_data:
    name = "-".join(sd.split("/")[1:3])
    datasets[name] = {
        "ds": sd,
        "maxlumis": -1,
        "perjob": 100,
        "runtime": 40,
        "mem_cfg": me_cfgs["nome"],
        "script": 'heppy_crab_script_data.sh'
    }
datasets.update({
    'ttHTobb': {
        "ds": '/ttHTobb_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 10,
        "runtime": 40,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    'ttHToNonbb': {
        "ds": '/ttHToNonbb_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 100,
        "runtime": 40,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    'TTbar_inc': {
        "ds": '/TT_TuneEE5C_13TeV-powheg-herwigpp/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 100,
        "runtime": 40,
        "mem_cfg": me_cfgs["default"],
        "script": 'heppy_crab_script.sh'
    },
    'TTbar_sl': {
        "ds": '/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 100,
        "runtime": 40,
        "mem_cfg": me_cfgs["leptonic"],
        "script": 'heppy_crab_script.sh'
    },
    'TTbar_dl': {
        "ds": '/TTTo2L2Nu_13TeV-powheg/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 200,
        "runtime": 40,
        "mem_cfg": me_cfgs["leptonic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD300': {
        "ds": '/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 500,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD500': {
        "ds": '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 500,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD700': {
        "ds": '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 300,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD1000': {
        "ds": '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 200,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD1500': {
        "ds": '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 100,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
    'QCD2000': {
        "ds": '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
        "maxlumis": -1,
        "perjob": 100,
        "runtime": 40,
        "mem_cfg": me_cfgs["hadronic"],
        "script": 'heppy_crab_script.sh'
    },
})

#now we construct the workflows from all the base datasets
workflow_datasets = {}
workflow_datasets["leptonic"] = {}
for k in ["ttHTobb", "ttHToNonbb", "TTbar_inc", "TTbar_sl", "TTbar_dl"]:
    workflow_datasets["leptonic"][k] = datasets[k]

workflow_datasets["data"] = {}
for k in datasets.keys():
    if "data" in datasets[k]["script"]:
        workflow_datasets["data"][k] = datasets[k]

workflow_datasets["hadronic"] = {}
for k in datasets.keys():
    if "QCD" in k or "ttH" in k:
        workflow_datasets["hadronic"][k] = datasets[k]
    elif k == "TTbar_inc":
        #don't run all of tt+jets
        D = deepcopy(datasets[k])
        D["maxlumis"] = 10000
        workflow_datasets["hadronic"][k] = D

#Pilot job for updating transfer functions, retraining BLR
workflow_datasets["pilot"] = {}
pilot_name = "TTbar_inc" 
D = deepcopy(datasets[pilot_name])
D["perjob"] = 300
D["mem_cfg"] = me_cfgs["nome"]
workflow_datasets["pilot"][pilot_name] = D

#1-lumi per job, 10 job testing of a few samples
workflow_datasets["testing"] = {}
#for k in ["ttHTobb", "TTbar_inc", "QCD1500"]:
for k in ["TTbar_inc"]:#, "SingleMuon-Run2016B-PromptReco-v2"]:
    D = deepcopy(datasets[k])
    D["maxlumis"] = 10
    D["perjob"] = 1
    if "data" in D["script"]:
        D["maxlumis"] = 250
        D["perjob"] = 25
    D["runtime"] = 1
    D["mem_cfg"] = "cfg_noME.py"
    workflow_datasets["testing"][k] = D

workflow_datasets["localtesting"] = {}
for k in ["TTbar_inc"]:#, "SingleMuon-Run2016B-PromptReco-v2"]:
    D = deepcopy(datasets[k])
    D["maxlumis"] = 10
    D["perjob"] = 1
    D["runtime"] = 1
    D["mem_cfg"] = "cfg_noME.py"
    workflow_datasets["localtesting"][k] = D

workflow_datasets["testing_withme"] = {}
for k in ["ttHTobb", "TTbar_inc", "QCD1500"]:
    D = deepcopy(datasets[k])
    D["maxlumis"] = 10
    D["perjob"] = 1
    D["runtime"] = 5
    D["mem_cfg"] = me_cfgs["default"]
    workflow_datasets["testing_withme"][k] = D

#Now select a set of datasets
sel_datasets = workflow_datasets[args.workflow]

if __name__ == '__main__':
    from CRABAPI.RawCommand import crabCommand
    from CRABClient.UserUtilities import getUsernameFromSiteDB

    def submit(config):
        res = crabCommand('submit', config = config)
    
    def localsubmit(config):
        TMPDIR = "/scratch/{0}/crab_{1}".format(os.environ["USER"], "x")
        CMSSW_VERSION = "CMSSW_8_0_5"
        workdir = os.path.join(TMPDIR, CMSSW_VERSION, "work")
        try: 
            shutil.rmtree(TMPDIR)
        except Exception as e:
            print e
        os.makedirs(TMPDIR)
        os.system("cd {0}".format(TMPDIR))
        pwd = os.getcwd() 
        os.chdir(TMPDIR)
        os.system("scramv1 project CMSSW {0}".format(CMSSW_VERSION))
        os.makedirs(workdir)
        os.chdir(pwd)
        for inf in config.JobType.inputFiles + [config.JobType.scriptExe, 'PSet.py', 'file.json']:
            print inf
            shutil.copy(inf, os.path.join(workdir, os.path.basename(inf)))
        os.system("cp -r $CMSSW_BASE/lib {0}/".format(workdir)) 
        os.system("cp -r $CMSSW_BASE/lib/proclib {0}/lib/slc*/".format(workdir)) 
        os.system('find $CMSSW_BASE/src/ -path "*/data/*" -type f | sed -s "s|$CMSSW_BASE/||" > files')
        os.system('cp files $CMSSW_BASE/; cd $CMSSW_BASE; for f in `cat files`; do cp --parents $f {0}/; done'.format(workdir))
        #os.system("cp -r $CMSSW_BASE/include {0}/".format(workdir)) 
        #os.system("cp -r $CMSSW_BASE/src {0}/".format(workdir)) 

    from CRABClient.UserUtilities import config
    config = config()
    submitname = args.tag
    config.General.workArea = 'crab_projects/' + submitname
    config.General.transferLogs = True

    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'heppy_crab_fake_pset.py'

    import os
    os.system("tar czf python.tar.gz --dereference --directory $CMSSW_BASE python")
    os.system("tar czf data.tar.gz --dereference --directory $CMSSW_BASE/src/TTH/MEAnalysis root")
    if not "testing" in args.workflow: 
        os.system("make -sf $CMSSW_BASE/src/TTH/Makefile get_hashes")
        os.system("echo '\n\n{0}\n-------------' >> $CMSSW_BASE/src/TTH/logfile.md".format(submitname))
        os.system("cat $CMSSW_BASE/src/TTH/hash >> $CMSSW_BASE/src/TTH/logfile.md")
    
    vhbb_dir = os.environ.get("CMSSW_BASE") + "/src/VHbbAnalysis/Heppy/test"
    config.JobType.inputFiles = [
        'hash',
        'analyze_log.py',
        'FrameworkJobReport.xml',
        'heppy_config.py',
        'heppy_config_data.py',
        'heppy_crab_script.py',
        'python.tar.gz',
        'data.tar.gz',
        "MEAnalysis_heppy.py",
        'MVAJetTags_620SLHCX_Phase1And2Upgrade.db',
        'combined_cmssw.py',
        vhbb_dir + '/vhbb.py',
        vhbb_dir + '/vhbb_combined.py',
        'TMVAClassification_BDT.weights.xml',
        'puData.root',
        vhbb_dir + '/puDataMinus.root',
        vhbb_dir + '/puDataPlus.root',
        'puMC.root',
        'json.txt',
        vhbb_dir + "/Zll-spring15.weights.xml",
        vhbb_dir + "/Wln-spring15.weights.xml",
        vhbb_dir + "/Znn-spring15.weights.xml",
        vhbb_dir + "/VBF-spring15.weights.xml",
        vhbb_dir + "/ttbar-fall15_TargetGenOverPt_GenPtCut0.weights.xml",
        vhbb_dir + '/TMVA_blikelihood_vbf_cmssw76_h21trained.weights.xml'
    ]

    config.Data.inputDBS = 'global'
    config.Data.splitting = 'LumiBased'
    config.Data.publication = True
    config.Data.ignoreLocality = False

    #config.Site.whitelist = ["T2_CH_CSCS", "T1_US_FNAL", "T2_DE_DESY", "T1_DE_KIT"]
    config.Site.storageSite = "T2_CH_CSCS"

    #loop over samples
    for sample in sel_datasets.keys():
        print 'submitting ' + sample, sel_datasets[sample]
        dataset = sel_datasets[sample]["ds"]
        nlumis = sel_datasets[sample]["maxlumis"]
        perjob = sel_datasets[sample]["perjob"]
        runtime = sel_datasets[sample]["runtime"]
        mem_cfg = sel_datasets[sample]["mem_cfg"]
        config.JobType.scriptExe = sel_datasets[sample]["script"]

        config.JobType.maxJobRuntimeMin = runtime * 60
        config.General.requestName = sample + "_" + submitname
        config.Data.inputDataset = dataset
        config.Data.unitsPerJob = perjob
        config.Data.totalUnits = nlumis
        config.Data.outputDatasetTag = submitname
        config.Data.outLFNDirBase = '/store/user/{0}/tth/'.format(getUsernameFromSiteDB()) + submitname
        config.JobType.scriptArgs = ['ME_CONF={0}'.format(mem_cfg)]
        if args.workflow == "localtesting":
            localsubmit(config)
        else:
            submit(config)
