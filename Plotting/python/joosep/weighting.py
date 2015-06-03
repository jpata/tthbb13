def get_weight(s, lumi=10000):
    if "ttjets_13TeV_phys14" in s:
        return lumi * 831.76 / 25049638.0
        #return lumi * 252.89 / 25049638.0
    elif s == "tth_13TeV_phys14":
        #https://cmsweb.cern.ch/das/request?input=dataset%3D%2FTTbarH_M-125_13TeV_amcatnlo-pythia8-tauola%2FPhys14DR-PU20bx25_tsg_PHYS14_25_V1-v2%2FMINIAODSIM&instance=prod%2Fglobal
        return lumi * 0.5085 / 199700.0
    return -1

