########################################
# Imports
########################################

import imp, os, sys
import subprocess

from CombineHelper import LimitGetter


print "MakeLimits.py called from cwd={0}".format(os.getcwd())
########################################
# Setup
########################################

if not len(sys.argv) in [3,4,5]:
    print "Wrong number of arguments"
    print "Usage: "
    print "{0} datacard_file.py inout_dir [analysis_to_process [group to_process]]".format(sys.argv[0])
    sys.exit()

# Get the datacard
dcard = imp.load_source("dcard", sys.argv[1])

# Get the input/output directory
inout_dir = sys.argv[2]

if len(sys.argv) >= 4:
    try:
        analyses = {sys.argv[3]: dcard.analyses[sys.argv[3]]}
    except KeyError:
        print sys.argv[3], "is not a valid analysis"
        print "Available are:", dcard.analyses.keys()
        sys.exit()
else:
    analyses = dcard.analyses


# If we receive a group-name from command line, only process this group
# Otherwise do all of them
group_to_process = ""
if len(sys.argv) == 5:
    group_to_process = sys.argv[4]


########################################
# Actual work
########################################

for analysis_name, analysis in analyses.iteritems():

    # Decide what to run on
    if group_to_process:
        groups = [group_to_process]
    else:
        groups = analysis.groups.keys()

    # Prepare the limit getter
    lg = LimitGetter(inout_dir)

    for group_name in groups:

        group = analysis.groups[group_name]    
        print "Doing {0} consisting of {1} categories".format(group_name, len(group))    

        # Get all the per-category datacards and use combineCards to merge into one "group datacard"
        input_dcard_names = ["shapes_{0}.txt".format(c.full_name) for c in group]
        add_dcard_command = ["combineCards.py"] + input_dcard_names 
        process = subprocess.Popen(add_dcard_command, 
                                   stdout=subprocess.PIPE, 
                                   cwd=inout_dir)        
        group_dcard = process.communicate()[0]

        # Write the group datacard to a file
        group_dcard_filename = os.path.join(inout_dir, "shapes_group_{0}.txt".format(group_name))
        group_dcard_file = open(group_dcard_filename, "w")
        group_dcard_file.write(group_dcard)
        group_dcard_file.close()

        # And run limit setting on it
        lg(group_dcard_filename)

    # End loop over groups
# End of loop over analyses

