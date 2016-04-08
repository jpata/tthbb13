#!/usr/bin/env python
#This script dumps a json that corresponds to the heppy
from MEAnalysis_heppy import config
from PhysicsTools.HeppyCore.framework.looper import Looper

treean = config.sequence[-1]
colls = treean.collections

#A big nested dict that holds the output
ret = {}

#Dump all collections
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


#Dump all global objects
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

#Dump all global variables
ret["globalVariables"] = {}
colls = treean.globalVariables
for var in colls:
    collname_short = var.name
    ret["globalVariables"][collname_short] = var.type.__name__
for var in ["run", "lumi", "evt"]:
    ret["globalVariables"][var] = "long"
for var in ["xsec", "nTrueInt", "puWeight", "genWeight"]:
    ret["globalVariables"][var] = "float" 

import json
js = json.dumps(ret, sort_keys=True, indent=2)

of = open("tree.json", "w")
of.write(js)
of.close()
