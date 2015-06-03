import sys, os, shutil
from grid_control import ConfigError, RethrowError, Job, utils
from grid_control.backends import WMS, LocalWMS

class JMS(LocalWMS):

	_statusMap = {		# dictionary mapping vanilla condor job status to GC job status
		#'0' : Job.WAITING	,# unexpanded (never been run)
		"PENDING" : Job.WAITING	,# idle (waiting for a machine to execute on)
		"RUNNING" : Job.RUNNING	,# running
		"COMPLETED" : Job.DONE	,# running
		"COMPLETING" : Job.DONE	,# running
		"CANCELLED+" : Job.ABORTED	,# removed
		"CANCELLED" : Job.ABORTED	,# removed
		#'5' : Job.WAITING	,#DISABLED	,# on hold
		"FAILED" : Job.FAILED	,# submit error
		}

	#_statusMap = { 's': Job.QUEUED, 'r': Job.RUNNING, 'CG': Job.DONE, 'w': Job.WAITING }

	def __init__(self, config, wmsName = None):
		LocalWMS.__init__(self, config, wmsName,
			submitExec = utils.resolveInstallPath('sbatch'),
			statusExec = utils.resolveInstallPath('sacct'),
			cancelExec = utils.resolveInstallPath('scancel'))


	def unknownID(self):
		return 'not in queue !'


	def getJobArguments(self, jobNum, sandbox):
		return repr(sandbox)


	def getSubmitArguments(self, jobNum, jobName, reqs, sandbox, stdout, stderr):
		# Job name
		params = ' -J "%s"' % jobName
		# Job requirements
		#if WMS.QUEUES in reqs:
		#	params += ' -c %s' % reqs[WMS.QUEUES][0]
		#if self.checkReq(reqs, WMS.WALLTIME):
		#	params += ' -T %d' % ((reqs[WMS.WALLTIME] + 59) / 60)
		#if self.checkReq(reqs, WMS.CPUTIME):
		#	params += ' -t %d' % ((reqs[WMS.CPUTIME] + 59) / 60)
		#if self.checkReq(reqs, WMS.MEMORY):
		#	params += ' -m %d' % reqs[WMS.MEMORY]
		# processes and IO paths
		params += ' -o "%s" -e "%s"' % (stdout, stderr)
		if WMS.QUEUES in reqs:
			params += ' -p %s' % reqs[WMS.QUEUES][0]

		return params


	def parseSubmitOutput(self, data):
		# job_submit: Job 121195 has been submitted.
		return int(data.split()[3].strip())

	def parseStatus(self, status):
		#for s in status:
		for jobline in str.join('', list(status)).split('\n'):
			if jobline == '':
				continue

			jobinfo = dict()

			jl = jobline.split()
			#print("jobline=", jl)

			#squeue
			### try:
			### 	jobinfo["id"] = "%d" % int(jl[0])
			### 	jobinfo["status"] = str(jl[1])
			### except Exception:
			### 	print "unable to parse id", jl
			### 	continue
			if not jl[5] in self._statusMap.keys():
				#print "unable to parse status=", jl[5]
				continue

			jobinfo["id"] = str(int(jl[0]))
			jobinfo["queue"] = jl[2]
			jobinfo["status"] = jl[5]
			#print("jobinfo=", jobinfo)
			yield jobinfo


	def getCheckArguments(self, wmsIds):
		#squeue
		#return '-ho %%i,%%T -j %s' % str.join(',', wmsIds)
		#sacct
		a = '-n -j %s' % str.join(',', wmsIds)
		#print a
		return a


	def getCancelArguments(self, wmsIds):
		return str.join(' ', wmsIds)


class SLURM(JMS):
	pass
