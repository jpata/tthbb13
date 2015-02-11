#!/bin/env python
#################################################################
# data_replica.py
#
# Author: Leonardo Sala <leonardo.sala@cern.ch>
#
# $Id: data_replica.py,v 1.43 2012/05/21 11:42:56 leo Exp $
#################################################################



import os
from os import popen, path, environ, getpid
from sys import argv,exit
from optparse import OptionParser
from time import time


PREFERRED_SITES = []
DENIED_SITES = ["T0","MSS"]
PROTOCOL = "srmv2"

###WARNING: this enables the possibility to fully replicate a SE
ENABLE_REPLICATION=False

LCG_OPTIONS_COMMON = " -b "
###for lcg-utils>=1.7 and < 1.11
LCG_OPTIONS_17 = LCG_OPTIONS_COMMON
LCG_OPTIONS_17 += "--srm-timeout=6000 "
LCG_OPTIONS_17+= "-n 1 "
LCG_OPTIONS_17+= "--connect-timeout=6000 "
LCG_OPTIONS_17+= "--bdii-timeout=6000 "
LCG_OPTIONS_17+= "--sendreceive-timeout=6000 "

###for lcg-utils>= 1.11
#LCG_OPTIONS_1_11
###for lcg-utisl <1.7
LCG_OPTIONS = LCG_OPTIONS_COMMON
LCG_OPTIONS = "--timeout=6000 "
LCG_OPTIONS+= "-n 1 "

SRM_OPTIONS = "-streams_num=1 "
#SRM_OPTIONS += "-cksm_type=negotiate "
#SRM_OPTIONS += "-overwrite_mode=ALWAYS "
SRM_OPTIONS += "-retry_num=1 "
SRM_OPTIONS += "-request_lifetime=6000 "


#### HardCoded sites:
CERN_EOS_SRM = "srm://srm-eoscms.cern.ch:8443/srm/v2/server?SFN=/eos/cms/"
CERN_CASTOR_SRM = "srm://srm-cms.cern.ch:8443/srm/managerv2?SFN="

if __name__ == "__main__":
    usage = """usage: %prog [options] filelist.txt [dest_dir]

    This program will replicate a list of files from a site to another one using SRM

    filelist.txt is a text file containing a list of LFN you want to replicate to a site, one LFN per line 

    dest_dir must be a complete PFN, eg file:///home/user/, if none it will be retrieved from the lfn
    information and the destination site

    you must at least declare [dest_dir] or the --to-site option

    Sites must have a standard name, e.g. T2_CH_CSCS

    Five log-files can be produced by this script:
       * <logfile>.log: contains a PhEDEx-style log
       * <logfile>_existingList.log: contains LFNs and PFNs of files existing on destination (SRM
         endpoints only)
       * <logfile>_failedList.log: a list of all the LFNs which failed
       * <logfile>_successList.log: a list of all the LFNs successfully copied
       * <logfile>_noReplica.log: a list of files with no replicas found (check DENIED_SITES list in the
         script header)
    
    
[USE CASES]

* Replicate a file list without specifying a source node (discovery). In this case, a source nodes list is retrieved from PhEDEx data service: 
      data_replica --discovery --to-site YOUR_SITE filelist.txt

  * Replicate a file list using discovery and giving a destination folder:
      data_replica --discovery --to-site YOUR_SITE filelist.txt /store/user/leo

  * Replicate a file list NOT registered in PhEDEx. In this case, you should specify --from-site.
      data_replica  --from-site FROM_SITE --to-site YOUR_SITE filelist.txt

  * Replicate a file list NOT registered in PhEDEx, giving a destination folder.Also in this case, you should specify --from-site.
      data_replica  --from-site FROM_SITE --to-site YOUR_SITE filelist.txt /store/user/leo

  * Copying data locally: in this case you don't have to give the --to-site option but you need to give
  a dest_dir in PFN format. Warning: if you intend to use the --recreate-subdirs option, you need to create yourself the local directory structure:
      data_replica --from-site FROM_SITE filelist.txt  file:///`pwd`/

  * Copying data from a local area: the list of files should contain only full paths:
      data_replica.py --from-site LOCAL --to-site T3_CH_PSI filelist.txt /store/user/leo/test1

  * Copying files from CAF:
      data_replica.py --from-site T2_CH_CAF --to-site T3_CH_PSI filelist.txt /store/user/leo/testCastor4 

  * Copying files from user area under CASTOR@CERN (files not registered to DBS). In this case, PFN are not retrievable from PhEDEx data service,
  so the file list must contain Castor full path (/castor/cern.ch/....) and the source site is CERN_CASTOR_USER:
      data_replica.py --from-site CERN_CASTOR_USER --to-site T3_CH_PSI filelist.txt /store/user/leo/testCastor3 

  * When copying from a Castor area from lxplus and you want to pre-stage files to a local /tmp directory through rfcp
  (useful when copying files not accessed since long, avoiding srm timeouts), use --castor-stage.

  * Copying data from EOS@CERN, you have to specify --from-site CERN_EOS (this is automatically done for T2_CH_CAF, at the time of writing). Filenames in filelist.txt are still LFN (/store/...):
      data_replica.py --from-site CERN_EOS --to-site T3_CH_PSI filelist.txt /store/user/leo/testEos
  
  Use the -h option for more information
  
  """

    parser = OptionParser(usage = usage, version="%prog 1.0")
    parser.add_option("--logfile",action="store", dest="logfile",default="data_replica.log",
                      help="file for the phedex-like log, default is data_replica.log")
    parser.add_option("--discovery",
                      action="store_true", dest="usePDS", default=False,
                      help="Retrieve data distribution from PhEDEx Data Service")
    parser.add_option("--from-site",
                      action="store", dest="FROM_SITE", default="",
                      help="Source site, eg: T2_CH_CSCS. If LOCAL is indicated, the file list must be a list of global paths")
    parser.add_option("--to-site",
                      action="store", dest="TO_SITE", default="",
                      help="Destination file, eg: T2_CH_CSCS")
    parser.add_option("--recreate-subdirs",
                      action="store_true", dest="RECREATE_SUBDIRS", default=False,
                      help="Recreate the full subdir tree")
    
    parser.add_option("--dryrun",
                      action="store_true", dest="DRYRUN", default=False,
                      help="Don not actually copy anything")
    
    parser.add_option("--debug",
                      action="store_true", dest="DEBUG", default=False,
                      help="Verbose mode")
    
    parser.add_option("--copy-tool",
                      action="store", dest="TOOL", default="lcg-cp",
                      help="Selects the copy tool to be used (lcg-cp or srmcp). By default lcg-cp is used")
    
    parser.add_option("--castor-stage",
                      action="store_true", dest="CASTORSTAGE", default=False,
                      help="Enables staging of Castor files in a local tmp dir. Works only on lxplus, and uses $TMPDIR as tmp dir.")
    
    parser.add_option("--delete",
                      action="store_true", dest="DELETE", default=False,
                      help="If file exists at destination and its size is _smaller_ than the source one, delete it. WARNING: destination files are checked only for SRM endpoints.")

    parser.add_option("--whitelist",
                      action="store", dest="WHITELIST", default="",
                      help="Sets up a comma-separated White-list (preferred sites). Transfers will start from thse sites, then data_replica will use the other sites found with the --discovery option (without --discovery this option makes no sense). Sites not included in the whitelist will be not excluded: use --blacklist for this.")

    parser.add_option("--blacklist",
                      action="store", dest="BLACKLIST", default="",
                      help="Sets up a comma-separated Black-list (excluded sites). Data_replica won't use these sites (without --discovery this option makes no sense).")
        
    (moptions, args) = parser.parse_args()
    moptions.Replicate = ENABLE_REPLICATION
    
    if len(args)<1:
        print usage
        exit(-1)
    



def writeLog(logname,message):
    success_f = open(logname,"a")
    success_f.write(message)
    success_f.close()
                          
    
def printDebug(string):
    if options.DEBUG:
        print "[DEBUG]: "+str(string)

def printError(string):
    print "[ERROR]: "+str(string)

def printOutput(string, level=0, logfile=''):
    out = ""
    for i in range(level): out +="\t"
    out += " "+string
    print out
    if logfile!='':
        writeLog(logfile, out+'\n')


###given a lfn and an array, retrieves and stores in the array a dictionary like {"node", node_name}
def retrieve_siteList(lfn,entry):
    if len(lfn)<2:
        printError( lfn+" is not a valid LFN")
        exit(1)
    command = """wget --no-check-certificate -O- \"https://cmsweb.cern.ch/phedex/datasvc/xml/prod/FileReplicas?lfn="""+lfn+"""\"  2>/dev/null"""
    out = popen(command)
    init = 0
    for x in out:
        old_x = x
        init = x[init:].find(" node='")
        
        while init!=-1:
            init += len(" node='")
            site = x[init:][:x[init:].find("'")]
            x = x[init:]
            init = x.find(" node='")
                            
            ##this exclude the destination site from the list
            if options.TO_SITE!="" and site.find(options.TO_SITE)!=-1: continue
            
            if site.find("MSS")==-1:
                entry.append({"node":site} )
               

        search_string = " bytes='"
        x = old_x[old_x.find("<file "):]
        init = x.find(search_string)
        while init!=-1:
            init += len(search_string)
            value = x[init:][:x[init:].find("'")]
            size = value
            x = x[init:]
            init = x.find(search_string)

        for y in entry:
            y["size"] = size

        
            

###given a lfn, a site and an array, retrieves and stores in the array a dictionary like {"pfn", value_of_pfn}            
def retrieve_pfn(lfn,site):
    pfn = ""
    #site = entry["node"]
    if len(lfn)<2:
        printError( lfn+" is not a valid LFN")
        exit(1)

    if site=='LOCAL':
        pfn = "file:///"+lfn
    else:
        command = "wget --no-check-certificate -O- \"https://cmsweb.cern.ch/phedex/datasvc/xml/prod/lfn2pfn?node="+site+"&protocol="+PROTOCOL+"&lfn="+lfn+"""\" 2>/dev/null |sed -e \"s/.*pfn='\([^']*\).*/"""+r"\1\n"+"""/\" """
        out = popen(command)
        for x in out:
            pfn = x.strip("\n")
            
    if len(pfn) <1:
        printError( pfn+" is not a valid PFN")      
        exit(1)
                    
    #printDebug(pfn)
    return pfn


### given a lfn and an empty dict, fills the dictionary as:
### {lfn_value:[{"node":node_value,"pfn":pfn_name}, {"node":node_value,"pfn":pfn_name}, ...], {..} }
def retrieve_siteAndPfn(lfn):
    entry = []
    retrieve_siteList(lfn,entry)
    for x in entry:
        x["pfn"] =  retrieve_pfn(lfn,x["node"])
    return entry
                            


### Fill the PREFERRED_SITES and DENIED_SITES arrays
def setBlackWhiteSiteList(options,PREFERRED_SITES, DENIED_SITES  ):
    if options.WHITELIST!="":
        for site in options.WHITELIST.split(","):
            PREFERRED_SITES.append(site)
    if options.BLACKLIST!="":
        for site in options.BLACKLIST.split(","):
            DENIED_SITES.append(site)        


### arrange sources, putting preferred ones before
def arrange_sources(sitelist,PREFERRED_SITES, DENIED_SITES ):
    new_sitelist = []
    notPref_sitelist = []
    for entry in sitelist:
        allowed = True
        for dSite in DENIED_SITES:
            if dSite in entry["node"]:
                allowed = False
                break
        if not allowed:   continue

        preferred=False
        for pSite in PREFERRED_SITES:
            if entry["node"].find(pSite)!=-1:
                new_sitelist.append(entry)
                preferred = True
        if preferred: continue    
        notPref_sitelist.append(entry)

    for entry in notPref_sitelist:
        new_sitelist.append(entry)
    return new_sitelist



def getFileSizeLCG(pfn):
    command = "lcg-ls "+LCG_OPTIONS_COMMON+" -T "+PROTOCOL+" -l "+pfn+" 2>/dev/null | awk '{print $5}'"
    printDebug("Check file size with: " + command)
    out_pipe = popen("lcg-ls "+LCG_OPTIONS_COMMON+" -T "+PROTOCOL+" -l "+pfn+" 2>/dev/null | awk '{print $5}'")
    #print "lcg-ls -l "+pfn+" 2>/dev/null | awk '{print $5}'"
    out = out_pipe.readlines()
    #out_pipe.close()
    for i in out: printDebug("Output: " + i.strip('\n'))
        
    if len(out) == 0:
        size = -1
    else:
        size = out[0].strip("\n")
    return size
#source["size"] = out[0].strip("\n")



###
def createSubdir(lfn, DESTINATION):
    pfn_DESTINATION = ""
    if lfn.find('file:///')!=-1: filename = lfn[ len('file///'):]
    filename = lfn.split("/")[-1]
        
    subdir = ""
    for dir in lfn.split("/")[:-1]:
        subdir += dir+"/"
        
    dir = ""
    for i in DESTINATION.split("/")[:-1]:
        print i
        dir += i+"/"
                    
    pfn_DESTINATION = dir+subdir
    pfn_DESTINATION += filename

    return pfn_DESTINATION



###
def createDestFileName(lfn, options, DESTINATION):
    filename = lfn.split("/")[-1]
    if options.TO_SITE!="":
        new_DESTINATION = ""
        if options.RECREATE_SUBDIRS:
            lfn_dir = ""
            for subdir in lfn.split("/")[:-1]:
                lfn_dir += subdir+"/"
            new_DESTINATION = DESTINATION+lfn_dir
        else:
            new_DESTINATION = DESTINATION
                
        if new_DESTINATION != "":
            pfn_DESTINATION = retrieve_pfn(new_DESTINATION,options.TO_SITE)
            if pfn_DESTINATION[-1] != "/": pfn_DESTINATION+="/"
            pfn_DESTINATION += filename
        else:
            pfn_DESTINATION = retrieve_pfn(lfn,options.TO_SITE)
                    
    else:
        if options.RECREATE_SUBDIRS:
            pfn_DESTINATION = createSubdir(lfn, DESTINATION)
        else:
            pfn_DESTINATION = DESTINATION+filename

    return filename, pfn_DESTINATION


###

def castorStage(castor_pfn, myLog,logfile, tabLevel=2):
    if not os.environ["TMPDIR"]: ##not sure about it
        tmp = "/tmp/"
    else:
        tmp = os.environ["TMPDIR"]
    if tmp[-1]!= "/": tmp += "/"
    
    command = "rfcp "+castor_pfn+" "+tmp
    pipe = os.popen(command)
    exit_status = pipe.close()
    
    filename = castor_pfn.split("/")[-1]
    
    if exit_status == None:
        exit_status = 0

    local_pfn = tmp+filename
    printDebug("CastorStaging: result "+str(local_pfn)+" "+str(exit_status))
    myLog["local-pfn"] = local_pfn
    printOutput( "Castor PFN: "+castor_pfn,tabLevel)
    printOutput( "Local PFN: "+ local_pfn, tabLevel)
    if exit_status != 0:
        myLog["t-done"] = time()
        myLog["report-code"] = exit_status
        stageError = "Castor error "+str(exit_status)+" on file "+castor_pfn
        myLog["detail"] = "" 
        writePhedexLog(myLog,logfile)
        printOutput( "Error: "+stageError,tabLevel)

    return local_pfn, exit_status




def copyFile(tool,copyOptions, source,  dest, srm_prot, myLog, logfile, isStage):

    printDebug("Starting copyFile")

    myLog["from"] = source["node"]
    myLog["to"] = options.TO_SITE
    myLog["from-pfn"] = source["pfn"]
    myLog["to-pfn"] = dest
    myLog["t-assign"] = time()
    myLog["t-export"] = time()
    myLog["t-inxfer"] = time()
    myLog["t-xfer"] = time()
    myLog["size"] = source["size"]
    SUCCESS = -1
    
    if isStage:
        castor_pfn = source["pfn"].split("=")[-1]
        printDebug(castor_pfn)
        local_pfn, stageExit =  castorStage(castor_pfn, myLog,logfile)
        source["pfn"] = "file:///"+local_pfn
    
    error_log = ""
    command = "unset SRM_PATH"
    if tool=="srmcp":
        command += "&& srmcp "+srm_prot+" "+copyOptions+" "+source["pfn"]+" "+dest+ " 2>&1"
    else:
        command += "&& lcg-cp -V cms "+copyOptions+" -T "+PROTOCOL+" -U "+PROTOCOL+" "+source["pfn"]+" "+dest+ " 2>&1"
    printDebug( command )

    if not options.DRYRUN:
        checkFileExist = -1
        ### checking file existance only for SRM destinations
        if dest.find('srm://')!=-1: destSize = getFileSizeLCG(dest)
        else:
            destSize = -1
        ### if no file at dest, copy
        if destSize==-1:
            pipe = popen(command)
            out = pipe.readlines()
            for l in out:
                error_log += l
            exit_status = pipe.close()
        else:
            ## if file at destination is greater, exit with error
            if float(destSize) > float(myLog["size"]):
                SUCCESS = -1
                error_log = "Confused: file at destination ("+destSize+" b) is greater than file at source ("+myLog["size"]+" b), exiting with error"
                printOutput(error_log,2)
                exit_status = 1
            else:
                ###if sizes differ, delete the file at destination
                if float(destSize) <  float(myLog["size"]) and options.DELETE:
                    printOutput("Incomplete transfer found, deleting file at dest", 2, ADMIN_LOGFILE)
                    delCommand = "srmrm "+dest+" 2>&1"
                    pipe = popen(delCommand)
                    out = pipe.readlines()
                    
                    for l in out:
                        error_log += l
                    ### actual copy    
                    pipe = popen(command)
                    out = pipe.readlines()
                    for l in out:
                        error_log += l
                    exit_status = pipe.close()
                ### if nodelete or file has the same size
                else:
                    exit_status = 1
                    error_log = 'File exists on destination.'
                    if float(destSize) <  float(myLog["size"]):
                        error_log += " It seems an incomplete transfer, you may want to try to run with  --delete."
                            
        if exit_status == None and len(error_log.strip(" ").strip("\n"))<1: 
            SUCCESS = 0
        else:
            if exit_status == None:
                exit_status = 1
            exit_status = os.WEXITSTATUS(exit_status)
        
        myLog["t-done"] = time()
        myLog["report-code"] = SUCCESS
        myLog["detail"] = error_log
    else:
        myLog["t-done"] = time()

    ### checking size after transfer
    if SUCCESS == 0:
        if dest.find('file:///')!=-1:
            if not os.path.isfile( dest[len('file:///'):].strip()): myLog["dest size"] = 0
            else: myLog["dest size"] = os.stat( dest[len('file:///'):].strip()).st_size
        else:
            myLog["dest size"] = getFileSizeLCG(dest)

        if  float(myLog["dest size"]) != float(myLog['size']):
            SUCCESS = -1
            myLog["report-code"] = SUCCESS
            error_log += 'Size mismatch: source='+str(myLog['size'])+" dest="+str(myLog['dest size'])
            myLog["detail"] = error_log
        
    if not options.DRYRUN: writePhedexLog(myLog,logfile)
        
    if SUCCESS == 0:
        speed = float(myLog["size"])/((1024*1024)*float(float(myLog["t-done"]) - float(myLog["t-xfer"]) ) )
        writeLog(SUCCESS_LOGFILE,myLog["lfn"]+'\n')
    else:
        speed = 0

    out = "\t\t Elapsed Time: "+str( myLog["t-done"]-myLog["t-assign"] )+ " s\n"    
    out+= "\t\t Speed: "+str(speed)+" MB/s\n"
    out+= "\t\t Success: "+str(SUCCESS)+'\n'
    out+= "\t\t Error: "+parseErrorLog(error_log)

    printOutput(out, 0, ADMIN_LOGFILE)

    if isStage:
        pipe = os.popen("rm "+local_pfn)
        printDebug("CastorStaging: deleted "+local_pfn)
    printDebug("Full Error: "+error_log)
    printDebug("sleeping")
    os.popen("sleep 2")
    
    return SUCCESS,error_log    




def parseErrorLog(error_log):
    new_error_log = ""
    init = error_log.find("failed with error:[")
    if init!=-1:
        end = error_log[init:].find("]")
        short_error_log = error_log[init:init+end]
        if short_error_log != "":
            new_error_log = "("+short_error_log+")"
        else:
            init = error_log.find("srm client error:")
            end = error_log[init:]
            short_error_log = error_log[init:]
        if short_error_log != "":
            new_error_log = "("+short_error_log.replace("\n","")+")"
        else:
            new_error_log = "()"

    init = error_log.find("SRM_FAILURE")
    if init != -1:
        new_error_log = "("+error_log[init:error_log.find("explanation")]+" "+error_log[error_log.find("state"):error_log.find("srm://")]+")"
    else:
        new_error_log = "("+error_log.replace("\n"," ")+")" 
        
    return new_error_log

###
def writePhedexLog(myLog,logfile):
    f_logfile = open(logfile,"a")

    order = ("task",
             "file",
             "from",
             "to",
             "priority",
             "report-code",
             "xfer-code",
             "size",
             "t-expire",
             "t-assign",
             "t-export",
             "t-inxfer",
             "t-xfer",
             "t-done",
             "lfn",
             "from-pfn",
             "to-pfn",
             "detail",
             "validate",
             "job-log")

    myLog["detail"] = parseErrorLog(myLog["detail"])

    if myLog["to"] == "":
        myLog["to"] = "local"
        
    date_pipe = popen("date -d @"+str(time())+" +\"%F %T\"")
    date = date_pipe.readlines()[0].strip("\n")

    log = date+": FileDownload[24130]: xstats: "
    for x in order:
        log += x+"="+str(myLog[x])+" "

    f_logfile.write(log+"\n")
    f_logfile.close()



###
def logTransferHeader(entry, pfn_DESTINATION, logfile=''):
    out = "\n\t Trial from: "+entry["node"]+"--------------\n"
    out += "\t\t From-PFN: "+entry["pfn"]+'\n'
    out += "\t\t To-PFN: "+pfn_DESTINATION+'\n'
    out += "\t\t Size: "+entry["size"] + " bytes ("+str(float(entry['size'])/(1024*1024))+" MB)"
    print out
    if logfile!='':
        writeLog(logfile, out+'\n')






################### BEGIN of MAIN

def data_replica(args, moptions):
    global options
    global DATAREPLICA_LOGFILE,EXISTING_LOGFILE, FAILED_LOGFILE, SUCCESS_LOGFILE, NOREPLICA_LOGFILE, ADMIN_LOGFILE
    options= moptions

    if len(args) == 2: DESTINATION = args[1]
    else: DESTINATION = ""
    
    if options.usePDS and options.FROM_SITE!="":
        print "You can either PhEDEx dataservice query for sites or choose one yourself, not both"
        exit(-1)
        
    if not options.usePDS and options.FROM_SITE=="":
        print "You can either query PhEDEx dataservice for sites or choose one yourself, but at least one..."
        exit(-1)
        
    if options.TO_SITE == "":
        print "WARNING: no dest site given, assuming PFN destination"
        if DESTINATION.find("srm://")==-1 and DESTINATION.find("file://")==-1 :
            printError("PFN destination incorrect, please check. ")
            exit(-1)
                    
        
    if options.TO_SITE != "" and DESTINATION=="":
        if options.Replicate: print "No DESTINATION given, replicating data using lfn2pfn information"
        else:
            print "Full SE replica disabled, please give a destination"
            exit(-1)
            
    if options.TO_SITE == "" and DESTINATION=="":
        print "You need to specify at least --to-site or dest_dir"
        
    if options.RECREATE_SUBDIRS and DESTINATION=="" and  options.usePDS:
        print "If you want to create a exact replica, you do not need --recreate-subdirs. Otherwise, you need to specify a dest_dir"
        exit(-1)
        
    if options.RECREATE_SUBDIRS and options.TO_SITE=="":
        print "--recreate-subdirs does not work without setting --to-site, sorry"
        exit(-1)
        
    if options.CASTORSTAGE:
        if os.environ["HOSTNAME"].find("lxplus")==-1 or (options.FROM_SITE!="T2_CH_CAF" and options.FROM_SITE!="CERN_CASTOR_USER" ):
            print "--castor-stage option works only from a lxplus machine and setting --from-site=T2_CH_CAF or CERN_CASTOR_USER"
            exit(-1)

    if not options.usePDS and (options.WHITELIST!="" or options.BLACKLIST!=""):
        print "Black/white lists make sense only if --discovery is activated, exiting."
        exit(-1)

    ###fill black/white lists
    setBlackWhiteSiteList(options,PREFERRED_SITES, DENIED_SITES)
    
### Log files definition
    myPid = os.getpid() # want to use???
    ### Log files definition
    USER = os.getenv('LOGNAME')
    DATE = popen("date +'%Y%m%d%k%M'").readlines()[0].strip('\n').replace(" ","0")
    splittedLogfile = options.logfile.split(".")
    additionalLogName = ""
    if options.logfile=="data_replica.log": additionalLogName = "-"+USER+"-"+DATE
    DATAREPLICA_LOGFILE = splittedLogfile[-2]+additionalLogName+".log"
    EXISTING_LOGFILE = splittedLogfile[-2]+"_existingList"+additionalLogName+".log"
    FAILED_LOGFILE = splittedLogfile[-2]+"_failedList"+additionalLogName+".log"
    SUCCESS_LOGFILE = splittedLogfile[-2]+"_successList"+additionalLogName+".log"
    NOREPLICA_LOGFILE =splittedLogfile[-2]+"_noReplica"+additionalLogName+".log"
    ADMIN_LOGFILE = "/tmp/data_replica-admin-"+USER+"-"+DATE+'.log'

    print """\n##########################################
    Welcome to the DataReplica service
    from PSI/ETHZ with love
##########################################\n"""

    print "Preferred Sites: ",PREFERRED_SITES
    print "Denied Sites: ", DENIED_SITES

    ### checks existance of proxy
    pipe = os.popen("voms-proxy-info")
    if pipe.close()!=None:
        print "Please create a voms-proxy before using this program: voms-proxy-init -voms cms"
        exit(-1)

    proxy_timeleft = os.popen("voms-proxy-info -timeleft").readlines()
    if int(proxy_timeleft[0]) < 3600:
        print "Your proxy will last for less than an hour, please renew it with: voms-proxy-init -voms cms"
        exit(-1)
    else:
        print "Your proxy will last "+str( round( float(proxy_timeleft[0])/3600,1) )+" hours, if you think you'll need more time please renew it."

    printDebug("phedex-like logfile: "+ DATAREPLICA_LOGFILE)

    counter = 0

    if not os.path.isfile(args[0]):
        print "[ERROR] List file is not a file!"
        exit(-1)

    #writing header in admin logfile
    writeLog(ADMIN_LOGFILE,'PID: '+str(myPid)+'\n')
    writeLog(ADMIN_LOGFILE,'User: '+USER+'\nDate: '+DATE+'\n')
    writeLog(ADMIN_LOGFILE,'Options: '+str(options)+'\n')
    writeLog(ADMIN_LOGFILE,'Filelist:\n')

    list = open(args[0])
    total_files=0
    for x in list.readlines():
        if x[0]=="#": continue #forget about lines starting with #
        if x!='\n':
            total_files += 1
            writeLog(ADMIN_LOGFILE,x)
    list.seek(0)
    os.popen("sleep 5")

    copyOptions = ""
    ### lcg-utils version check
    if options.TOOL=='lcg-cp':
        pipe = os.popen('lcg-cp --version | grep lcg_util')
        out = pipe.readlines()[0]
        pipe.close()
        splitOut = out.split('-')
        if len(splitOut)>1:
            version = splitOut[1].split('.')[0]+'.'+splitOut[1].split('.')[1]#+splitOut[1].split('.')[2]
            ### valid only for 1.X versions
            version = version.split('.')[1]
            version = float(version)
            
        printDebug("LCG-UTILS version: "+ str(version))
        if version >= 7: copyOptions = LCG_OPTIONS_17
        #elif version >= 1.11: copyOptions = LCG_OPTIONS_1_11
        else:  copyOptions = LCG_OPTIONS
    elif options.TOOL=='srmcp':
        copyOptions = SRM_OPTIONS

    failedTransfers = 0
    SUCCESS = 1
    list.seek(0)
    for lfn in list.readlines():
        if lfn[0]=="#": continue #forget about lines starting with #
        
        lfn = lfn.strip("\n").strip(" ").strip("\t")

        printDebug("LFN: "+lfn)
        SUCCESS = 1

        if lfn!= "":
            counter +=1
            printOutput("\n### Copy process of file "+str(counter)+"/"+str(total_files)+": "+ lfn, 0, ADMIN_LOGFILE )

            printOutput( "Using PhEDEx Data Service for Discovery: "+str(options.usePDS),1, ADMIN_LOGFILE )
            if str(options.TO_SITE)=="":
                printOutput("To site: LOCAL",1, ADMIN_LOGFILE)
            else:
                printOutput("To site: "+str(options.TO_SITE),1, ADMIN_LOGFILE)


            myLog = {"task":"1","file":"1","from":"","to":"",
                     "priority":"3", "report-code":"","xfer-code":"", "size":0,
                     "t-expire":9999999999, "t-assign":"","t-export":"","t-inxfer":"",
                     "t-xfer":"","t-done":"","lfn":"","from-pfn":"","to-pfn":"",
                     "detail":"","validate":"()","job-log":"none"}

            myLog["lfn"] = lfn

            if options.usePDS:
                filelist = retrieve_siteAndPfn(lfn)

            if DESTINATION != "":
                if DESTINATION[-1] != "/": DESTINATION+="/"
            else:
                printOutput( "Recreating the whole tree to "+options.TO_SITE,1,ADMIN_LOGFILE)

            ### creating the destination PFN
            filename, pfn_DESTINATION = createDestFileName(lfn, options, DESTINATION)
            ### local dest check
            if pfn_DESTINATION.find("file:/")!=-1 and  pfn_DESTINATION.find("file:////")==-1:
                 printOutput( "Error in local destination, must be e.g. in this form: file:////tmp/",1,ADMIN_LOGFILE)
                 exit(1)
            srm_prot = ""
            if PROTOCOL == "srmv2": srm_prot = "-2"

            isFileAtSource = True  ## keeps track if the file exist at source

            ###Special case for user dir on castor
            ### file list is supposed to be in the form /castor/ (PFN)
            if ( options.FROM_SITE=='CERN_CASTOR_USER' or options.FROM_SITE=='T2_CH_CAF' ) and options.CASTORSTAGE:
                    local_pfn, exitStatus = castorStage(lfn,  myLog, DATAREPLICA_LOGFILE,1)
                    if exitStatus !=0 :  continue
                    entry = {"pfn":"file:///"+local_pfn,"node":options.FROM_SITE}
                    entry["size"] = popen("rfdir "+lfn+" | awk '{print $5}'").readlines()[0].strip("\n")
                
                    logTransferHeader(entry, pfn_DESTINATION, ADMIN_LOGFILE)                        
                    SUCCESS, error_log = copyFile(options.TOOL,copyOptions, entry, pfn_DESTINATION, srm_prot, myLog,DATAREPLICA_LOGFILE, False)
                    pipe = os.popen("rm "+local_pfn)
                    printDebug("CastorStaging: deleted "+local_pfn)
                    
            elif options.usePDS:
                sources_list = arrange_sources(filelist,PREFERRED_SITES,  DENIED_SITES )
                if sources_list == []:
                    printOutput( "ERROR: no replicas found",0,ADMIN_LOGFILE)
                    isFileAtSource=False
                    writeLog(NOREPLICA_LOGFILE,lfn+"\n")
                    #continue
    
                for entry in sources_list:
                    logTransferHeader(entry, pfn_DESTINATION, ADMIN_LOGFILE)
                    SUCCESS, error_log = copyFile(options.TOOL,copyOptions, entry, pfn_DESTINATION, srm_prot, myLog,DATAREPLICA_LOGFILE, options.CASTORSTAGE)
                    if SUCCESS == 0:  break
                    elif error_log.lower().find("file exist")!=-1:  break
                

            else:
                if options.FROM_SITE=='CERN_CASTOR_USER':
                    pfn = CERN_CASTOR_SRM+lfn
                elif options.FROM_SITE=='CERN_EOS':
                    pfn = CERN_EOS_SRM+lfn
                else:
                    pfn = retrieve_pfn(lfn,options.FROM_SITE)
                printDebug("PFN:"+ pfn)
                source = {"pfn":pfn,"node":options.FROM_SITE}

                if options.FROM_SITE!='LOCAL':
                    source["size"] =  getFileSizeLCG(pfn )#out[0].strip("\n")
                    if source["size"]==-1:
                        printOutput( "[ERROR] file does not exist on source: "+pfn, 0, ADMIN_LOGFILE)
                        isFileAtSource=False
                        writeLog(NOREPLICA_LOGFILE,myLog["lfn"]+'\n')
                        #continue
                else:
                    ###Using lfn, as in this case is the full path
                    if not os.path.isfile(lfn):
                        printOutput( "[ERROR] file does not exist on source",0,ADMIN_LOGFILE)
                        writeLog(NOREPLICA_LOGFILE,myLog["lfn"]+'\n')
                        isFileAtSource=False
                        #continue
                    source["size"] = str(os.path.getsize(lfn))
                
                if isFileAtSource:    
                    logTransferHeader(source,pfn_DESTINATION, ADMIN_LOGFILE)
                    SUCCESS, error_log = copyFile(options.TOOL, copyOptions, source, pfn_DESTINATION, srm_prot, myLog, DATAREPLICA_LOGFILE, options.CASTORSTAGE)
                else:
                    SUCCESS=1

            if SUCCESS != 0:
                if myLog['detail'].lower().find('file exist')!=-1:
                    writeLog(EXISTING_LOGFILE,lfn+" "+myLog['to-pfn']+"\n")
                elif myLog['detail'].find('file does not exist')==-1 and myLog['detail'].find('no replicas')==-1:
                ### does not consider existing file as error...
                    writeLog(FAILED_LOGFILE,lfn+"\n")
                    failedTransfers+=1
                else:
                    failedTransfers+=1   

                        
    print "Returned code "+str(failedTransfers)
    return failedTransfers


if __name__ == "__main__":
    data_replica(args, moptions)



    
