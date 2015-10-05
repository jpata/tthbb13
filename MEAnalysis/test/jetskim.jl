
using ROOT, ROOTDataFrames, DataFrames, ROOTHistograms, Histograms

function process(df, ofname)
    out = TreeDataFrame(
        ofname,

        #branch names
        [:pt, :eta, :id, :btag1],

        #all branches are doubles
        [Float64, Float64, Float64, Float64],

        #all branches are scalars
        [Val{1}, Val{1}, Val{1}, Val{1}];

        treename="tree"
    )


    println("looping over $(nrow(df)) rows")
    ntot = 0
    for iev=1:nrow(df)
        load_row(df, iev, 
            [:is_sl, :njets, :jets_pt, :jets_eta, :jets_mcFlavour, :jets_btagCSV]
        )

        const nj = df.row.njets()
        const id = df.row.jets_mcFlavour()
        const pt = df.row.jets_pt()
        const eta = df.row.jets_eta()
        const btag_1 = df.row.jets_btagCSV()

        for ijet=1:nj
            #id = jetFlavour(id[ijet])
            out[ijet, :pt] = pt[ijet]
            out[ijet, :eta] = eta[ijet]
            out[ijet, :id] = id[ijet]
            out[ijet, :btag1] = btag_1[ijet]
            ntot += Fill(out.tt)
            #push!(ret, Float64[pt[ijet], eta[ijet], id[ijet], btag_1[ijet]])
        end
    end
    Write(out.tt, "tree", 4)
    println("Filled $(round(ntot/1024/1024,2)) Mb in $(nrow(out)) rows.")
    Close(out.tf)
end


path = "/Users/joosep/Documents/tth/data/ntp/v13/"
df = TreeDataFrame([
    "$path/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttbb.root",
    "$path/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttb.root",
    "$path/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_tt2b.root",
    "$path/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttcc.root",
]; treename="tree")

process(df, "jets.root")
