println("including kinematics.jl on pid=", myid())
module Kinematics

using HEP
abstract AbstractParticle
using ROOTDataFrames
import Base.string

immutable Particle <: AbstractParticle
	p::FourVectorSph
	id::Int64
end

immutable Jet <: AbstractParticle
	p::FourVectorSph
	id::Int64
	bdisc::Float64
end

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
	mem_tth_p::Vector{Float64}
	mem_ttbb_p::Vector{Float64}
	run::Int64
	lumi::Int64
	evt::Int64
end


function parse_branches{P <: Jet}(
    df::TreeDataFrame,
    p::Type{P}
    )
    const n = df.row.njets()

    const pt = df.row.jets_pt()
    const eta = df.row.jets_eta()
    const phi = df.row.jets_phi()
    const mass = df.row.jets_mass()
    const id = df.row.jets_mcFlavour()
    const csv = df.row.jets_btagCSV()
 
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

@generated function parse_event{T, S}(df::TreeDataFrame{T}, s::Type{Val{S}})
    #println("generating parse_event{$df, $s}")

	if s == Type{Val{:nominal}}
		syst = ""
	else
    	syst = string("_", s.parameters[1].parameters[1])
	end
    ex = quote
        jets = parse_branches(df, Jet)
        Event(
            jets,
            getfield(df.row, $(QuoteNode(symbol("numJets", syst))))(),
            getfield(df.row, $(QuoteNode(symbol("nBCSVM", syst))))(),

            df.row.is_sl(),
            df.row.is_dl(),
            df.row.weight_xs(),
            df.row.genWeight(),

			df.row.mem_tth_p(),
			df.row.mem_ttbb_p(),

            df.row.run(),
            df.row.lumi(),
            df.row.evt(),
        )
    end
    #println(ex)
    return ex
end

@generated function systweight{T}(ev::Event, lumi, t::Val{T})
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

function string(ev::Event, l::Int64=0) 
    s = "$(ev.numJets)J $(ev.nBCSVM)T"
    if l>0
        # for x in ev.leptons
        #     s = string(s, "\n l ", string(x))
        # end
        # for x in ev.signal_leptons
        #     s = string(s, "\n L ", string(x))
        # end
        for x in ev.jets
            s = string(s, "\n j ", string(x))
        end
    end
    return s
end

export pt, et, phi, mass, weight
export parse_event

end #module Kinematics
