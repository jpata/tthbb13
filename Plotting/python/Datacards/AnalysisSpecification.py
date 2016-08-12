#!/usr/bin/env python
#The production of the datacards follows the following pattern:
#Each final limit, (e.g. full ttH limit) corresponds to an Analysis.
#Each Analysis is made of Groups, which are made of Categories.
import os

from TTH.Plotting.Datacards.AnalysisSpecificationClasses import make_csv_categories_abstract, make_csv_groups_abstract

from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig

analyses = {}
for config in ["config_sl.cfg", "config_dl.cfg"]:
    name, analysis = analysisFromConfig(os.path.join(os.environ["CMSSW_BASE"],
                                                     "src/TTH/Plotting/python/Datacards",
                                                     config))
    analyses[name] = analysis

def main():
    print "Printing all analyses"
    for k, v in analyses.items():
        print k
        print v
    
    #write out all categories that we want to create
    make_csv_categories_abstract(analyses)

    #write out all the combine groups
    make_csv_groups_abstract(analyses)


if __name__ == "__main__":
    main()
