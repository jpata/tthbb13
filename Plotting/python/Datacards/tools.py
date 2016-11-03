from __future__ import print_function

from collections import OrderedDict

from sparse import save_hdict
from utils import bins_to_category, reduce_dict, make_hist, make_hist_bins
from representations import KIT_SL_v13_DatacardRepresentation, DESY_DL_v13_DatacardRepresentation

def convert_categories_to_sob(datacard_representation, infile, outfile, sob_hi):
    """Given an input datacard file that contains all the categories and final discriminants,
    create a signal-over-background sorted plot of all the bins.
    
    Args:
        infile (string): Input file, should contain TH1D-s for each category
            $ rootls /mnt/t3nfs01/data01/shome/jpata/tth/datacards/v13/common/ttH_hbb_13TeV_sl.root | grep "^ttH_hbb" | grep final | head -n5
            ttH_hbb_finaldiscr_ljets_j4_t2
            ttH_hbb_finaldiscr_ljets_j4_t2_CMS_res_jDown
            ttH_hbb_finaldiscr_ljets_j4_t2_CMS_res_jUp
            ttH_hbb_finaldiscr_ljets_j4_t2_CMS_scale_jDown
            ttH_hbb_finaldiscr_ljets_j4_t2_CMS_scale_jUp
            ...

        outfile (TYPE): Description
        sob_hi (float): high value of SoB histogram
    Returns:
        TYPE: Description
    """
    nd = datacard_representation.get_representation(
        infile
    )


    print("categories in file")
    for cat in sorted(datacard_representation.all_categories):
        print(" " + cat)

    print("samples in file")
    for samp in sorted(datacard_representation.all_samples):
        print(" " + samp)

    print("systematics in file")
    for syst in sorted(datacard_representation.all_systematics):
        print(" " + syst)

    #create individual categories from bins
    nd2 = bins_to_category(nd)

    #create a dictionary with [bin category] -> signal over background value
    ret = reduce_dict(
        nd2,
        datacard_representation.calculate_signal_over_background
    )

    bins_sorted = sorted(ret.keys(), key=lambda x: ret[x], reverse=False)
    sob_data = [ret[b] for b in bins_sorted]

    #print best bins
    print("Best bins by SoB are")
    for bs in bins_sorted[-10:]:
        print(" {0} {1}".format(bs, ret[bs]))

    #create the [sample][systematic][bin category] -> (bin, error) dict
    #such that sample information is aggregated
    nd3 = OrderedDict()
    for samp in sorted(datacard_representation.all_samples):
        nd3[samp] = OrderedDict()
        for syst in datacard_representation.all_systematics:
            nd3[samp][syst] = OrderedDict()
            for cat, b in bins_sorted:
                if not nd[cat][samp].has_key(syst):
                    nd3[samp][syst][(cat, b)] = (0.0, 0.0)
                else:
                    nd3[samp][syst][(cat, b)] = nd[cat][samp][syst][b]


    #convert bins to histogram with name={sample}_sob_{systematic}
    hists = OrderedDict()
    for samp in nd3.keys():
        for syst in nd3[samp].keys():
            name = "_".join([samp, "sob", syst])
            if len(nd3[samp][syst]) > 0:
                name = name.replace("_nominal", "")
                hists[name] = make_hist(
                    name,
                    nd3[samp][syst].values(),
                    sob_data,
                    nbins=20,
                    lo=0.0,
                    hi=sob_hi
                )

    print("saving {0} histograms".format(
        len(hists)
    ))
    save_hdict(outfile, hists)

if __name__ == "__main__":

    dcard_repr_sl = KIT_SL_v13_DatacardRepresentation()

    nd_tot = OrderedDict()
    nd = dcard_repr_sl.get_representation(
        "/mnt/t3nfs01/data01/shome/jpata/tth/datacards/v13/common/ttH_hbb_13TeV_sl.root"
    )
    for k in sorted(nd.keys()):
        print("sl cat {0}".format(k))
    nd_tot.update(nd)
    nd2_sl = bins_to_category(nd)
    for k1 in sorted(nd2_sl.keys()):
        for k2 in sorted(nd2_sl[k1].keys()):
            for k3 in sorted(nd2_sl[k1][k2].keys()):
                print("sl bincat {0} {1} {2}".format(k1, k2, k3))

    dcard_repr_dl = DESY_DL_v13_DatacardRepresentation()

    nd = dcard_repr_dl.get_representation(
        "/mnt/t3nfs01/data01/shome/jpata/tth/datacards/v13/common/ttH_hbb_13TeV_dl.root"
    )
    for k in sorted(nd.keys()):
        print("dl cat {0}".format(k))
    nd_tot.update(nd)
    nd2_dl = bins_to_category(nd)
    for k1 in sorted(nd2_dl.keys()):
        for k2 in sorted(nd2_dl[k1].keys()):
            for k3 in sorted(nd2_dl[k1][k2].keys()):
                print("dl bincat {0} {1} {2}".format(k1, k2, k3))

    print(nd2_sl.keys())
    print(nd2_dl.keys())

    ret_sl = reduce_dict(
        nd2_sl,
        dcard_repr_sl.calculate_signal_over_background
    )

    ret_dl = reduce_dict(
        nd2_dl,
        dcard_repr_dl.calculate_signal_over_background
    )

    ret_tot = OrderedDict()
    ret_tot.update(ret_sl)
    ret_tot.update(ret_dl)

    bins_sorted = sorted(ret_tot.keys(), key=lambda x: ret_tot[x], reverse=False)
    sob_data = [ret_tot[b] for b in bins_sorted]

    print("Best bins by SoB are")
    for bs in bins_sorted[-10:]:
        print(" {0} {1:.4f}".format(bs, ret_tot[bs]))

    nd3 = OrderedDict()
    for samp in sorted(set(dcard_repr_sl.all_samples + dcard_repr_dl.all_samples)):
        nd3[samp] = OrderedDict()
        for syst in set(dcard_repr_sl.all_systematics + dcard_repr_dl.all_systematics):
            nd3[samp][syst] = OrderedDict()
            for cat, b in bins_sorted:
                if nd_tot[cat].has_key(samp):
                    if not nd_tot[cat][samp].has_key(syst):
                        nd3[samp][syst][(cat, b)] = (0.0, 0.0)
                    else:
                        nd3[samp][syst][(cat, b)] = nd_tot[cat][samp][syst][b]


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
                    nbins=20,
                    lo=-4,
                    hi=0.0
                )

    for samp in nd3.keys():
        for syst in nd3[samp].keys():
            name = "_".join([samp, "bins", syst])
            if len(nd3[samp][syst]) > 0:
                name = name.replace("_nominal", "")
                hists[name] = make_hist_bins(
                    name,
                    nd3[samp][syst],
                    sob_data,
                    nbins=20,
                    lo=-4,
                    hi=0.0
                )

    print("saving {0} histograms".format(
            len(hists)
        ))
    save_hdict("sob.root", hists)
    # infile = 
    # outfile = "sob_sl.root"
    # convert_categories_to_sob(dcard_repr, infile, outfile, 1.0)

    # dcard_repr = DESY_DL_v13_DatacardRepresentation()
    # infile = "/mnt/t3nfs01/data01/shome/jpata/tth/datacards/v13/common/ttH_hbb_13TeV_dl.root"
    # outfile = "sob_dl.root"
    # convert_categories_to_sob(dcard_repr, infile, outfile, 0.5)
    
