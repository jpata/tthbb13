import FWCore.ParameterSet.Config as cms
import glob, os
import ConfigParser

#Cross-sections from
# $t \bar{t} + \mathrm{jets}$ - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO, $M_{top} = 172.5$ GeV
# ttH - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV, $M_H = 125.0$ GeV
xsec = {}
xsec[("ttjets", "8TeV")] = 252.89
xsec[("ttjets", "13TeV")] = 831.76

br_h_to_bb = 0.569
xsec[("tth", "8TeV")] = 0.1302
xsec[("tthbb", "8TeV")] = xsec[("tth", "8TeV")] * br_h_to_bb

#https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV#s_13_0_TeV
xsec[("tth", "13TeV")] = 0.5085
xsec[("tthbb", "13TeV")] = xsec[("tth", "13TeV")] * br_h_to_bb

xsec[("qcd_ht300to500", "13TeV")] = 366800.0
xsec[("qcd_ht500to700", "13TeV")] = 29370.0
xsec[("qcd_ht700to1000", "13TeV")] = 6524.0
xsec[("qcd_ht1500to2000", "13TeV")] = 121.5
xsec[("qcd_ht2000toinf", "13TeV")] = 25.42

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

def lfn_to_pfn(fn):
    return fn

#These assume the files are located on the local tier
if "kbfi" in hn or "kbfi" in vo:
    pfPath = "/hdfs/cms/"
    lfPrefix = "file://"
    def lfn_to_pfn(fn):

        #fix to replace broken file names
        if fn.startswith("file://"):
            return fn
        else:
            return "file:///hdfs/cms" + fn
elif "psi" in hn or "psi" in vo:
    # pfPath = "/pnfs/psi.ch/cms/trivcat/"
    # lfPrefix = "dcap://t3se01.psi.ch:22125/"
    def lfn_to_pfn(fn):
        if fn.startswith("file://"):
            return fn
        else:
            return "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/" + fn
else:
    print "Warning: host '{0}' VO '{1}' is unknown, using xrootd".format(hn, vo)
    pfPath = ""
    lfPrefix = "root://xrootd-cms.infn.it/"
    def lfn_to_pfn(fn):
        return fn

def getSampleNGen(sample):
    import ROOT
    n = 0
    nneg = 0
    npos = 0
    for f in sample.subFiles:
        tfn = lfn_to_pfn(f)
        tf = ROOT.TFile.Open(tfn)
        hc = tf.Get("Count")
        hneg = tf.Get("CountNegWeight")
        hpos = tf.Get("CountPosWeight")
        n += hc.GetBinContent(1)
        nneg += hneg.GetBinContent(1)
        npos += hpos.GetBinContent(1)
        tf.Close()
        del tf
        #print tfn, hc.GetBinContent(1)
    return int(npos-nneg)
