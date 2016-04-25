#define RUNONDATA 0
#define LOGSCALE 0
#define NORMALIZE 0
#define POISSON 0
#define SAVEPLOTS 0
#define MAXEVENTS 100000
#define NMAXJETS 30
#define CAT 11    // 7, 8, 9, 10, 11 or <0 for all
#define METHOD8 11 // 10=4w2h2t or 11=3w2h2t
#define CUT_HT 500.0
#define PSB_FAC 0.02
#define CSVM 0.89
#define LUMI 10.0  //Just for now

#include <fstream>

void MED_plots(){

  TStopwatch* clock = new TStopwatch();
  clock->Start();

  float xmin  = 0;
  float xmax  = 200;

  string folder = "/scratch/dsalerno/TTH_MEM_74X/V14/crab_151222/";

  string variable;
  //variable = "leadjet_pt";
  //variable = "num_btag";
  //variable = "leadjet_eta";
  //variable = "btagLR";     xmin=-1.0;  xmax=2.0;     //xmin sets the bLR cut
  
  variable = "Psb";       xmin=0.0;  xmax=1.0;

  string tag = "_withtrig"; //"_Psb0pt55";
  string method = "";
  if(CUT_HT>0) tag += Form("_HT%.0f",CUT_HT);  
  if(CAT<0) tag += "_catAll";
  else tag += Form("_cat%d",CAT);
  tag += Form("_%.3f",PSB_FAC);
  if(variable == "btagLR") tag += Form("bLR_%f",xmin);
  if(RUNONDATA) tag += "_data";
  if(LOGSCALE)  tag += "_log";  

  // determine ME method used if not cat all
  int element=-1;
  if(CAT==7){
    element = 11;
    method = "_3w2h2t";
  }
  else if(CAT==8){
    element = METHOD8; //10 or 11
    if(METHOD8==10) method = "_4w2h2t";
    else  method = "_3w2h2t"; //4w2h2t or 3w2h2t
  }
  else if(CAT==9){
    element = 10;
    method = "_4w2h2t";
  }
  else if(CAT==10){
    element = 12;
    method = "_4w2h1t";
  }
  else if(CAT==11){
    element = 12;
    method = "_4w2h21";
  }
  if(CAT>=0) tag += method;

  std::ofstream outfile( ("./logs/log_MED_"+variable+tag+".txt").c_str() ); 

  outfile << "Plotting variable " << variable << endl << endl;

  gStyle->SetOptStat(0);
  gStyle->SetTitleFillColor(0);
  gStyle->SetCanvasBorderMode(0);
  gStyle->SetCanvasColor(0);
  gStyle->SetPadBorderMode(0);
  gStyle->SetPadColor(0);
  gStyle->SetTitleFillColor(0);
  gStyle->SetTitleBorderSize(0);
  gStyle->SetTitleH(0.04);
  //gStyle->SetTitleFontSize(0.025);
  gStyle->SetTitleStyle(0);
  gStyle->SetTitleOffset(1.3,"y");

  TCanvas *c1 = new TCanvas("c1","",5,30,640,580);
  TPad *p1 = new TPad("p1","",0,0,1,1);
  
  if( tag.find("ratio") != string::npos ){
    c1 = new TCanvas("c1","",5,30,640,580/0.85);
    p1 = new TPad("p1","",0,0.155,1,1);
  }

  p1->SetGrid(0,0);
  p1->SetFillStyle(4000);
  p1->SetFillColor(10);
  p1->SetTicky();
  p1->SetTicks(0,0);
  p1->SetObjectStat(0);
  p1->Draw();
  p1->cd();

  p1->SetTopMargin(0.05);

  TString cmsinfo = "";
  if(RUNONDATA==0) cmsinfo = Form("Simulation                                                  %.1f fb^{-1} (13 TeV)",LUMI);
  else cmsinfo =             Form("CMS Preliminary                                     %.1f fb^{-1} (13 TeV)",LUMI);

  TPaveText *pt_title = new TPaveText(0.1, 0.952, 0.9, 1.0,"brNDC");
  pt_title->SetFillStyle(1001);
  pt_title->SetBorderSize(0);
  pt_title->SetFillColor(0);
  pt_title->SetTextFont(42); 
  pt_title->SetTextSize(0.04); 
  pt_title->AddText(cmsinfo);

  TLegend* leg = new TLegend(0.42,0.54,0.67,0.91,NULL,"brNDC");
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetFillColor(10);
  leg->SetTextSize(0.04);

  THStack* hStack = new THStack("hStack","Title; x-axis ; events ");

  // set samples here
  vector<string> samples;
  //samples.push_back("dummy");
  //samples.push_back("QCDMultijet");
  samples.push_back("QCD");
  samples.push_back("TTJets");
  samples.push_back("TTH");
  if(RUNONDATA)  samples.push_back("Data");

  TH1F* hS    = 0;
  TH1F* hData = 0;
  TH1F* hErr  = 0;

  TH1F* httH  = 0;
  TH1F* hQCD  = 0;
  TH1F* httjj = 0;
  TH1F* httcc = 0;
  TH1F* httb  = 0;
  TH1F* httbb = 0;

  // determine plot parameters for different variables
  TString title = "Histogram title";
  int   nbins = 30;
  TString xaxis = "m";

  if(variable=="leadjet_pt"){
    title = "seventh jet pT";
    nbins = 30;
    xmin = 20;
    xmax = 8000;
    xaxis = "p_{T}";
  }
  if(variable=="num_btag"){
    title = "number of CSVM";
    nbins = 9;
    xmin = 0;
    xmax = 9;
    xaxis = "no. b";
  }
  if(variable=="leadjet_eta"){
    title = "leading jet #eta";
    nbins = 30;
    xmin = -3.0;
    xmax = 3.0;
    xaxis = "leading jet #eta";
  }
  if(variable.find("btagLR")==0){
    title = ("b_{LR}: "+variable).c_str();
    nbins = 30;
    xaxis = "b_{LR}";
  }
  if(variable.find("Psb")==0){
    title = "Matrix Element Discriminant";
    nbins = 6;
    xaxis = "Psb";
  }

  // master histogram (all other histograms are a clone of this one)
  TH1F* h1 = new TH1F("h1",""+title+"; "+xaxis+"; Events", nbins , xmin, xmax );

  h1->GetXaxis()->SetTitleFont(62);
  h1->GetXaxis()->SetTitleSize(0.04);
  h1->GetXaxis()->SetLabelFont(62);
  h1->GetXaxis()->SetLabelSize(0.038);

  h1->GetYaxis()->SetTitleFont(62);
  h1->GetYaxis()->SetTitleSize(0.039);
  h1->GetYaxis()->SetLabelFont(62);
  h1->GetYaxis()->SetLabelSize(0.038);

  // clone histograms
  httH  = (TH1F*)h1->Clone("httH" );
  hQCD  = (TH1F*)h1->Clone("hQCD" );
  httjj = (TH1F*)h1->Clone("httjj");
  httcc = (TH1F*)h1->Clone("httcc");
  httb  = (TH1F*)h1->Clone("httb" );
  httbb = (TH1F*)h1->Clone("httbb");
  hErr  = (TH1F*)h1->Clone("Err");
  hData = (TH1F*)h1->Clone("hData");
  hS    = (TH1F*)h1->Clone("hS");

  // set histogram styles
  hS   ->SetLineWidth( 4 );
  hS   ->SetLineColor( kBlue+2 );
  hS   ->Sumw2();
  httH ->SetLineColor( kBlue+2 );
  httH ->SetFillColor( kBlue+2 );
  httH ->SetFillStyle( 3002 );
  httH ->SetMarkerColor( kBlue+2 );
  httH ->SetMarkerStyle( 20 );
  httH ->SetMarkerSize( 2 );
  httH ->Sumw2();
  hQCD ->SetLineColor( kGreen+3 );
  hQCD ->SetFillColor( kGreen+3 );
  hQCD ->SetMarkerColor( kGreen+3 );
  hQCD ->SetMarkerStyle( 21 );
  hQCD ->SetMarkerSize( 2 );
  hQCD ->Sumw2();
  httjj->SetLineColor( kRed-7 );
  httjj->SetFillColor( kRed-7 );
  httjj->SetMarkerColor( kRed-7 );
  httjj->SetMarkerStyle( 22 );
  httjj->SetMarkerSize( 2 );
  httjj->Sumw2();
  httcc->SetLineColor( kRed+1 );
  httcc->SetFillColor( kRed+1 );
  httcc->SetMarkerColor( kRed+1 );
  httcc->SetMarkerStyle( 33 );
  httcc->SetMarkerSize( 2 );
  httcc->Sumw2();
  httb ->SetLineColor( kRed-2 );
  httb ->SetFillColor( kRed-2 );
  httb ->SetMarkerColor( kRed-2 );
  httb ->SetMarkerStyle( 34 );
  httb ->SetMarkerSize( 2 );
  httb ->Sumw2();
  httbb->SetLineColor( kRed+3 );
  httbb->SetFillColor( kRed+3 );
  httbb->SetMarkerColor( kRed+3 );
  httbb->SetMarkerStyle( 29 );
  httbb->SetMarkerSize( 2 );
  httbb->Sumw2();
  hErr ->SetLineColor( kBlack );
  hErr ->SetFillColor( kBlack );
  hErr ->SetFillStyle( 3654 );
  hData->SetMarkerStyle( 20 );
  hData->SetMarkerSize( 1.5 );
  hData->SetMarkerColor( kBlack );
  hData->SetLineColor( kBlack );
  hData->SetLineWidth( 2 );

  // loop over samples
  for(unsigned int s=0; s<samples.size(); s++){

    outfile << endl << "Running sample " << samples[s] << endl;
    cout << endl << "Running sample " << samples[s] << endl;

    vector<string> fname;
    
    if( samples[s] == "QCD" ){
      //fname.push_back(folder+"QCD300/tree_QCD300.root");      
      fname.push_back(folder+"QCD500/tree_QCD500.root");
      fname.push_back(folder+"QCD700/tree_QCD700.root");
      fname.push_back(folder+"QCD1000/tree_QCD1000.root");
      fname.push_back(folder+"QCD1500/tree_QCD1500.root");
      fname.push_back(folder+"QCD2000/tree_QCD2000.root");
    }
    else if( samples[s].find("Data") != string::npos ){
      fname.push_back(folder+"ME_data.root");
    }
    else if( samples[s] == "TTH" ){
      fname.push_back(folder+"TTH/tree_TTH_part.root");
    }
    else{
      fname.push_back(folder+samples[s]+"/tree_"+samples[s]+".root");
    }
    // loop over input files
    for(unsigned int f=0; f<fname.size(); f++){
      
      outfile << endl << "Running file " << fname[f] << endl;

      float nGen_fac = 1.0;
      if( fname[f].find("/TTH/") != string::npos ) nGen_fac = 3933404.0/(3933404.0-3089.0);
      // else if( fname[f].find("TTJets") != string::npos ) nGen_fac = 19757190.0/14278690.0;
      // else if( fname[f].find("QCD300") != string::npos ) nGen_fac = 19466760.0/18282047.0;
      // else if( fname[f].find("QCD500") != string::npos ) nGen_fac = 19664159.0/17830047.0;
      // else if( fname[f].find("QCD700") != string::npos ) nGen_fac = 15165288.0/13441279.0;
      // else if( fname[f].find("QCD1000") != string::npos ) nGen_fac = 4963895.0/4461516.0;
      // else if( fname[f].find("QCD1500") != string::npos ) nGen_fac = 3691495.0/3415737.0;
      // else if( fname[f].find("QCD2000") != string::npos ) nGen_fac = 1912529.0/1862522.0
							    ;

      //float psb_bins[13] = {0.0, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 1.0};
      float psb_bins[13] = {0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.63, 0.67, 0.7, 0.8, 0.9, 1.1};
      float psb_counts[12] = {0.0};

      // load file
      TFile* file = TFile::Open( fname[f].c_str() );
      if(file==0 || file->IsZombie() ) continue;
      
      // load tree
      TTree *tree = (TTree*)file->Get("tree");

      // Declare calculated variables
      int numEvents = 0;
      int numSelected = 0;
      int numttbb = 0;
      int numttbj = 0;
      int numttcc = 0;
      int numttjj = 0;
      float eval;
      int MCweight = 0;

      // Declare leaf types
      int    numJets;
      int    nBCSVM;
      int    cat;
      int    njets;
      double ht;
      double jets_pt      [NMAXJETS];  //jets sorted by decreasing pT
      double jets_eta     [NMAXJETS];
      double jets_phi     [NMAXJETS];
      double jets_mass    [NMAXJETS];
      double jets_btagCSV [NMAXJETS];
      double jets_qgl     [NMAXJETS];
      
      int   nleps;
      // float leps_pt     [99];  //loose leptons
      // float leps_eta    [99];
      // float leps_phi    [99];
      // float leps_mass      [99];
      // float lepton_charge [99];
      // float lepton_rIso   [99];
      // int   lepton_type   [99];

      // float MET_pt;
      // float MET_phi;
      // float MET_sumEt;
 
      // int       Vtype;
      // EventInfo EVENT;
      // UChar_t   triggerFlags[70];
      double    weight_xs;
      // float     QCDweight;
      // float     Trigweight;
      int       cat_gen;        //-1=unknown, 0=SL, 1=DL, 2=FH
      double    puWeight;
      double    genWeight;
      double    btag_LR;
      double    mem_tth_p[13];
      double    mem_ttbb_p[13];
      int       triggerDecision;
      
      //float p4H       [4];    //generator level 4-vectors: 0=pT, 1=eta, 2=phi, 3=m
      //float p4T       [4];
      //float p4Tbar    [4];
      
      //int   nSimBs;
      int   nMatchSimB;    //use for tt+jets subsample: ttbb, ttbj, or ttjj
      int   nMatchSimC;    //use for tt+jets subsample: ttcc or ttjj

      // Connect the branches with their member variables.
      if(!tree) return;
      tree->SetBranchAddress("numJets",       &numJets);
      tree->SetBranchAddress("nBCSVM",        &nBCSVM);
      tree->SetBranchAddress("cat",           &cat);
      tree->SetBranchAddress("njets",         &njets);
      tree->SetBranchAddress("ht",            &ht);     
      tree->SetBranchAddress("jets_pt",       jets_pt);
      tree->SetBranchAddress("jets_eta",      jets_eta);
      tree->SetBranchAddress("jets_phi",      jets_phi);
      tree->SetBranchAddress("jets_mass",     jets_mass);
      tree->SetBranchAddress("jets_btagCSV",  jets_btagCSV);
      tree->SetBranchAddress("jets_qgl",      jets_qgl);

      tree->SetBranchAddress("nleps",        &nleps);
      //tree->SetBranchAddress("leps_pt",      leps_pt);
      //tree->SetBranchAddress("leps_eta",     leps_eta);
      //tree->SetBranchAddress("leps_phi",     leps_phi);
      //tree->SetBranchAddress("leps_mass",    leps_mass);
      //tree->SetBranchAddress("lepton_charge",lepton_charge);
      //tree->SetBranchAddress("lepton_rIso",  lepton_rIso);
      //tree->SetBranchAddress("lepton_type",  lepton_type);

      //tree->SetBranchAddress("MET_pt",       &MET_pt);
      //tree->SetBranchAddress("MET_phi",      &MET_phi);
      //tree->SetBranchAddress("MET_sumEt",    &MET_sumEt);
      
      //tree->SetBranchAddress("Vtype",         &Vtype);
      //tree->SetBranchAddress("EVENT",        &EVENT);
      //tree->SetBranchAddress("triggerFlags",  triggerFlags);
      tree->SetBranchAddress("weight_xs",        &weight_xs);
      //tree->SetBranchAddress("QCDweight",     &QCDweight);
      //tree->SetBranchAddress("Trigweight",    &Trigweight);
      
      tree->SetBranchAddress("cat_gen",          &cat_gen);
      tree->SetBranchAddress("puWeight",         &puWeight);
      tree->SetBranchAddress("genWeight",        &genWeight);
      tree->SetBranchAddress("btag_LR_4b_2b",    &btag_LR);
      tree->SetBranchAddress("mem_tth_p",        mem_tth_p);
      tree->SetBranchAddress("mem_ttbb_p",       mem_ttbb_p);
      tree->SetBranchAddress("triggerDecision",  &triggerDecision);
      
      //tree->SetBranchAddress("p4H",          p4H);
      //tree->SetBranchAddress("p4T",          p4T);
      //tree->SetBranchAddress("p4Tbar",       p4Tbar);
      
      //tree->SetBranchAddress("nSimBs",       &nSimBs);
      tree->SetBranchAddress("nMatchSimB",  &nMatchSimB);
      tree->SetBranchAddress("nMatchSimC",  &nMatchSimC);
      
      int totalEntries = tree->GetEntries();
      outfile << totalEntries << endl;
      
      int nEvents = 0;
      if( (MAXEVENTS<0) || (MAXEVENTS>totalEntries)  ) nEvents = totalEntries;
      else nEvents = MAXEVENTS;

      float scalefac = float(totalEntries)/float(nEvents) * nGen_fac;
      float lumi = LUMI*1000.0; //weight_xs scales to 1 pb-1 or 0.001 fb-1
     
      // no rescaling for all hadronic ttbar decay filter

      //////////////////////////////////////////////////// loop over events
      for(int entry=0; entry < nEvents; entry++){
	tree->GetEntry(entry);
	numEvents++;
	eval = -99.;
	
	// print the processed event number
	if(entry%(totalEntries/20)==0){
	  cout << entry << " (" << float(entry)/float(totalEntries)*100 << " %)" << endl;
	}
	// lepton veto
	if( nleps > 0 ) continue;
	
	int limit = njets<NMAXJETS ? njets : NMAXJETS;
	
	// calculate number of b-tag medium and save indices	
	int n_btag = nBCSVM;
	if( (samples[s].find("QCDMultijet") != string::npos) && n_btag == 2 ) n_btag = 4;

	// calculate HT
	// already in tree as "ht"

	// event selection - category and correct tt+jets subsample
	bool pass = true;

	// gen filter on all hadronic ttbar decay
	// if( (samples[s]== "TTH" || samples[s]== "TTJets") && cat_gen!=2 ) continue;
	
	// Trigger selection
	if( triggerDecision<=0 ) continue;

	// HT cut
	if( ht < CUT_HT) continue;

	// MED selection
	if( CAT>=0 && cat!=CAT ) continue;

	// Cut on Psb
	// if( mem_tth_p[6]/(mem_tth_p[6]+PSB_FAC*mem_ttbb_p[6])<0.55 ) continue;
	
	// selection
	if( pass ){
	  
	  // determine ME method used if cat all
	  if(CAT<0){
	    if(cat==7){
	      element = 11;
	    }
	    else if(cat==8){
	      element = METHOD8;
	    }
	    else if(cat==9){
	      element = 10;
	    }
	    else if(cat==10){
	      element = 12;
	    }
	    else if(cat==11){
	      element = 12;
	    }
	  }

	  MCweight = genWeight/abs(genWeight);  //either +1 or -1

	  // calculate variable to be plotted
	  /*if(variable=="leadjet_pt"){
	    float maxpt = 0.0;
	    for(int i=0; i<limit; i++){
	      if(jet_pt[i]>maxpt) maxpt = jet_pt[i];
	    }
	    eval = maxpt;
	    numSelected += MCweight;
	  }
	  if(variable=="num_btag"){
	    eval = float(n_btag);
	    numSelected += MCweight;
	  }
	  if(variable=="leadjet_eta"){
	    float maxpt = 0.0;
	    float leadeta = -99.0;
	    for(int i=0; i<limit; i++){
	      if(jet_pt[i]>maxpt){
		maxpt = jet_pt[i];
		leadeta = jet_eta[i];
	      }
	    }
	    eval = leadeta;
	    numSelected += MCweight;
	  }
	  if(variable=="btagLR"){
	    if(btagLR >= xmin){
	      eval = btag_LR;
	      numSelected += MCweight;
	    }
	  } */
	  if(variable=="Psb"){
	    eval = mem_tth_p[element]/(mem_tth_p[element]+PSB_FAC*mem_ttbb_p[element]);
	    numSelected += MCweight;

	    // determine Psb bin - to find optimal Psb cut
	    // for( int i=0; i<12; i++){
	    //   if( eval >= psb_bins[i] && eval < psb_bins[i+1] ){
	    // 	psb_counts[i] += MCweight*weight_xs*scalefac*lumi; //need Trigweight
	    //   }
	    // }

	  }

	  // determine tt+jets subsample
	  int ttjets = 0;
	  if( samples[s].find("TTJets") != string::npos ){	  
	    if( nMatchSimB >= 2 ){
	      ttjets = 1; //ttbb
	    }
	    else if( nMatchSimB == 1 ){
	      ttjets = 2; //ttb
	    }
	    else if( nMatchSimB == 0 && nMatchSimC >= 1 ){
	      ttjets = 3; //ttcc
	    }
	    else if( nMatchSimB == 0 && nMatchSimC == 0 ){
	      ttjets = 4; //ttjj
	    }
	    else cout << "Error determining tt+jets subsample" << endl;
	  }

	  // fill the historams
	  if( samples[s].find("TTJets") != string::npos ){
	    if( ttjets == 1 ){
	      httbb->Fill(eval,MCweight*weight_xs*scalefac*lumi); //need Trigweight
	      numttbb++;
	    }	    
	    if( ttjets == 2 ){
	      httb ->Fill(eval,MCweight*weight_xs*scalefac*lumi);
	      numttbj++;
	    }
	    if( ttjets == 3 ){
	     httcc->Fill(eval,MCweight*weight_xs*scalefac*lumi);
	     numttcc++;
	    }
	    if( ttjets == 4 ){
	      httjj->Fill(eval,MCweight*weight_xs*scalefac*lumi);
	      numttjj++;
	    }
	  }
	  else if( samples[s].find("TTH") != string::npos ){
	    httH->Fill(eval,MCweight*weight_xs*scalefac*lumi);  //need Trigweight
	  }
	  else if( samples[s] == "QCD" ){
	    hQCD->Fill(eval,MCweight*weight_xs*scalefac*lumi);
	  }
	  else if( samples[s].find("QCDMultijet") != string::npos ){
	    //hQCD->Fill(eval,QCDweight*scalefac);
	  }
	  else if( samples[s].find("Data") != string::npos ){
	    hData->Fill(eval,MCweight*weight_xs*scalefac);
	  }
	  else{
	    outfile << "sample not found!" << endl;
	  }

	} //end selection
	
      } //end loop over events    

      outfile << "Total number of events " << numEvents << endl;
      outfile << "Number of selected events " << numSelected << endl;
      if( samples[s].find("TTJets") != string::npos ){
	outfile << "Number of ttbb events " << numttbb << " integral " << httbb->Integral() << endl;
	outfile << "Number of ttb  events " << numttbj << " integral " << httb ->Integral() << endl;
	outfile << "Number of ttcc events " << numttcc << " integral " << httcc->Integral() << endl;
	outfile << "Number of ttjj events " << numttjj << " integral " << httjj->Integral() << endl;
	outfile << "Bin integral " << httbb->Integral()+httb->Integral()+httcc->Integral()+httjj->Integral() << endl;
      }
      if( samples[s].find("TTH") != string::npos ){
	outfile << "Bin integral " << httH->Integral() << endl;
      }
      if( samples[s].find("QCD") != string::npos ){
	outfile << "Bin integral " << hQCD->Integral() << endl;
      }

      // for( int i=0; i<12; i++){
      // 	outfile << psb_bins[i] << " ";
      // }
      // outfile << endl;

      // for( int i=0; i<12; i++){
      // 	outfile << psb_counts[i] << " ";
      // }
      // outfile << endl;

    } //end loop over files
    
  } //end loop over samples

  
  if( RUNONDATA){
    if( POISSON ) hData->SetBinErrorOption(TH1::kPoisson);
    else hData->Sumw2();
  }
  
  // add histrograms to background error
  hErr->Add(hQCD, 1.0);
  hErr->Add(httbb, 1.0);
  hErr->Add(httb , 1.0);
  hErr->Add(httcc, 1.0);
  hErr->Add(httjj, 1.0);

  hS  ->Add(httH , 10.0);
  
  // add histrograms to stack
  hStack->Add(hQCD);
  hStack->Add(httbb);
  hStack->Add(httb);
  hStack->Add(httcc);
  hStack->Add(httjj);
  hStack->Add(httH);
  
  // add histograms to legend
  leg->AddEntry(httH,  "t#bar{t}H (125)", "F");
  leg->AddEntry(httjj, "t#bar{t} + lf", "F");
  leg->AddEntry(httcc, "t#bar{t} + c#bar{c}", "F");
  leg->AddEntry(httb,  "t#bar{t} + b", "F");
  leg->AddEntry(httbb, "t#bar{t} + b#bar{b}", "F");
  leg->AddEntry(hQCD,  "QCD Multijet", "F");
  if(RUNONDATA) leg->AddEntry(hData, "Data", "LPE");
  leg->AddEntry(hErr,  "Bkg. Unc.", "F");
  leg->AddEntry(hS,    "t#bar{t}H (125) x 10", "L");
 
  // set y-axis range
  float max =  TMath::Max( hErr->GetMaximum()*1.15,(hData!=0 ? hData->GetMaximum()*1.45 : -1.));
  if(LOGSCALE){
    hErr->GetYaxis()->SetRangeUser(1, max*8.0 );
    p1->SetLogy(1);
  }
  else hErr->GetYaxis()->SetRangeUser(0, max );
  cout << "max range is " << max << endl;
  // draw histograms
  hErr  ->Draw("HIST");
  hStack->Draw("HISTSAME");
  hS    ->Draw("HISTSAME");
  hErr  ->Draw("E2SAME");
  if(hData!=0) hData->Draw("PE1SAME");
  leg->Draw();

  pt_title->Draw();

    
  //-----------------------ratio plot-------------------
  if( tag.find("ratio") != string::npos ){
    
    c1->cd();
    TPad *p2 = new TPad("p1","",0,0,1,0.175);
    p2->SetGrid(0,0);
    p2->SetFillStyle(4000);
    p2->SetFillColor(10);
    p2->SetTicky();
    p2->SetObjectStat(0);
    p2->Draw();
    p2->cd();
    
    TF1* one = new TF1("one","1",0,1);

    TH1F* one_error = 0;
    one_error = (TH1F*)h1->Clone("one_error");
    
    TH1F* h_ratio = 0;
    h_ratio = (TH1F*)h1->Clone("h_ratio");

    TGraphAsymmErrors* g_ratio = new TGraphAsymmErrors(h1);
    if( g_ratio->GetN() != h_ratio->GetNbinsX() ){
      outfile << "g_ratio has different number of bins to h_ratio. return!" << endl;
      return;
    }

    // loop over bins
    for(int b=1; b<= h_ratio->GetNbinsX() ; b++){

      float nbkg     = hErr->GetBinContent(b);
      float nbkg_up  = hErr->GetBinContent(b) + hErr->GetBinError(b);
      float nbkg_low = hErr->GetBinContent(b) - hErr->GetBinError(b);
    
      float ndata      = hErr->GetBinContent(b);
      float ndataErr   = hErr->GetBinError(b);  
      if(RUNONDATA){
	ndata      = hData->GetBinContent(b);
	ndataErr   = hData->GetBinError(b);
      }

      float r       = nbkg>0 ? ndata/nbkg      : 0;
      float rErr    = nbkg>0 ? ndataErr/nbkg   : 0;

      float one_up  = nbkg_low >0 ? nbkg/nbkg_low : 0;
      float one_low = nbkg_up  >0 ? nbkg/nbkg_up  : 0;

      float xPoint  = h1->GetBinCenter(b);
      float xWidth  = 0.5*h1->GetBinWidth(b);

      h_ratio->SetBinContent(b, r);
      h_ratio->SetBinError(b,rErr);

      if(RUNONDATA && POISSON){

	float dataErrLow = hData->GetBinErrorLow(b);
	float dataErrUp  = hData->GetBinErrorUp(b);
	float rErrUp     = nbkg>0 ? dataErrUp/nbkg  : 0;
	float rErrLow    = nbkg>0 ? dataErrLow/nbkg : 0;

	g_ratio->SetPoint(b-1, xPoint, r);
	g_ratio->SetPointEYlow(b-1, rErrLow);
	g_ratio->SetPointEYhigh(b-1, rErrUp);
	g_ratio->SetPointEXlow(b-1, xWidth);
	g_ratio->SetPointEXhigh(b-1, xWidth);
      }

      one_error->SetBinContent(b, 1.0);
      one_error->SetBinError(b, (one_up-one_low)/2 );
    
    } //end loop over bins

    // set ratio histogram styles
    one_error->SetTitle(0);
    one_error->GetYaxis()->SetRangeUser(0.0,2.0);

    one_error->GetXaxis()->SetTitle(0);
    one_error->GetXaxis()->SetLabelSize(0);
    one_error->GetXaxis()->SetNdivisions(0);
    one_error->GetXaxis()->SetTickLength(0.1);

    one_error->GetYaxis()->SetTitleSize(0.18);
    one_error->GetYaxis()->SetTitleOffset(0.24);
    one_error->GetYaxis()->SetTitle("Data/MC  ");
    one_error->GetYaxis()->SetNdivisions(202);
    one_error->GetYaxis()->SetLabelSize(0.16);

    one_error->SetFillColor(kGreen);

    h_ratio->SetMarkerStyle(20);
    h_ratio->SetMarkerSize(1.5);
    h_ratio->SetMarkerColor(kBlack);
    h_ratio->SetLineColor(kBlack);
    h_ratio->SetLineWidth(2);

    g_ratio->SetMarkerStyle(20);
    g_ratio->SetMarkerSize(1.5);
    g_ratio->SetMarkerColor(kBlack);
    g_ratio->SetLineColor(kBlack);
    g_ratio->SetLineWidth(2);

    one->SetLineColor(kBlack);
    one->SetLineStyle(kDashed);
    one->SetLineWidth(1);

    one_error->Draw("E2");
    one->Draw("SAME");
    if(RUNONDATA && POISSON) g_ratio->Draw("PE1SAME");
    else h_ratio->Draw("PE1SAME");

  } //end ratio plot
  
  
  // save plots
  if( SAVEPLOTS ){
    c1->SaveAs(  ("./MED_plots/AH_"+variable+tag+".pdf").c_str() ); 
  }

  // Normalized plot
  if( NORMALIZE ){
    TCanvas *c2 = new TCanvas("c2","",5,30,640,580);
    TPad *p2 = new TPad("p2","",0,0,1,1);
  
    p2->SetGrid(0,0);
    p2->SetFillStyle(4000);
    p2->SetFillColor(10);
    p2->SetTicky();
    p2->SetTicks(0,0);
    p2->SetObjectStat(0);
    p2->Draw();
    p2->cd();
    
    p2->SetTopMargin(0.05);

    httH ->SetLineWidth( 4 );
    //httH ->SetFillStyle( 0 );

    hQCD ->SetLineWidth( 4 );
    //hQCD ->SetFillStyle( 0 );

    httjj ->SetLineWidth( 4 );
    //httjj ->SetFillStyle( 0 );

    httcc ->SetLineWidth( 4 );
    //httcc ->SetFillStyle( 0 );

    httb ->SetLineWidth( 4 );
    //httb ->SetFillStyle( 0 );

    httbb ->SetLineWidth( 4 );
    //httbb ->SetFillStyle( 0 );

    hQCD ->GetYaxis()->SetTitle("Normalized units");
    hQCD ->SetMaximum( hQCD->GetMaximum()*2.0 );   //CHANGE HERE
    hQCD ->DrawNormalized("PE");
    httbb->DrawNormalized("PESAME");
    httb ->DrawNormalized("PESAME");
    httcc->DrawNormalized("PESAME");
    httjj->DrawNormalized("PESAME");
    httH ->DrawNormalized("PESAME");
    leg->Draw();
    pt_title->Draw();

    if( SAVEPLOTS ){
      c2->SaveAs(  ("./MED_plots/AH_"+variable+tag+"_norm.pdf").c_str() ); 
    }
  }

  float time1 = clock->CpuTime();
  outfile << endl << "*** Plot done in " << time1/60.0 << " min." << endl;

  outfile.close();
  
  return;
}
