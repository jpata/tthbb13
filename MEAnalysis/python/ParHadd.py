#!/usr/bin/env python
"""
ParHadd.py uses parallelization and multiple steps to merge large amounts of ROOT files.
Usage:
	./ParHadd.py output_file.root input_file1.root input_file2.root ...
	See also ./ParHadd.py --help

Example call:
    python ParHadd.py --njobs=5 --nfiles=10 --nsteps=2 /scratch/jpata/QCD_HT500to700_v14.root /shome/nchernya/Hbb/skim_trees/v14/QCD_HT500to700_v14/skimmed*.root

Author: Joosep Pata (ETHz) joosep.pata@cern.ch
"""

import argparse
from multiprocessing import Pool
import ROOT
import subprocess
import os

from TTH.MEAnalysis.Helpers import chunks

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--njobs',
	type=int,
	default=5,
	help="Number of concurrent jobs"
)

parser.add_argument('--nfiles',
	type=int,
	default=250,
	help="Number of files per job"
)

parser.add_argument('--nsteps',
	type=int,
	default=2,
	help="Number of successive merge steps"
)

parser.add_argument('--tempdir',
	type=str,
	default="/scratch/" + os.environ["USER"] + "/",
	help="Temporary directory for output files"
)

#parser.add_argument('--verbose', '-v', action='count')
pargs, remaining_args = parser.parse_known_args()

def hadd(args):
	""" Uses hadd to merge ROOT files.

	Args:
		args (tuple): a 2-element tuple (outfile, infiles), where outfile is a str
			and infiles is a list of strs with the paths to the files

	Returns:
		str: Path to output file

	Raises:
		Exception if call to merge failed.
	"""
	outfile = args[0]
	infiles = args[1]
	print "merging {0} files -> {1}".format(len(infiles), outfile)
	cmd = ["hadd", "-f", outfile] + infiles
	print " ".join(cmd)
	ret = subprocess.call(cmd)
	if ret != 0:
		raise Exception("could not merge {0}".format(outfile))
	return outfile



def chunked_step(pool, infiles, index, nchunks=20, delete_inputs=False):
	""" Runs a merge step over a list of files using parallelization.

	Args:
		pool (multiprocessing.Pool): an instance of Pool which is used
			for parallelization.
		infiles (list of strs): list of paths to input files.
		index (int): the index of this merge step, used to name the temp files.
		nchunks (int, optional): specifies how many files per one hadd command to use.
		delete_inputs (bool, optional): if True, input files are deleted after a successful merge.

	Returns:
		list of strs: the output files from hadd.
	"""
	args = []
	i = 0
	for ch in chunks(infiles, nchunks):
		args += [("{0}/s{1}_{2}.root".format(pargs.tempdir, index, i), ch)]
		i += 1
	ret = pool.map(hadd, args)
	if delete_inputs:
		print "deleting inputs"
		for infile in infiles:
			os.remove(infile)
	return ret

def par_hadd(outfile, infiles, nchunks, njobs, nsteps):
	print "Adding {0} files to outfile {1}".format(len(infiles), outfile)
	pool = Pool(processes=njobs)

	of = infiles
	for i in range(nsteps):
		print "step {0} running over {1} files".format(i, len(of))
		of = chunked_step(pool, of, i, nchunks=nchunks, delete_inputs=i>0)
		if len(of)==1:
			break
	pool.close()
	hadd((outfile, of))

if __name__ == "__main__":
	outfile = remaining_args[0]
	infiles = remaining_args[1:]
	par_hadd(outfile, infiles, pargs.nfiles, pargs.njobs, pargs.nsteps)
