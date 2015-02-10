#!/usr/bin/env julia
include("kinematics.jl")

module Analysis

using DataFrames, ROOT, ROOTDataFrames
using HEP
import Base.string
using PyCall

@pyimport imp

fn = ""
if length(ARGS)==1
	fn = ARGS[1]
else
	fn = "cfg.py"
end

isfile(fn) || error("File error: $fn")

const CFG = imp.load_source("cfg", fn)[:process][:fwliteInput]
const SAMPLES = CFG[:samples]

const HYPOS = [:tthbb, :ttjets]
const BTAG_LR_HYPOS = [:ttjj, :ttbb]

using HEP
using Kinematics

module Cuts
	import ..CFG
	const muPtTight = float64(CFG[:lepPtTight][:_value])
	const muEtaTight = float64(CFG[:muEtaTight][:_value])
	const jetPt = float64(CFG[:jetPtThreshold][:_value])
	const jetEta = 2.5
end #module Cuts

import HEP: eta, phi
pt(x::AbstractParticle) = perp(x.p)
eta(x::AbstractParticle) = eta(x.p)
phi(x::AbstractParticle) = phi(x.p)
mass(x::AbstractParticle) = l(x.p)

string(x::FourVector) = @sprintf("(%.3f %.3f %.3f %.3f)", x.t, x.x, x.y, x.z)
string(x::FourVectorSph) = @sprintf("(%.3f %.3f %.3f %.3f)", x.perp, x.eta, x.phi, x.l)
string(p::Particle) = @sprintf("p=%s id=%d", string(p.p), p.id)
string(p::Jet) = @sprintf("p=%s id=%d b(csv)=%.3f", string(p.p), p.id, p.bdisc)
string(p::Lepton) = @sprintf("p=%s id=%d Ir=%.3f", string(p.p), p.id, p.iso)
string(p::SignalLepton) = "idx=$(p.idx + 1)"

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

module EventHypothesis
    const mumu = 0
    const ee = 1
    const mun = 2
    const en = 3
    const nn = 4
    const emu = 5
    const taumu = 6
    const taue = 7
    const taun = 8
    const tautau = 9
    const UNKNOWN_HYPO = 10
    const BAD_HYPO = 11

    lut = Dict{Int64, Symbol}([])

    for n in names(EventHypothesis, true)
    	if !(n in [:lut, :EventHypothesis, :Module, :eval])
    		EventHypothesis.lut[EventHypothesis.eval(n)] = n
    	end
    end

    function as{T <: Integer}(i::T)
    	_i = int(i)
    	haskey(lut, _i)|| error("could not parse $i as EventHypothesis")
    	return lut[_i]::Symbol
    end
end

function parse_branches{P <: Jet}(
	df::TreeDataFrame,
	i::Int64,
	p::Type{P}
	)
	const n = df[i, :n__jet]::Int32

	const pt = 		df[i, :jet__pt, Float32] 		|> float64
	const eta = 	df[i, :jet__eta, Float32] 		|> float64
	const phi = 	df[i, :jet__phi, Float32] 		|> float64
	const mass = 	df[i, :jet__mass, Float32] 		|> float64
	const id = 		df[i, :jet__id, Int32] 			|> int64
	const csv = 	df[i, :jet__bd_csv, Float32] 	|> float64
 
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

function parse_branches{P <: Lepton}(
	df::TreeDataFrame,
	i::Int64,
	p::Type{P}
	)
	const n = df[i, :n__lep]::Int32

	const pt = 		df[i, :lep__pt, Float32] 		|> float64
	const eta = 	df[i, :lep__eta, Float32] 		|> float64
	const phi = 	df[i, :lep__phi, Float32] 		|> float64
	const mass = 	df[i, :lep__mass, Float32] 		|> float64
	const id = 		df[i, :lep__id, Int32] 			|> int64
	const iso = 	df[i, :lep__rel_iso, Float32]	|> float64

	particles = P[
		P(
			FourVectorSph(
				pt[k],
				eta[k],
				phi[k],
				mass[k]
			),
			id[k],
			iso[k],
		) for k=1:n
	]

	return particles
end

function parse_branches{P <: SignalLepton}(
	df::TreeDataFrame,
	i::Int64,
	p::Type{P})
	nj = df[i, :n__sig_lep]::Int32

	particles = P[
		P(
			df[i, :sig_lep__idx, Int32][k]|>int64,
		) for k=1:nj
	]

	return particles
end

function parse_event(df::TreeDataFrame, i::Int64)
	jets = parse_branches(df, i, Jet)
	leps = parse_branches(df, i, Lepton)
	sig_leps = parse_branches(df, i, SignalLepton)

	vtype_ = df[i, :hypo1]
	Event(
		jets, leps, sig_leps,
		EventHypothesis.as(vtype_),
		assign_lepton_category(EventHypothesis.as(vtype_)),
		int64(df[i, :event__id]),
		int64(df[i, :event__run]),
		int64(df[i, :event__lumi]),
	)
end

#select single lepton events
#passes if there is exactly one good signal lepton
function select_sl(ev::Event)
	passes = false

	length(ev.signal_leptons) == 1 || return (passes, Lepton[])

	const sig_lep = first(ev.signal_leptons)
	const main_lep = ev.leptons[sig_lep.idx + 1]

	if ev.vtype == :en
		#println("SL e")

		abs(main_lep.id) == 11 || error("event incorrectly classified $(main_lep) $(ev.vtype)")
		passes = pt(main_lep) > Cuts.muPtTight
		passes = passes && abs(eta(main_lep)) < Cuts.muEtaTight

	elseif ev.vtype == :mun
		#println("SL mu")
		abs(main_lep.id) == 13 || error("event incorrectly classified $(main_lep) $(ev.vtype)")
	elseif ev.vtype == :taun
		#println("SL tau")
		abs(main_lep.id) == 15 || error("event incorrectly classified $(main_lep) $(ev.vtype)")
	end
	if passes
		#println("lepton passes SL")
	end

	return (passes, Lepton[main_lep])
end

function assign_lepton_category(vtype::Symbol)
	if vtype in [:en, :mun, :taun]
		return :sl
	elseif vtype in [:ee, :mumu, :emu, :taue]
		return :dl
	elseif vtype in [:nn]
		return :had
	end
	return vtype
end


#selects good jets and returns at most the 6 hardest jets
function select_jets(ev::Event)

	jets = Jet[]
	for jet in ev.jets
		passes = pt(jet) > Cuts.jetPt
		passes = passes && abs(eta(jet)) < Cuts.jetEta
		passes && push!(jets, jet)
	end

	jets = sort(jets, by=x->pt(x), rev=true)

	nmax = 6
	return jets[1:min(length(jets), nmax)]
end

const DEBUG = 2

#File with jet CSV distributions as histograms
const cp = ROOT.TFile(string(ENV["CMSSW_BASE"], "/src/TTH/MEAnalysis/", CFG[:pathToCP][:_value]))

import StatsBase.Histogram

function Histogram(h::TH1D)
	const nb = int32(GetNbinsX(h))
	bins = Float64[]
	contents = Float64[]
	for i=int32(1):nb
		push!(bins, GetBinLowEdge(h, i))
		push!(contents, GetBinContent(h, i))
	end
	push!(bins, GetBinLowEdge(h, nb + int32(1)))
	return Histogram{Float64, 1, (Vector{Float64}, )}((bins, ), contents, :right)
end

function findbin{T <: Real, N, E}(h::Histogram{T, N, E}, xs::Real)
    is = if h.closed == :right
        map((edge, x) -> searchsortedfirst(edge,x) - 1, h.edges, xs)
    else
        map(searchsortedlast, h.edges, xs)
    end
    return is
end

function findbin{T <: Real, E}(h::Histogram{T, 1, E}, x::Real)
    i = if h.closed == :right 
        searchsortedfirst(h.edges[1], x) - 1 
    else
        searchsortedlast(h.edges[1], x)
    end
    return i
end

#B-tagging probabilities
const btag_prob_maps = Dict(
	:b => Histogram(root_cast(TH1D, Get(cp, "csv_b_Bin0__csv_rec"))) |> HEP.normalize,
	:c => Histogram(root_cast(TH1D, Get(cp, "csv_c_Bin0__csv_rec"))) |> HEP.normalize,
	:l => Histogram(root_cast(TH1D, Get(cp, "csv_l_Bin0__csv_rec"))) |> HEP.normalize
)

#println(btag_prob_maps)

#Returns the probability density value of a jet, taking into account the true flavour
#and the jet CSV score
function pdf_bdisc(csv::Float64, flavour::Symbol)
	h = btag_prob_maps[flavour]
	b = findbin(h, csv)
	if b <= 0
		b = 1
	end
	if b > length(h.weights)
		b = length(h.weights)
	end

	#we know that b is inside the array bounds, don't do the check (unsafe but fast)
	@inbounds return h.weights[b]
end

function lh(jets, n_b)
	_P = 0.0
	nc = 0
	for comb in combinations(1:length(jets), n_b)
		p = 1.0
		for i in 1:length(jets)
			p = p * pdf_bdisc(jets[i].bdisc, i in comb ? :b : :l)
			nc += 1
		end
		_P += p
	end
	_P = _P / nc
	return _P
end

function flavour_index(ind, n_b, n_c)
	if ind>=1 && ind<1+n_b
		return 1 #b
	elseif ind>=1+n_b && ind<1+n_b+n_c
		return 2 #c
	else
		return 3 #l
	end
	
end

function lh(bdiscs::Array{Float64, 2}, njets::Int64, perms::Vector{Vector{Int64}}, n_b::Int64, n_c::Int64)
	_P = 0.0
	nc = 0
	const flavour_inds = Int64[flavour_index(i, n_b, n_c) for i=1:njets]
	for perm::Vector{Int64} in perms
		p = 1.0
		for i::Int64 in perm
			@inbounds p = p * bdiscs[flavour_inds[i], i]
			nc += 1
		end
		_P += p
	end
	_P = _P / nc
	return _P
end

dprintln(level::Int64, msg) = DEBUG>=level && println([" " for i=1:level]..., msg)

perms = Dict{Int64, Vector{Vector{Int64}}}(5=>collect(permutations(1:5)), 6=>collect(permutations(1:6)))

function calculate_btag_lr(bdiscs::Array{Float64, 2})

	njets = size(bdiscs, 2)
	l_ttbb = lh(bdiscs, njets, perms[njets], 4, 0)
	l_ttjj = lh(bdiscs, njets, perms[njets], 2, 0)
	ret = l_ttbb / (l_ttbb + l_ttjj)
	return isnan(ret) ? 0.0 : ret
end

function calculate_btag_lr_with_c(bdiscs::Array{Float64, 2})

	njets = size(bdiscs, 2)
	l_ttbb = 0.5 * (lh(bdiscs, njets, perms[njets], 4, 0) + lh(bdiscs, njets, perms[njets], 4, 1))
	l_ttjj = 0.5 * (lh(bdiscs, njets, perms[njets], 2, 0) + lh(bdiscs, njets, perms[njets], 2, 1))
	l_ttcc = 0.5 * (lh(bdiscs, njets, perms[njets], 2, 2) + lh(bdiscs, njets, perms[njets], 2, 3))
	ret = l_ttbb / (l_ttbb + l_ttjj + l_ttcc)
	return isnan(ret) ? 0.0 : ret
end

function process_sample(fn::ASCIIString)
	println("processing $fn")
	isfile(fn) || error("file not found: $fn")
	df = TreeDataFrame([fn], "tthNtupleAnalyzer/events")

	SetCacheSize(df.tt, 0)

	# ERROR: LoadError: TypeError: getfield: expected Symbol, got ASCIIString
	#  in process_sample at /home/joosep/mac-docs/tth/sw-slc6/CMSSW/src/TTH/Plotting/julia/joosep/ntuple.jl:387
	#  in main at /home/joosep/mac-docs/tth/sw-slc6/CMSSW/src/TTH/Plotting/julia/joosep/ntuple.jl:506


	for b in ["jet__*", "n__jet*". "n__lep*", "lep__*", "sig_lep*", "hypo1", "event*"]
	    #AddBranchToCache(df.tt, "$b")
	end
	SetCacheSize(df.tt, 256 * 1024 * 1024)

	ofdf = similar(
		DataFrame(
			event=Int64[], run=Int64[], lumi=Int64[],
			btag_lr=Float32[],
			btag_lr_with_c=Float32[],
			njets=Int32[], pass_sl=Int32[],
			lepton_pt=Float32[], lepton_eta=Float32[], lepton_phi=Float32[], lepton_mass=Float32[],
		), nrow(df)
	)

	const t0 = time()
	#for i=1:nrow(df)

	ntot = 0

	fail_lep = 0
	idx2 = 1
	for idx1=1:nrow(df)

		const doprint = idx1<50

		idx1%10000==0 && println(idx1)

		#Load the TTree row
		load_row(df, idx1)
		
		#Get the primary event interpretation
		const ev = parse_event(df, idx1)

		#######################
		### Single lepton (SL)
		#######################
		pass_sl, lepton_sl = select_sl(ev)

		if !pass_sl
			continue
		end
		
		ofdf[idx2, :event] = ev.event
		ofdf[idx2, :run] = ev.run
		ofdf[idx2, :lumi] = ev.lumi

		analyzed_event = Nullable{AbstractEvent}()

		doprint && println(string(ev, 0))

		##################
		### Jet selection
		##################
		jets = select_jets(ev)

		ofdf[idx2, :njets] = int32(length(jets))
		doprint && println("selected jets $(length(jets))")

		ofdf[idx2, :pass_sl] = int32(pass_sl)
		if pass_sl
			analyzed_event = InterpretedEventSL(jets, lepton_sl, ev.vtype)
		end

		sj = ""
		for jet in jets
			sj = string(sj, " ", jet.id)
		end
		doprint && println("jets ", sj)

		###############################
		### B-tagging likelihood ratio
		###############################

		jets_by_csv = sort(jets, by=x->x.bdisc, rev=true)
		if length(jets_by_csv) >= 5
			jets_by_csv_first = jets_by_csv[1:min(length(jets), 6)]
			bdiscs = zeros(Float64, 3, length(jets_by_csv_first))

			for (iflavour, flavour) in zip(1:3, [:b, :c, :l])
				for nj=1:length(jets_by_csv_first)
					@inbounds bdiscs[iflavour, nj] = pdf_bdisc(jets_by_csv_first[nj].bdisc, flavour)
				end
			end
			btag_lr = calculate_btag_lr(bdiscs)
			btag_lr_with_c = calculate_btag_lr_with_c(bdiscs)

			ofdf[idx2, :btag_lr] = float32(btag_lr)
			ofdf[idx2, :btag_lr_with_c] = float32(btag_lr_with_c)

			doprint && println("bLR = $btag_lr bLRc = $btag_lr_with_c")
		end #at least 5 jets

		doprint && println("---")

		ntot += 1
		idx2 += 1
	end
	ofdf = sub(ofdf, 1:idx2)
	const t1 = time()

	const speed = nrow(df) / (t1 - t0)
	println("processed $(round(speed, 0)) events/second")
	println("failed lepton $fail_lep")
	println("writing output")
	writetree("output.root", ofdf)
	writetable("output.csv.gz", ofdf)
	return ntot
end

function main()
	nproc = 0
	for sample in SAMPLES
		const FN = string(
			CFG[:pathToFile][:_value],
			"/",
			CFG[:ordering][:_value],
			sample[:name][:_value],
			".root"
		)
		nproc += process_sample(FN)
	end
end #main

end #module Analysis
