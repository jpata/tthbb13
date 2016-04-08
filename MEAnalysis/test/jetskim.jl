
using ROOT, ROOTDataFrames, DataFrames, ROOTHistograms, Histograms

const OUTFILE = ARGS[1]

function process(df, ofname, maxev=-1)
    t0 = time()
    out = TreeDataFrame(
        ofname,

        #branch names
        [:pt, :eta, :id, :btagCSV, :btagBDT],

        #all branches are doubles
        [Float64, Float64, Float64, Float64, Float64],

        #all branches are scalars
        [Val{1}, Val{1}, Val{1}, Val{1}, Val{1}];

        treename="tree"
    )


    ntot = 0
    if maxev < 0
        maxev = nrow(df)
    end
    println("looping over $(maxev) rows")
    #loop over shuffled events in sorted order

    for iev=sort(randperm(nrow(df)))[1:maxev]
        load_row(df, iev, 
            [:is_sl, :njets, :jets_pt, :jets_eta, :jets_mcFlavour, :jets_btagCSV, :jets_btagBDT]
        )

        const nj = df.row.njets()
        const id = df.row.jets_mcFlavour()
        const pt = df.row.jets_pt()
        const eta = df.row.jets_eta()
        const btagCSV = df.row.jets_btagCSV()
        const btagBDT = df.row.jets_btagBDT()

        for ijet=1:nj
            #id = jetFlavour(id[ijet])
            out[ijet, :pt] = pt[ijet]
            out[ijet, :eta] = eta[ijet]
            out[ijet, :id] = id[ijet]
            out[ijet, :btagCSV] = btagCSV[ijet]
            out[ijet, :btagBDT] = btagBDT[ijet]
            ntot += Fill(out.tt)
        end
    end
    t1 = time()
    Write(out.tt, "tree", 4)
    println("Filled $(round(ntot/1024/1024,2)) Mb in $(nrow(out)) rows in $(t1-t0) seconds.")
    Close(out.tf)
end


path = "/Users/joosep/Documents/tth/data/ntp/v13/"
df = TreeDataFrame([
    "$path/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttbb.root",
    "$path/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttb.root",
    "$path/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_tt2b.root",
    "$path/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttcc.root",
    "$path/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttll.root",
]; treename="tree")

process(df, OUTFILE)
