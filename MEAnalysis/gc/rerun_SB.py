#!/usr/bin/env python
"""
Thomas:

"""

########################################
# Imports
########################################

import subprocess
import os
import shutil
import re
import gzip
from time import sleep
import time
import datetime


########################################
# Functions
########################################

def Create_Error_Report( workdir ):

    n_specific_prints = 0

    dirs = os.listdir( 'work.{0}/output/'.format(workdir) )

    out_f = open( 'Errors-{0}.txt'.format(workdir) , 'w' )

    for jobdir in dirs:

        stdout_filename = 'work.{0}/output/{1}/job.stderr.gz'.format(workdir,jobdir)

        if not os.path.isfile( stdout_filename ):
            continue

        out_f.write( '\nERROR IN {0}\n=================\n'.format(jobdir) )

        f = gzip.open(stdout_filename, 'rb')
        out_f.write( f.read() )
        f.close()

    out_f.close()


########################################
# Main
########################################

def main():

    key_list = [ 'sig', 'bkg' ]
    #key_list = [ 'sig' ]
    #key_list = [ 'bkg' ]


    start_time = time.time()

    gopy = 'grid-control/go.py'

    submitcmd   = { 'sig' : [ gopy , 'confs/sig-psi.conf', '-q' ] ,
                    'bkg' : [ gopy , 'confs/bkg-psi.conf', '-q' ] }

    statuscmd   = { 'sig' : [ gopy , 'confs/sig-psi.conf', '-qs' ],
                    'bkg' : [ gopy , 'confs/bkg-psi.conf', '-qs' ] }

    retrievecmd = { 'sig' : [ gopy , 'confs/sig-psi.conf', '-r' ],
                    'bkg' : [ gopy , 'confs/bkg-psi.conf', '-r' ] }

    # Delete currently existing jobs
    subprocess.call( [ 'qdel', '-u', 'tklijnsm' ] )

    for key in key_list:
        # Remove the work.sig directory
        if os.path.isdir('work.{0}'.format(key)):
            print 'Removing work.{0}'.format(key)
            shutil.rmtree('work.{0}'.format(key))

    # Submit jobs
    for k in key_list:
        print 'Submitting jobs ({0})'.format(k)
        subprocess.call( submitcmd[k] , stdout=open(os.devnull, 'wb') )

    n_success = {}
    n_running = {}
    n_queued  = {}
    p_success = {}

    # Check status repeatedly - detect 100% success rate to stop repeating
    n_limit_checks = 450

    for i_check in range(n_limit_checks):

        for k in key_list:

            print 'Checking {0} status (call {1})'.format( k, i_check )

            subprocess.call( statuscmd[k], stdout=open(os.devnull, 'wb'))

            output = subprocess.Popen(
                retrievecmd[k], stdout=subprocess.PIPE ).communicate()[0]

            match = re.search( r'FAILED:\s*\d+\s*(\d+)', output )
            if int(match.group(1)) > 0:
                print 'There was a failed job. '\
                    'See error report in Errors-{0}.txt'.format(k)
                Create_Error_Report(k)
                return 0
            
            match = re.search( r'SUCCESS:\s*(\d+)\s*(\d+)', output )
            n_success[k] = match.group(1)
            p_success[k] = int(match.group(2))

            match = re.search( r'RUNNING:\s*(\d+)\s*(\d+)', output )
            n_running[k] = match.group(1)

            match = re.search( r'QUEUED:\s*(\d+)\s*(\d+)', output )
            n_queued[k] = match.group(1)

            print '    Running: {0:4s} , Queued: {1:4s} , Finished: {2:4s}'.format(
                n_running[k], n_queued[k], n_success[k] )

        run_finished = True
        for key in key_list:
            if not p_success[key] == 100:
                run_finished = False

        if run_finished: break
        else: sleep(120)



    end_time = time.time()
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
    end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
    print 'Started run on: {0}'.format( start_time_str )
    print 'Ended run on:   {0}'.format( end_time_str )
    print 'Duration:       {0} seconds'.format( end_time - start_time )



########################################
# End of Main
########################################
if __name__ == "__main__":
    main()
