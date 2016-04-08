#!/usr/bin/env julia


#Samples by the Pozzorini group at http://www.physik.uzh.ch/data/ttHsim/TTBBV1/
#Implemented after https://github.com/bianchini/TTHStudies/blob/master/bin/HepMCtoStep2Converter.cc

module GenAnalysis

using Cxx, HEP, ROOT, Histograms, ROOTHistograms, ROOTDataFrames

addHeaderDir("/usr/local/include/", kind=C_System)
Libdl.dlopen("/usr/local/lib/libfastjet.dylib", Libdl.RTLD_GLOBAL)

    const VERBOSE = true

cxx"""
#include <fastjet/ClusterSequence.hh>
#include <vector>
#include <iostream>
using namespace fastjet;
using namespace std;
"""

cxx"""
typedef vector<PseudoJet*> VectorPseudoJet; 
vector<PseudoJet> cluster(vector<PseudoJet*>* _particles, double R, JetAlgorithm algo) {
    JetDefinition jet_def(algo, R);
    vector<PseudoJet> particles;
    for (auto* p : *_particles ) {
        particles.push_back(*p);
    }
    ClusterSequence cs(particles, jet_def);
    return sorted_by_pt(cs.inclusive_jets());
}
"""

immutable PseudoJet
    p4::FourVector
end

function cluster(
    constituents::Vector{PseudoJet},
    R=0.5,
    jetalgo=@cxx(fastjet::antikt_algorithm)
    )
    pvec = @cxxnew VectorPseudoJet()
    for j in constituents
        pj = @cxxnew PseudoJet(x(j.p4), y(j.p4), z(j.p4), t(j.p4))
        @cxx pvec->push_back(pj)
    end
    ret = @cxx cluster(pvec, R, jetalgo)
    nret = @cxx ret->size()

    outparticles = Array(PseudoJet, nret)
    for i=1:nret
        pj = @cxx ret->at(i-1)
        
        px = @cxx pj->px()
        py = @cxx pj->py()
        pz = @cxx pj->pz()
        E = @cxx pj->E()

        outparticles[i] = PseudoJet(FourVector(E, px, py, pz))
    end
    return outparticles
end


cxx"""
#include "HepMC/IO_GenEvent.h"
#include "HepMC/GenEvent.h"
"""
Libdl.dlopen("/usr/local/lib/libHepMC.dylib", Libdl.RTLD_GLOBAL)

type GenVertex
    pos::FourVector
    id::Int64
end

function GenVertex(vtx)
    if vtx != C_NULL
        p4 = @cxx(vtx->position())
        ret = GenVertex(
            FourVector(
                @cxx(p4->e()),
                @cxx(p4->px()),
                @cxx(p4->py()),
                @cxx(p4->pz()),
            ),
            Int64(@cxx(vtx->id()))
        )
        return ret
    end
    return Nullable{GenVertex}()
end

type GenParticle
    p4::FourVector
    status::Int64
    pdgid::Int64
    productionvertex::Nullable{GenVertex}
    endvertex::Nullable{GenVertex}
end

import Base.string
function string(p::FourVector)
    @sprintf("(t=%.2f x=%.2f y=%.2f z=%.2f)", t(p), x(p), y(p), z(p))
end

function string(p::GenParticle)
    return "p4=$(p.p4) status=$(p.status) pdgid=$(p.pdgid)"
end

cxx"""
HepMC::GenParticle* GenParticleIterator_deref(HepMC::GenEvent::particle_iterator it) {
    return *it;
}

HepMC::GenEvent::particle_iterator GenParticleIterator_next(HepMC::GenEvent::particle_iterator it) {
    return ++it;
}

bool GenParticleIterator_atend(HepMC::GenEvent::particle_iterator it, HepMC::GenEvent* evt) {
    return it == evt->particles_end();
}
"""

isFinalState(p::GenParticle) = isnull(p.endvertex) && p.status == 1
isInvisible(p::GenParticle) = abs(p.pdgid) in [12,14,16]
isChargedLepton(p::GenParticle) = abs(p.pdgid) in [11,13]
isLightQuark(p::GenParticle) = abs(p.pdgid)<4 || abs(p.pdgid)==21
isCQuark(p::GenParticle) = abs(p.pdgid)==4
isBQuark(p::GenParticle) = abs(p.pdgid)==5
isTQuark(p::GenParticle) = abs(p.pdgid)==6
isHBoson(p::GenParticle) = abs(p.pdgid)==25
isWBoson(p::GenParticle) = abs(p.pdgid)==24
isZBoson(p::GenParticle) = abs(p.pdgid)==23

function isLHadron(p::GenParticle)
    pdg = abs(p.pdgid)
    return (pdg != 22 &&
        (   (pdg%1000/100 > 0 && pdg%1000/100 < 4) ||
            (pdg%10000/1000 > 0 && pdg%10000/1000 < 4)
        ) && p->status() == 1
    )

end

function isGoodFinalStateParticle(p)
    return (
        isFinalState(p) &&
        !(isTQuark(p) || isHBoson(p) || isWBoson(p) || isZBoson(p)) &&
        !(isInvisible(p))
    )
end

function isSLLepton(p::GenParticle)
end

const MINPT = 0.0001
const CONE_MINDR = 0.0001

function isPartonForMatch(p::GenParticle)
    status = p.status
    pdg = abs(p.pdgid)
    return (
        pt(p.p4) > MINPT &&
        abs(p.productionvertex.id)==4 && status==11 &&
        (pdg==1 || pdg==2 || pdg==3 || pdg==4 || pdg==5 || pdg==21)
    )

end

function convertHepMC(event)
    part_iter = @cxx(event->particles_begin())
    ret = GenParticle[]
    np = 1
    #println("np = ", @cxx(event->particles_size()))
    while !@cxx(GenParticleIterator_atend(part_iter, event))
        p = @cxx(GenParticleIterator_deref(part_iter))
        endvertex = GenVertex(@cxx(p->end_vertex()))
        productionvertex = GenVertex(@cxx(p->production_vertex()))

        p4 = @cxx(p->momentum())
        gp = GenParticle(
            FourVector(
                @cxx(p4->e()),
                @cxx(p4->px()),
                @cxx(p4->py()),
                @cxx(p4->pz())
            ),
            @cxx(p->status()),
            @cxx(p->pdg_id()),
            productionvertex,
            endvertex,
        )
        push!(ret, gp)
        if part_iter != @cxx(event->particles_end())
            part_iter = @cxx(GenParticleIterator_next(part_iter))
        end
        np += 1
    end
    return ret
end

function incone(p, seed, conesize)
    p4seed = seed.p4
    dr = deltar(p4seed, p.p4)
    return dr>CONE_MINDR && dr<conesize
end

function relativeIsolation(particle, others, conesize)
    particlesincone = filter(x->incone(x, particle, conesize), others)
    sumpt = map(x->perp(x.p4), particlesincone)
    return sumpt / perp(particle.p4)
end

function main()
    ascii_in = @cxxnew HepMC::IO_GenEvent(
        pointer("/Users/joosep/Downloads/LO_stab/S_stab_1.hepmc2g"),
        @cxx(std::ios::in)
        )

    evt = @cxx ascii_in->read_next_event()


    out = TreeDataFrame(
        "gen.root",

        #branch names
        [
            :nGenJet, :GenJet_pt, :GenJet_eta, :GenJet_phi, :GenJet_mass, :GenJet_flavour,
            :nGenLepton, :GenLepton_pt, :GenLepton_eta
        ],
        [
            Int64, Float64, Float64, Float64, Float64, Int64,
            Int64, Float64, Float64
        ],
        [Val{1}, :nGenJet, :nGenJet, :nGenJet, :nGenJet, :nGenJet, Val{1}, :nGenLepton, :nGenLepton];

        treename="tree"
    )

    hjetpt = ErrorHistogram(linspace(0,500,100))
    iev = 0
    t0 = time()
    irow = 1
    nb = 0
    while evt != C_NULL

        println("---")
        iev += 1
        genparticles = convertHepMC(evt)

        finalstateparticles = filter(
            isGoodFinalStateParticle, genparticles
        )

        if VERBOSE
            for fs in genparticles
                println("genp ", fs.pdgid, " ", fs.status, " fs=", fs in finalstateparticles ? "1" : "0")
            end
        end

        leptons = filter(
            isChargedLepton, finalstateparticles
        )
        out[irow, :nGenLepton] = length(leptons)
        out[irow, :GenLepton_pt] = Float64[HEP.perp(l.p4) for l in leptons]
        out[irow, :GenLepton_eta] = Float64[HEP.eta(l.p4) for l in leptons]

        if VERBOSE && length(leptons)>0
            println("lepton ", leptons)
        end

        pseudojets = [PseudoJet(gp.p4) for gp in finalstateparticles]
        if VERBOSE
            println("N[pj]=", length(pseudojets))
        end

        jets = cluster(pseudojets, 0.5)
        jets = filter(
            x->perp(x.p4)>20, jets
        )

        VERBOSE && println("found $(length(jets)) inclusive jets: pts = $(Float64[round(perp(j.p4), 2) for j in jets])")

        out[irow, :nGenJet] = length(jets)
        out[irow, :GenJet_pt] = Float64[HEP.perp(j.p4) for j in jets]
        out[irow, :GenJet_eta] = Float64[HEP.eta(j.p4) for j in jets]
        out[irow, :GenJet_phi] = Float64[HEP.phi(j.p4) for j in jets]
        out[irow, :GenJet_mass] = Float64[HEP.l(j.p4) for j in jets]

        for jet in jets
            pt = perp(jet.p4)
            #println("jet $jet ", pt)
            
            push!(hjetpt, pt)
        end
        evt = @cxx ascii_in->read_next_event()
        irow += 1
        nb += Fill(out.tt)
    end
    dt = time() - t0

    Write(out.tf)
    Close(out.tf)

    println("processed $iev events, $(round(iev/dt, 2)) ev/s, wrote $(round(nb/1024/1024,2)) Mb")
    ROOTHistograms.write_hists_to_file(
        "ttbb_gen.root",
        Dict(
            "jet_pt"=>hjetpt
        )
    )
end

end #module GenAnalysis

GenAnalysis.main()
