from TTH.Plotting.Datacards.AnalysisSpecificationClasses import make_csv_abstract

from TTH.Plotting.Datacards.AnalysisSpecificationSL import analyses as analyses_SL
from TTH.Plotting.Datacards.AnalysisSpecificationDL import analyses as analyses_DL

analyses = dict((k, v) for d in [analyses_SL, analyses_DL] for k, v in d.items())

def make_csv():
    return make_csv_abstract(analyses)

