import json
import sys
import numpy as np
from collections import Counter

def crab_report(fn):
    data = json.load(open(fn))

    durs = []
    sites = []
    retries = []
    states = []
    for k in data.keys():
        retries += [data[k]["Retries"]]
        states += [data[k]["State"]]
        if data[k]["State"] == "finished":
            nhours = data[k]['WallDurations'][-1]/3600.0
            sites += data[k]["SiteHistory"]
            durs += [nhours]

    mu = np.mean(durs)
    sig = np.std(durs)

    print "runtime {0:.2f} +- {1:.2f} hours".format(mu, sig)
    print "states:"
    for k, v in sorted(Counter(states).items(), key=lambda x: x[0]):
        print "  {0}={1}".format(k,v)
    print "sites:"
    for k, v in sorted(Counter(sites).items(), key=lambda x: x[0]):
        print "  {0}={1}".format(k,v)
    print "retries"
    for k, v in sorted(Counter(retries).items(), key=lambda x: x[0]):
        print "  {0}={1}".format(k,v)

crab_report(sys.argv[1])
