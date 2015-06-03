def get_weight(s, lumi=20000):
    if "ttjets_13TeV_phys14" in s:
        return lumi * 831.76 / 25049638.0
        #return lumi * 252.89 / 25049638.0
    elif s == "tth_13TeV_phys14":
        return lumi * 0.5085 / 199699.0
        #return lumi * 0.1302 / 199699.0
    return -1

