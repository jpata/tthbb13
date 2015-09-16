#!/usr/bin/env julia
include("kinematics.jl")

module Analysis

using DataFrames, ROOT, ROOTDataFrames, Histograms, ROOTHistograms
using HEP
import Base.string

using HEP
using Kinematics

const LUMI = 10000.0


function string(ev::Event, l::Int64=0) 
    s = "$(length(ev.jets))J $(length(ev.leptons))l Vt=$(ev.vtype)"
    if l>0
        for x in ev.leptons
            s = string(s, "\n l ", string(x))
        end
        for x in ev.signal_leptons
            s = string(s, "\n L ", string(x))
        end
        for x in ev.jets
            s = string(s, "\n j ", string(x))
        end
    end
    return s
end

const dict_type = Dict{Symbol,Union(Array{Symbol,1},Symbol)}

function parse_branches{P <: Jet}(
    df::TreeDataFrame,
    p::Type{P}
    )
    const n = df.row.njets()

    const pt = df.row.jets_pt()
    const eta = df.row.jets_eta()
    const phi = df.row.jets_phi()
    const mass = df.row.jets_mass()
    const id = df.row.jets_mcFlavour()
    const csv = df.row.jets_btagCSV()
 
    particles = P[
        P(
            FourVectorSph(
                pt[k],
                eta[k],
                phi[k],
                mass[k]
            ),
            id[k],
            csv[k]
        ) for k=1:n
    ]
    return particles
end

function parse_event{T}(df::TreeDataFrame{T})
    jets = parse_branches(df, Jet)
    #leps = parse_branches(df, i, Lepton)
    #sig_leps = parse_branches(df, i, SignalLepton)

    #vtype_ = df[i, :hypo1]
    Event(
        jets,
        df.row.numJets(),
        df.row.nBCSVM(),

        df.row.is_sl(),
        df.row.is_dl(),
        df.row.weight_xs(),
        df.row.genWeight(),

        df.row.run(),
        df.row.lumi(),
        df.row.evt(),
    )
end


@generated function parse_event{T, S}(df::TreeDataFrame{T}, s::Type{Val{S}})
    println("generating parse_event{$df, $s}")

    syst = s.parameters[1].parameters[1]
    println("s=$s syst=$syst")
    ex = quote
        jets = parse_branches(df, Jet)
        $syst
        Event(
            jets,
            $(symbol("df.row.numJets_", syst))(),
            df.row.nBCSVM_$syst(),

            df.row.is_sl(),
            df.row.is_dl(),
            df.row.weight_xs(),
            df.row.genWeight(),

            df.row.run(),
            df.row.lumi(),
            df.row.evt(),
        )
    end
    println(ex)
    return ex
end



function process_sample(fn::ASCIIString; do_cache=true)
    println("processing $fn")
    isfile(fn) || error("file not found: $fn")
    df = TreeDataFrame([fn]; treename="tree")

    results = Dict(
        :sl_jge6_tge4=>Dict(
            :jet0_pt=>ErrorHistogram(linspace(0,500, 100))
        )
    )

    if do_cache
        SetCacheSize(df.tt, 0)
        SetCacheSize(df.tt, 16 * 1024 * 1024)
        brs = ["jets_*", "njets", "is_*", "numJets", "nBCSVM", "weight_xs", "genWeight"]
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
    for idx1=1:100000

        idx1%10000==0 && println(idx1, " ", Int64(round(idx1/(time()-t0))))

        #Load the TTree row
        nloaded += load_row(df, idx1)
        df.row.numJets() >= 3 || continue
        df.row.nBCSVM() >= 1 || continue

        #Get the primary event interpretation
        const ev = parse_event(df)
        const ev_JESUp = parse_event(df, Val{:JESUp})

        if ev.is_sl && ev.numJets>=6  && ev.nBCSVM>=4
            push!(
                results[:sl_jge6_tge4][:jet0_pt],
                pt(ev.jets[1]),
                weight(ev, LUMI)
            )
        end
        
        ntot += 1
        idx2 += 1
    end
    const t1 = time()
    dt = t1 - t0
    nloaded = nloaded / 1024 / 1024
    const speed = idx1 / dt
    println("processed $(round(speed, 0)) ev/s, $(round(nloaded/dt)) Mb/s")
    return results
end

import Base.+
function +(d1::Dict, d2::Dict)
    s1 = Set(keys(d1))
    s2 = Set(keys(d2))
    ret = Dict()
    for k in intersect(s1, s2)
        ret[k] = d1[k]+d2[k]
    end
    for k in setdiff(s1, s2)
        ret[k] = d1[k]
    end
    for k in setdiff(s2, s1)
        ret[k] = d2[k]
    end
    return ret
end

function main()
    ret = Dict()
    ret += process_sample("/Users/joosep/Documents/tth/data/ntp/v12/Sep9_jec_jer/ttHTobb_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9.root")
    return ret
end #main

end #module Analysis
