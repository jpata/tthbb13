#!/usr/local/bin/python

import urllib
import os
import httplib
from urlparse import urlparse

def checkUrl(url):
    p = urlparse(url)
    conn = httplib.HTTPConnection(p.netloc)
    conn.request('HEAD', p.path)
    resp = conn.getresponse()
    return resp.status < 400

if __name__ == '__main__':

    # path = "http://submit-4.t2.ucsd.edu/CSstoragePath/74/uscms5689/151101_134821:dsalerno_crab_TTH_v3/job_out." #TTH
    # path = "https://cmsweb.cern.ch/scheddmon/095/cms320/151102_094247:dsalerno_crab_TTJets_v2/job_out." #TTJets
    path = "http://submit-5.t2.ucsd.edu/CSstoragePath/74/uscms5689/151102_101912:dsalerno_crab_QCD300_v2/job_out." #QCD300
    # path = "https://cmsweb.cern.ch/scheddmon/059/cms320/151102_102820:dsalerno_crab_QCD500_v1/job_out." #QCD500
    # path = "https://cmsweb.cern.ch/scheddmon/095/cms320/151102_103023:dsalerno_crab_QCD700_v3/job_out." #QCD700
    # path = "https://cmsweb.cern.ch/scheddmon/0109/cms320/151102_103137:dsalerno_crab_QCD1000_v1/job_out." #QCD1000
    # path = "http://submit-4.t2.ucsd.edu/CSstoragePath/74/uscms5689/151102_101512:dsalerno_crab_QCD1500_v1/job_out." #QCD1500
    # path = "https://cmsweb.cern.ch/scheddmon/096/cms320/151102_101108:dsalerno_crab_QCD2000_v5/job_out." #QCD2000

    for n in range(0,1326):
        
        i = str(n+1)
        
        f = urllib.urlopen("http://www.google.com")
        for m in range(6,-1,-1):
            j = str(m)
            if checkUrl(path+i+"."+j+".txt"):
                f = urllib.urlopen(path+i+"."+j+".txt")
                break
            #else:
                #print "webpage does not exist i="+i+" j="+j
            
        lines = f.readlines()
        f.close()

        if (lines[0].find("Job output has not been processed") >=0):
            print "job running: "+i
            continue

        exitcode = -99
        for line in lines:
            if (line.find("Short exit status:") >= 0):
                a, b = line.split(":")
                B = b.strip()
                exitcode = int(B)
                #print "exit code = ", exitcode
                break

        crash = 0
        if (exitcode != 0):
            print "job failed : "+i+" (exitcode="+str(exitcode)+")"
        else:
            for l in lines:
                if (l.find("The remote file is not open") >= 0):
                    print "probably crashed: "+i
                    crash = 1
                    break
            if(crash==0):
                print "job ok     : "+i
