
class SparseHistogram:
    def __init__(self, **kwargs):
        self.infile = kwargs.get("infile")
        self.ngen = kwargs.get("ngen")
        self.lumi = kwargs.get("lumi")
        self.blr_cuts = kwargs.get("blr_cuts")
        self.systematics = kwargs.get("systematics")

sparse_data = {
    "Aug8": SparseHistogram(
        infile = "root://t3se01.psi.ch//store/user/jpata/tth/histograms/August2016A/Sparse_Aug8.root",
        ngen = {
            'TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 9468936.0,
            'TT_TuneCUETP8M1_13TeV-powheg-pythia8': 92886960.0,
            'ttHToNonbb_M125_13TeV_powheg_pythia8': 3820981.0,
            'ttHTobb_M125_13TeV_powheg_pythia8': 3912212.0,
            'TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 11947951.0,
            'TTTo2L2Nu_13TeV-powheg': 104327168.0
        },
        # brilcalc on golden json, overestimated by a few % for SingleElectron
        # http://dashb-cms-job.cern.ch/dashboard/templates/task-analysis/#user=Joosep+Pata&refresh=60&table=Mains&p=1&records=-1&sorting%5B%5D=2&sorting%5B%5D=desc&activemenu=2&pattern=*tth_Aug3_V24_v2*&task=&from=&till=&timerange=lastMonth
        lumi = {
            "SingleMuon": 12891.528,
            "SingleElectron": 12891.528,
            "MuonEG": 12891.528,
            "DoubleEG": 12891.528,
            "DoubleMuon": 12891.528,
        },
        blr_cuts = {
            "sl_j4_t2": 20,
            "sl_j4_t3": 1.1,
            "sl_j4_tge4": -20,
            
            "sl_j5_t2": 20,
            "sl_j5_t3": 2.3,
            "sl_j5_tge4": -20,
            
            "sl_jge6_t2": -0.4,
            "sl_jge6_t3": 2.9,
            "sl_jge6_tge4": -20,

            "dl_j3_t2": 20,
            "dl_j3_t3": -20,
            "dl_jge4_t2": 20,
            "dl_jge4_t3": 2.3,
            "dl_jge4_tge4": -20,
        },
        systematics = [
            "CMS_scale_j",
            "CMS_res_j",
            "pu",
            #"CMS_ttH_CSVcferr1",
            #"CMS_ttH_CSVcferr2",
            #"CMS_ttH_CSVhf",
            #"CMS_ttH_CSVhfstats1",
            #"CMS_ttH_CSVhfstats2",
            #"CMS_ttH_CSVjes",
            #"CMS_ttH_CSVlf",
            #"CMS_ttH_CSVlfstats1",
            #"CMS_ttH_CSVlfstats2"
        ]
    ),
    "Aug10": SparseHistogram(
        infile = "file:///mnt/t3nfs01/data01/shome/jpata/tth/datacards/Sparse_Aug10.root",
        ngen = {
            'TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 9468936.0,
            'TT_TuneCUETP8M1_13TeV-powheg-pythia8': 92886960.0,
            'ttHToNonbb_M125_13TeV_powheg_pythia8': 3820981.0,
            'ttHTobb_M125_13TeV_powheg_pythia8': 3912212.0,
            'TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 11947951.0,
            'TTTo2L2Nu_13TeV-powheg': 104327168.0
        },
        # brilcalc on golden json, overestimated by a few % for SingleElectron
        # http://dashb-cms-job.cern.ch/dashboard/templates/task-analysis/#user=Joosep+Pata&refresh=60&table=Mains&p=1&records=-1&sorting%5B%5D=2&sorting%5B%5D=desc&activemenu=2&pattern=*tth_Aug3_V24_v2*&task=&from=&till=&timerange=lastMonth
        lumi = {
            "SingleMuon": 12891.528,
            "SingleElectron": 12891.528,
            "MuonEG": 12891.528,
            "DoubleEG": 12891.528,
            "DoubleMuon": 12891.528,
        },
        blr_cuts = {
            "sl_j4_t2": 20,
            "sl_j4_t3": 1.1,
            "sl_j4_tge4": -20,
            
            "sl_j5_t2": 20,
            "sl_j5_t3": 2.3,
            "sl_j5_tge4": -20,
            
            "sl_jge6_t2": -0.4,
            "sl_jge6_t3": 2.9,
            "sl_jge6_tge4": -20,

            "dl_j3_t2": 20,
            "dl_j3_t3": -20,
            "dl_jge4_t2": 20,
            "dl_jge4_t3": 2.3,
            "dl_jge4_tge4": -20,
        },
        systematics = [
            "CMS_scale_j",
            "CMS_res_j",
            "pu",
            "CMS_ttH_CSVcferr1",
            "CMS_ttH_CSVcferr2",
            "CMS_ttH_CSVhf",
            "CMS_ttH_CSVhfstats1",
            "CMS_ttH_CSVhfstats2",
            "CMS_ttH_CSVjes",
            "CMS_ttH_CSVlf",
            "CMS_ttH_CSVlfstats1",
            "CMS_ttH_CSVlfstats2"
        ]
    ),
    "Aug11": SparseHistogram(
        infile = "file:///mnt/t3nfs01/data01/shome/jpata/tth/datacards/Sparse_Aug11.root",
        ngen = {
            'TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 9468936.0,
            'TT_TuneCUETP8M1_13TeV-powheg-pythia8': 92886960.0,
            'ttHToNonbb_M125_13TeV_powheg_pythia8': 3820981.0,
            'ttHTobb_M125_13TeV_powheg_pythia8': 3912212.0,                     
            'TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 11947951.0,
            'TTTo2L2Nu_13TeV-powheg': 104327168.0
        },
        # brilcalc on golden json, overestimated by a few % for SingleElectron
        # http://dashb-cms-job.cern.ch/dashboard/templates/task-analysis/#user=Joosep+Pata&refresh=60&table=Mains&p=1&records=-1&sorting%5B%5D=2&sorting%5B%5D=desc&activemenu=2&pattern=*tth_Aug3_V24_v2*&task=&from=&till=&timerange=lastMonth
        lumi = {
            "SingleMuon": 12891.528,
            "SingleElectron": 12891.528,
            "MuonEG": 12891.528,
            "DoubleEG": 12891.528,
            "DoubleMuon": 12891.528,
        },
        blr_cuts = {
            "sl_j4_t2": 20,
            "sl_j4_t3": 1.1,
            "sl_j4_tge4": -20,
            
            "sl_j5_t2": 20,
            "sl_j5_t3": 2.3,
            "sl_j5_tge4": -20,
            
            "sl_jge6_t2": -0.4,
            "sl_jge6_t3": 2.9,
            "sl_jge6_tge4": -20,

            "dl_j3_t2": 20,
            "dl_j3_t3": -20,
            "dl_jge4_t2": 20,
            "dl_jge4_t3": 2.3,
            "dl_jge4_tge4": -20,
        },
        systematics = [
            "CMS_scale_j",
            "CMS_res_j",
            "pu",
            "CMS_ttH_CSVcferr1",
            "CMS_ttH_CSVcferr2",
            "CMS_ttH_CSVhf",
            "CMS_ttH_CSVhfstats1",
            "CMS_ttH_CSVhfstats2",
            "CMS_ttH_CSVjes",
            "CMS_ttH_CSVlf",
            "CMS_ttH_CSVlfstats1",
            "CMS_ttH_CSVlfstats2"
        ]
    ),
    "Aug12": SparseHistogram(
        infile = "file:///mnt/t3nfs01/data01/shome/gregor/tth/gc/sparse/GCf39f28ab2b5e/sparse.root",

        ngen = {  
            'TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 9468936.0,
            'TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 11929057.0,
            'TT_TuneCUETP8M1_13TeV-powheg-pythia8': 92837064.0,
            'ttHToNonbb_M125_13TeV_powheg_pythia8': 3860872.0,
            'ttHTobb_M125_13TeV_powheg_pythia8': 3912212.0,
        },
        # brilcalc on golden json, overestimated by a few % for SingleElectron
        # http://dashb-cms-job.cern.ch/dashboard/templates/task-analysis/#user=Joosep+Pata&refresh=60&table=Mains&p=1&records=-1&sorting%5B%5D=2&sorting%5B%5D=desc&activemenu=2&pattern=*tth_Aug3_V24_v2*&task=&from=&till=&timerange=lastMonth
        # Calculate via calcLumis.py
        lumi = {
            "SingleMuon": 11629.565,
            "SingleElectron": 9287.066,
            "MuonEG": 13574.864,
            "DoubleEG": 10548.956,
            "DoubleMuon": 13512.161,
            "BTagCSV": 9999.9999,
        },
        blr_cuts = {
            "sl_j4_t2": 20,
            "sl_j4_t3": 1.1,
            "sl_j4_tge4": -20,
            
            "sl_j5_t2": 20,
            "sl_j5_t3": 2.3,
            "sl_j5_tge4": -20,
            
            "sl_jge6_t2": -0.4,
            "sl_jge6_t3": 2.9,
            "sl_jge6_tge4": -20,

            "dl_j3_t2": 20,
            "dl_j3_t3": -20,
            "dl_jge4_t2": 20,
            "dl_jge4_t3": 2.3,
            "dl_jge4_tge4": -20,
        },
        systematics = [
            #"CMS_scale_j",
            #"CMS_res_j",
            #"pu",
            #"CMS_ttH_CSVcferr1",
            #"CMS_ttH_CSVcferr2",
            #"CMS_ttH_CSVhf",
            #"CMS_ttH_CSVhfstats1",
            #"CMS_ttH_CSVhfstats2",
            #"CMS_ttH_CSVjes",
            #"CMS_ttH_CSVlf",
            #"CMS_ttH_CSVlfstats1",
            #"CMS_ttH_CSVlfstats2"
        ]
    ),
    "Aug15_FH": SparseHistogram(
        infile = "file:///mnt/t3nfs01/data01/shome/sdonato/tth/forPR/CMSSW/src/TTH/MEAnalysis/gc/ControlPlotsSparse.root",
        ngen = {
            'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 194.0,
            'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 199.0,
            'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 149.0,
            'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 169.0,
            'ttHTobb_M125_13TeV_powheg_pythia8': 200.0,
            'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 182.0,
            'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 203.0,
            'TT_TuneCUETP8M1_13TeV-powheg-pythia8': 200.0,
            'ttHToNonbb_M125_13TeV_powheg_pythia8': 200.0
        },
        # brilcalc on golden json, overestimated by a few % for SingleElectron
        # http://dashb-cms-job.cern.ch/dashboard/templates/task-analysis/#user=Joosep+Pata&refresh=60&table=Mains&p=1&records=-1&sorting%5B%5D=2&sorting%5B%5D=desc&activemenu=2&pattern=*tth_Aug3_V24_v2*&task=&from=&till=&timerange=lastMonth
        lumi = {
            "SingleMuon": 12891.528,
            "SingleElectron": 12891.528,
            "MuonEG": 12891.528,
            "DoubleEG": 12891.528,
            "DoubleMuon": 12891.528,
            "BTagCSV": 12891.528,
        },
        blr_cuts = { 
            #see MEAnalysis_cfg_heppy.py
            "sl_j4_t2": 20,
            "sl_j4_t3": 1.1,
            "sl_j4_tge4": -20,
            
            "sl_j5_t2": 20,
            "sl_j5_t3": 2.3,
            "sl_j5_tge4": -20,
            
            "sl_jge6_t2": -0.4,
            "sl_jge6_t3": 2.9,
            "sl_jge6_tge4": -20,

            "dl_j3_t2": 20,
            "dl_j3_t3": -20,
            "dl_jge4_t2": 20,
            "dl_jge4_t3": 2.3,
            "dl_jge4_tge4": -20,

            ##[CHECK-ME]
            "fh_j9_t4": -20,
            "fh_j8_t3": -20,
            "fh_j8_t4": -20,
            "fh_j7_t4": -20,
            "fh_j7_t3": -20,
            "fh_jge6_t4": -20,
            "fh_jge6_t3": -20,
        },
        systematics = [
            "CMS_scale_j",
            "CMS_res_j",
            "pu",
            "CMS_ttH_CSVcferr1",
            "CMS_ttH_CSVcferr2",
            "CMS_ttH_CSVhf",
            "CMS_ttH_CSVhfstats1",
            "CMS_ttH_CSVhfstats2",
            "CMS_ttH_CSVjes",
            "CMS_ttH_CSVlf",
            "CMS_ttH_CSVlfstats1",
            "CMS_ttH_CSVlfstats2"
        ]
    ),
    "Aug29": SparseHistogram(
        infile = "file:///mnt/t3nfs01/data01/shome/gregor/tth/gc/sparse/GCd38a0fafd62d/sparse.root",

        # gc:count.conf + hadd + getCounts    
        ngen = {  
            'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 6107821.0, 
            'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 5752692.0, 
            'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 4008755.0, 
            'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 9407120.0, 
            'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 5275233.0, 
            'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 3385165.0,
            'TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 9251823.0, 
            'TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': 11870599.0, 
            'TTTo2L2Nu_13TeV-powheg': 73972288.0, 
            'TT_TuneCUETP8M1_13TeV-powheg-pythia8': 56752956.0, 
            'ttHToNonbb_M125_13TeV_powheg_pythia8': 3820872.0, 
            'ttHTobb_M125_13TeV_powheg_pythia8': 3912212.0, 
        },
        # Calculate via calcLumis.py
        lumi = {
            'SingleMuon': 4884.125,
            'SingleElectron': 1243.151,
            'MuonEG': 12408.951,
            'DoubleEG': 6612.721,
            'DoubleMuon': 12793.602,
            'BTagCSV': 1162.172,
        },
        blr_cuts = {
            "sl_j4_t2": 20,
            "sl_j4_t3": 1.1,
            "sl_j4_tge4": -20,
            
            "sl_j5_t2": 20,
            "sl_j5_t3": 2.3,
            "sl_j5_tge4": -20,
            
            "sl_jge6_t2": -0.4,
            "sl_jge6_t3": 2.9,
            "sl_jge6_tge4": -20,

            "dl_j3_t2": 20,
            "dl_j3_t3": -20,
            "dl_jge4_t2": 20,
            "dl_jge4_t3": 2.3,
            "dl_jge4_tge4": -20,

            "fh_j9_t4": -20,
            "fh_j8_t3": -20,
            "fh_j8_t4": -20,
            "fh_j7_t4": -20,
            "fh_j7_t3": -20,
            "fh_jge6_t4": -20,
            "fh_jge6_t3": -20,
        },
        systematics = [
        ]
    ),
}

