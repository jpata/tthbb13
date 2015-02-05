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

immutable Top <: AbstractParticle
	p::FourVectorSph
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
	event::Int64
	run::Int64
	lumi::Int64
end

immutable InterpretedEventSL <: AbstractEvent
	jets::Vector{Jet}
	leptons::Vector{Lepton}
	vtype::Symbol
end

export AbstractParticle, Particle, Jet, Lepton, SignalLepton
export AbstractEvent
export Event, InterpretedEventSL

end #module Kinematics