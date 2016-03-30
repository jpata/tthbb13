########################################
# Imports
########################################

import imp, os, sys

from CombineHelper import LimitGetter


########################################
# Setup
########################################

if not len(sys.argv) in [2,3]:
    print "Wrong number of arguments"
    print "Usage: "
    print "{0} datacard_file.py [group to process]".format(sys.argv[0])

# TODO: define input/output directories

# Get the datacard
dcard = imp.load_source("dcard", sys.argv[1])


# If we receive a group-name from command line, only process this group
# Otherwise do all of them
if len(sys.argv) == 2:
    groups_to_process = dcard.analysis.groups.keys()
else:
    group = sys.argv[2]

    # Make sure we have a valid group
    if not group in dcard.analysis.groups.keys():
        print group, "does not name a valid group. Available are:"
        print dcard.analysis.groups.keys()
        sys.exit()
    else:
        groups_to_process = [group]

    
print "Processing groups:", groups_to_process

# Prepare the limit getter
lg = LimitGetter(dcard.analysis.output_directory)


########################################
# Actual work
########################################

for group in groups_to_process:

    print "Doing {0} consisting of {1} categories".format(group, len(dcard.analysis.groups[group]))    

    lg(os.path.join(dcard.analysis.output_directory, "shapes_{0}.txt".format(group)))

# End loop over groups
