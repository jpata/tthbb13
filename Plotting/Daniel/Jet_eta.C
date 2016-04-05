#define NMAXJETS 30
#define SAVEPLOTS 0
#define LUMI 10
#define VAR "nj" // "eta" or "nj"

void Jet_eta(){

  int jet = 8; //nth jet for eta plot

  vector<string> samples;
  samples.push_back( "TTH" );
  samples.push_back( "TTJets" ); 
  samples.push_back( "QCD300" );
  samples.push_back( "QCD500" );
  samples.push_back( "QCD700" );
  samples.push_back( "QCD1000" );  
  samples.push_back( "QCD1500" );
  samples.push_back( "QCD2000" );

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
  
  TString cmsinfo = "";
  cmsinfo = "Simulation                                                  Normalized";

  TPaveText *pt_title = new TPaveText(0.1, 0.952, 0.9, 1.0,"brNDC");
  pt_title->SetFillStyle(1001);
  pt_title->SetBorderSize(0);
  pt_title->SetFillColor(0);
  pt_title->SetTextFont(42); 
  pt_title->SetTextSize(0.04); 
  pt_title->AddText(cmsinfo);
  
  TLegend* leg = new TLegend(0.22,0.54,0.47,0.91,NULL,"brNDC");
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetFillColor(kYellow);
  leg->SetTextSize(0.04);
  
  TH1F* httH  = 0;
  TH1F* hQCD  = 0;
  TH1F* httJ  = 0;
  
  string n = "";
  if(jet==1) n = "1st";
  else if(jet==2) n = "2nd";   
  else if(jet==3) n = "3rd";    
  else n= Form("%dth",jet);
  
  // master histogram (all other histograms are a clone of this one)
  TH1F* h1 = new TH1F("h1",("Eta of "+n+" jet; #eta; Normalized units").c_str(), 100 , -5.0, 5.0 );
  if(VAR == "nj"){
    TH1F* h2 = new TH1F("h2","Number of jets with |#eta|<2.4; n_{jet}; Normalized units", 9 , 0, 9 );
    h1  = (TH1F*)h2->Clone("h1" );
  }

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
  httJ  = (TH1F*)h1->Clone("httJ" );

  // set histogram styles
  httH ->SetLineColor( kBlue+2 );
  httH ->SetMarkerColor( kBlue+2 );
  httH ->SetMarkerStyle( 20 );
  httH ->SetMarkerSize( 1 );
  httH ->SetLineWidth( 4 );
  httH ->SetFillStyle( 0 );
  //httH ->Sumw2();

  hQCD ->SetLineColor( kGreen+3 );
  hQCD ->SetMarkerColor( kGreen+3 );
  hQCD ->SetMarkerStyle( 21 );
  hQCD ->SetMarkerSize( 1 );
  hQCD ->SetLineWidth( 4 );
  hQCD ->SetFillStyle( 0 );
  //hQCD ->Sumw2();

  httJ ->SetLineColor( kRed-2 );
  httJ ->SetFillColor( kRed-2 );
  httJ ->SetMarkerColor( kRed-2 );
  httJ ->SetMarkerStyle( 22 );
  httJ ->SetMarkerSize( 1 );
  httJ ->SetLineWidth( 4 );
  httJ ->SetFillStyle( 0 );
  //httJ ->Sumw2();
 
  cout << "Sample Total Range1 Range2 Range3" << endl;

  // loop over samples
  for(int s=0; s<samples.size(); s++){
    float weight = -99.0;
    if(samples[s] == "TTH") weight = 0.5085*0.577/90000; //xsec*BR/nGen in file only
    else if(samples[s] == "TTJets") weight = 831.76/90555;
    else if(samples[s] == "QCD300") weight = 366800.0/85185;
    else if(samples[s] == "QCD500") weight = 29370.0/98732;
    else if(samples[s] == "QCD700") weight = 6524.0/83929;
    else if(samples[s] == "QCD1000") weight = 1064.0/70989;
    else if(samples[s] == "QCD1500") weight = 121.5/93081;
    else if(samples[s] == "QCD2000") weight = 25.42/84179;
    
    if(weight<0){
      cout << "negative weight! return" << endl;
      return;
    }

    cout << samples[s] << " ";
    //cout << endl << "Running sample " << samples[s] << endl;
    
    // load file
    TFile* file = TFile::Open( ("jets_"+samples[s]+".root").c_str() );
    if(file==0 || file->IsZombie() ) continue;
    
    // load tree
    TTree *tree = (TTree*)file->Get("tree");

    // Declare calculated variables
    int numEvents = 0;
    int numSelected = 0;
    float numTotal = 0.0;
    float numRange1 = 0.0; //|eta|<2.4       or njeteta==jet
    float numRange2 = 0.0; //|eta|>2.4       or njeteta==jet-1
    float numRange3 = 0.0; //2.4<|eta|>3.0   or njeteta < jet-1
    float eta;
    int nj;   

    // declare leaf types
    int njet;      //njets with pT>30 GeV
    int njeteta;   //njets with pT>30 GeV && |eta|<2.4
    int nbtag;     //njets with pT>30 GeV && CSV>0.89
    int nbtageta;  //njets with pT>30 GeV && CSV>0.89 && |eta|<2.4
    int nhardjet;  //njets with pT>40 GeV && |eta|<2.4
    float HT;
    float jet_pt      [NMAXJETS];  //jets sorted by decreasing pT
    float jet_eta     [NMAXJETS];
    float jet_csv     [NMAXJETS];
    
    // Connect the branches with their member variables.
    if(!tree) return;
    tree->SetBranchAddress("njet",         &njet);
    tree->SetBranchAddress("njeteta",      &njeteta);
    tree->SetBranchAddress("nbtag",        &nbtag);
    tree->SetBranchAddress("nbtageta",     &nbtageta);
    tree->SetBranchAddress("nhardjet",     &nhardjet); 
    tree->SetBranchAddress("HT",           &HT);
    tree->SetBranchAddress("jet_pt",       jet_pt);
    tree->SetBranchAddress("jet_eta",      jet_eta);
    tree->SetBranchAddress("jet_csv",      jet_csv);

    int totalEntries = tree->GetEntries();
    //cout << totalEntries << endl;
    
    // loop over events
    for(int entry=0; entry < totalEntries; entry++){
      tree->GetEntry(entry);
      numEvents++;
      eta = -99.;
      nj = -99;

      // get nth jet eta
      if( njet >= jet ){
	numSelected ++;
	eta = jet_eta[jet-1];
	if( njet == jet ) nj = njeteta;

	if( VAR=="eta" ){
	  numTotal += weight*1000*LUMI;
	  if( abs(jet_eta[jet-1]) < 2.4 ) numRange1 += weight*1000*LUMI;
	  if( abs(jet_eta[jet-1]) > 2.4 ) numRange2 += weight*1000*LUMI;
	  if( abs(jet_eta[jet-1]) > 2.4 &&  abs(jet_eta[jet-1]) < 3.0 ) numRange3 += weight*1000*LUMI;	
	}
	else if( VAR=="nj" && njet == jet ){
	  numTotal += weight*1000*LUMI;
	  if( njeteta == jet   ) numRange1 += weight*1000*LUMI;
	  if( njeteta == jet-1 ) numRange2 += weight*1000*LUMI;
	  if( njeteta < jet-1 ) numRange3 += weight*1000*LUMI;  
	}

        if( samples[s]=="TTH" ){
	  if(VAR == "eta") httH->Fill(eta,weight);
	  else if( nj>-1 ) httH->Fill(nj,weight);
	}
	else if( samples[s]=="TTJets" ){
	  if(VAR == "eta") httJ->Fill(eta,weight);
	  else if( nj>-1 ) httJ->Fill(nj,weight);
	}
	else if( samples[s].find("QCD") != string::npos ){
	  if(VAR == "eta") hQCD->Fill(eta,weight);
	  else if( nj>-1 ) hQCD->Fill(nj,weight);
	}
	else{
	  cout << "sample not found. return" << endl;
	  return;
	}
	
	  
      } //end selection
      
      
    } //end loop over events

    cout << numTotal << " " << numRange1 << " " << numRange2 << " " << numRange3 << " " << endl;

  } //end loop over samples

  leg->AddEntry(httH,  "t#bar{t}H (125)", "F");
  leg->AddEntry(httJ, "t#bar{t}", "F");
  leg->AddEntry(hQCD,  "QCD", "F");

  hQCD ->GetYaxis()->SetTitle("Normalized units");
  hQCD ->SetMaximum( hQCD->GetMaximum()*2.0 );   //CHANGE HERE
  hQCD ->DrawNormalized("HIST");
  httJ ->DrawNormalized("HISTSAME");
  httH ->DrawNormalized("HISTSAME");
  leg->Draw();
  pt_title->Draw();
  
  string variable = Form("%d",jet);
  if( SAVEPLOTS ){
    if(VAR=="eta") c2->SaveAs( ("./Jet_plots/eta_"+variable+"jet_norm.pdf").c_str() ); 
    else if(VAR=="nj") c2->SaveAs( ("./Jet_plots/nj_"+variable+"jet_norm.pdf").c_str() );
  }


}
