from MEAnalysis_heppy import config
from PhysicsTools.HeppyCore.framework.looper import Looper

treean = config.sequence[-1]
colls = treean.collections

ret = {}
ret["collections"] = {}
for collname in colls.keys():
    vard = {}
    collname_short = colls[collname].name
    for v in colls[collname].objectType.allVars(True):
        vard[v.name] = (v.type.__name__, v.help)
    if len(vard) == 1:
        k = list(vard.keys())[0]
        vard[collname] = vard.pop(k)
    ret["collections"][collname_short] = (vard, colls[collname].maxlen)

ret["globalObjects"] = {}
colls = treean.globalObjects
for collname in colls.keys():
    vard = {}
    collname_short = colls[collname].name
    for v in colls[collname].objectType.allVars(True):
        vard[v.name] = (v.type.__name__, v.help)
    if len(vard) == 1:
        k = list(vard.keys())[0]
        vard[collname] = vard.pop(k)
    ret["globalObjects"][collname_short] = (vard, 1)

ret["globalVariables"] = {}
colls = treean.globalVariables
for var in colls:
    collname_short = var.name
    ret["globalVariables"][collname_short] = var.type.__name__

import json
js = json.dumps(ret, sort_keys=True, indent=2)

of = open("tree.json", "w")
of.write(js)
of.close()
