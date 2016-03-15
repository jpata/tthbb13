
import os
import sys
import pdb
import glob
import pickle


#params = ["n_layers", "n_nodes", "dropout", "lr", "decay", "momentum", "nb_epoch"]
params = ["n_blocks", "n_conv_layers", "conv_nfeat", "conv_size", "pool_size", "n_dense_layers", "n_dense_nodes", "lr", "decay", "momentum" , "nb_epoch"]


if not len(sys.argv) == 2:
    print "Invalid number of arguments"
    print "Usage: {0} path_to_check".format(sys.argv[0])
    sys.exit()

path_to_check = sys.argv[1]

di = {}

#print os.path.join(path_to_check, "*")

if False:
    for subdir in glob.glob(os.path.join(path_to_check, "*")):

        name = os.path.basename(subdir)
        print name

        fn_env = os.path.join(subdir, "env.txt")
        fn_valacc = os.path.join(subdir, "valacc.txt")
        fn_maxvalacc = os.path.join(subdir, "maxvalacc.txt")
        fn_delacc = os.path.join(subdir, "deltaacc.txt")

        di[name] = {}
        di[name]["name"] = name

        f = open(fn_valacc)
        di[name]["valacc"] = float(f.read().strip())
        f.close()

        f = open(fn_maxvalacc)
        di[name]["maxvalacc"] = float(f.read().strip())
        f.close()

        f = open(fn_delacc)
        di[name]["delacc"] = float(f.read().strip())
        f.close()


        f = open(fn_env)
        for line in f:
            line = line.strip()
            line_atoms = line.split("=")
            if line_atoms[0] in params:
                di[name][line_atoms[0]] = float(line_atoms[1])
        f.close()

#f = open(os.path.join(path_to_check, "summary.pickle"), "wb")
#pickle.dump(di, f)
#f.close()

f = open(os.path.join(path_to_check, "summary.pickle"), "r")
di = pickle.load(f)
f.close()

def pretty_print(d):
    fields = [ "valacc", "maxvalacc", "delacc"] + params    
    n_fields = len(fields)
    
    form_string = " ".join(["{" + str(i) + ": <12.4" + "}" for i in range(n_fields)])
    vals =  [float(d[f]) for f in fields]


    
    return form_string.format(*vals)


fields = ["maxvalacc", "valacc", "delacc"] + params    
n_fields = len(fields)
form_string = " ".join(["{" + str(i) + ": <12" + "}" for i in range(n_fields)])
print form_string.format(*fields)

#pdb.set_trace()

#for k in di.keys():
#    print k, di[k], di[k]["valacc"].__class__ 

sorted_keys = sorted(di.keys(), key = lambda x:di[x]["valacc"])[-50:]

for k in sorted_keys:
    print pretty_print(di[k]), k

    
    

    
