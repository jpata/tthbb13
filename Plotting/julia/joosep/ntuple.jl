using DataFrames, ROOT, ROOTDataFrames
using HEP
import Base.string
using PyCall

@pyimport imp

length(ARGS)==1 || error("ntuple.jl file.py")

const fn = ARGS[1]
isfile(fn) || error("File error: $fn")

const CFG = imp.load_source("cfg", fn)[:process][:fwliteInput]
const SAMPLES = CFG[:samples]

const HYPOS = [:tthbb, :ttjets]
const BTAG_LR_HYPOS = [:ttjj, :ttbb]

module Cuts
	import ..CFG
	const muPtTight = float64(CFG[:lepPtTight][:_value])
	const muEtaTight = float64(CFG[:muEtaTight][:_value])
	const jetPt = float64(CFG[:jetPtThreshold][:_value])
	const jetEta = 2.5
end

module Kinematics

using HEP
abstract AbstractParticle

immutable Particle <: AbstractParticle
	p::FourVectorSph
	id::Int64
end

immutable Jet <: AbstractParticle
	p::FourVectorSph
	id::Int64
	bdisc::Float64
end

immutable Lepton <: AbstractParticle
	p::FourVectorSph
	id::Int64
	iso::Float64
end


immutable SignalLepton <: AbstractParticle
	idx::Int64
end

abstract AbstractEvent

immutable Event <: AbstractEvent
	jets::Vector{Jet}
	leptons::Vector{Lepton}
	signal_leptons::Vector{SignalLepton}
	vtype::Symbol
	lepton_category::Symbol
end

immutable InterpretedEventSL <: AbstractEvent
	jets::Vector{Jet}
	leptons::Vector{Lepton}
	vtype::Symbol
end

export AbstractParticle, Particle, Jet, Lepton, SignalLepton
export AbstractEvent
export Event, InterpretedEventSL

end

using Kinematics

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
	p::Type{P})
	nj = df[i, :n__jet]::Int32

	particles = P[
		P(
			FourVectorSph(
				df[i, :jet__pt, Float32][k],
				df[i, :jet__eta, Float32][k],
				df[i, :jet__phi, Float32][k],
				df[i, :jet__mass, Float32][k]
			),
			df[i, :jet__id, Int32][k] |> int64,
			df[i, :jet__bd_csv, Float32][k] |> float64
		) for k=1:nj
	]
	return particles
end

function parse_branches{P <: Lepton}(
	df::TreeDataFrame,
	i::Int64,
	p::Type{P})
	nj = df[i, :n__lep]::Int32

	particles = P[
		P(
			FourVectorSph(
				df[i, :lep__pt, Float32][k],
				df[i, :lep__eta, Float32][k],
				df[i, :lep__phi, Float32][k],
				df[i, :lep__mass, Float32][k]
			),
			df[i, :lep__id, Int32][k]|>int64,
			df[i, :lep__rel_iso, Float32][k]|>float64,
		) for k=1:nj
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
	Event(jets, leps, sig_leps,
		EventHypothesis.as(vtype_),
		assign_lepton_category(EventHypothesis.as(vtype_))
	)
end

function select_sl(ev::Event)
	passes = false

	length(ev.signal_leptons) == 1 || return (passes, Lepton[])

	const sig_lep = first(ev.signal_leptons)
	const main_lep = ev.leptons[sig_lep.idx + 1]

	if ev.vtype == :en
		println("SL e")

		abs(main_lep.id) == 11 || error("event incorrectly classified $(main_lep) $(ev.vtype)")
		passes = pt(main_lep) > Cuts.muPtTight
		passes = passes && abs(eta(main_lep)) < Cuts.muEtaTight

	elseif ev.vtype == :mun
		println("SL mu")
		abs(main_lep.id) == 13 || error("event incorrectly classified $(main_lep) $(ev.vtype)")
	elseif ev.vtype == :taun
		println("SL tau")
		abs(main_lep.id) == 15 || error("event incorrectly classified $(main_lep) $(ev.vtype)")
	end
	if passes
		println("lepton passes SL")
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

cp = ROOT.TFile(string(ENV["CMSSW_BASE"], "/src/TTH/MEAnalysis/", CFG[:pathToCP][:_value]))

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

btag_prob_maps = Dict(
	:h => Histogram(root_cast(TH1D, Get(cp, "csv_b_Bin0__csv_rec"))),
	:l => Histogram(root_cast(TH1D, Get(cp, "csv_l_Bin0__csv_rec")))
)

println(btag_prob_maps)

function pdf_bdisc(csv::Float64, flavour::Symbol)
	h = btag_prob_maps[flavour]
	b = findbin(h, csv)
	if b <= 0
		b = 1
	end
	if b > length(h.weights)
		b = length(h.weights)
	end
	@inbounds return h.weights[b]
end

dprintln(level::Int64, msg) = DEBUG>=level && println([" " for i=1:level]..., msg)
function calculate_btag_lr(jets::AbstractVector{Jet})
	P = Dict{Symbol, Float64}()

	for hypo in BTAG_LR_HYPOS
		_P = 0.0

		#count how many combinations per jet
		nc = 0

		ntagged = 2
		if hypo == :ttbb
			ntagged = 4
		end

		#jets in selected combination are assumed to be true b quarks
		for comb in combinations(1:length(jets), ntagged)
			#dprintln(2, "comb=$comb")
			p = 1.0

			nc += 1
			for i in 1:length(jets)
				p = p * pdf_bdisc(jets[i].bdisc, i in comb ? :h : :l)
				#dprintln(3, "p=$p")
			end
			_P += p
		end
		dprintln(1, "P[$hypo]=$_P nc=$nc")
		P[hypo] = _P / nc
	end
	ret = P[:ttbb] / sum(values(P))
	return isnan(ret) ? 0.0 : ret
end

function process_sample(fn::ASCIIString)
	println("processing $fn")
	df = TreeDataFrame([fn], "tthNtupleAnalyzer/events")

	const t0 = time()
	for i=1:nrow(df)

		#Load the TTree row
		load_row(df, i)

		#Get the primary event interpretation
		const ev = parse_event(df, i)
		analyzed_event = Nullable{AbstractEvent}()

		println(string(ev, 0))

		##################
		### Jet selection
		##################
		jets = select_jets(ev)
		println("selected jets $(length(jets))")

		#######################
		### Single lepton (SL)
		#######################
		pass_sl, lepton_sl = select_sl(ev)

		if pass_sl
			analyzed_event = InterpretedEventSL(jets, lepton_sl, ev.vtype)
		end

		###############################
		### B-tagging likelihood ratio
		###############################
		btag_lr = calculate_btag_lr(jets)

		println("bLR = $btag_lr")

		println("---")
	end
	const t1 = time()

	const speed = nrow(df) / (t1 - t0)
	println("processed $(round(speed, 0)) events/second")
end

for sample in SAMPLES
	const FN = string(
		CFG[:pathToFile][:_value],
		"/",
		sample[:name][:_value],
		".root"
	)
	process_sample(FN)
end
