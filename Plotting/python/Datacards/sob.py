from __future__ import print_function

from collections import OrderedDict

from sparse import save_hdict
from utils import bins_to_category, reduce_dict, make_hist, make_hist_bins
from representations import KIT_SL_v13_DatacardRepresentation, DESY_DL_v13_DatacardRepresentation, CombineRepresentation

import numpy as np

if __name__ == "__main__":
    
    path = "/Users/joosep/Documents/datacards_v13/"

    dcard_repr = CombineRepresentation()
    hists = dcard_repr.get_representation(path + "mlfitNamesShapes.root")

    dcard_repr_sl = KIT_SL_v13_DatacardRepresentation()
    nd_tot = OrderedDict()
    nd = dcard_repr_sl.get_representation(
        path + "/common/ttH_hbb_13TeV_sl.root"
    )
    nd_tot.update(nd)

    # nd2_sl = bins_to_category(nd)

    dcard_repr_dl = DESY_DL_v13_DatacardRepresentation()

    nd = dcard_repr_dl.get_representation(
        path + "/common/ttH_hbb_13TeV_dl.root"
    )
    nd_tot.update(nd)

    category_mapper = {
        'dl_3j3t': 'dl_j3_t3_BDT',
        'dl_ge4j3t_high': 'dl_gej4_t3_high_BDT',
        'dl_ge4j3t_low': 'dl_gej4_t3_low_BDT',
        'dl_ge4jge4t_high': 'dl_gej4_get4_high_BDT',
        'dl_ge4jge4t_low': 'dl_gej4_get4_low_BDT',
        'sl_j4_t4_high': 'finaldiscr_ljets_j4_t4_high',
        'sl_j4_t4_low': 'finaldiscr_ljets_j4_t4_low',
        'sl_j5_tge4_high': 'finaldiscr_ljets_j5_tge4_high',
        'sl_j5_tge4_low': 'finaldiscr_ljets_j5_tge4_low',
        'sl_jge6_t3_high': 'finaldiscr_ljets_jge6_t3_high',
        'sl_jge6_t3_low': 'finaldiscr_ljets_jge6_t3_low',
        'sl_jge6_tge4_high': 'finaldiscr_ljets_jge6_tge4_high',
        'sl_jge6_tge4_low': 'finaldiscr_ljets_jge6_tge4_low',
    }

    # histo_binning = np.array([
    #     -2.4,
    #     -2.3,
    #     -2.2,
    #     -2.1,
    #     -2.0,
    #     -1.9,
    #     -1.8,
    #     -1.7,
    #     -1.6,
    #     -1.5,
    #     -1.4,
    #     -1.3,
    #     -1.2,
    #     -1.1,
    #     -1.0,
    #     -0.9,
    #     -0.8,
    #     -0.6,
    #     -0.4,
    #     -0.2
    # ])

    histo_binning = np.array([
        -2.4,
        -2.2,
        -2.0,
        -1.8,
        -1.6,
        -1.4,
        -1.2,
        -1.0,
        -0.8,
        -0.6,
        -0.4,
        -0.2
    ])

    for cat in hists.keys():
        hists[cat]["data_obs"] = OrderedDict()
        hists[cat]["data_obs"]["shapes_prefit"] = nd_tot[category_mapper[cat]]["data_obs"]["nominal"]
        for samp in hists[cat].keys():
            for syst in hists[cat][samp].keys():
                old_d = hists[cat][samp][syst]
                new_d = OrderedDict()
                for ibin in range(1, len(hists[cat]["data_obs"]["shapes_prefit"]) + 1):
                    label = "bin_{0}".format(ibin)
                    new_d[label] = old_d[label]
                hists[cat][samp][syst] = new_d

    bins = bins_to_category(hists)
    bins_sob = reduce_dict(
        bins,
        dcard_repr.calculate_signal_over_background
    )
    bins_sorted = sorted(bins_sob.keys(), key=lambda x: bins_sob[x], reverse=False)
    sob_data = [bins_sob[b] for b in bins_sorted]
    print("Best bins by SoB are")
    for bs in bins_sorted[-10:]:
        print(" {0} {1:.4f}".format(bs, bins_sob[bs]))

    nd3 = OrderedDict()
    for samp in ["total_signal", "total_background", "data_obs"]:
        nd3[samp] = OrderedDict()
        for syst in ["shapes_prefit", "shapes_fit_s", "shapes_fit_b"]:
            nd3[samp][syst] = OrderedDict()
            if not hists[cat][samp].has_key(syst):
                continue
            for cat, b in bins_sorted:
                nd3[samp][syst][(cat, b)] = hists[cat][samp][syst][b]

    #convert bins to histogram with name={sample}_sob_{systematic}
    hists = OrderedDict()
    for samp in nd3.keys():
        for syst in nd3[samp].keys():
            name = "_".join([samp, "sob", syst])
            if len(nd3[samp][syst]) > 0:
                name = name.replace("_nominal", "")
                hists[name] = make_hist(
                    name,
                    nd3[samp][syst],
                    sob_data,
                    histo_binning
                )
    # for samp in nd3.keys():
    #     for syst in nd3[samp].keys():
    #         name = "_".join([samp, "bins", syst])
    #         if len(nd3[samp][syst]) > 0:
    #             name = name.replace("_nominal", "")
    #             hists[name] = make_hist_bins(
    #                 name,
    #                 nd3[samp][syst],
    #                 sob_data,
    #             )

    save_hdict("sob.root", hists)
