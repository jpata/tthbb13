#! /usr/bin/env python
import os
import subprocess
from ROOT import TH1F, TCanvas, TFile, TObject

sample = "QCD1500"
copy = 1
extract = 1
analyse = 1

se = "root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat//store/user/dsalerno"
path = {
    # "QCD300":"tth/VHBBHeppyV21_tthbbV9_v3/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v3/160514_193325",
    # "QCD500":"tth/VHBBHeppyV21_tthbbV9_v3/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v3/160514_194135",
    # "QCD700":"tth/VHBBHeppyV21_tthbbV9_v3/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v3/160514_193622",
    # "QCD1000":"tth/VHBBHeppyV21_tthbbV9_v3/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v3/160514_193740",
    # "QCD1500":"tth/VHBBHeppyV21_tthbbV9_v3/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v3/160514_194255",
    # "QCD2000":"tth/VHBBHeppyV21_tthbbV9_v3/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v3/160514_193858",
    # "TTbar":"tth/VHBBHeppyV21_tthbbV9_v3_2/TT_TuneCUETP8M1_13TeV-powheg-pythia8/VHBBHeppyV21_tthbbV9_v3_2/160515_085747",
    # "ttHbb":"tth/VHBBHeppyV21_tthbbV9_v3_3/ttHTobb_M125_13TeV_powheg_pythia8/VHBBHeppyV21_tthbbV9_v3_3/160518_110721",
    # "ttHNon":"tth/VHBBHeppyV21_tthbbV9_v3_3/ttHToNonbb_M125_13TeV_powheg_pythia8/VHBBHeppyV21_tthbbV9_v3_3/160518_110839",

    "QCD300":"tth/VHBBHeppyV21_tthbbV9_v2/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v2/160503_194235",
    "QCD500":"tth/VHBBHeppyV21_tthbbV9_v2/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v2/160503_194354",
    "QCD700":"tth/VHBBHeppyV21_tthbbV9_v2/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v2/160503_194510",
    "QCD1000":"tth/VHBBHeppyV21_tthbbV9_v2/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v2/160503_194632",
    "QCD1500":"tth/VHBBHeppyV21_tthbbV9_v2/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v2/160503_194746",
    "QCD2000":"tth/VHBBHeppyV21_tthbbV9_v2/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBBHeppyV21_tthbbV9_v2/160503_194905",
    "TTbar":"tth/VHBBHeppyV21_tthbbV9_v2/TT_TuneCUETP8M1_13TeV-powheg-pythia8/VHBBHeppyV21_tthbbV9_v2/160503_194119",
    "ttHbb":"tth/VHBBHeppyV21_tthbbV9_v2/ttHTobb_M125_13TeV_powheg_pythia8/VHBBHeppyV21_tthbbV9_v2/160503_194005",
}

endpath = "/scratch/dsalerno/tth/VHBBHeppyV21_tthbbV9_v2/"
destination = endpath+sample

if( copy ):
    listdir = "gfal-ls "+se+"/"+path[sample]
    p = subprocess.Popen(listdir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    for line in p.stdout.readlines():
        directory = line.split()[0]
        print "directory ", directory
        listlog = listdir+"/"+directory+"/log"
        q = subprocess.Popen(listlog, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        for line in q.stdout.readlines():
            logfile = line.split()[0]
            #print "logfile ", logfile
            if( os.path.isfile(destination+"/"+logfile) ):
                print logfile, " already copied"
                continue
            half = logfile.split("_")[1]
            num = half.split(".")[0]
            stdoutfile = "cmsRun-stdout-"+num+".log"
            if( os.path.isfile(destination+"/"+stdoutfile) ):
                print logfile, " already extracted"
                continue
            copylog = "gfal-copy "+se+"/"+path[sample]+"/"+directory+"/log/"+logfile+" file://"+destination
            #print copylog
            os.system(copylog)

if( extract ):
    r = subprocess.Popen("ls "+destination, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    for line in r.stdout.readlines():
        zipfile = line.split()[0]
        if(zipfile.find('log.tar.gz')<0):
            continue
        #print "zipfile ", zipfile
        half = zipfile.split("_")[1]
        num = half.split(".")[0]
        stdoutfile = "cmsRun-stdout-"+num+".log"
        #print "stdoutfile", stdoutfile
        if( os.path.isfile(destination+"/"+stdoutfile) ):
            print stdoutfile, " already extracted"
            continue
        unzip = "tar -C "+destination+" -zxvf "+destination+"/"+zipfile
        os.system(unzip)
    os.system("rm "+destination+"/cmsRun_*.log.tar.gz")
    os.system("rm "+destination+"/FrameworkJobReport-*.xml")   

if( analyse ):
    outf = TFile.Open(endpath+"/jobtime.root","UPDATE")
    outf.cd()
    htime_total = TH1F("htime_total","htime_total",100,0,50)
    htime_vhbb  = TH1F("htime_vhbb" ,"htime_vhbb" ,100,0,10)
    htime_mem   = TH1F("htime_mem"  ,"htime_mem"  ,100,0,50)

    h_0_7_322   = TH1F("h_0_7_322","h_0_7_322",200,0,200)
    h_0_7_022   = TH1F("h_0_7_022","h_0_7_022",300,0,300)
    h_0_7_021   = TH1F("h_0_7_021","h_0_7_021",300,0,300)

    h_0_8_422   = TH1F("h_0_8_422","h_0_8_422",200,0,200)    
    h_0_8_322   = TH1F("h_0_8_322","h_0_8_322",500,0,500)
    h_0_8_022   = TH1F("h_0_8_022","h_0_8_022",300,0,300)
    h_0_8_021   = TH1F("h_0_8_021","h_0_8_021",300,0,300)

    h_0_9_422   = TH1F("h_0_9_422","h_0_9_422",2000,0,2000)    
    h_0_9_022   = TH1F("h_0_9_022","h_0_9_022",2000,0,2000)
    h_0_9_021   = TH1F("h_0_9_021","h_0_9_021",2000,0,2000)

    h_0_10_421   = TH1F("h_0_10_422","h_0_10_422",300,0,300)    
    h_0_10_021   = TH1F("h_0_10_021","h_0_10_021",200,0,200)

    h_0_11_421   = TH1F("h_0_11_422","h_0_11_422",200,0,200)    
    h_0_11_021   = TH1F("h_0_11_021","h_0_11_021",200,0,200)

    h_1_7_322   = TH1F("h_1_7_322","h_1_7_322",300,0,300)
    h_1_7_022   = TH1F("h_1_7_022","h_1_7_022",500,0,500)
    h_1_7_021   = TH1F("h_1_7_021","h_1_7_021",500,0,500)

    h_1_8_422   = TH1F("h_1_8_422","h_1_8_422",200,0,200)    
    h_1_8_322   = TH1F("h_1_8_322","h_1_8_322",500,0,500)
    h_1_8_022   = TH1F("h_1_8_022","h_1_8_022",500,0,500)
    h_1_8_021   = TH1F("h_1_8_021","h_1_8_021",500,0,500)

    h_1_9_422   = TH1F("h_1_9_422","h_1_9_422",2000,0,2000)    
    h_1_9_022   = TH1F("h_1_9_022","h_1_9_022",2000,0,2000)
    h_1_9_021   = TH1F("h_1_9_021","h_1_9_021",2000,0,2000)

    h_1_10_421   = TH1F("h_1_10_422","h_1_10_422",500,0,500)    
    h_1_10_021   = TH1F("h_1_10_021","h_1_10_021",300,0,300)

    h_1_11_421   = TH1F("h_1_11_422","h_1_11_422",200,0,200)    
    h_1_11_021   = TH1F("h_1_11_021","h_1_11_021",200,0,200)

    s = subprocess.Popen("ls "+destination, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    for line in s.stdout.readlines():
        if(line.find('stdout') > 0):
            outfile = line.split()[0]
            #print "outfile", outfile
            f = open(destination+"/"+outfile)
            lines = f.readlines()
            hypo = -1
            cat = -1
            method = -1
            for l in lines:
                if(l.find('timeto_doVHbb') == 0):
                    time_vhbb = float(l.split()[1])/3600
                    htime_vhbb.Fill( time_vhbb )
                if(l.find('timeto_doMEM') == 0):
                    htime_mem.Fill( (float(l.split()[1]) - time_vhbb*3600)/3600 )
                if(l.find('timeto_totalJob') == 0):
                    htime_total.Fill( float(l.split()[1])/3600 )
                if(l.find('hypo=0')>0):
                    hypo = 0
                if(l.find('hypo=1')>0):
                    hypo = 1                   

                if(l.find('fh_j7_tge5')>0 or l.find('fh_j7_t4')>0):
                    cat = 7
                if(l.find('fh_j8_tge5')>0 or l.find('fh_j8_t4')>0):
                    cat = 8                    
                if(l.find('fh_jge9_tge5')>0 or l.find('fh_jge9_t4')>0):
                    cat = 9
                if(l.find('fh_j8_t3')>0 ):
                    cat = 10
                if(l.find('fh_j7_t3')>0 ):
                    cat = 11

                if(l.find('conf=FH_3w2h2t')>0):
                    method = 322
                if(l.find('conf=FH_4w2h2t')>0):
                    method = 422
                if(l.find('conf=FH_4w2h1t')>0):
                    method = 421
                if(l.find('conf=FH_0w0w2h2t')>0):
                    method = 022
                if(l.find('conf=FH_0w0w2h1t')>0):
                    method = 021

                if(l.find('Job done in...............')>0):
                    half = l.split('...............')[1]
                    time = float(half.split()[0])
                    if(hypo==0):
                        if(cat==7):
                            if(method==322):
                                h_0_7_322.Fill(time)
                            if(method==022):
                                h_0_7_022.Fill(time)
                            if(method==021):
                                h_0_7_021.Fill(time)
                        if(cat==8):
                            if(method==422):
                                h_0_8_422.Fill(time)
                            if(method==322):
                                h_0_8_322.Fill(time)
                            if(method==022):
                                h_0_8_022.Fill(time)
                            if(method==021):
                                h_0_8_021.Fill(time)
                        if(cat==9):
                            if(method==422):
                                h_0_9_422.Fill(time)
                            if(method==022):
                                h_0_9_022.Fill(time)
                            if(method==021):
                                h_0_9_021.Fill(time)
                        if(cat==10):
                            if(method==421):
                                h_0_10_421.Fill(time)
                            if(method==021):
                                h_0_10_021.Fill(time)
                        if(cat==11):
                            if(method==421):
                                h_0_11_421.Fill(time)
                            if(method==021):
                                h_0_11_021.Fill(time)
                    if(hypo==1):
                        if(cat==7):
                            if(method==322):
                                h_1_7_322.Fill(time)
                            if(method==022):
                                h_1_7_022.Fill(time)
                            if(method==021):
                                h_1_7_021.Fill(time)
                        if(cat==8):
                            if(method==422):
                                h_1_8_422.Fill(time)
                            if(method==322):
                                h_1_8_322.Fill(time)
                            if(method==022):
                                h_1_8_022.Fill(time)
                            if(method==021):
                                h_1_8_021.Fill(time)
                        if(cat==9):
                            if(method==422):
                                h_1_9_422.Fill(time)
                            if(method==022):
                                h_1_9_022.Fill(time)
                            if(method==021):
                                h_1_9_021.Fill(time)
                        if(cat==10):
                            if(method==421):
                                h_1_10_421.Fill(time)
                            if(method==021):
                                h_1_10_021.Fill(time)
                        if(cat==11):
                            if(method==421):
                                h_1_11_421.Fill(time)
                            if(method==021):
                                h_1_11_021.Fill(time)

            # t = subprocess.Popen("grep 'timeto' "+destination+"/"+outfile, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            # for line in t.stdout.readlines():
            #     if(line.find('totalJob') > 0):
            #         jobtime = line.split()[1]
            #         #print "jobtime ", float(jobtime)/3600
            #         htime.Fill(float(jobtime)/3600)

    treedir = outf.GetDirectory( sample)
    if(treedir==None):
        treedir = outf.mkdir( sample )

    treedir.cd()
    htime_total.Write("", TObject.kOverwrite)
    htime_vhbb.Write("", TObject.kOverwrite)
    htime_mem.Write("", TObject.kOverwrite)

    h_0_7_322.Write("", TObject.kOverwrite)
    h_0_7_022.Write("", TObject.kOverwrite)
    h_0_7_021.Write("", TObject.kOverwrite)
    h_0_8_422.Write("", TObject.kOverwrite)
    h_0_8_322.Write("", TObject.kOverwrite)
    h_0_8_022.Write("", TObject.kOverwrite)
    h_0_8_021.Write("", TObject.kOverwrite)
    h_0_9_422.Write("", TObject.kOverwrite)
    h_0_9_022.Write("", TObject.kOverwrite)
    h_0_9_021.Write("", TObject.kOverwrite)
    h_0_10_421.Write("", TObject.kOverwrite)
    h_0_10_021.Write("", TObject.kOverwrite)
    h_0_11_421.Write("", TObject.kOverwrite)
    h_0_11_021.Write("", TObject.kOverwrite)

    h_1_7_322.Write("", TObject.kOverwrite)
    h_1_7_022.Write("", TObject.kOverwrite)
    h_1_7_021.Write("", TObject.kOverwrite)
    h_1_8_422.Write("", TObject.kOverwrite)
    h_1_8_322.Write("", TObject.kOverwrite)
    h_1_8_022.Write("", TObject.kOverwrite)
    h_1_8_021.Write("", TObject.kOverwrite)
    h_1_9_422.Write("", TObject.kOverwrite)
    h_1_9_022.Write("", TObject.kOverwrite)
    h_1_9_021.Write("", TObject.kOverwrite)
    h_1_10_421.Write("", TObject.kOverwrite)
    h_1_10_021.Write("", TObject.kOverwrite)
    h_1_11_421.Write("", TObject.kOverwrite)
    h_1_11_021.Write("", TObject.kOverwrite)

    outf.Close()
