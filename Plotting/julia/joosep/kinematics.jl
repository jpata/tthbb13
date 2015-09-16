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
# 
# immutable Lepton <: AbstractParticle
# 	p::FourVectorSph
# 	id::Int64
# 	iso::Float64
# end
# 
# immutable Top <: AbstractParticle
# 	p::FourVectorSph
# end
# 
# immutable SignalLepton <: AbstractParticle
# 	idx::Int64
# end

abstract AbstractEvent

immutable Event <: AbstractEvent
	jets::Vector{Jet}
	#leptons::Vector{Lepton}
	#signal_leptons::Vector{SignalLepton}
	#vtype::Symbol
	numJets::Int64
	nBCSVM::Int64
	is_sl::Bool
	is_dl::Bool
	weight_xs::Float64
	weight_gen::Float64
	run::Int64
	lumi::Int64
	evt::Int64
end

weight(ev::Event, lumi) = lumi * ev.weight_xs * ev.weight_gen

import HEP: eta, phi
export AbstractParticle, Particle, Jet
export AbstractEvent
export Event
pt(x::AbstractParticle) = perp(x.p)
eta(x::AbstractParticle) = eta(x.p)
phi(x::AbstractParticle) = phi(x.p)
mass(x::AbstractParticle) = l(x.p)

string(x::FourVector) = @sprintf("(%.3f %.3f %.3f %.3f)", x.t, x.x, x.y, x.z)
string(x::FourVectorSph) = @sprintf("(%.3f %.3f %.3f %.3f)", x.perp, x.eta, x.phi, x.l)
string(p::Particle) = @sprintf("p=%s id=%d", string(p.p), p.id)
string(p::Jet) = @sprintf("p=%s id=%d b(csv)=%.3f", string(p.p), p.id, p.bdisc)

export pt, et, phi, mass, weight

end #module Kinematics
