#!/usr/bin/env python
#The production of the datacards follows the following pattern:
#Each final limit, (e.g. full ttH limit) corresponds to an Analysis.
#Each Analysis is made of Groups, which are made of Categories.
from TTH.Plotting.Datacards.AnalysisSpecificationClasses import make_csv_categories_abstract, make_csv_groups_abstract

from TTH.Plotting.Datacards.AnalysisSpecificationSL import analyses as analyses_SL
from TTH.Plotting.Datacards.AnalysisSpecificationDL import analyses as analyses_DL

analyses = dict((k, v) for d in [analyses_SL, analyses_DL] for k, v in d.items())

print "Printing all analyses"
for k, v in analyses.items():
    print k
    print v

def make_csv_categories():
    return make_csv_categories_abstract(analyses)

def make_csv_groups():
    return make_csv_groups_abstract(analyses)

if __name__ == "__main__":
    make_csv_categories()
    make_csv_groups()
