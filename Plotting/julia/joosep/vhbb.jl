using ROOT, ROOTDataFrames, DataFrames, ROOTHistograms, Histograms

pad(x) = [-Inf, x..., Inf]

function jetFlavour(x)
    ax = abs(x)
    if ax == 5
        return :b
    elseif ax == 4
        return :c
    end
    return :l
end

type Jet
    pt::Float64
    eta::Float64 
    btag_csv::Float64
    btag_bdt::Float64
    id::Symbol
end


type Lepton
    pt::Float64
    eta::Float64 
    relIso::Float64
    pdgId::Int64
end

function makeLeptons(row)
    nlep = row.nselLeptons()
    leptons = Array(Lepton, nlep)

    pt = row.selLeptons_pt()
    eta = row.selLeptons_eta()
    iso = row.selLeptons_relIso03()
    pdgid = row.selLeptons_pdgId()
    for i=1:nlep
        leptons[i] = Lepton(pt[i], eta[i], iso[i], pdgid[i])
    end
    return leptons
end

function process(df; isMC=true, weight=1.0)

    flavours = isMC ? [:l, :c, :b] : [:any]

    ret = Dict()
    for sel in [:nosel, :jge6_tge2]
        for fl in flavours
            ret[(sel, :btag1, fl)] = ErrorHistogram(linspace(0, 1, 101) |> pad)
            ret[(sel, :btag2, fl)] = ErrorHistogram(linspace(-1, 1, 101) |> pad)
        end
    end

    enabled_rows = [
    :json,
    :nJet,
    :Jet_pt, :Jet_eta,
    :Jet_btagCSV, :Jet_btagBDT,
    :nselLeptons, :selLeptons_pt, :selLeptons_eta, :selLeptons_relIso03, :selLeptons_pdgId
    ]
    if isMC
        push!(enabled_rows, :Jet_mcFlavour)
    end

    println("processing $(nrow(df)) events")
    for iev=1:nrow(df)
        load_row(df, iev, enabled_rows)

        df.row.json() == 1 || continue
        leptons = makeLeptons(df.row)
        goodmuons = filter(
            x->x.pt>20 && abs(x.eta)<2.5 && x.relIso < 0.15 && abs(x.pdgId)==13,
            leptons
        )

        nj = df.row.nJet()
        if isMC
            ids = df.row.Jet_mcFlavour()
        end
        pt = df.row.Jet_pt()
        eta = df.row.Jet_eta()
        btag_1 = df.row.Jet_btagCSV()
        btag_2 = df.row.Jet_btagBDT()
        
        jets = Array(Jet, nj)
        for ijet=1:nj
            if isMC
                id = jetFlavour(ids[ijet])
            else
                id = :any
            end
            jets[ijet] = Jet(pt[ijet], eta[ijet], btag_1[ijet], btag_2[ijet], id)
            if pt[ijet] > 30 && abs(eta[ijet]) < 2.5
                #println(btag_1[ijet], " ", btag_2[ijet])
                push!(ret[(:nosel, :btag1, id)], btag_1[ijet], weight)
                push!(ret[(:nosel, :btag2, id)], btag_2[ijet], weight)
            end
        end

        goodjets = filter(x->x.pt>30 && abs(x.eta)<4.0, jets)
        bjets = filter(x->x.btag_csv > 0.85, goodjets)

        if length(goodmuons)==1 && length(goodjets)>=5 && length(bjets)>=2
            for jet in goodjets
                push!(ret[(:jge6_tge2, :btag1, jet.id)], jet.btag_csv, weight)
                push!(ret[(:jge6_tge2, :btag2, jet.id)], jet.btag_bdt, weight)
            end
        end

    end
    return ret
end

const path = "/Users/joosep/Documents/tth/data/ntp/v13/vhbb/"
const samples = Dict(
    :SingleMuon => ("$path/SingleMuon.root", false),
    :JetHT => ("$path/JetHT.root", false),
    :BTagCSV => ("$path/BTagCSV.root", false),
    :ttjets => ("$path/ttjets.root", true),
)

function getCount(fn)
    rfile = TFile(fn)
    hcount = root_cast(TH1D, Get(rfile, "Count"))
    bc = GetBinContent(hcount, 1)
    Close(rfile)
    return bc
end

const XS = Dict(
    :ttjets => 831.76,
)

totret = Dict()
for (name, (file, isMC)) in samples
    df = TreeDataFrame([file]; treename="tree")

    fi = open("df.txt", "w")
    print(fi, df)
    close(fi)

    ngen = isMC ? getCount(file) : 1.0
    xs = get(XS, name, 1.0)
    ret = process(df; isMC=isMC, weight=xs/ngen)
    for (k,v) in ret
        ks = join(k, "_")
        totret["$name/$ks"] = v
    end
end

write_hists_to_file("hists_vhbb.root", totret; verbose=false)
