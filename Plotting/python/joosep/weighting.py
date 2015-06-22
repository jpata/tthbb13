def get_weight(s, lumi=10000):
    if "tth" in s:
        return 199700.0 / 93694.0 * lumi
    return lumi
