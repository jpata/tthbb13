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


module Cuts
	import ..CFG
	const muPtTight = float64(CFG[:lepPtTight][:_value])
	const muEtaTight = float64(CFG[:muEtaTight][:_value])
	const jetPt = float64(CFG[:jetPtThreshold][:_value])
	const jetEta = 2.5
end

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

immutable Event
	jets::Vector{Jet}
	leptons::Vector{Lepton}
	signal_leptons::Vector{SignalLepton}
	vtype_::Int64
	vtype::Symbol
end

immutable InterpretedEventSL
	jets::Vector{Jet}
	leptons::Vector{Lepton}
	vtype::Symbol
end


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
	Event(jets, leps, sig_leps, vtype_, EventHypothesis.as(vtype_))
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

function select_jets(ev::Event)

	jets = Jet[]
	for jet in ev.jets
		passes = pt(jet) > Cuts.jetPt
		passes = passes && abs(eta(jet)) < Cuts.jetEta

		passes && push!(jets, jet)
	end

	return jets
end


function process_sample(fn::ASCIIString)
	println("processing $fn")
	df = TreeDataFrame([fn], "tthNtupleAnalyzer/events")

	const t0 = time()
	for i=1:nrow(df)
		load_row(df, i)
		const ev = parse_event(df, i)

		println(string(ev, 1))

		pass_sl, lepton_sl = select_sl(ev)
		jets = select_jets(ev)

		if pass_sl
			analyzed_event = InterpretedEventSL(jets, lepton_sl, ev.vtype)
		end

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
