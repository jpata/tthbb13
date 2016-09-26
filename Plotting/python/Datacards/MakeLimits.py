########################################
# Imports
########################################

import imp, os, sys
import subprocess

from CombineHelper import LimitGetter

from EnvForCombine import PATH, LD_LIBRARY_PATH, PYTHONPATH

print "MakeLimits.py called from cwd={0}".format(os.getcwd())


########################################
# Actual work
########################################

def main(
        inout_dir,
        analysis_cfg,
        group
):
    

    ## Get the datacard
    #dcard = imp.load_source("dcard", dcard_path)
#
#    # What analysis to run
#    if analysis_arg:
#        try:
#            analyses = {analysis_arg: dcard.analyses[analysis_arg]}
#        except KeyError:
#            print analysis_arg, "is not a valid analysis"
#            print "Available are:", dcard.analyses.keys()
#            sys.exit()
#
#    else:

    analyses = [analysis_cfg]

    for analysis in analyses:

        # Decide what to run on
        if group:
            groups = [group]
        else:
            groups = analysis.groups.keys()

        # Prepare the limit getter
        lg = LimitGetter(inout_dir)

        for group_name in groups:

            group = [x for x in analysis.groups[group_name] if x.do_limit]

            print group
            
            print "Doing {0} consisting of {1} categories".format(group_name, len(group))    

            # Get all the per-category datacards and use combineCards to merge into one "group datacard"
            input_dcard_names = ["shapes_{0}.txt".format(c.full_name) for c in group]
            add_dcard_command = ["combineCards.py"] + input_dcard_names 

            print "Command:", add_dcard_command 
            process = subprocess.Popen(add_dcard_command, 
                                       stdout=subprocess.PIPE, 
                                       cwd=inout_dir,
                                       env=dict(os.environ, 
                                                PATH=PATH,
                                                LD_LIBRARY_PATH = LD_LIBRARY_PATH,
                                                PYTHONPATH=PYTHONPATH
                                            ))

            group_dcard = process.communicate()[0]

            print "Finished with group_card making"

            # Write the group datacard to a file
            group_dcard_filename = os.path.join(inout_dir, "shapes_group_{0}.txt".format(group_name))
            group_dcard_file = open(group_dcard_filename, "w")
            group_dcard_file.write(group_dcard)
            group_dcard_file.close()

            print "Written to file, running limit setting"

            # And run limit setting on it
            lg(group_dcard_filename)

        # End loop over groups
    # End of loop over analyses


#if __name__ == "__main__":
#
#    if not len(sys.argv) in [3,4,5]:
#        print "Wrong number of arguments"
#        print "Usage: "
#        print "{0} datacard_file.py inout_dir [analysis_to_process [group to_process]]".format(sys.argv[0])
#        sys.exit()
#
#    dcard_path = sys.argv[1]
#
#    # Get the input/output directory
#    inout_dir = sys.argv[2]
#
#    if len(sys.argv) >= 4:
#        analysis_arg = sys.argv[3]
#    else:
#        analysis_arg = ""
#
#    if len(sys.argv) == 5:
#        group_arg = sys.argv[4]
#    else:
#        group_arg = ""
#
#    main(dcard_path, inout_dir, analysis_arg, group_arg)
