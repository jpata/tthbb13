import glob, os

#Cross-sections from
# $t \bar{t} + \mathrm{jets}$ - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO, $M_{top} = 172.5$ GeV
# ttH - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV, $M_H = 125.0$ GeV
xsec = {}
xsec[("ttjets", "8TeV")] = 252.89
xsec[("ttjets", "13TeV")] = 831.76
#http://pdg.lbl.gov/2013/reviews/rpp2013-rev-top-quark.pdf page 3, A-C
br_tt_to_ll = 0.105
br_tt_to_lj = 0.438

xsec[("ttjets", "tt_to_ll", "13TeV")] = xsec[("ttjets", "13TeV")] * br_tt_to_ll
xsec[("ttjets", "tt_to_lj", "13TeV")] = xsec[("ttjets", "13TeV")] * br_tt_to_lj

br_h_to_bb = 0.577
xsec[("tth", "8TeV")] = 0.1302
xsec[("tthbb", "8TeV")] = xsec[("tth", "8TeV")] * br_h_to_bb

#https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV#s_13_0_TeV
xsec[("tth", "13TeV")] = 0.5085
xsec[("tthbb", "13TeV")] = xsec[("tth", "13TeV")] * br_h_to_bb
xsec[("tth_nonhbb", "13TeV")] = xsec[("tth", "13TeV")] * (1.0 - br_h_to_bb)

xsec[("qcd_ht300to500", "13TeV")] = 366800.0
xsec[("qcd_ht500to700", "13TeV")] = 29370.0
xsec[("qcd_ht700to1000", "13TeV")] = 6524.0
xsec[("qcd_ht1000to1500", "13TeV")] = 1064.0
xsec[("qcd_ht1500to2000", "13TeV")] = 121.5
xsec[("qcd_ht2000toinf", "13TeV")] = 25.42

#From the AN
xsec[("wjets", "13TeV")] = 61526.7

xsec[("ttw_wqq", "13TeV")] = 0.435
xsec[("ttw_wlnu", "13TeV")] = 0.21
xsec[("ttz_zqq", "13TeV")] = 0.611

xsec[("stop_tW", "13TeV")] = 35.6
xsec[("stop_tbarW", "13TeV")] = 35.6
xsec[("stop_t", "13TeV")] = 45.34
xsec[("stop_tbar", "13TeV")] = 26.98 
xsec[("stop_s", "13TeV")] = 3.44

xsec[("ww", "13TeV")] = 118.7
xsec[("wz", "13TeV")] = 47.13
xsec[("zz", "13TeV")] = 16.523

samples_nick = {
    'ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1': "stop_s",
    'ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1': "stop_t",
    'ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1': "stop_tbar",
    'ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1': "stop_t",
    'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1': "stop_tbarW",
    'ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1':"stop_tW",
    'TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':"ttbarUnsplit",
    'TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': "ttbarUnsplit",
    'TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': "ttbarUnsplit",
    'TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': "ttbarUnsplit",
    'TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': "ttbarUnsplit",
    'TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': "ttbarUnsplit",
    'TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': "ttbarUnsplit",
    'TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8': "ttbarUnsplit",
    'TTTo2L2Nu_13TeV-powheg': 'ttbarUnsplit',
    'TT_TuneEE5C_13TeV-powheg-herwigpp': 'ttbarUnsplit',
    'TT_TuneCUETP8M1_13TeV-amcatnlo-pythia8': "ttbarUnsplit",
    'TT_TuneCUETP8M1_13TeV-powheg-pythia8': "ttbarUnsplit",
    'TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8': "ttW_Wlnu",
    'TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8':"ttW_Wqq",
    'TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8': "ttZ_Zqq",
    'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':"wjets_Wlnu_ht_100_200",
    'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':"wjets_Wlnu_ht_100_200",
    'WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':"wjets_Wlnu_ht_600_inf",
    'WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8':"wjets_Wqq_ht_600_inf",
    'WW_TuneCUETP8M1_13TeV-pythia8': "ww",
    'WZ_TuneCUETP8M1_13TeV-pythia8': "wz",
    'ZZ_TuneCUETP8M1_13TeV-pythia8': "zz",
    'ttHToNonbb_M125_13TeV_powheg_pythia8': "ttH_nonhbb",
    'ttHTobb_M125_13TeV_powheg_pythia8': "ttH_hbb",
    'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 'qcd',
    'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 'qcd',
    'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 'qcd',
    'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 'qcd',
    'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 'qcd',
    'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 'qcd',
    "SingleMuon": "data_m",
    "SingleElectron": "data_e",
    "MuonEG": "data_em",
    "DoubleEG": "data_ee",
    "DoubleMuon": "data_mm",
    "BTagCSV": "data_fh",
}

#Numeric keys for processes, used for filling the process axis
#in the sparse histogram
PROCESS_MAP = {
    "ttH_hbb": 0,
    "ttH_nonhbb": 1,
    "ttbarPlusBBbar": 2,
    "ttbarPlus2B": 3,
    "ttbarPlusB": 4,
    "ttbarPlusCCbar": 5,
    "ttbarOther": 6,
    "qcd": 13,

#need to keep different data samples separate at this point
    "data_e": 7,
    "data_m": 8,
    "data_mm": 9,
    "data_ee": 10,
    "data_em": 11,
    "data_fh": 12,
}

TRIGGERPATH_MAP = {
    "m": 1,
    "e": 2,
    "mm": 3,
    "em": 4,
    "ee": 5,
    "fh": 6,
}

xsec_sample = {
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8":     xsec[("ttjets", "13TeV")],
    "TT_TuneEE5C_13TeV-powheg-herwigpp":        xsec[("ttjets", "13TeV")],
    "TTTo2L2Nu_13TeV-powheg":                   xsec[("ttjets", "tt_to_ll", "13TeV")],
    "TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 0.5*xsec[("ttjets", "tt_to_lj", "13TeV")],
    "TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":    0.5*xsec[("ttjets", "tt_to_lj", "13TeV")],
    "ttHTobb_M125_13TeV_powheg_pythia8":        xsec[("tthbb", "13TeV")],
    "ttHToNonbb_M125_13TeV_powheg_pythia8":     xsec[("tth_nonhbb", "13TeV")],

    'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' :   xsec[("qcd_ht300to500", "13TeV")],
    'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' :   xsec[("qcd_ht500to700", "13TeV")],
    'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' :  xsec[("qcd_ht700to1000", "13TeV")],
    'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : xsec[("qcd_ht1000to1500", "13TeV")],
    'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : xsec[("qcd_ht1500to2000", "13TeV")],
    'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' :  xsec[("qcd_ht2000toinf", "13TeV")],
}

#Configure the site-specific file path
import os
hn = os.environ.get("HOSTNAME", "")
vo = os.environ.get("VO_CMS_DEFAULT_SE", "")

def pfn_to_lfn(fn):
    """
    Converts a PFN to a LFN. Filename must be of
    /store/XYZ type.
    """
    return fn[fn.find("/store"):]

def get_files(fname):
    # Expect fname relative to CMSSW BASE
    fname = fname.replace("$CMSSW_BASE", os.environ["CMSSW_BASE"])
    lines = open(fname).readlines()
    lines = map(lambda x: x.strip(), lines)
    lines = filter(lambda x: "root" in x, lines)
    lines = map(lambda x: x.split()[0], lines)
    return lines

# This function is used everywher to translate LFN /store to PFN root://
# currently all files are assumed to reside at CSCS
site_prefix = "root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat"
def getSitePrefix(fn=""):
    if fn.startswith("/store"):
        return site_prefix  + fn
    elif fn.startswith("file://") or fn.startswith("root://"):
        return fn
    else:
        raise Exception("Could not open file: {0}".format(fn))

def get_prefix_sample(datasetpath):
    spl = datasetpath.split("__")
    if len(spl) == 2:
        prefix = spl[0]
        sample = spl[1]
    elif len(spl) == 1:
        prefix = ""
        sample = datasetpath
    else:
        raise Exception("could not parse DATASETPATH: {0}".format(datasetpath))
    return (prefix, sample)

def getSampleNGen(sample):
    import ROOT
    n = 0
    nneg = 0
    npos = 0
    nw = 0
    for f in sample.subFiles:
        tfn = lfn_to_pfn(f)
        tf = ROOT.TFile.Open(tfn)
        hc = tf.Get("Count")
        hneg = tf.Get("CountNegWeight")
        hpos = tf.Get("CountPosWeight")
        hw = tf.Get("CountWeighted")
        n += hc.GetBinContent(1)
        nneg += hneg.GetBinContent(1)
        npos += hpos.GetBinContent(1)
        nw += hw.GetBinContent(1)
        tf.Close()
        del tf
        print tfn, npos, nneg, nw
    return int(nw)
