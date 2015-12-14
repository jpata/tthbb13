#!/usr/bin/env python
import sys, os

sample = "QCD2000"
perjob = 10000

datafiles = []
for line in open(sample+".events").readlines():
    f, n = line.split()
    datafiles += [(f, int(n))]

l = []
for df, dn in datafiles:
    cur = 0
    while cur < dn:
        l += [(df, cur, perjob)]
        cur += perjob

outfile = open(sample+".jobs","w")

n = 0
for fn, cur, perjob in l:
    outfile.write("{0}___{1}___{2}\n".format(fn, cur, perjob))
    n+=1

print "wrote {0} lines to {1}".format(n, outfile)
outfile.close()
