#!/usr/bin/env python
"""
Thomas:

Retrieves the statistics from individual in job.stdout.gz files.

"""

########################################
# Imports
########################################

import re
import os
import gzip

from operator import add

########################################
# Functions
########################################

def Create_Statistics_Report( workdir, outdir, out_f_name = 'None', verbose = True ):


    ########################################
    # Fill the dict
    ########################################

    dirs = os.listdir( 'work.{0}/output/'.format(workdir) )

    key_list = []

    for jobdir in dirs:

        stdout_filename = 'work.{0}/output/{1}/job.stdout.gz'.format(workdir,jobdir)

        if not os.path.isfile( stdout_filename ):
            if verbose: print '{0} does not exist (yet)'.format( stdout_filename )
            continue

        f = gzip.open(stdout_filename, 'rb')
        full_out = f.read()
        f.close()


        begin_match = re.search( r'Statistics\n==========', full_out )
        end_match = re.search( r'==========\nEnd of Statistics', full_out )
        
        if not begin_match or not end_match:
            if verbose: print 'Could not find Statistics'
            return

        begin_text = begin_match.end()
        end_text = end_match.start()

        report = full_out[ begin_text : end_text ]

        # Get the key_list, runs just once
        if key_list == []:

            # Create the key_list
            key_matches = re.finditer( r'([\w\+]+)\s+=\s\d+', report )

            for key_match in key_matches:

                key = key_match.group(1)

                if report[key_match.end()] == ')':
                    key_list.append('#' + key)
                else:
                    key_list.append(key)

            # Initialize the stat_dict
            stat_dict = {}
            for key in key_list:
                if key[0] == '#':
                    stat_dict[key[1:]] = 0
                else:
                    stat_dict[key] = 0


        key_matches = re.findall( r'([\w\+]+)\s+=\s(\d+)', report )

        for (key, value) in key_matches:
            stat_dict[key] += int(value)
        

    ########################################
    # Write the dict
    ########################################

    out_f = open( '{0}/{1}'.format(outdir,out_f_name) , 'w' )

    for key in key_list:

        if key[0] == '#':
            if verbose: print '  ({0:25s} = {1})'.format( key[1:], stat_dict[key[1:]] )
            out_f.write( '  ({0:25s} = {1})\n'.format( key[1:], stat_dict[key[1:]]))
        else:
            if verbose: print '{0:30s} = {1}'.format( key, stat_dict[key] )
            out_f.write( '{0:30s} = {1}\n'.format( key, stat_dict[key] ) )

    out_f.close()



def Create_Match_Tree_Report( workdir, outdir, out_f_name, verbose = True ):

    ########################################
    # Fill the dict
    ########################################

    dirs = os.listdir( 'work.{0}/output/'.format(workdir) )

    # Just make big enough
    numbers = [ 0 for i in range(1000) ]

    for jobdir in dirs:

        stdout_filename = 'work.{0}/output/{1}/job.stdout.gz'.format(workdir,jobdir)

        if not os.path.isfile( stdout_filename ):
            if verbose: print '{0} does not exist (yet)'.format( stdout_filename )
            continue

        f = gzip.open(stdout_filename, 'rb')
        full_out = f.read()
        f.close()

        begin_match = re.search( r'Match Trees\n==========', full_out )
        end_match = re.search( r'==========\nEnd of Match Trees', full_out )
        
        if not begin_match or not end_match:
            if verbose: print 'Could not find Match Trees'
            return

        begin_text = begin_match.end()
        end_text = end_match.start()

        report = full_out[ begin_text : end_text ]

        numbers_thisjob = re.findall( r'\D(\d)+\D', report )

        numbers = [ int(i)+j for (i,j) in zip( numbers_thisjob, numbers ) ]

    f = open( '{0}/{1}'.format(outdir,out_f_name) , 'w' )
    Write_Tree( numbers, 'b', f )
    Write_Tree( numbers[16:], 'l', f )
    Write_Tree( numbers[32:], 'total', f )
    f.close()



def Write_Tree( numbers, particle, f ):

    f.write( '\nPrinting match tree {0}\n'.format( particle ) )
    f.write( '====================\n' )
    f.write( '  Total count           = {0}\n'.format( numbers[0] ) )
    f.write( '  Total passable to MEM = {0}\n\n'.format( numbers[1] ) )

    f.write( '|{0:13s}|{1:10s}|{2:13s}|{3:10s}|{4:13s}|{5:10s}|\n'.format(
        'Jet to Qrk',
        '',
        'Subj to Qrk',
        '',
        'Jet to Subj',
        '',
        ) )

    f.write( '|-------------+----------+-------------+----------+-------------+----------|\n' )

    f.write( '|{0:13s}|{1:10s}|{2:13s}|{3:10s}|{4:13s}|{5:10s}|\n'.format(
        'Success',
        str( numbers[2] ),
        'Success',
        str( numbers[3] ),
        'Success',
        str( numbers[4] ),
        ) )


    f.write( '|{0:13s}|{1:10s}|{2:13s}|{3:10s}|{4:13s}|{5:10s}|\n'.format(
        '',
        '',
        '',
        '',
        'Failed',
        str( numbers[5] ),
        ) )

    f.write( '|             |          |-------------+----------+-------------+----------|\n' )

    f.write( '|{0:13s}|{1:10s}|{2:13s}|{3:10s}|{4:13s}|{5:10s}|\n'.format(
        '',
        '',
        'Failed',
        str( numbers[6] ),
        'Success',
        str( numbers[7] ),
        ) )

    f.write( '|{0:13s}|{1:10s}|{2:13s}|{3:10s}|{4:13s}|{5:10s}|\n'.format(
        '',
        '',
        '',
        '',
        'Failed',
        str( numbers[8] ),
        ) )

    f.write( '|-------------+----------+-------------+----------+-------------+----------|\n' )

    f.write( '|{0:13s}|{1:10s}|{2:13s}|{3:10s}|{4:13s}|{5:10s}|\n'.format(
        'Failed',
        str( numbers[9] ),
        'Success',
        str( numbers[10] ),
        'Success',
        str( numbers[11] ),
        ) )


    f.write( '|{0:13s}|{1:10s}|{2:13s}|{3:10s}|{4:13s}|{5:10s}|\n'.format(
        '',
        '',
        '',
        '',
        'Failed',
        str( numbers[12] ),
        ) )

    f.write( '|             |          |-------------+----------+-------------+----------|\n' )

    f.write( '|{0:13s}|{1:10s}|{2:13s}|{3:10s}|{4:13s}|{5:10s}|\n'.format(
        '',
        '',
        'Failed',
        str( numbers[13] ),
        'Success',
        str( numbers[14] ),
        ) )

    f.write( '|{0:13s}|{1:10s}|{2:13s}|{3:10s}|{4:13s}|{5:10s}|\n'.format(
        '',
        '',
        '',
        '',
        'Failed',
        str( numbers[15] ),
        ) )

    f.write( '----------------------------------------------------------------------------\n' )





def Create_Specific_Print_Report( workdir, outdir, out_f_name, verbose = True ):

    ########################################
    # Fill the dict
    ########################################

    n_specific_prints = 0

    work_output_dir = 'work.{0}/output/'.format(workdir)
    dirs = os.listdir( work_output_dir )

    out_f = open( '{0}/{1}'.format(outdir,out_f_name) , 'w' )


    for jobdir in dirs:

        stdout_filename = '{0}/{1}/job.stdout.gz'.format(work_output_dir,jobdir)

        if not os.path.isfile( stdout_filename ):
            if verbose:
                print '{0} does not exist (yet)'.format( stdout_filename )
            continue

        f = gzip.open(stdout_filename, 'rb')
        full_out = f.read()
        f.close()

        begin_matches = re.finditer( r'Specific Print\n==========', full_out )
        end_matches = re.finditer( r'==========\nEnd of Specific Print', full_out )
        
        if not begin_matches or not end_matches:
            #out_f.write( 'Could not find Specific Print\n\n' )
            continue


        for (begin_match, end_match) in zip( begin_matches, end_matches):

            n_specific_prints += 1

            out_f.write( 'Specific Print number {0} in {1} ({2})\n'.format(
                n_specific_prints, jobdir, workdir) )
            out_f.write( '====================\n' )

            begin_text = begin_match.end()
            end_text = end_match.start()

            specific_print = full_out[ begin_text : end_text ]

            out_f.write( specific_print )
            out_f.write( '\n' )

    out_f.write( 'Total specific prints found in {0}: {1}'.format(
        workdir, n_specific_prints ) )



def Create_sig_Report( outdir, i_iter ):

    outdirs = [ '{0}/Statistics'.format(outdir),
                '{0}/Match_Trees'.format(outdir),
                '{0}/Specific_Prints'.format(outdir) ]

    for outdir in outdirs:

        if not os.path.isdir( outdir ):
            os.makedirs( outdir )
            continue

        if i_iter == 0:
            contents = os.listdir(outdir)
            for content in contents:
                os.remove( outdir + '/' + content)
            

    Create_Statistics_Report( 'sig', outdirs[0],
        'Statistics{0}.txt'.format(i_iter), False )

    Create_Match_Tree_Report( 'sig', outdirs[1],
        'Match_Tree{0}.txt'.format(i_iter), False )

    Create_Specific_Print_Report( 'sig', outdirs[2],
        'Specific_Print{0}.txt'.format(i_iter), False )


def Create_Single_sig_Report():

    outdir = 'Reports'

    if not os.path.isdir( outdir ):
        os.makedirs( outdir )

    Create_Statistics_Report( 'sig', outdir,
        'Statistics_sig.txt', False )

    Create_Match_Tree_Report( 'sig', outdir,
        'Match_Tree_sig.txt', False )

    Create_Specific_Print_Report( 'sig', outdir,
        'Specific_Print_sig.txt', False )




########################################
# End of Main
########################################
if __name__ == "__main__":
    Create_Single_sig_Report()
