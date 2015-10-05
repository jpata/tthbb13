using ROOT, ROOTDataFrames, Histograms, ROOTHistograms

const path = "/Users/joosep/Documents/tth/data/ntp/v13/"

samples = Dict(
    :ttH_hbb => "$path/ttHTobb_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root",

    :ttbarPlus2B => "$path/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_tt2b.root",
    :ttbarPlusB => "$path/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttb.root",
    :ttbarPlusBBbar => "$path/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttbb.root",
    #:ttbarPlusCCbar => "$path/ttHTobb_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root",
    #:ttbarOther => "$path/ttHTobb_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root",
)

function process_sample(name, file)
    df = TreeDataFrame([file]; treename="tree")

    hists = Dict(
        :mem_SL_0w2h2t=>ErrorHistogram([-Inf, linspace(0.0, 1.0, 7)..., Inf]),
        :mem_SL_0w2h2t_sj=>ErrorHistogram([-Inf, linspace(0.0, 1.0, 7)..., Inf]),
        :mem_SL_2w2h2t=>ErrorHistogram([-Inf, linspace(0.0, 1.0, 7)..., Inf]),
        :mem4=>ErrorHistogram([-Inf, linspace(0.0, 1.0, 7)..., Inf]),
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

    loop(df,
        fillfunc,
        #row-> row.is_sl() == 1 && row.numJets() == 4 && row.nBCSVM() == 2 && row.btag_LR_4b_2b() > 0.95 && row.n_excluded_bjets() < 2 && row.ntopCandidate() == 1,
        row-> row.is_sl() == 1 && row.numJets() == 4 && row.nBCSVM() == 2 && row.btag_LR_4b_2b() > 0.95,
        [:is_sl, :is_dl, :mem_tth_p, :mem_ttbb_p, :numJets, :nBCSVM, :btag_LR_4b_2b, :njets, :jets_pt, :n_excluded_bjets, :ntopCandidate, :tth_mva],
        1:length(df),
    )
    return Dict(
        "$name/mem_SL_0w2h2t"=>hists[:mem1],
        "$name/mem_SL_0w2h2t_sj"=>hists[:mem2],
        "$name/mem_SL_2w2h2t"=>hists[:mem3],
        "$name/mem_SL_2w2h2t_sj"=>hists[:mem4],
        "$name/mva"=>hists[:mva],
    )
end

res = Dict()
for sn in keys(samples)
    r = process_sample(sn, samples[sn])
    merge!(res, r)
end

write_hists_to_file("hists.root", res; verbose=false)
