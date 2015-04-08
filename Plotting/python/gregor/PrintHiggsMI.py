import pickle
from HiggsTaggingVariables import *




for v08, v15 in zip(mass_vars_ak08_v10, mass_vars_ca15_v10):
    
    print v08.pretty_name.replace("AK (R=0.8) ",""), ";",


    for input_filename in ["MIPickle/mass_vars_ak08_v10_pt-170-to-300_mi.pickle",
                           "MIPickle/mass_vars_ca15_v10_pt-170-to-300_mi.pickle",
                           "MIPickle/mass_vars_ak08_v10_pt-300-to-470_mi.pickle",
                           "MIPickle/mass_vars_ca15_v10_pt-300-to-470_mi.pickle",
                           "MIPickle/mass_vars_ak08_v10_pt-470-to-600_mi.pickle",
                           "MIPickle/mass_vars_ca15_v10_pt-470-to-600_mi.pickle",
                           "MIPickle/mass_vars_ak08_v10_pt-600-to-800_mi.pickle",
                           "MIPickle/mass_vars_ca15_v10_pt-600-to-800_mi.pickle"]:
    
    
        f = open(input_filename, "r")    
        m = pickle.load(f)

        if "ca15" in input_filename:
            print "{0:0.2f}".format(m[v15.name][v15.name]),";",
        elif "ak08" in input_filename:
            print "{0:0.2f}".format(m[v08.name][v08.name]),";",
    print 

    #for var in vars:
    #    print input_filename, var.pretty_name, 
    #    
    #    
    #        print "{0} {1:.2f} {2:.2f}".format(key, m[key][key],v)
