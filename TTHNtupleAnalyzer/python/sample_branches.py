#sample branches file for headergen.py
#uses branch classes from headergen
from TTH.TTHNtupleAnalyzer.headergen import *

defines.extend(["#define ADD_TRUE_TOP_MATCHING_FOR_FJ 0",
                "#define ADD_TRUE_TOP_MATCHING_FOR_HTT 0"])

# True Top Branches
for t in ["t", "tbar", "t2", "tbar2"]:
    for v in [
        ("eta"), ("mass"), ("phi"), ("pt"), ("status"),
        ("b__eta"), ("b__mass"), ("b__phi"), ("b__pt"), ("b__status"),
        ("w_d1__eta"), ("w_d1__mass"), ("w_d1__phi"), ("w_d1__pt"), ("w_d1__status"), ("w_d1__id"),
        ("w_d2__eta"), ("w_d2__mass"), ("w_d2__phi"), ("w_d2__pt"), ("w_d2__status"), ("w_d2__id")
    ]:
        typ = "float"
        if "status" in v or "id" in v:
            typ = "int"
        process += [Scalar("gen_%s__%s" % (t, v), typ)]

from TTH.TTHNtupleAnalyzer.toptagger_branches import *

