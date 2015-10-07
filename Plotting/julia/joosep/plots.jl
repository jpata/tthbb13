using ROOT, ROOTDataFrames, Histograms, ROOTHistograms, PyCall
@pyimport TTH.Plotting.Datacards.MiniSamples as minisamples

samples = Dict{Symbol, ASCIIString}()
for (k, v) in minisamples.samples_dict
    samples[symbol(k)] = v
end

function process_sample(name, cutfunc, file)
    df = TreeDataFrame([file]; treename="tree")

    hists = Dict(
        :mem_SL_0w2h2t=>ErrorHistogram([-Inf, linspace(0.0, 1.0, 7)..., Inf]),
        :mem_SL_0w2h2t_sj=>ErrorHistogram([-Inf, linspace(0.0, 1.0, 7)..., Inf]),
        :mem_SL_2w2h2t=>ErrorHistogram([-Inf, linspace(0.0, 1.0, 7)..., Inf]),
        :mem_SL_2w2h2t_sj=>ErrorHistogram([-Inf, linspace(0.0, 1.0, 7)..., Inf]),
        :mva=>ErrorHistogram([-Inf, linspace(0.0, 1.0, 21)..., Inf]),
    )
    
    memfn(row, i, w=0.2) = row.mem_tth_p()[i] > 0 ? row.mem_tth_p()[i] / (row.mem_tth_p()[i] + w*row.mem_ttbb_p()[i]) : 0.0
    function fillfunc(row)
        push!(hists[:mem_SL_0w2h2t], memfn(row, 1, 0.2))
        push!(hists[:mem_SL_0w2h2t_sj], memfn(row, 11, 0.2))
        push!(hists[:mem_SL_2w2h2t], memfn(row, 6, 0.2))
        push!(hists[:mem_SL_2w2h2t_sj], memfn(row, 10, 0.2))
        push!(hists[:mva], row.tth_mva())
    end
    
    branches = [
        :is_sl, :is_dl,
        :mem_tth_p, :mem_ttbb_p,
        :numJets, :nBCSVM,
        :btag_LR_4b_2b,
        :njets,
        :jets_pt,
        :n_excluded_bjets, :ntopCandidate, :tth_mva
    ]
    loop(df,
        fillfunc,
        cutfunc,
        branches
    )

    ret = Dict()
    for k in keys(hists)
        ret["$name/$k"] = hists[k] 
    end
    return ret
end

cutfuncs = Dict(
    :sl_jge6_tge4_boosted => row -> (
        row.is_sl() == 1 &&
        row.numJets() >= 6 &&
        row.nBCSVM() >= 4 &&
        row.btag_LR_4b_2b() > 0.95 && row.n_excluded_bjets() < 2 && row.ntopCandidate() == 1
    ),
    :sl_jge6_t3_boosted => row -> (
        row.is_sl() == 1 &&
        row.numJets() >= 6 &&
        row.nBCSVM() == 3 &&
        row.btag_LR_4b_2b() > 0.95 && row.n_excluded_bjets() < 2 && row.ntopCandidate() == 1
    ),
)

res = Dict()
for sn in keys(samples)
    for (cutname, cutfunc) in cutfuncs
        r = process_sample("$sn/$cutname", cutfunc, samples[sn])
        merge!(res, r)
    end
end

write_hists_to_file("hists.root", res; verbose=false)
