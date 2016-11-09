import rootpy
import plotlib

tf = rootpy.io.File("sob_sl.root")
samps = [
    ("ttH_hbb", "tt+H"),
    ("ttH_htt", "tt+H (nonbb)"),
    ("diboson", "diboson"),
    ("ttbarW", "tt+W"),
    ("ttbarZ", "tt+Z"),
    ("wjets", "w+jets"),
    ("zjets", "z+jets"),
    ("singlet", "single-top"),
    ("ttbarOther", "tt+ll"),
    ("ttbarPlusBBbar", "tt+bb"),
    ("ttbarPlus2B", "tt+2b"),
    ("ttbarPlusB", "tt+b"),
    ("ttbarPlusCCbar", "tt+cc"),
]
ret = plotlib.draw_data_mc(
    tf,
    "sob",
    samps,
    ["ttH_hbb"],
    pattern="{sample}_{hname}",
    colors = [plotlib.colors[c] for c in [
        "ttH_hbb",
        "ttH_nonhbb",
        "diboson",
        "ttv",
        "ttv",
        "wjets",
        "wjets",
        "stop",
        "ttbarOther",
        "ttbarPlusBBbar",
        "ttbarPlus2B",
        "ttbarPlusB",
        "ttbarPlusCCbar"
    ]],
    systematics=[
        ("_CMS_res_jDown", "_CMS_res_jUp"),
        ("_CMS_scale_jDown", "_CMS_scale_jUp"),
        ("_CMS_ttH_CSVCErr1Down", "_CMS_ttH_CSVCErr1Up"),
        ("_CMS_ttH_CSVCErr2Down", "_CMS_ttH_CSVCErr2Up"),
        ("_CMS_ttH_CSVHFDown", "_CMS_ttH_CSVHFUp"),
        ("_CMS_ttH_CSVHFStats1Down", "_CMS_ttH_CSVHFStats1Up"),
        ("_CMS_ttH_CSVHFStats2Down", "_CMS_ttH_CSVHFStats2Up"),
    ]
);
ret["axes"][0].set_yscale("log")
ret["axes"][0].set_ylim(10, 10**6)
ret["axes"][1].set_xlim(0, 0.5)
ret["axes"][1].set_xlabel(r"$S/\sqrt{B}$")
ret["axes"][0].set_ylabel(r"events / bin")

plotlib.svfg("sob.pdf")