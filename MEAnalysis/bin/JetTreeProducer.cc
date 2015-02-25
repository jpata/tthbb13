#include "FWCore/FWLite/interface/AutoLibraryLoader.h"

#include <cstdlib>
#include <iostream>
#include <fstream>
#include <map>
#include <string>

#include "TSystem.h"
#include "TROOT.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1D.h"
#include "TF1.h"
#include "TF2.h"
#include "TGraph.h"
#include "Math/GenVector/LorentzVector.h"
#include "TLorentzVector.h"
#include "TVectorD.h"

#include "PhysicsTools/FWLite/interface/TFileService.h"

#include "FWCore/ParameterSet/interface/ProcessDesc.h"
#include "FWCore/PythonParameterSet/interface/PythonProcessDesc.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/FWLite/interface/Event.h"
#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/GeometryVector/interface/VectorUtil.h"
#include "DataFormats/FWLite/interface/LuminosityBlock.h"
#include "DataFormats/FWLite/interface/Run.h"
#include "DataFormats/Luminosity/interface/LumiSummary.h"

#include "TTH/MEAnalysis/interface/Samples.h"
#include "TTH/MEAnalysis/interface/HelperFunctions.h"
#include "TTH/MEAnalysis/interface/JetTree.hh"


#define GENJETDR 0.3
#define VERBOSE  false

using namespace std;


Float_t deltaR(TLorentzVector j1, TLorentzVector j2) {
	float res = TMath::Sqrt(TMath::Power(j1.Eta()-j2.Eta(),2) + TMath::Power( TMath::ACos(TMath::Cos(j1.Phi()-j2.Phi())) ,2));
	return res;
}


int main(int argc, const char* argv[])
{

	std::cout << "TreeProducerNew" << std::endl;
	gROOT->SetBatch(true);

	gSystem->Load("libFWCoreFWLite");
	gSystem->Load("libDataFormatsFWLite");

	AutoLibraryLoader::enable();

	string target = argc>2 ? string(argv[2]) : "";
	string extraname = argc>3 ? "TEST"+target+string(argv[3]) : "TEST"+target;
	
	PythonProcessDesc builder(argv[1]);
	const edm::ParameterSet& in = builder.processDesc()->getProcessPSet()->getParameter<edm::ParameterSet>("fwliteInput");
	const edm::VParameterSet& samples = in.getParameter<edm::VParameterSet>("samples") ;
	const std::string out_fn = in.getParameter<std::string>("outFileName") ;

	TFile* outfile = new TFile(out_fn.c_str(), "RECREATE");
	outfile->cd();
	//fwlite::TFileService fs = fwlite::TFileService(out_fn.c_str());
	//TTree* genTree			= fs.make<TTree>("genTree","event tree");
	//genTree->SetDirectory(&(fs.file()));
	//TTree* genJetLightTree	= fs.make<TTree>("genJetLightTree","event tree");
	//TTree* genJetGluonTree	= fs.make<TTree>("genJetGluonTree","event tree");
	//TTree* genJetHeavyTree	= fs.make<TTree>("genJetHeavyTree","event tree");
	//TTree* genEventTree		= fs.make<TTree>("genEventTree","event tree");
	
	TTree* genTree			= new TTree("genTree","event tree");
	TTree* genJetLightTree	= new TTree("genJetLightTree","event tree");
	TTree* genJetGluonTree	= new TTree("genJetGluonTree","event tree");
	TTree* genJetHeavyTree	= new TTree("genJetHeavyTree","event tree");
	TTree* genEventTree		= new TTree("genEventTree","event tree");


	JetTree* jt = new JetTree(genTree, genJetLightTree, genJetGluonTree, genJetHeavyTree, genEventTree);
	jt->make_branches();

	std::string pathToFile   (in.getParameter<std::string>("pathToFile" ) );
	std::string ordering	 (in.getParameter<std::string>("ordering" ) );
	double lumi				(in.getParameter<double>	 ("lumi") );
	bool verbose			 (in.getParameter<bool>		 ("verbose") );
	bool evalReg			 (in.getParameter<bool>		 ("evalReg") );
	int  maxnum				(in.getParameter<int>		("maxnum") );

	//Float_t readerVars[12];
	//TMVA::Reader* reader = evalReg ? getTMVAReader("./root/weights/", "target-"+target, "BDTG", readerVars) : 0;

	bool openAllFiles  = false;
	Samples* mySamples = new Samples(openAllFiles, pathToFile, ordering, samples, lumi, verbose);
	vector<string> mySampleFiles;

	if(mySamples->IsOk()) {

		cout << "Ok!" << endl;
		mySampleFiles = mySamples->Files();

		for( unsigned int i = 0 ; i < mySampleFiles.size(); i++) {
			string sampleName		 = mySampleFiles[i];

			if(verbose) {
				cout << mySampleFiles[i] << " ==> " << mySamples->GetXSec(sampleName)
					 << " pb,"
					 << " ==> weight = "			<< mySamples->GetWeight(sampleName) << endl;
			}
		}
	}
	else {
		cout << "Problems... leaving" << endl;
		return 0;
	}

	//string currentName0		 = mySampleFiles[0];
	//mySamples->OpenFile( currentName0 );
	//TTree* currentTree0		 = mySamples->GetTree( currentName0, "tree");

	for(unsigned int sample = 0 ; sample < mySampleFiles.size(); sample++) {

		string currentName = mySampleFiles[sample];

		cout << "Opening file " << currentName << endl;
		TTree* currentTree		 = mySamples->GetTree( currentName, TTH_TTREE_NAME);
		TTHTree* it = new TTHTree(currentTree);
		it->set_branch_addresses();
		cout << "Done!!" << endl;

		Long64_t nentries = currentTree->GetEntries();
		cout << "Total entries: " << nentries << endl;
		
		genTopInfo genTop = {};
		genTopInfo genTbar = {};
		
		genParticleInfo genB = {};
		genParticleInfo genBbar = {};

		for (Long64_t entry = 0; entry < nentries ; entry++) {

			if(entry%5000==0) cout << entry << "  (" << float(entry)/float(nentries)*100. << " % completed)" << endl;

			if(entry>maxnum) {
				entry = nentries;
				continue;
			}

			currentTree->GetEntry(entry);

			jt->loop_initialize();
			
			genTop.bmass = it->gen_t__b__mass;
			genTop.bpt = it->gen_t__b__pt;
			genTop.beta = it->gen_t__b__eta;
			genTop.bphi = it->gen_t__b__phi;
			genTop.bphi = it->gen_t__b__phi;
			genTop.bstatus = it->gen_t__b__status;
			
			genTop.wdau1mass = it->gen_t__w_d1__mass;
			genTop.wdau1pt = it->gen_t__w_d1__pt;
			genTop.wdau1eta = it->gen_t__w_d1__eta;
			genTop.wdau1phi = it->gen_t__w_d1__phi;
			genTop.wdau1id = it->gen_t__w_d1__id;

			genTop.wdau2mass = it->gen_t__w_d2__mass;
			genTop.wdau2pt = it->gen_t__w_d2__pt;
			genTop.wdau2eta = it->gen_t__w_d2__eta;
			genTop.wdau2phi = it->gen_t__w_d2__phi;
			genTop.wdau2id = it->gen_t__w_d2__id;
			
			genTbar.bmass = it->gen_tbar__b__mass;
			genTbar.bpt = it->gen_tbar__b__pt;
			genTbar.beta = it->gen_tbar__b__eta;
			genTbar.bphi = it->gen_tbar__b__phi;
			genTbar.bphi = it->gen_tbar__b__phi;
			genTbar.bstatus = it->gen_tbar__b__status;
			
			genTbar.wdau1mass = it->gen_tbar__w_d1__mass;
			genTbar.wdau1pt = it->gen_tbar__w_d1__pt;
			genTbar.wdau1eta = it->gen_tbar__w_d1__eta;
			genTbar.wdau1phi = it->gen_tbar__w_d1__phi;
			genTbar.wdau1id = it->gen_tbar__w_d1__id;

			genTbar.wdau2mass = it->gen_tbar__w_d2__mass;
			genTbar.wdau2pt = it->gen_tbar__w_d2__pt;
			genTbar.wdau2eta = it->gen_tbar__w_d2__eta;
			genTbar.wdau2phi = it->gen_tbar__w_d2__phi;
			genTbar.wdau2id = it->gen_tbar__w_d2__id;
			
			genB.mass = it->gen_b__mass; 
			genB.pt = it->gen_b__pt; 
			genB.eta = it->gen_b__eta; 
			genB.phi = it->gen_b__phi; 
			genB.status = it->gen_b__status; 
			genB.charge = 0;
			genB.momid = 25;
			
			genBbar.mass = it->gen_bbar__mass; 
			genBbar.pt = it->gen_bbar__pt; 
			genBbar.eta = it->gen_bbar__eta; 
			genBbar.phi = it->gen_bbar__phi; 
			genBbar.status = it->gen_bbar__status; 
			genBbar.charge = 0;
			genBbar.momid = 25;

			// read top decay products from input files
			TLorentzVector topBLV   (1,0,0,1);
			TLorentzVector topW1LV  (1,0,0,1);
			TLorentzVector topW2LV  (1,0,0,1);
			TLorentzVector atopBLV  (1,0,0,1);
			TLorentzVector atopW1LV (1,0,0,1);
			TLorentzVector atopW2LV (1,0,0,1);
			TLorentzVector genBLV   (1,0,0,1);
			TLorentzVector genBbarLV(1,0,0,1);

			// set-up top decay products (if available from input file...)
			if(genTop.bmass>0) {
				topBLV.SetPtEtaPhiM(  genTop.bpt,genTop.beta,genTop.bphi,genTop.bmass );
				topW1LV.SetPtEtaPhiM( genTop.wdau1pt,genTop.wdau1eta, genTop.wdau1phi,genTop.wdau1mass);
				topW2LV.SetPtEtaPhiM( genTop.wdau2pt,genTop.wdau2eta, genTop.wdau2phi,genTop.wdau2mass);
			}
			if(genTbar.bmass>0) {
				atopBLV.SetPtEtaPhiM(  genTbar.bpt,genTbar.beta,genTbar.bphi,genTbar.bmass );
				atopW1LV.SetPtEtaPhiM( genTbar.wdau1pt,genTbar.wdau1eta, genTbar.wdau1phi,genTbar.wdau1mass);
				atopW2LV.SetPtEtaPhiM( genTbar.wdau2pt,genTbar.wdau2eta,genTbar.wdau2phi,genTbar.wdau2mass);
			}
			if(genB.mass>0 && (genB.momid==25 || genB.momid==23)) {
				genBLV.SetPtEtaPhiM(genB.pt,genB.eta ,genB.phi, genB.mass );
			}
			if(genBbar.mass>0 && (genBbar.momid==25 || genBbar.momid==23)) {
				genBbarLV.SetPtEtaPhiM(genBbar.pt,genBbar.eta ,genBbar.phi, genBbar.mass );
			}


			// define LV for the 6 (8) particles in ttbb (ttH) events
			TLorentzVector TOPHADW1(1,0,0,1);
			TLorentzVector TOPHADW2(1,0,0,1);
			TLorentzVector TOPHADB (1,0,0,1);
			TLorentzVector TOPLEPW1(1,0,0,1);
			TLorentzVector TOPLEPW2(1,0,0,1);
			TLorentzVector TOPLEPB (1,0,0,1);
			TLorentzVector HIGGSB1 (1,0,0,1);
			TLorentzVector HIGGSB2 (1,0,0,1);

			HIGGSB1.SetPtEtaPhiM( genBLV.Pt(),	genBLV.Eta(),	genBLV.Phi(),	genBLV.M());
			HIGGSB2.SetPtEtaPhiM( genBbarLV.Pt(), genBbarLV.Eta(), genBbarLV.Phi(), genBbarLV.M());

			if( abs(genTop.wdau1id)>6 && abs(genTbar.wdau1id)<6) {
				TOPHADW1.SetPxPyPzE( atopW1LV.Px(), atopW1LV.Py(), atopW1LV.Pz(), atopW1LV.E());
				TOPHADW2.SetPxPyPzE( atopW2LV.Px(), atopW2LV.Py(), atopW2LV.Pz(), atopW2LV.E());
				TOPHADB.SetPxPyPzE( atopBLV.Px(),  atopBLV.Py(),   atopBLV.Pz(),  atopBLV.E());
				if( abs(genTop.wdau1id)==11 || abs(genTop.wdau1id)==13 || abs(genTop.wdau1id)==15 ) {
					TOPLEPW1.SetPxPyPzE  ( topW1LV.Px(), topW1LV.Py(), topW1LV.Pz(), topW1LV.E());
					TOPLEPW2.SetPxPyPzE  ( topW2LV.Px(), topW2LV.Py(), topW2LV.Pz(), topW2LV.E());
				}
				else {
					TOPLEPW1.SetPxPyPzE  ( topW2LV.Px(), topW2LV.Py(), topW2LV.Pz(), topW2LV.E());
					TOPLEPW2.SetPxPyPzE  ( topW1LV.Px(), topW1LV.Py(), topW1LV.Pz(), topW1LV.E());
				}
				TOPLEPB.SetPxPyPzE(  topBLV.Px(),  topBLV.Py(),   topBLV.Pz(), topBLV.E());
			}
			else if(abs(genTop.wdau1id)<6 && abs(genTbar.wdau1id)>6) {
				TOPHADW1.SetPxPyPzE( topW1LV.Px(), topW1LV.Py(), topW1LV.Pz(), topW1LV.E());
				TOPHADW2.SetPxPyPzE( topW2LV.Px(), topW2LV.Py(), topW2LV.Pz(), topW2LV.E());
				TOPHADB.SetPxPyPzE( topBLV.Px(),  topBLV.Py(),   topBLV.Pz(),  topBLV.E());
				if( abs(genTbar.wdau1id)==11 || abs(genTbar.wdau1id)==13 || abs(genTbar.wdau1id)==15 ) {
					TOPLEPW1.SetPxPyPzE  ( atopW1LV.Px(), atopW1LV.Py(), atopW1LV.Pz(), atopW1LV.E());
					TOPLEPW2.SetPxPyPzE  ( atopW2LV.Px(), atopW2LV.Py(), atopW2LV.Pz(), atopW2LV.E());
				}
				else {
					TOPLEPW1.SetPxPyPzE  ( atopW2LV.Px(), atopW2LV.Py(), atopW2LV.Pz(), atopW2LV.E());
					TOPLEPW2.SetPxPyPzE  ( atopW1LV.Px(), atopW1LV.Py(), atopW1LV.Pz(), atopW1LV.E());
				}
				TOPLEPB.SetPxPyPzE( atopBLV.Px(),  atopBLV.Py(),   atopBLV.Pz(),  atopBLV.E());
			}
			else if(abs(genTop.wdau1id)>6 && abs(genTbar.wdau1id)>6) {
				if( abs(genTop.wdau1id)==11 || abs(genTop.wdau1id)==13 || abs(genTop.wdau1id)==15 ) {
					TOPHADW1.SetPxPyPzE  ( topW1LV.Px(), topW1LV.Py(), topW1LV.Pz(), topW1LV.E());
					TOPHADW2.SetPxPyPzE  ( topW2LV.Px(), topW2LV.Py(), topW2LV.Pz(), topW2LV.E());
				}
				else {
					TOPHADW1.SetPxPyPzE  ( topW2LV.Px(), topW2LV.Py(), topW2LV.Pz(), topW2LV.E());
					TOPHADW2.SetPxPyPzE  ( topW1LV.Px(), topW1LV.Py(), topW1LV.Pz(), topW1LV.E());
				}
				TOPHADB.SetPxPyPzE( topBLV.Px(),  topBLV.Py(),   topBLV.Pz(),  topBLV.E());
				if( abs(genTbar.wdau1id)==11 || abs(genTbar.wdau1id)==13 || abs(genTbar.wdau1id)==15 ) {
					TOPLEPW1.SetPxPyPzE  ( atopW1LV.Px(), atopW1LV.Py(), atopW1LV.Pz(), atopW1LV.E());
					TOPLEPW2.SetPxPyPzE  ( atopW2LV.Px(), atopW2LV.Py(), atopW2LV.Pz(), atopW2LV.E());
				}
				else {
					TOPLEPW1.SetPxPyPzE  ( atopW2LV.Px(), atopW2LV.Py(), atopW2LV.Pz(), atopW2LV.E());
					TOPLEPW2.SetPxPyPzE  ( atopW1LV.Px(), atopW1LV.Py(), atopW1LV.Pz(), atopW1LV.E());
				}
				TOPLEPB.SetPxPyPzE( atopBLV.Px(),  atopBLV.Py(),   atopBLV.Pz(),  atopBLV.E());
			}

			// conisder only semileptonic decays ...
			if(  !((abs(genTop.wdau1id)<6 &&  abs(genTbar.wdau1id)>6) ||
					(abs(genTop.wdau1id)>6 &&  abs(genTbar.wdau1id)<6))  ) {
				continue;
			}

			//////////////////////////////////////////////////
			// met
			//////////////////////////////////////////////////

			jt->sumEt   = it->met__sumet;
			jt->etReco  = it->met__pt;
			jt->phiReco = it->met__phi;

			TVector3 recoMEt( jt->etReco*TMath::Cos(jt->phiReco), jt->etReco*TMath::Sin(jt->phiReco), 0.0) ;
			jt->pxReco   = recoMEt.Px();
			jt->pyReco   = recoMEt.Py();
			jt->puWeight = it->weight__pu;

			jt->px = TMath::Abs(TOPLEPW2.Py())>0 ? TOPLEPW2.Px() : DEF_VAL_FLOAT;
			jt->py = TMath::Abs(TOPLEPW2.Py())>0 ? TOPLEPW2.Py() : DEF_VAL_FLOAT;
			jt->et = TMath::Abs(TOPLEPW2.Py())>0 ? TOPLEPW2.Pt() : DEF_VAL_FLOAT;
			jt->phi = TMath::Abs(TOPLEPW2.Py())>0 ? TOPLEPW2.Phi() : DEF_VAL_FLOAT;

			genEventTree->Fill();

			//////////////////////////////////////////////////
			// jets
			//////////////////////////////////////////////////

			vector<TLorentzVector> genHeavy;
			if( TMath::Abs(HIGGSB1.Py())>0) genHeavy.push_back( HIGGSB1);
			if( TMath::Abs(HIGGSB2.Py())>0) genHeavy.push_back( HIGGSB2);
			if( TMath::Abs(TOPHADB.Py())>0) genHeavy.push_back( TOPHADB);
			if( TMath::Abs(TOPLEPB.Py())>0) genHeavy.push_back( TOPLEPB);
			vector<TLorentzVector> genLight;
			if(  TMath::Abs(TOPHADW1.Py())>0) genLight.push_back( TOPHADW1);
			if(  TMath::Abs(TOPHADW2.Py())>0) genLight.push_back( TOPHADW2);

			
			int nj = it->n__jet;
			//jet loop
			for(int hj = 0; hj < nj; hj++) {
				//std::cout << "jet n " << hj << std::endl;
				float eGen   = it->gen_jet__pt[hj] * TMath::CosH(it->gen_jet__eta[hj]);
				float ptGen  = it->gen_jet__pt[hj];
				float etaGen = it->gen_jet__eta[hj];
				float phiGen = it->gen_jet__phi[hj];

				float pt = it->jet__pt[hj];
				float eta = it->jet__eta[hj];
				float phi = it->jet__phi[hj];
				float e = it->jet__energy[hj];
				float m = it->jet__mass[hj];

				// This is filled only for hJets
				//int id = it->jet__pileupJetId[hj];
				//float JECUnc = (coll==0) ? aint)hJet_JECUnc  [hj] : aJet_JECUnc  [hj];
				int flavor = it->jet__id[hj];

				// only jets passing ID...
				//if (id < 0.5) continue;
				if (!(pt > 20)) continue;
				if (!(TMath::Abs(eta) < 2.5)) continue;

				TLorentzVector p4;
				p4.SetPtEtaPhiM( pt, eta, phi, m );

				// only jets above the pt cut

				// only jets in acceptance

				// for csv systematics
				float csv = TMath::Max(it->jet__bd_csv[hj], float(0.0));
				float csv_std = 0.0;
				float csv_mva = 0.0;

				// this is to avoid the spike
				if( csv_std<=0. ) csv_mva = 0.;

				// matches a gen b quark from t->bW or H->bb ?
				int matchesB = 0;
				int posB = 999;
				for(int k = 0; k < (int)genHeavy.size(); k++) {
					if( deltaR(genHeavy[k], p4 ) < 0.3 ) {
						matchesB++;
						posB = k;
					}
				}
				// matches a gen udcs quark from W->qq' ?
				int matchesL = 0;
				int posL = DEF_VAL_INT;
				for(int k = 0; k < (int)genLight.size(); k++) {
					if( deltaR(genLight[k], p4 ) < 0.3 ) {
						matchesL++;
						posL = k;
					}
				}

				// 1st case: the jet is matched to flavor 5
				if( abs(flavor)==5 ) {

					//fillRegressionBranchesPerJet( jt->regVarsFHeavy, jt->regVarsIHeavy, currentTree0, i, hj, int(verbose));

					jt->eRecoHeavy	= e;
					jt->ptRecoHeavy   = pt;
					jt->etaRecoHeavy  = eta;
					jt->phiRecoHeavy  = phi;
					jt->massRecoHeavy = m;
					jt->csvRecoHeavy  = csv;
					jt->csvRecoStdHeavy  = csv_std;
					jt->csvRecoMVAHeavy  = csv_mva;

					jt->flavorHeavy   = abs(flavor);

					jt->eGenHeavy	 = eGen;
					jt->ptGenHeavy	= ptGen;
					jt->etaGenHeavy   = etaGen;
					jt->phiGenHeavy   = phiGen;

					// no ambiguous matches...
					if( matchesB==1 && matchesL==0 && posB != DEF_VAL_INT ) {
						jt->ePartHeavy = genHeavy[posB].E();
						jt->ptPartHeavy = genHeavy[posB].Pt();
						jt->etaPartHeavy = genHeavy[posB].Eta();
						jt->phiPartHeavy=  genHeavy[posB].Phi();
					}
					else {
						jt->ePartHeavy   = DEF_VAL_FLOAT;
						jt->ptPartHeavy  = DEF_VAL_FLOAT;
						jt->etaPartHeavy = DEF_VAL_FLOAT;
						jt->phiPartHeavy = DEF_VAL_FLOAT;
					}

					if ( evalReg ) {
						float output = DEF_VAL_FLOAT;
						//getRegressionEnergy(output, "BDTG", reader, readerVars, currentTree0, i, hj, 1.0, int(verbose));
						jt->eRecoRegHeavy  = output*TMath::CosH( jt->etaRecoHeavy );
						jt->ptRecoRegHeavy = output;
					}
					else {
						jt->eRecoRegHeavy  = DEF_VAL_FLOAT;
						jt->ptRecoRegHeavy = DEF_VAL_FLOAT;
					}

					genJetHeavyTree->Fill();
				}

				// 2nd case: the jet is matched to flavor < 5
				else if( abs(flavor)<5 ) {
					jt->eRecoLight	= e;
					jt->ptRecoLight   = pt;
					jt->etaRecoLight  = eta;
					jt->phiRecoLight  = phi;
					jt->massRecoLight = m;
					jt->csvRecoLight  = csv;
					jt->csvRecoStdLight  = csv_std;
					jt->csvRecoMVALight  = csv_mva;
					jt->flavorLight   = abs(flavor);

					jt->eGenLight	 = eGen;
					jt->ptGenLight	= ptGen;
					jt->etaGenLight   = etaGen;
					jt->phiGenLight   = phiGen;

					// no ambiguous matches...
					if( matchesB==0 && matchesL==1 && posL != DEF_VAL_INT ) {
						jt->ePartLight = genLight[posL].E();
						jt->ptPartLight = genLight[posL].Pt();
						jt->etaPartLight = genLight[posL].Eta();
						jt->phiPartLight = genLight[posL].Phi();
					}
					else {
						jt->ePartLight = DEF_VAL_FLOAT;
						jt->ptPartLight = DEF_VAL_FLOAT;
						jt->etaPartLight = DEF_VAL_FLOAT;
						jt->phiPartLight = DEF_VAL_FLOAT;
					}

					genJetLightTree->Fill();

				}

				// 3rd case: gluon
				else if( abs(flavor)==21 ) {

					jt->eRecoGluon = e;
					jt->ptRecoGluon = pt;
					jt->etaRecoGluon = eta;
					jt->phiRecoGluon = phi;
					jt->massRecoGluon = m;
					jt->csvRecoGluon = csv;
					jt->csvRecoStdGluon = csv_std;
					jt->csvRecoMVAGluon = csv_mva;
					jt->flavorGluon = abs(flavor);

					jt->eGenGluon = eGen;
					jt->ptGenGluon = ptGen;
					jt->etaGenGluon = etaGen;
					jt->phiGenGluon = phiGen;

					genJetGluonTree->Fill();
				}


			} //jet loop

			//////////////////////////////////////////////////
			// gen decay
			//////////////////////////////////////////////////

			if(TMath::Abs(TOPHADW2.Py())>0 &&  TMath::Abs(TOPHADW1.Py())>0 && TMath::Abs(TOPHADB.Py())>0 &&
					TMath::Abs(TOPLEPW2.Py())>0 &&  TMath::Abs(TOPLEPW1.Py())>0 && TMath::Abs(TOPLEPB.Py())>0 &&
					(it->hypo1 == 2 || it->hypo1 == 3) //check for SL
			  ) {

				TLorentzVector TOPLEP = TOPLEPW1+TOPLEPW2+TOPLEPB;
				TLorentzVector TOPHAD = TOPHADW1+TOPHADW2+TOPHADB;

				TVector3 boostToTopHadCMS = TOPHAD.BoostVector();
				TVector3 boostToTopLepCMS = TOPLEP.BoostVector();

				// first deal with TOPHAD...

				TOPHADW1.Boost(-boostToTopHadCMS);
				TOPHADW2.Boost(-boostToTopHadCMS);
				TOPHADB.Boost( -boostToTopHadCMS);

				TVector3 boostToWHadCMS = (TOPHADW1+TOPHADW2).BoostVector();
				TOPHADW1.Boost(-boostToWHadCMS);
				TOPHADW2.Boost(-boostToWHadCMS);

				jt->BetaW	 = TMath::Cos((TOPHADB.Vect()).Angle( boostToTopHadCMS  ));
				//FIXME, what is this i?
				//jt->GammaW	= i%2==0 ? TMath::Cos( (TOPHADW1.Vect()).Angle(boostToWHadCMS) ) : TMath::Cos( (TOPHADW2.Vect()).Angle(boostToWHadCMS) );  //average over W flavor (unobserved)


				// then deal with TOPLEP...

				TOPLEPW1.Boost(-boostToTopLepCMS);
				TOPLEPW2.Boost(-boostToTopLepCMS);
				TOPLEPB.Boost( -boostToTopLepCMS);

				TVector3 boostToWLepCMS = (TOPLEPW1+TOPLEPW2).BoostVector();
				TOPLEPW1.Boost(-boostToWLepCMS);
				TOPLEPW2.Boost(-boostToWLepCMS);

				jt->BetaWLep	 = TMath::Cos( (TOPLEPB.Vect()).Angle( boostToTopLepCMS  ));
				jt->GammaWLep	= TMath::Cos( (TOPLEPW1.Vect()).Angle(boostToWLepCMS) );

				/*
				cout << "*** check..." << endl;
				cout << "- TOPLEPW1 M=" << TOPLEPW1.M() << endl;
				cout << "- TOPLEPW2 M=" << TOPLEPW2.M() << endl;
				cout << "- GammaWLep = " << GammaWLep << endl;
				cout << "************" << endl;
				*/

				genTree->Fill();
			}

		} // event loop

	} // samples loop

	std::cout << "genTree " << genTree->GetEntries() << std::endl;
	outfile->Write();	
	return 0;

}
