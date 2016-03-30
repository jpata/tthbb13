#!/usr/bin/env python
import ROOT
import sys, imp, os, copy
def PrintDatacard(categories, event_counts, filenames, dcof):

    number_of_bins = len(categories)
    number_of_backgrounds = len(list(set(reduce(lambda x,y:x+y, [c.processes for c in categories], [])))) - 1 
    analysis_categories = list(set([c.name for c in categories]))

    
    dcof.write("imax {0}\n".format(number_of_bins))
    dcof.write("jmax {0}\n".format(number_of_backgrounds))
    dcof.write("kmax *\n")
    dcof.write("---------------\n")

    for cat in categories:
        analysis_var = cat.discriminator
        dcof.write("shapes * {0} {1} $PROCESS/$CHANNEL/{2} $PROCESS/$CHANNEL/{2}_$SYSTEMATIC\n".format(
            cat.name,
            filenames[cat.name],
            analysis_var)
        )
        
    dcof.write("---------------\n")

    dcof.write("bin\t" +  "\t".join(analysis_categories) + "\n")
    dcof.write("observation\t" + "\t".join("-1" for _ in analysis_categories) + "\n")
    dcof.write("---------------\n")

    bins        = []
    processes_0 = []
    processes_1 = []
    rates       = []

    # Conversion: 
    # Example: ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8_hbb -> ttH_hbb

    for cat in categories:
        for i_sample, sample in enumerate(cat.processes):
            bins.append(cat.name)
            processes_0.append(sample)
            if sample in cat.signal_processes:
                i_sample = -i_sample
            processes_1.append(str(i_sample))
            rates.append(str(event_counts[cat.name][sample]))

    dcof.write("bin\t"+"\t".join(bins)+"\n")
    dcof.write("process\t"+"\t".join(processes_0)+"\n")
    dcof.write("process\t"+"\t".join(processes_1)+"\n")
    dcof.write("rate\t"+"\t".join(rates)+"\n")
    dcof.write("---------------\n")
    
    
    
    # Gather all shape uncerainties
    all_shape_uncerts = []
    all_scale_uncerts = []
    for cat in categories:
        for proc in cat.processes:
            all_shape_uncerts.extend(cat.shape_uncertainties[proc].keys())
            all_scale_uncerts.extend(cat.scale_uncertainties[proc].keys())
    # Uniquify
    all_shape_uncerts = sorted(list(set(all_shape_uncerts)))
    all_scale_uncerts = sorted(list(set(all_scale_uncerts)))
    
    for syst in all_shape_uncerts:
        dcof.write(syst + "\t shape \t")
        for cat in categories:
            for proc in cat.processes:
                if (cat.shape_uncertainties.has_key(proc) and
                    cat.shape_uncertainties[proc].has_key(syst)):
                    dcof.write(str(cat.shape_uncertainties[proc][syst]))
                else:
                    dcof.write("-")
                dcof.write("\t")
        dcof.write("\n")
    

    for syst in all_scale_uncerts:
        dcof.write(syst + "\t lnN \t")
        for cat in categories:
            for proc in cat.processes:
                if (cat.scale_uncertainties.has_key(proc) and
                    cat.scale_uncertainties[proc].has_key(syst)):
                    dcof.write(str(cat.scale_uncertainties[proc][syst]))
                else:
                    dcof.write("-")
                dcof.write("\t")
        dcof.write("\n")
    # 
    # shapename = os.path.basename(datacard.output_datacardname)
    # shapename_base = shapename.split(".")[0]
    # dcof.write("# Execute with:\n")
    # dcof.write("# combine -n {0} -M Asymptotic -t -1 {1} \n".format(shapename_base, shapename))
