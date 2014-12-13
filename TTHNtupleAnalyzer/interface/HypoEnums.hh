#ifndef TTH_HYPOENUMS
#define TTH_HYPOENUMS

#include "TAxis.h"

namespace TTH {

//Initial classification based on the decay mode of the two top quarks
//enum CandidateType{
//Zmumu, -> 0
//Zee, -> 1
//Wmun, -> 2
//Wen, -> 3
//Znn, -> 4 
//Zemu, Ztaumu, Ztaue, Wtaun, Ztautau, Zbb, UNKNOWN};
enum EventHypothesis {
    mumu, 
    ee,
    mun,
    en, //3
    nn,
    emu,
    taumu, //6
    taue,
    taun,
    tautau,
    //bb,
    //could not assign a hyothesis
    UNKNOWN_HYPO,

    //assigned multiple hypotheses
    BAD_HYPO
};
	
	void label_axis(TAxis* ax) {
		int i=1;
		for (const char* v : {
			"mumu",
			"ee",
			"mun",
			"en",
			"nn",
			"emu",
			"taumu",
			"taue",
			"taun",
			"tautau",
			"UNKNOWN_HYPO",
			"BAD_HYPO"
		}) {
			ax->SetBinLabel(i, v);
			i += 1;
		}
	}

	
//top quark pair decay mode
enum DecayMode {
    dileptonic,
    semileptonic,
    hadronic,
    UNKNOWN_MODE
};
}

#endif
