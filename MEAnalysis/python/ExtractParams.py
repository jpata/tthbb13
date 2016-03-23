
import os
import sys
import pdb
import glob
import pickle


if not len(sys.argv) >= 3:
    print "Invalid number of arguments"
    print "Usage: {0} gc_onfiguration path_to_check ".format(sys.argv[0])
    sys.exit()

gc_conf_file = sys.argv[1]
path_to_check = sys.argv[2]

if len(sys.argv) ==4:
    sort_by = sys.argv[3]
else:
    sort_by = "valacc"


pickle_file_path = os.path.join(path_to_check, "summary.pickle")

if os.path.exists(pickle_file_path):
    f = open(pickle_file_path, "r")
    di = pickle.load(f)
    f.close()

    params = [k for k in di.values()[0].keys() if not k in [ "valacc", "maxvalacc", "delacc"] ]

else:
    # extract which parameters we care about 
    lines = open(gc_conf_file).readlines()
    param_line = [l for l in lines if "parameters" in l and "=" in l][0]
    param_line = param_line.strip()
    params = param_line.split("=")[1].split(" ")
    params = [p for p in params if p] # remove empty strings

    print "Found parameters"
    print params


    di = {}
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

    f = open(pickle_file_path, "wb")
    pickle.dump(di, f)
    f.close()


fields = [ "valacc", "maxvalacc", "delacc"] + params    

def pretty_print(d):

    n_fields = len(fields)
    
    form_string = " ".join(["{" + str(i) + ": <12.4" + "}" for i in range(n_fields)])
    vals =  [float(d[f]) for f in fields]
    
    return form_string.format(*vals)

print "\n\n"

n_fields = len(fields)
form_string = " ".join(["{" + str(i) + ": <12" + "}" for i in range(n_fields)])
print form_string.format(*fields)

sorted_keys = sorted(di.keys(), key = lambda x:di[x][sort_by])[-50:]

for k in sorted_keys:
    print pretty_print(di[k]), k

    
    

    
