import sys, re

workflows = [
    "leptonic",
    "hadronic",
    "pilot",
    "testing"
]

import argparse
parser = argparse.ArgumentParser(description='Submits crab jobs')
parser.add_argument('--workflow', action="store", required=True, help="Type of workflow to run", type=str, choices=workflows)
parser.add_argument('--tag', action="store", required=True, help="Input file with datasets")
args = parser.parse_args()

me_cfgs = {
    "default": "MEAnalysis_cfg_heppy.py",
    "leptonic": "cfg_leptonic.py",
    "hadronic": "cfg_FH.py",
}

datasets = {
    'ttHTobb': (
        '/ttHTobb_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
        -1, 10, me_cfgs["default"],
    ),
    'ttHToNonbb': (
        '/ttHToNonbb_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
        -1, 100, me_cfgs["default"],
    ),
    'TTbar_inc': (
        '/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1/MINIAODSIM',
        -1, 100, me_cfgs["default"],
    ),
    'TTbar_sl': (
        '/TTToSemiLeptonic_13TeV-powheg/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM',
        -1, 100, me_cfgs["leptonic"],
    ),
    'TTbar_dl': (
        '/TTTo2L2Nu_13TeV-powheg/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM',
        -1, 200, me_cfgs["leptonic"],
    ),
    'QCD300': (
        '/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
        -1, 500, me_cfgs["hadronic"],
    ),
    'QCD500': (
        '/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
        -1, 500, me_cfgs["hadronic"],
    ),
    'QCD700': (
        '/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
        -1, 300, me_cfgs["hadronic"],
    ),
    'QCD1000': (
        '/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
        -1, 200, me_cfgs["hadronic"],
    ),
    'QCD1500': (
        '/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
        -1, 100, me_cfgs["hadronic"],
    ),
    'QCD2000': (
        '/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
        -1, 100, me_cfgs["hadronic"],
    ),
}

workflow_datasets = {}
workflow_datasets["leptonic"] = {}
for k in ["ttHTobb", "ttHToNonbb", "TTbar_inc", "TTbar_sl", "TTbar_dl"]:
    workflow_datasets["leptonic"][k] = datasets[k]

workflow_datasets["hadronic"] = {}
for k in datasets.keys():
    if "QCD" in k or "ttH" in k:
        workflow_datasets["hadronic"][k] = datasets[k]
    elif k == "TTbar_inc":
        #don't run all of tt+jets
        D = list(datasets[k])
        D[1] = 10000
        workflow_datasets["hadronic"][k] = tuple(D)

workflow_datasets["pilot"] = {}
D = list(datasets["ttHTobb"])
D[2] = 50
workflow_datasets["pilot"]["ttHTobb"] = D

workflow_datasets["testing"] = {}
for k in ["ttHTobb"]:
#for k in ["ttHTobb", "TTbar_inc", "QCD1500"]:
    D = list(datasets[k])
    D[1] = 10
    D[2] = 1
    workflow_datasets["testing"][k] = D

sel_datasets = workflow_datasets[args.workflow]

if __name__ == '__main__':
    from CRABAPI.RawCommand import crabCommand
    from CRABClient.UserUtilities import getUsernameFromSiteDB

    def submit(config):
        res = crabCommand('submit', config = config)

    from CRABClient.UserUtilities import config
    config = config()
    submitname = 'VHBBHeppyV21_tthbbV9_' + args.tag
    config.General.workArea = 'crab_projects/' + submitname
    config.General.transferLogs = True

    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'heppy_crab_fake_pset.py'
    config.JobType.scriptExe = 'heppy_crab_script.sh'
    config.JobType.maxJobRuntimeMin = 1 * 60

    import os
    os.system("tar czf python.tar.gz --dereference --directory $CMSSW_BASE python")
    os.system("tar czf data.tar.gz --dereference --directory $CMSSW_BASE/src/TTH/MEAnalysis root")
    os.system("make -sf $CMSSW_BASE/src/TTH/Makefile get_hashes")
    os.system("echo '\n\n{0}\n-------------' >> $CMSSW_BASE/src/TTH/logfile.md".format(submitname))
    os.system("cat $CMSSW_BASE/src/TTH/hash >> $CMSSW_BASE/src/TTH/logfile.md")
    
    vhbb_dir = os.environ.get("CMSSW_BASE") + "/src/VHbbAnalysis/Heppy/test"
    config.JobType.inputFiles = [
        'hash',
        'FrameworkJobReport.xml',
        'heppy_config.py',
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

    config.Site.storageSite = "T2_CH_CSCS"

    #loop over samples
    for sample in sel_datasets.keys():
        dataset, nlumis, perjob, cfgname = sel_datasets[sample]
        print 'submitting ' + sample
        config.General.requestName = sample + "_" + submitname
        config.Data.inputDataset = dataset
        config.Data.unitsPerJob = perjob
        config.Data.totalUnits = nlumis
        config.Data.outputDatasetTag = submitname
        config.Data.outLFNDirBase = '/store/user/{0}/tth/'.format(getUsernameFromSiteDB()) + submitname
        config.JobType.scriptArgs = ['ME_CONF={0}'.format(cfgname)]
        submit(config)
