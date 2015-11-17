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
    [](const Event& ev){{
      return {cuts};
    }},
    {catid},
    conf)
"""
    else:
        s = r"""
new {catkind}(
    [](const Event& ev){{
      return {cuts};
    }},
    {catid},
    conf,
    {subcats}
)"""

    s = s.format(**{
    "catkind": catkind,
    "cuts": parseCut(catname),
    "catid": "{" + parseId(catname) + "}",
    "subcats": "{"+", ".join([makeCategory(c, ids) for c in subcats])+"}"}
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


def makeCategoryProcessorHeader(name):
    """
    Create a new category processor class
    """
    r = """
class {0} : public CategoryProcessor {{
public:
    {0}(
        std::function<int(const Event& ev)> _cutFunc,
        const vector<CategoryKey::CategoryKey>& _keys,
        const Configuration& _conf,
        const vector<const CategoryProcessor*>& _subCategories={{}}
    ) :
      CategoryProcessor(_cutFunc, _keys, _conf, _subCategories) {{}};
     
    virtual void fillHistograms(
        const Event& event,
        ResultMap& results,
        const tuple<
            vector<CategoryKey::CategoryKey>,
            SystematicKey::SystematicKey
        >,
        double weight
    ) const;
}};
""".format(
    name
)
    return r

def makeCategoryProcessorImpl(name, histograms):
    """
    Create the fill function for the category processor based on the histograms
    """
    r = """
void {0}::fillHistograms(
    const Event& event,
    ResultMap& results,
    const tuple<
        vector<CategoryKey::CategoryKey>,
        SystematicKey::SystematicKey
    > key,
    double weight
    ) const {{
{1}
}}
""".format(
    name,
    "\n".join([makeHistogram(h).replace("\n", "\n        ") for h in histograms])
)
    return r


#List of all systematics that we want to consider
systematics = [
    "nominal",
    "CMS_scale_jUp",
    "CMS_scale_jDown",
    "CMS_ttH_CSVStats1Up",
    "CMS_ttH_CSVStats1Down",
    "CMS_ttH_CSVStats2Up",
    "CMS_ttH_CSVStats2Down",
    "CMS_ttH_CSVLFUp",
    "CMS_ttH_CSVLFDown",
    "CMS_ttH_CSVHFUp",
    "CMS_ttH_CSVHFDown",
]

#List of all processes
processes = [
    "ttH",
    "ttH_hbb",
    "ttbarPlusBBbar",
    "ttbarPlusB",
    "ttbarPlus2B",
    "ttbarPlusCCbar",
    "ttbarOther",
    "ttH_nohbb",
    "ttw_wlnu",
    "ttw_wqq",
    "ttz_zqq",
    "ttz_zllnunu",
    "UNKNOWN"
]

#List of all individual category "bits"
categories = [
    "sl",
    "dl",

    "j3_t2",
    "jge4_t2",
    "jge3_t3",
    "jge4_tge4",

    "j4_t3",
    "j4_t4",
    "j5_t3",
    "j5_tge4",
    "jge6_t2",
    "jge6_t3",
    "jge6_tge4",

    "blrL",
    "blrH",

    "boostedHiggs",
]

#Map categories to their respective C++ cuts. The Event is available as "ev"
cuts = {
    "sl": "BaseCuts::sl(ev)",
    "dl": "BaseCuts::dl(ev)",
    "jge6_tge4": "ev.numJets>=6 && ev.nBCSVM>=4",
    "jge6_t3": "ev.numJets>=6 && ev.nBCSVM==3",
    "jge6_t2": "ev.numJets>=6 && ev.nBCSVM==2",
    "jge6_t3": "ev.numJets>=6 && ev.nBCSVM==3",
    "j5_tge4": "ev.numJets==5 && ev.nBCSVM>=4",
    "j5_t3": "ev.numJets==5 && ev.nBCSVM==3",
    "blrH": "ev.btag_LR_4b_2b > 0.95",
    "boostedHiggs": "ev.nhiggsCandidate >= 1",
}

#Nested list of (name, type, subcategory) triplets, corresponding to the
#category tree to create
categories_tree = [
    ("sl", "ControlCategoryProcessor", [
        ("jge6_tge4", "ControlCategoryProcessor", []),
        ("jge6_t3", "ControlCategoryProcessor", [
            ("boostedHiggs", "BoostedCategoryProcessor", [])
        ]),
        ("jge6_t2", "ControlCategoryProcessor", [
            ("boostedHiggs", "BoostedCategoryProcessor", [])
        ]),
        ("j5_tge4", "ControlCategoryProcessor", [
            ("boostedHiggs", "BoostedCategoryProcessor", [])
        ]),
        ("j5_t3", "ControlCategoryProcessor", [
            ("boostedHiggs", "BoostedCategoryProcessor", [])
        ]),
    ]),
    ("sl", "SparseCategoryProcessor", [
    ]),
    ("dl", "SparseCategoryProcessor", [
    ])
]

#Kinematic control histograms
#name, nbins, low, high, fillFunction, cutFunction, title
histograms_control = [
    ("jet0_pt", 100, 0, 600, "event.jets.at(0).p4.Pt()", "event.jets.size()>0", "Leading jet pt"),
    ("jet1_pt", 100, 0, 600, "event.jets.at(1).p4.Pt()", "event.jets.size()>1", "Subleading jet pt"),
    ("jet0_eta", 100, -3, 3, "event.jets.at(0).p4.Eta()", "event.jets.size()>0", "Leading jet eta"),
    ("jet1_eta", 100, -3, 3, "event.jets.at(1).p4.Eta()", "event.jets.size()>1", "Subleading jet eta"),
]

#Kinematic control histograms
#name, nbins, low, high, fillFunction, cutFunction, title
histograms_boosted = [
    ("higgsCandidate_pt", 100, 200, 600, "event.jets.at(0).p4.Pt()", "event.jets.size()>0", "Leading jet pt"),
]

#MEM histograms
histograms_mem = [
    ("mem_SL_0w2h2t", 6, 0, 1, "event.mem_SL_0w2h2t", "true", "SL 022"),
    ("mem_SL_2w2h2t", 6, 0, 1, "event.mem_SL_2w2h2t", "true", "SL 222"),
    ("mem_SL_2w2h2t_sj", 6, 0, 1, "event.mem_SL_2w2h2t_sj", "true", "SL 222 sj"),
    ("mem_DL_0w2h2t", 6, 0, 1, "event.mem_DL_0w2h2t", "true", "SL 022"),
]

#Histograms not defined in codegen
additional_histograms = [
    "sparse"
]

#Pairs of all new category processors along with the histograms to plot there
category_processors = [
    ("ControlCategoryProcessor", histograms_control),
    ("BoostedCategoryProcessor", histograms_boosted)
]

#List of all histograms to create (for enum HistogramKey)
all_histogram_keys = (
    [h[0] for h in histograms_control] +
    [h[0] for h in histograms_mem] +
    [h[0] for h in histograms_boosted] +
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
    for name, hists in category_processors:
        categories_h.write(makeCategoryProcessorHeader(name))

    categories_h.write("const vector<const CategoryProcessor*> makeCategories(const Configuration& conf);\n")

    #Create the function that fills the category processor tree
    categories_c.write("const vector<const CategoryProcessor*> makeCategories(const Configuration& conf) {\n" +
        "return { \n" + 
        ",\n".join([makeCategory(cat) for cat in categories_tree]) + 
        "\n}; // categories"
        "\n} // makeCategories"
    )
    #create all CategoryProcessors
    for name, hists in category_processors:
        categories_c.write(makeCategoryProcessorImpl(name, hists))

    #Done
    categories_h.close()
    categories_c.close()
    of_h.close()
    of_c.close()
