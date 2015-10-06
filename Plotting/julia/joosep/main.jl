#!/usr/bin/env julia
#addprocs(4)

const TIME0 = time()

const wd = dirname(Base.source_path())

include("utils.jl")
@everywhere using ROOT, ROOTDataFrames, ROOTHistograms, HEP, DataFrames

# Go to work dir on all workers
sendto(workers(), wd=wd)
@everywhere cd(wd)

@everywhere include("$wd/ntuple.jl")
@everywhere using Analysis, ROOTHistograms

@everywhere process(args) = Analysis.process_sample(args[1], args[2]; range=args[3]:args[4])

function main()
    res = pmap(process, args)
    ret = reduce(+,
        Dict(),
        res 
    )
    return ret
end #main

function systematize_output(ret)
    newret = Dict()
    for (k, v) in ret
        k = collect(k)
        #println(k, " ", typeof(v))
        name = join(k[1:end-2], "/")
        if k[end] == :nominal
            name = "$name/$(k[end-1])"
        else
            name = "$name/$(k[end-1])_$(k[end])"
        end
        newret[name] = v
    end
    return newret
end

const path = "/Users/joosep/Documents/tth/data/ntp/v13/"

samples = Dict(
    :ttH_hbb => "$path/ttHTobb_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root",
    :ttbarPlus2B => "$path/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_tt2b.root",
    :ttbarPlusB => "$path/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttb.root",
    :ttbarPlusBBbar => "$path/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttbb.root",
    :ttbarPlusCCbar => "$path/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttcc.root",
    :ttbarOther => "$path/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttll.root",
)
function make_args(f, stype, chunksize)
    args = Any[]
    const df = TreeDataFrame([f]; treename="tree")
    const n = length(df)
    for i=1:chunksize:n
        push!(args, (f, stype, i, min(n, i+chunksize-1)))
    end
    return args
end

const chunksize = 500000 

function make_args(samples::Dict, chunksize)
    args = Any[]
    for (sn, fn) in samples
        a = make_args(fn, sn, chunksize)
        push!(args, a)
    end
    return vcat(args...)
end

const args = make_args(samples, chunksize)

const ret = main()
const newret = systematize_output(ret)

write_hists_to_file("hists_main.root", newret; verbose=false)

const TIME1 = time()
println("elapsed time: ", @sprintf("%.2f", TIME1-TIME0), "s")
