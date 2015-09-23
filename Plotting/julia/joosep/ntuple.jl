#!/usr/bin/env julia
println("including ntuple.jl on pid=", myid())
include("kinematics.jl")

module Analysis

using Kinematics, HEP, Histograms, ROOT, ROOTDataFrames, ROOTHistograms, DataFrames

const LUMI = 10000.0

fill! = push!

function process_event!(results, ev, prefix, syst)
    if ev.numJets == 5
        if ev.nBCSVM == 2
            fill_histograms_1!(results, ev, (prefix, :sl_j5_t2, ), syst)
        elseif ev.nBCSVM == 3
            fill_histograms_1!(results, ev, (prefix, :sl_j5_t3, ), syst)
        elseif ev.nBCSVM >= 4
            fill_histograms_1!(results, ev, (prefix, :sl_j5_tge4, ), syst)
        end
    elseif ev.numJets >= 6
        if ev.nBCSVM == 2
            fill_histograms_1!(results, ev, (prefix, :sl_jge6_t2, ), syst)
        elseif ev.nBCSVM == 3
            fill_histograms_1!(results, ev, (prefix, :sl_jge6_t3, ), syst)
        elseif ev.nBCSVM >= 4
            fill_histograms_1!(results, ev, (prefix, :sl_jge6_tge4, ), syst)
        end
    end

end

function make_results(prefix, syst)

    jet_pt_bins = linspace(0, 500, 100)

    results = Dict{Any, ErrorHistogram}()
    for k in [:sl_j5_t2, :sl_j5_t3, :sl_j5_tge4, :sl_jge6_t2, :sl_jge6_t3, :sl_jge6_tge4]
        results[tuple(prefix, k, :jet0_pt, syst)] = ErrorHistogram(jet_pt_bins)
    end

    return results
end

function fill_histograms_1!(results, ev, key, syst)
    fill!(
        results[tuple(key..., :jet0_pt, syst)],
        pt(ev.jets[1]),
        weight(ev, LUMI)
    )
end

const ResultDict = Dict{Any, ErrorHistogram}
function process_sample(fn, prefix;range=nothing, do_cache=true, nprint=5)
    println("processing $fn")
    isfile(fn) || error("file not found: $fn")
    df = TreeDataFrame([fn]; treename="tree")
    if range == nothing
        range = 1:length(df)
    end
    results = ResultDict()
    for syst in [:nominal, :JESUp, :JESDown]
        results += make_results(prefix, syst)
    end

    if do_cache
        SetCacheSize(df.tt, 0)
        SetCacheSize(df.tt, 16 * 1024 * 1024)
        brs = ["jets_*", "njets", "is_*", "numJets*", "nBCSVM*", "weight_xs", "genWeight"]
        enable_branches(df, brs)
        for b in brs
            AddBranchToCache(df.tt, b)
        end
    end #do_cache

    const t0 = time()
    #for i=1:nrow(df)

    ntot = 0
    nloaded = 0

    fail_lep = 0
    idx1 = 1
    idx2 = 1
    println("looping $range")
    for idx1 in range

        idx1%10000==0 && println("ev=$idx1 dt(10k)=", Int64(round(idx1/(time()-t0))))

        #Load the TTree row
        nloaded += load_row(df, idx1)
        if idx1<=nprint
            println("---")
            println("read event")
        end

        df.row.numJets() >= 3 || continue
        df.row.nBCSVM() >= 1 || continue

        #Get the primary event interpretation
        const ev = parse_event(df)
        if idx1<=nprint
            println("$(ev.run):$(ev.lumi):$(ev.evt)")
        end
        const ev_JESUp = parse_event(df, Val{:JESUp})
        const ev_JESDown = parse_event(df, Val{:JESDown})
        evd = Dict(:nominal=>ev, :JESUp=>ev_JESUp, :JESDown=>ev_JESDown)
        
        if idx1<=nprint
            for (syst, ev) in evd
                println("syst=$syst ", string(ev))
            end
        end
        for (syst, ev) in evd
            process_event!(results, ev, prefix, syst)
        end

        ntot += 1
        idx2 += 1
    end
    const t1 = time()
    dt = t1 - t0
    nloaded = nloaded / 1024 / 1024
    const speed = length(range) / dt
    println("processed $range total, $idx2 passed, $(round(speed, 0)) ev/s, $(round(nloaded/dt)) Mb/s")
    return results
end

#Define a way to add two result dictionaries together
import Base.+
function +(d1::Dict, d2::Dict)
    s1 = Set(keys(d1))
    s2 = Set(keys(d2))
    ret = Dict()

    #is common in both, add both
    for k in intersect(s1, s2)
        ret[k] = d1[k]+d2[k]
    end

    #is in d1 only
    for k in setdiff(s1, s2)
        ret[k] = d1[k]
    end

    #is in d2 only
    for k in setdiff(s2, s1)
        ret[k] = d2[k]
    end
    return ret
end

end #module Analysis
