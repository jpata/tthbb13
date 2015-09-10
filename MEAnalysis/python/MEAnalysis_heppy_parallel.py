#!/usr/bin/env python
from MEAnalysis_heppy import *
import sys

i = int(sys.argv[1])
inputSamples, samples = prepareInputSamples("python/samples_small.py")

if __name__ == "__main__":
    #print "processing sample ", samp
    samp = inputSamples[i]
    config = cfg.Config(
        #Run across these inputs
        components = [samp],

        #Using this sequence
        sequence = sequence,

        #save output to these services
        services = [output_service],

        #This defines how events are loaded
        events_class = Events
    )

    #Configure the number of events to run
    from PhysicsTools.HeppyCore.framework.looper import Looper
    looper = Looper(
        'Loop_{0}'.format(samp.name),
        config,
        nPrint = 0,
        firstEvent=0,
        nEvents=10000000
    )

    #execute the code
    looper.loop()

    tf = looper.setup.services["outputfile"].file 
    tf.cd()
    ts = ROOT.TNamed("config", conf_to_str(Conf))
    ts.Write("", ROOT.TObject.kOverwrite)
    
    #write the output
    looper.write()
