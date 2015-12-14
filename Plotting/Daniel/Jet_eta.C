#include "TTree.h"

#define CSVM 0.89
#define ETACUT 2.4
#define PTCUT 30.0
#define HARDPTCUT 30.0
#define HTCUT 450.0
#define NBCUT 3
#define NMAXJETS 30

void Jet_eta(){

  vector<string> samples;
  //samples.push_back( "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/ethz-higgs/run2/VHBBHeppyV14/ttHTobb_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V14_ttHTobb_M125_13TeV_powheg_pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151025_084144/0000/tree_33.root" );
  //samples.push_back( "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/ethz-higgs/run2/VHBBHeppyV14/TT_TuneCUETP8M1_13TeV-powheg-pythia8/VHBB_HEPPY_V14_TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151024_212301/0000/tree_33.root" );
  samples.push_back( "root://xrootd-cms.infn.it//store/user/arizzi/VHBBHeppyV14/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V14_QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151026_081050/0000/tree_33.root" );
  samples.push_back( "root://xrootd-cms.infn.it//store/user/arizzi/VHBBHeppyV14/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V14_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151024_181957/0000/tree_33.root" );
  samples.push_back( "root://xrootd-cms.infn.it//store/user/arizzi/VHBBHeppyV14/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V14_QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151025_083726/0000/tree_33.root" );
  samples.push_back( "root://xrootd-cms.infn.it//store/user/arizzi/VHBBHeppyV14/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V14_QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151025_083753/0000/tree_33.root" );
  samples.push_back( "root://xrootd-cms.infn.it//store/user/arizzi/VHBBHeppyV14/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V14_QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151025_093151/0000/tree_33.root" );
  samples.push_back( "root://xrootd-cms.infn.it//store/user/arizzi/VHBBHeppyV14/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V14_QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151024_184123/0000/tree_22.root" );

  for(int s=0; s<samples.size(); s++){
    TString fname;
    if(samples[s].find("ttHTobb") != string::npos) fname = "TTH";
    if(samples[s].find("TT_Tune") != string::npos) fname = "TTJets";
    if(samples[s].find("QCD_HT300") != string::npos) fname = "QCD300";
    if(samples[s].find("QCD_HT500") != string::npos) fname = "QCD500";
    if(samples[s].find("QCD_HT700") != string::npos) fname = "QCD700";
    if(samples[s].find("QCD_HT1000") != string::npos) fname = "QCD1000";
    if(samples[s].find("QCD_HT1500") != string::npos) fname = "QCD1500";
    if(samples[s].find("QCD_HT2000") != string::npos) fname = "QCD2000";

    // Declare calculated variables
    int tot = 0;
    
    TString outname = "jets_"+fname+".root";
    // clean output file (if any)
    gSystem->Exec( "rm "+outname );
    // create output file
    TFile *fout_tmp = TFile::Open( outname,"UPDATE");

    // output tree
    TTree *tree  = new TTree("tree","");

    // variables to save in new trees
    int njet; //njets with pT>30 GeV
    int njeteta; //njets with pT>30 GeV && |eta|<2.4
    int nbtag; //njets with pT>30 GeV && CSV>0.89
    int nbtageta; //njets with pT>30 GeV && CSV>0.89 && |eta|<2.4
    int nhardjet; //njets with pT>40 GeV && |eta|<2.4
    float HT;
    float jet_pt      [NMAXJETS];  //jets sorted by decreasing pT
    float jet_eta     [NMAXJETS];
    float jet_csv     [NMAXJETS];
    
    // branches to save
    tree->Branch("njet",         &njet,         "njet/I");
    tree->Branch("njeteta",      &njeteta,      "njeteta/I");
    tree->Branch("nbtag",        &nbtag,        "nbtag/I");
    tree->Branch("nbtageta",     &nbtageta,     "nbtageta/I");
    tree->Branch("nhardjet",     &nhardjet,     "nhardjet/I");
    tree->Branch("HT",           &HT,           "HT/F");
    tree->Branch("jet_pt",       jet_pt,        "jet_pt[njet]/F");
    tree->Branch("jet_eta",      jet_eta,       "jet_eta[njet]/F");
    tree->Branch("jet_csv",      jet_csv,       "jet_csv[njet]/F");
    
    // declare histograms
    TH1F* hnjet = new TH1F("hnjet","; njets; Events", 15 , 0, 15 );
    TH1F* hnjeteta = new TH1F("hnjeteta","; njets; Events", 15 , 0, 15 );
    TH1F* hnbtag = new TH1F("hnbtag","; nbtags; Events", 8 , 0, 8 );
    TH1F* hnbtageta = new TH1F("hnbtageta","; nbtags; Events", 8 , 0, 8 );
    TH1F* hnhardjet = new TH1F("hnhardjet","; njets; Events", 15 , 0, 15 );
    TH1F* hHT = new TH1F("hHT","; HT [GeV]; Events", 40 , 0, 2000 );
    
    // load file
    //TFile* file = TFile::Open( "root://xrootd-cms.infn.it//store/user/arizzi/VHBBHeppyV14/ttHTobb_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V14_ttHTobb_M125_13TeV_powheg_pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151025_084144/0000/tree_3.root" );
    TFile *file = TFile::Open( samples[s].c_str() );
    
    if(file==0 || file->IsZombie() ) return;
    
    // load tree
    TTree *intree = (TTree*)file->Get("tree");
    
    // declare leaf types
    Int_t   nJet;
    Float_t Jet_pt[NMAXJETS];
    Float_t Jet_eta[NMAXJETS];
    Float_t Jet_btagCSV[NMAXJETS];
    
    // Connect the branches with their member variables.
    if(!intree) return;
    intree->SetBranchAddress("nJet",        &nJet);
    intree->SetBranchAddress("Jet_pt",      Jet_pt);
    intree->SetBranchAddress("Jet_eta",     Jet_eta);
    intree->SetBranchAddress("Jet_btagCSV", Jet_btagCSV);
    
    int totalEntries = intree->GetEntries();
    cout << totalEntries << endl;
    
    //////////////////////////////////////////////////// loop over events
    for(int entry=0; entry < totalEntries; entry++){
      intree->GetEntry(entry);
      tot++;
      
      // reset variables
      nhardjet = 0;
      njet = 0;
      njeteta = 0;
      nbtag = 0;
      nbtageta = 0;
      HT = 0.0;
      for(int k = 0; k < NMAXJETS ; k++ ){
	jet_pt   [k] = -99;
	jet_eta  [k] = -99;
	jet_csv  [k] = -99;
      }
      
      // print the processed event number
      if(entry%10000==0){
	cout << entry << " (" << float(entry)/float(totalEntries)*100 << " %)" << endl;
      }
      
      
      for(int j=0; j<nJet; j++){
	if(Jet_pt[j]>PTCUT ){
	  jet_pt[njet]=Jet_pt[j];
	  jet_eta[njet]=Jet_eta[j];
	  jet_csv[njet]=Jet_btagCSV[j];	
	  HT += Jet_pt[j];
	  njet++;
	  if( Jet_btagCSV[j] > CSVM && Jet_btagCSV[j]<=1 ) nbtag++;
	  if( Jet_eta[j]<ETACUT && Jet_eta[j]>-ETACUT ){
	    njeteta++;
	    if( Jet_pt[j] > HARDPTCUT ) nhardjet++;
	    if( Jet_btagCSV[j] > CSVM && Jet_btagCSV[j]<=1 ) nbtageta++;
	  }
	}
      }
      
      // fill the tree...
      tree->Fill();
      
      // fill historgrams
      hnjet->Fill(njet);
      hnjeteta->Fill(njeteta);
      hnbtag->Fill(nbtag);
      hnbtageta->Fill(nbtageta);
      hnhardjet->Fill(nhardjet);
      hHT->Fill(HT);
    }
    
    // save the tree and histograms in the ROOT file
    fout_tmp->cd();
    tree ->Write("",TObject::kOverwrite );
    hnjet     ->Write("",TObject::kOverwrite );
    hnjeteta  ->Write("",TObject::kOverwrite );
    hnbtag    ->Write("",TObject::kOverwrite );
    hnbtageta ->Write("",TObject::kOverwrite );
    hnhardjet ->Write("",TObject::kOverwrite );
    hHT       ->Write("",TObject::kOverwrite );
    fout_tmp->Close();
  }
  
  return;
}
