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

if not len(sys.argv) in [3,5]:
    print "Wrong number of arguments"
    print "Usage: "
    print "{0} datacard_file.py datacard_directory [analysis_to_process [group to_process]]".format(sys.argv[0])
    sys.exit()

# Get the datacard
dcard = imp.load_source("dcard", sys.argv[2])

# Get the input/output directory
inout_dir = sys.argv[3]

if len(sys.argv) >= 4:
    analyses = [dcard.analyses[sys.argv[4]]]
else:
    analyses = dcard.analyses


# If we receive a group-name from command line, only process this group
# Otherwise do all of them
group_to_process = ""
if len(sys.argv) == 5:
    group_to_process = sys.argv[5]



########################################
# Actual work
########################################

<<<<<<< Updated upstream
for group_name in groups_to_process:

    group = dcard.analysis.groups[group_name]    
    print "Doing {0} consisting of {1} categories".format(group_name, len(group))    
    

    # Get all the per-category datacards and use combineCards to merge into one "group datacard)"
    input_dcard_names = ["shapes_{0}.txt".format(c.full_name) for c in group]
    add_dcard_command = ["combineCards.py"] + input_dcard_names 
    print "Running combineCards: {0}".format(" ".join(add_dcard_command))
    process = subprocess.Popen(add_dcard_command, 
                               stdout=subprocess.PIPE, 
                               #cwd=dcard.analysis.output_directory)
                               cwd="./")
    group_dcard = process.communicate()[0]

    # Write the group datacard to a file
    group_dcard_filename = os.path.join(
        #dcard.analysis.output_directory,
        "./",
        "shapes_group_{0}.txt".format(group_name)
    )
    group_dcard_file = open(group_dcard_filename, "w")
    group_dcard_file.write(group_dcard)
    group_dcard_file.close()
    print "Running limit on {0}".format(group_dcard_filename)
    # And run limit setting on it
    lg(group_dcard_filename)

# End loop over groups
=======
for analysis in dcard.analyses:

    # Decide what to run on
    if group_to_process:
        groups = [group_to_process]
    else:
        groups = analysis.groups.keys()

    # Prepare the limit getter
    lg = LimitGetter(inout_dir)

    for group_name in groups:

        group = dcard.analysis.groups[group_name]    
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
>>>>>>> Stashed changes
