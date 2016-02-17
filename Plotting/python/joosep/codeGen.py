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
    #if catkind == "SparseCategoryProcessor" or catkind == "ControlCategoryProcessor":
    #    wfunc = "getSystWeights()"

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
        const tuple<
            vector<CategoryKey::CategoryKey>,
            SystematicKey::SystematicKey
        >,
        double weight
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
    const tuple<
        vector<CategoryKey::CategoryKey>,
        SystematicKey::SystematicKey
    > key,
    double weight
    ) const {{
    //fill base histograms
    {1}::fillHistograms(event, results, key, weight);
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
]

systematic_weights = []
for k in systematics:
    if "CSV" in k:
        systematic_weights += [
            (k, "nominal_weight(ev, conf)/ev.bTagWeights.at(SystematicKey::nominal) * ev.bTagWeights.at(SystematicKey::{0})".format(k)),
        ]

#List of all processes
processes = [
    "ttH",
    "ttH_hbb",
    "ttH_nonhbb",
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
    "SingleMuon",
    "SingleElectron",
    "DoubleMuon",
    "DoubleEG",
    "MuonEG",
    "UNKNOWN"
]

#List of all individual category "bits"
categories = [
    "sl",
    "dl",
    
    "j3_t2",
    "j3_t3",
    "jge4_t3",
    "jge4_t2",
    "jge4_tge4",
#
    "j4_t3",
    "j4_t4",
    "j5_t2",
    "j5_t3",
    "j5_tge4",
    "jge6_t2",
    "jge6_t3",
    "jge6_tge4",
]

#Map categories to their respective C++ cuts. The Event is available as "ev"
cuts = {
    "sl": "BaseCuts::sl(ev)",
    "sl_mu": "BaseCuts::sl_mu(ev)",
    "sl_el": "BaseCuts::sl_el(ev)",
    
    "dl_mumu": "BaseCuts::dl_mumu(ev)",
    "dl_ee": "BaseCuts::dl_ee(ev)",
    "dl_emu": "BaseCuts::dl_emu(ev)",

    "dl": "BaseCuts::dl(ev)",
    
    "j3_t2": "ev.numJets==3 && ev.nBCSVM==2",
    "j3_t3": "ev.numJets==3 && ev.nBCSVM==3",
    "jge4_t3": "ev.numJets>=4 && ev.nBCSVM==3",
    "jge4_t2": "ev.numJets>=4 && ev.nBCSVM==2",
    "jge4_tge4": "ev.numJets>=4 && ev.nBCSVM>=4",
    
    "jge6_tge4": "ev.numJets>=6 && ev.nBCSVM>=4",
    "jge6_t3": "ev.numJets>=6 && ev.nBCSVM==3",
    "jge6_t2": "ev.numJets>=6 && ev.nBCSVM==2",
    "jge6_t3": "ev.numJets>=6 && ev.nBCSVM==3",
    "j5_tge4": "ev.numJets==5 && ev.nBCSVM>=4",
    "j5_t3": "ev.numJets==5 && ev.nBCSVM==3",
    "j5_t2": "ev.numJets==5 && ev.nBCSVM==2",
    "j4_t4": "ev.numJets==4 && ev.nBCSVM==4",
    "j4_t3": "ev.numJets==4 && ev.nBCSVM==3",
#    "blrH": "ev.btag_LR_4b_2b > 0.95",
#    "boostedHiggs": "ev.nhiggsCandidate >= 1",
#    "boostedHiggsOnly": "ev.nhiggsCandidate >= 1 && ev.ntopCandidate==0",
#    #"boostedHiggsHighPt": "ev.nhiggsCandidate >= 1 && ev.higgsCandidate_pt > 300",
#    #"boostedHiggsGenMatch": "(ev.nhiggsCandidate >= 1) && (ev.higgsCandidate_dr_genHiggs < 0.5)",
#    #"boostedHiggsGenNoMatch": "(ev.nhiggsCandidate >= 1) && (ev.higgsCandidate_dr_genHiggs > 0.5)",
#    "boostedTop": "ev.ntopCandidate >= 1",
#    "boostedTopOnly": "ev.ntopCandidate >= 1 && ev.nhiggsCandidate==0",
#    "boostedHiggsTop": "ev.ntopCandidate >= 1 && ev.nhiggsCandidate>=1",
}

#Nested list of (name, type, subcategory) triplets, corresponding to the
#category tree to create
categories_tree = [
#    ("sl", "ControlCategoryProcessor", [
#        ("jge6_tge4", "ControlCategoryProcessor", []),
#        ("jge6_t3", "ControlCategoryProcessor", []),
#        ("jge6_t2", "ControlCategoryProcessor", []),
#        ("j5_tge4", "ControlCategoryProcessor", []),
#        ("j5_t3", "ControlCategoryProcessor", []),
#        ("j4_t4", "ControlCategoryProcessor", []),
#        ("j4_t3", "ControlCategoryProcessor", []),
#    ]),
#    ("sl_mu", "ControlCategoryProcessor", [
#        ("jge6_tge4", "ControlCategoryProcessor", []),
#        ("jge6_t3", "ControlCategoryProcessor", []),
#        ("jge6_t2", "ControlCategoryProcessor", []),
#        ("j5_tge4", "ControlCategoryProcessor", []),
#        ("j5_t3", "ControlCategoryProcessor", []),
#        ("j5_t2", "ControlCategoryProcessor", []),
#        ("j4_t4", "ControlCategoryProcessor", []),
#        ("j4_t3", "ControlCategoryProcessor", []),
#    ]),
#    ("sl_el", "ControlCategoryProcessor", [
#        ("jge6_tge4", "ControlCategoryProcessor", []),
#        ("jge6_t3", "ControlCategoryProcessor", []),
#        ("jge6_t2", "ControlCategoryProcessor", []),
#        ("j5_tge4", "ControlCategoryProcessor", []),
#        ("j5_t3", "ControlCategoryProcessor", []),
#        ("j5_t2", "ControlCategoryProcessor", []),
#        ("j4_t4", "ControlCategoryProcessor", []),
#        ("j4_t3", "ControlCategoryProcessor", []),
#    ]),
#    ("dl", "ControlCategoryProcessor", [
#        ("j3_t2", "ControlCategoryProcessor", []),
#        ("jge3_t3", "ControlCategoryProcessor", []),
#        ("jge4_t2", "ControlCategoryProcessor", []),
#        ("jge4_tge4", "ControlCategoryProcessor", []),
#    ]),
#    ("dl_mumu", "ControlCategoryProcessor", [
#        ("j3_t2", "ControlCategoryProcessor", []),
#        ("jge3_t3", "ControlCategoryProcessor", []),
#        ("jge4_t2", "ControlCategoryProcessor", []),
#        ("jge4_tge4", "ControlCategoryProcessor", []),
#    ]),
#
#    ("dl_emu", "ControlCategoryProcessor", [
#        ("j3_t2", "ControlCategoryProcessor", []),
#        ("jge3_t3", "ControlCategoryProcessor", []),
#        ("jge4_t2", "ControlCategoryProcessor", []),
#        ("jge4_tge4", "ControlCategoryProcessor", []),
#    ]),
#    ("dl_ee", "ControlCategoryProcessor", [
#        ("j3_t2", "ControlCategoryProcessor", []),
#        ("jge3_t3", "ControlCategoryProcessor", []),
#        ("jge4_t2", "ControlCategoryProcessor", []),
#        ("jge4_tge4", "ControlCategoryProcessor", []),
#    ]),

    ("sl", "SparseCategoryProcessor", []),
    ("dl", "SparseCategoryProcessor", []),
]

#Kinematic control histograms
#name, nbins, low, high, fillFunction, cutFunction, title
histograms_control = [
    ("nPVs", 30, 0, 30, "event.data->nPVs", "true", "Number of primary vertices (reco)"),
    
    ("numJets", 8, 2, 10, "event.numJets", "true", "Number of resolved jets"),
    
    ("nBCSVM", 5, 2, 7, "event.nBCSVM", "true", "Number of CSVM jets"),
    ("nBCSVL", 8, 0, 8, "event.nBCSVL", "true", "Number of CSVL jets"),

    ("lep0_pt", 100, 0, 600, "event.leptons.at(0).p4.Pt()", "event.leptons.size()>0", "Leading lepton pt"),
    ("lep0_eta", 100, -3, 3, "event.leptons.at(0).p4.Eta()", "event.leptons.size()>0", "Leading lepton pt"),
    
    ("lep1_pt", 100, 0, 600, "event.leptons.at(1).p4.Pt()", "event.leptons.size()>1", "Sub-leading lepton pt"),
    ("lep1_eta", 100, -3, 3, "event.leptons.at(1).p4.Eta()", "event.leptons.size()>1", "Sub-leading lepton pt"),
    
    ("jet0_pt", 100, 0, 600, "event.jets.at(0).p4.Pt()", "event.jets.size()>0", "Leading jet pt"),
    ("jet1_pt", 100, 0, 600, "event.jets.at(1).p4.Pt()", "event.jets.size()>1", "Subleading jet pt"),

    ("jet0_eta", 100, -3, 3, "event.jets.at(0).p4.Eta()", "event.jets.size()>0", "Leading jet eta"),
    ("jet1_eta", 100, -3, 3, "event.jets.at(1).p4.Eta()", "event.jets.size()>1", "Subleading jet eta"),
    
    ("jet0_btagCSV", 100, 0, 1, "event.jets.at(0).btagCSV", "event.jets.size()>0", "Leading jet CSV"),
    ("jet1_btagCSV", 100, 0, 1, "event.jets.at(1).btagCSV", "event.jets.size()>1", "Subleading jet CSV"),

    ("jet0_btagBDT", 100, -1, 1, "event.jets.at(0).btagBDT", "event.jets.size()>0", "Leading jet BDT"),
    ("jet1_btagBDT", 100, -1, 1, "event.jets.at(1).btagBDT", "event.jets.size()>1", "Subleading jet BDT"),
    
    ("btag_LR_4b_2b", 100, 0, 1, "event.btag_LR_4b_2b", "event.jets.size()>=3", "btag likelihood"),
    ("btag_LR_4b_2b_logit", 100, -10, 10, "event.btag_LR_4b_2b_logit", "event.jets.size()>=3", "btag likelihood"),

    ("ntopCandidates", 4, 0, 4, "event.ntopCandidate + event.data->nothertopCandidate", "event.ntopCandidate>=0", "Number of HTTv2 candidates"),
    ("nhiggsCandidate", 4, 0, 4, "event.nhiggsCandidate", "event.nhiggsCandidate>=0", "Number of higgs candidates"),
    
    ("nMatch_wq", 4, 0, 4, "event.data->nMatch_wq", "isMC(conf.process)", "Number of jets matched to quarks from W"),
    ("nMatch_wq_btag", 4, 0, 4, "event.data->nMatch_wq_btag", "isMC(conf.process)", "Number of jets matched to quarks from W with b-tagging"),
    ("nMatch_hb", 4, 0, 4, "event.data->nMatch_hb", "isMC(conf.process)", "Number of jets matched to quarks from W"),
    ("nMatch_hb_btag", 4, 0, 4, "event.data->nMatch_hb_btag", "isMC(conf.process)", "Number of jets matched to quarks from W with b-tagging"),
    ("nMatch_tb", 4, 0, 4, "event.data->nMatch_tb", "isMC(conf.process)", "Number of jets matched to quarks from W"),
    ("nMatch_tb_btag", 4, 0, 4, "event.data->nMatch_tb_btag", "isMC(conf.process)", "Number of jets matched to quarks from W with b-tagging"),
    ("fullMatch", 2, 0, 2, "(event.data->nMatch_tb_btag >= 2 && event.data->nMatch_wq_btag >=2) && (isSignalMC(conf.process) ? event.data->nMatch_hb_btag>=2 : true)", "isMC(conf.process)", "Number of events with full match"),
]

#Kinematic control histograms
#name, nbins, low, high, fillFunction, cutFunction, title
histograms_boosted = [
    ("higgsCandidate_pt", 100, 200, 600, "event.nhiggsCandidate>0 ? event.higgsCandidate_pt : 0.0", "true", "Leading higgs candidate pt"),
    ("higgsCandidate_eta", 100, -3, 3, "event.nhiggsCandidate>0 ? event.higgsCandidate_eta : 0.0", "true", "Leading higgs candidate eta"),
    ("higgsCandidate_bbtag", 100, -1, 1, "event.nhiggsCandidate>0 ? event.higgsCandidate_bbtag : 0.0", "true", "Leading higgs candidate bbtag"),
    ("topCandidate_pt", 100, 200, 600, "event.ntopCandidate>0 ? event.topCandidate_pt : 0.0", "true", "Leading top candidate pt"),
    ("topCandidate_eta", 100, -3, 3, "event.ntopCandidate>0 ? event.topCandidate_eta : 0.0", "true", "Leading top candidate eta"),
    ("topCandidate_mass", 100, 0, 300, "event.ntopCandidate>0 ? event.topCandidate_mass : 0.0", "true", "Leading top candidate mass"),
    ("topCandidate_masscal", 100, 0, 300, "event.ntopCandidate>0 ? event.topCandidate_masscal : 0.0", "true", "Leading top candidate mass (calibrated)"),
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
    ("ControlCategoryProcessor", "CategoryProcessor", histograms_control+histograms_mem),
    ("BoostedCategoryProcessor", "ControlCategoryProcessor", histograms_boosted)
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
