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
from CreateStatisticsReport import Create_Single_sig_Report
from time import sleep


########################################
# Functions
########################################

def Create_Error_Report( workdir ):

    n_specific_prints = 0

    dirs = os.listdir( 'work.{0}/output/'.format(workdir) )

    out_f = open( 'AllErrors-{0}.txt'.format(workdir) , 'w' )

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

    gopy = 'grid-control/go.py'

    submitcmd   = [ gopy , 'confs/sig-psi.conf', '-q' ]
    statuscmd   = [ gopy , 'confs/sig-psi.conf', '-qs' ]
    retrievecmd = [ gopy , 'confs/sig-psi.conf', '-r' ]


    # Delete currently existing jobs
    subprocess.call( [ 'qdel', '-u', 'tklijnsm' ] )

    # Remove the work.sig directory
    if os.path.isdir('work.sig'):
        print 'Removing work.sig'
        shutil.rmtree('work.sig')

    # Submit the jobs
    print 'Submitting jobs'
    subprocess.call( submitcmd, stdout=open(os.devnull, 'wb') )

    # Check status repeatedly - detect 100% success rate to stop repeating
    n_limit_checks = 150
    for i_check in range(n_limit_checks):

        print 'Checking status (call {0})'.format(i_check)

        subprocess.call( statuscmd, stdout=open(os.devnull, 'wb'))

        output = subprocess.Popen( retrievecmd, stdout=subprocess.PIPE ).communicate()[0]

        match = re.search( r'FAILED:\s*\d+\s*(\d+)', output )
        if int(match.group(1)) > 0:
            print 'There was a failed job. Check work.*/output/job*/stderr.gz to debug'
            Create_Error_Report( 'sig' )
            return 0
        
        match = re.search( r'SUCCESS:\s*(\d+)\s*(\d+)', output )
        n_success = match.group(1)
        p_success = int(match.group(2))

        match = re.search( r'RUNNING:\s*(\d+)\s*(\d+)', output )
        n_running = match.group(1)

        match = re.search( r'QUEUED:\s*(\d+)\s*(\d+)', output )
        n_queued = match.group(1)

        print '    Running: {0:4s} , Queued: {1:4s} , Finished: {2:4s}'.format(
            n_running, n_queued, n_success )

        if p_success == 100:
            print 'Jobs completed'
            break
        else:
            sleep(120)

    print 'Creating statistics reports'
    Create_Single_sig_Report()




########################################
# End of Main
########################################
if __name__ == "__main__":
    main()
