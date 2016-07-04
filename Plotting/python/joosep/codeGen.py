#!/usr/bin/env python
"""
This file auto-generates the C++ code necessary for MELooper.cc

Mainly, it is responsible for creating the enums
SystematicKey, CategoryKey, HistogramKey, ProcessKey
which are used to keep track of the histograms in a big map during the loop.

This file can also create new classes deriving from CategoryProcessor, which
can have their own logic of filling histograms. Each CategoryProcessor corresponds
to a set of plots that you want to create in a particular category. They will also fill
Histograms of their parent categories.

#FIXME: if oyu add systematics, you need to change them here.

"""
def parseId(id):
    """
    Given an id that identifies a category, return the corresponding CategoryKey
    """
    return "CategoryKey::" + id

def parseCut(id):
    """
    Given an id that identifies a category, return the corresponding cut
    """
    return cuts[id]

def makeCategory(cat, ids=[]):
    """
    Given the category name and a list of ids of the preceding (parent) categories,
    make a new category instance.
    """
    assert(len(cat)==3)
    catname, catkind, subcats = cat
    isleaf = False
    if len(subcats)==0:
        isleaf = True
    ids = ids + [catname]

    #Don't put subcategories in case this is a leaf category
    if isleaf:
        s = r"""
new {catkind}(
    [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst){{
      return {cuts};
    }},
    {catid},
    conf,
    {{}},
    {weightfunc}
)
"""
    else:
        s = r"""
new {catkind}(
    [](const Event& ev){{
      return {cuts};
    }},
    {catid},
    conf,
    {subcats},
    {weightfunc}
)
"""

    #do re-weighting only for sparse categories
    #FIXME: here we specify what kind of weights to use for histogram projection
    #replace with getSystWeights() to have systematic variations of all control histograms
    #replace with getNominalWeights() to make running faster
    wfunc = "getSystWeights()"

    s = s.format(**{
    "catkind": catkind,
    "cuts": parseCut(catname),
    "catid": "{" + parseId(catname) + "}",
    "weightfunc": wfunc,
    "subcats": "{"+", ".join([makeCategory(c, ids) for c in subcats])+"}"
    }
)
    depth = len(ids) - 1
    s = s.replace("\n", "\n" + depth*"    ")
    return s
#end of makeCategory

def makeHistogram(h):
    """
    Given a histogram specification, generate code that creates and fills the histogram
    """
    assert(len(h) == 7)
    hname, nbins, low, high, fillfunc, cutfunc, htitle = h
    s = """
const auto {hname}_key = make_tuple(
    get<0>(key),
    get<1>(key),
    get<2>(key),
    HistogramKey::{hname}
);
if (!results.count({hname}_key)) {{
    results[{hname}_key] = new TH1D("{hname}", "{htitle}", {nbins}, {low}, {high});
}}
if ({cutfunc}) {{
    static_cast<TH1D*>(results[{hname}_key])->Fill({fillfunc}, weight);
}}
""".format(hname=hname, htitle=htitle, nbins=nbins, low=low, high=high,
    cutfunc=cutfunc, fillfunc=fillfunc
)
    return s

def makeEnumHeader(enumname, keys):
    """
    Make the .h side of an enum
    """
    r = """
namespace {0} {{
    enum {0} {{
{1}
    }}; //enum {0}
    const string to_string({0} k);
    const {0} from_string(const string& k);
}} //namespace {0}""".format(
    enumname,
    ",\n".join(["        "+k for k in keys]),
    ",\n".join(['        {{"{0}", {0}}}'.format(k) for k in keys])
)
    return r

def makeEnumImpl(enumname, keys):
    """
    Make the .cc side of an enum with enum<->string conversions
    """
    r = """
namespace {0} {{
    const unordered_map<const string, {0}, hash<string>> map_from_string = {{
{2}
    }}; //map
    const unordered_map<{0}, const string, hash<int>> map_to_string =
        reverse_map<{0}, const string, hash<int>, hash<string>>(map_from_string);
  
    const string to_string({0} k) {{
        if (map_to_string.find(k) == map_to_string.end()) {{
          cerr << "Could not find {0} " << k << endl;
          throw 1;
        }}
        return map_to_string.at(k); 
    }} //to_string
    const {0} from_string(const string& k) {{
        if (map_from_string.find(k) == map_from_string.end()) {{
          cerr << "Could not find {0} " << k << endl;
          throw 1;
        }}
        return map_from_string.at(k);
    }} //from_string
}} //namespace {0}""".format(
    enumname,
    ",\n".join(["        "+k for k in keys]),
    ",\n".join(['        {{"{0}", {0}}}'.format(k) for k in keys])
)
    return r


def makeCategoryProcessorHeader(name, parentname):
    """
    Create a new category processor class.
    name - name of the class
    parentname - name of the parent class
    """
    r = """
class {0} : public {1} {{
public:
    {0}(
        std::function<int(const Event& ev)> _cutFunc,
        const vector<CategoryKey::CategoryKey>& _keys,
        const Configuration& _conf,
        const vector<const CategoryProcessor*>& _subCategories={{}},
        const WeightMap& _weightFuncs=getNominalWeights()
    ) :
      {1}(_cutFunc, _keys, _conf, _subCategories, _weightFuncs) {{}};
     
    virtual void fillHistograms(
        const Event& event,
        ResultMap& results,
        tuple<
            ProcessKey::ProcessKey,
            vector<CategoryKey::CategoryKey>,
            SystematicKey::SystematicKey> key,
        double weight,
        const Configuration& conf
    ) const;
}};
""".format(
    name, parentname
)
    return r

def makeCategoryProcessorImpl(name, parentname, histograms):
    """
    Create the fill function for the category processor based on the histograms
    """
    r = """
void {0}::fillHistograms(
    const Event& event,
    ResultMap& results,
    tuple<
        ProcessKey::ProcessKey,
        vector<CategoryKey::CategoryKey>,
        SystematicKey::SystematicKey> key,
    double weight,
    const Configuration& conf
    ) const {{
    //fill base histograms
    {1}::fillHistograms(event, results, key, weight, conf);
{2}
}}
""".format(
    name,
    parentname,
    "\n".join([makeHistogram(h).replace("\n", "\n        ") for h in histograms])
)
    return r

def makeSystWeightFunction(name, func):
    return "{{SystematicKey::{0}, [](const Event& ev, const Configuration& conf) {{ return {1}; }} }}".format(
        name, func
    )


#List of all systematics that we want to consider
systematics = [
    "nominal",
    "CMS_scale_jUp",
    "CMS_scale_jDown",
    "CMS_ttH_CSVHFStats1Up",
    "CMS_ttH_CSVHFStats1Down",
    "CMS_ttH_CSVHFStats2Up",
    "CMS_ttH_CSVHFStats2Down",
    "CMS_ttH_CSVLFStats1Up",
    "CMS_ttH_CSVLFStats1Down",
    "CMS_ttH_CSVLFStats2Up",
    "CMS_ttH_CSVLFStats2Down",
    "CMS_ttH_CSVcErr1Up",
    "CMS_ttH_CSVcErr1Down",
    "CMS_ttH_CSVcErr2Up",
    "CMS_ttH_CSVcErr2Down",
    "CMS_ttH_CSVLFUp",
    "CMS_ttH_CSVLFDown",
    "CMS_ttH_CSVHFUp",
    "CMS_ttH_CSVHFDown",
    "CMS_ttH_CSVDisabled",
]

systematic_weights = []
for k in systematics:
    if "CSV" in k:
        if not "Disabled" in k:
            kstrip = k.replace("CMS_ttH_CSV", "")
            systematic_weights += [
                (k, "nominal_weight(ev, conf)/ev.data->bTagWeight * ev.data->bTagWeight_{0}".format(kstrip)),
            ]
        else:
            systematic_weights += [
                (k, "nominal_weight(ev, conf)/ev.data->bTagWeight"),
            ]

#List of all processes
#These will be converted to the enum ProcessKey
processes = [
    "ttH",
    "ttH_hbb",
    "ttH_nonhbb",
    "ttbarPlusBBbar",
    "ttbarPlusB",
    "ttbarPlus2B",
    "ttbarPlusCCbar",
    "ttbarOther",
    "ttbarUnsplit",
    "ttW_Wlnu",
    "ttW_Wqq",
    "ttZ_Zqq",
    "SingleMuon",
    "SingleElectron",
    "DoubleMuon",
    "DoubleEG",
    "MuonEG",
    "wjets",
    "ww",
    "wz",
    "zz",
    "stop_t",
    "stop_tbar",
    "stop_tW",
    "stop_tbarW",
    "stop_s",
    "UNKNOWN"
]

#List of all individual category "bits"
categories = [
    "sl",
    "dl",
]

#Map categories to their respective C++ cuts. The Event is available as "ev"
cuts = {
    "sl": "BaseCuts::sl(ev)",
    "dl": "BaseCuts::dl(ev)",
}

#Nested list of (name, type, subcategory) triplets, corresponding to the
#CategoryKey enum to create
categories_tree = [
    ("sl", "SparseCategoryProcessor", []),
    ("dl", "SparseCategoryProcessor", []),
]

#Histograms not defined in codegen
additional_histograms = [
    "sparse"
]

#Pairs of all new category processors along with the histograms to plot there
category_processors = [
]

#List of all histograms to create (for enum HistogramKey)
all_histogram_keys = (
    additional_histograms
)

if __name__ == "__main__":
    #file with enum includes
    of_h = open("interface/gen.h", "w")
    #file with enum to string conversions
    of_c = open("bin/gen.cc", "w")
    #file with CategoryProcessor declarations
    categories_h = open("interface/categories.h", "w")
    #file with CategoryProcessor fill implementations
    categories_c = open("bin/categories.cc", "w")

    of_c.write('// autogenerated with codeGen.py\n')
    of_c.write('#include "TTH/Plotting/interface/gen.h"\n')
    of_c.write("""
    //turns a map A -> B to B -> A
    template <class A, class B, class H1, class H2>
    const unordered_map<A, B, H1> reverse_map(const unordered_map<B, A, H2>& src) {
        unordered_map<A, B, H1> ret;
        for (auto& kv : src) {
            ret.insert(make_pair(kv.second, kv.first));
        }
        return ret;
    } 
    """)
    of_h.write(
    """// autogenerated with codeGen.py
    #include <string>
    #include <iostream>
    #include <unordered_map>
    using namespace std;
    """
    )

    categories_h.write(
    """
    //autogenerated with codeGen.py
    #include "TTH/Plotting/interface/Event.h"
    """
    )
    categories_c.write("""
    //autogenerated with codeGen.py
    #include "TTH/Plotting/interface/categories.h"
    """)

    #Create all enums
    for enumname, procs in [
        ("ProcessKey", processes),
        ("SystematicKey", systematics),
        ("CategoryKey", categories),
        ("HistogramKey", all_histogram_keys),
        ]:
        of_h.write(makeEnumHeader(enumname, procs) + "\n")
        of_c.write(makeEnumImpl(enumname, procs) + "\n")

    #create all CategoryProcessors
    for name, parentname, hists in category_processors:
        categories_h.write(makeCategoryProcessorHeader(name, parentname))

    categories_h.write("const vector<const CategoryProcessor*> makeCategories(const Configuration& conf);\n")

    #Create the function that fills the category processor tree
    categories_c.write("const vector<const CategoryProcessor*> makeCategories(const Configuration& conf) {\n" +
        "return { \n" + 
        ",\n".join([makeCategory(cat) for cat in categories_tree]) + 
        "\n}; // categories"
        "\n} // makeCategories"
    )
    #create all CategoryProcessors
    for name, parentname, hists in category_processors:
        categories_c.write(makeCategoryProcessorImpl(name, parentname, hists))

    categories_c.write("""
WeightMap getNominalWeights() {
    return {
        {SystematicKey::nominal, nominal_weight},
    };
}
""")

    categories_c.write("""
WeightMap getSystWeights() {
    return {
        {SystematicKey::nominal, nominal_weight},
""")
    for wname, wfunc in systematic_weights:
        categories_c.write("        " + makeSystWeightFunction(wname, wfunc) + ",\n")
    categories_c.write("    };\n")
    categories_c.write("}\n")

    #Done
    categories_h.close()
    categories_c.close()
    of_h.close()
    of_c.close()
