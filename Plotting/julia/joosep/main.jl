#!/usr/bin/env julia
#addprocs(4; exename=joinpath(Pkg.dir(), "ROOT", "root-julia"), exeflags="-H /Users/joosep/Documents/julia/usr/lib")
@everywhere using ROOT, ROOTDataFrames, ROOTHistograms, HEP, DataFrames
wd = dirname(Base.source_path())
#wd = dirname(pwd())

function sendto(p::Int; args...)
    for (nm, val) in args
        @spawnat(p, eval(Main, Expr(:(=), nm, val)))
    end
end

function sendto(ps::Vector{Int}; args...)
    for p in ps
        sendto(p; args...)
    end
end

sendto(workers(), wd=wd)

@everywhere cd(wd)
@everywhere include("$wd/ntuple.jl")
@everywhere using Analysis, ROOTHistograms

path = "/Users/joosep/Documents/tth/data/ntp/v12/Sep9_jec_jer"

f = "$path/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_ttll.root"
df = TreeDataFrame([f]; treename="tree")
n = length(df)

args = Any[]
chunksize = 50000 
for i=1:chunksize:n
    push!(args, (f, :ttjets, i, min(n, i+chunksize-1)))
end
println(args)

@everywhere process(args) = Analysis.process_sample(args[1], args[2]; range=args[3]:args[4])
#@everywhere process(args) = println(args)

function main()
    res = map(process, args)
    println(res)
    ret = reduce(+,
        Dict(),
        res 
    )
    return ret
end #main

ret = main()

function systematize_output(ret)
    newret = Dict()
    for (k, v) in ret
        k = collect(k)
        println(k, " ", typeof(v))
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

newret = systematize_output(ret)
write_hists_to_file("hists.root", newret; verbose=false)
