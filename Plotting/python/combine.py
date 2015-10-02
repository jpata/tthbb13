import os, sys, multiprocessing, subprocess

def runCombine(cardname, outname):
    p = subprocess.call(["combine", "-n", outname, "-M", "Asymptotic", "-t", "-1", cardname])

def runCombined_par(args):
    runCombine(*args)

files = sys.argv[1:]

arglist = []
for f in files:
    name = f.replace("shapes_", "")
    name = "_ttH_leptonic_" + name.replace(".txt", "")
    arglist += [(f, name)]

pool = multiprocessing.Pool(40)
pool.map(runCombined_par, arglist)
