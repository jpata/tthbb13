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
xsec[("tthbb", "8TeV")] = xsec[("tth", "8TeV")]

#https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV#s_13_0_TeV
xsec[("tth", "13TeV")] = 0.5085
xsec[("tthbb", "13TeV")] = xsec[("tth", "13TeV")] * br_h_to_bb

#Configure the site-specific file path
import os
hn = os.environ["HOSTNAME"]
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
if "kbfi" in hn or "comp-" in hn or "kbfi" in vo:
    pfPath = "/hdfs/cms/"
    lfPrefix = "file://"
    def lfn_to_pfn(fn):
        return "file:///hdfs/cms" + fn
elif "psi" in hn or "psi" in vo:
    pfPath = "/pnfs/psi.ch/cms/trivcat/"
    lfPrefix = "dcap://t3se01.psi.ch:22125/"
    def lfn_to_pfn(fn):
        return "dcap://t3se01.psi.ch:22125/pnfs/psi.ch/cms/trivcat" + fn
else:
    print "Warning: host '{0}' VO '{1}' is unknown, using xrootd".format(hn, vo)
    pfPath = ""
    lfPrefix = "root://cmsxrootd.fnal.gov/"
    def lfn_to_pfn(fn):
        return fn
