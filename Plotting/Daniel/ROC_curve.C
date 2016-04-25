#define SAVEPLOTS 1
#define CAT 11
#define CUT_HT 500.0
#define PSB_FAC 0.02

void ROC_curve(){
  
  const int abins = 100;
  const int bbins = 50;
  const int cbins = 20;
  float a = 0.0001;
  float b = 0.9;

  const int nbins = abins+bbins+cbins;
  float xbins[nbins+1] = {0};
  for(int j=0; j<nbins+1; j++){
    if(j<abins)            xbins[j] = a/abins*j;
    else if(j<abins+bbins) xbins[j] = a + (b-a)/bbins*(j-abins);
    else                   xbins[j] = b + (1.0-b)/cbins*(j-bbins-abins);
    //cout << xbins[j] << " ";
  }
  cout << endl;
  
  string tag = "_withtrig"; //"_Psb0pt55";
  string method = "";
  if(CUT_HT>0) tag += Form("_HT%.0f",CUT_HT);  
  if(CAT<0) tag += "_catAll";
  else tag += Form("_cat%d",CAT);
  tag += Form("_%.3f",PSB_FAC);

  string folder = "/scratch/dsalerno/TTH_MEM_74X/V14/crab_151222/";

  // load files
  TFile* fsignal = TFile::Open( (folder+"TTH/tree_TTH_part.root").c_str() );
  if(fsignal==0 || fsignal->IsZombie() ) return;

  TFile* fttj = TFile::Open( (folder+"TTJets/tree_TTJets.root").c_str() );
  if(fttj==0 || fttj->IsZombie() ) return;

  TFile* fqcd3 = TFile::Open( (folder+"QCD300/tree_QCD300.root").c_str() );
  if(fqcd3==0 || fqcd3->IsZombie() ) return;
  TFile* fqcd5 = TFile::Open( (folder+"QCD500/tree_QCD500.root").c_str() );
  if(fqcd5==0 || fqcd5->IsZombie() ) return;
  TFile* fqcd7 = TFile::Open( (folder+"QCD700/tree_QCD700.root").c_str() );
  if(fqcd7==0 || fqcd7->IsZombie() ) return;
  TFile* fqcd10 = TFile::Open( (folder+"QCD1000/tree_QCD1000.root").c_str() );
  if(fqcd10==0 || fqcd10->IsZombie() ) return;
  TFile* fqcd15 = TFile::Open( (folder+"QCD1500/tree_QCD1500.root").c_str() );
  if(fqcd15==0 || fqcd15->IsZombie() ) return;
  TFile* fqcd20 = TFile::Open( (folder+"QCD2000/tree_QCD2000.root").c_str() );
  if(fqcd20==0 || fqcd20->IsZombie() ) return;

  // determine ME method used
  string element="";
  if(CAT==7){
    element = "11";
    method = "_3w2h2t";
  }
  else if(CAT==8){
    element = "10"; //10 or 11 (leave at 10 as 11 hardcoded seperately)
    method = "_4w2h2t"; //4w2h2t or 3w2h2t
  }
  else if(CAT==9){
    element = "10";
    method = "_4w2h2t";
  }
  else if(CAT==10){
    element = "12";
    method = "_4w2h1t";
  }
  else if(CAT==11){
    element = "12";
    method = "_4w2h21";
  }

  if(CAT>=0) tag += method;

  // QCD scale factors
  double scalefac3 = 1.0; //19466760.0/18282047.0;
  double scalefac5 = 1.0; //19664159.0/17830047.0;
  double scalefac7 = 1.0; //15165288.0/13441279.0;
  double scalefac10 = 1.0; //4963895.0/4461516.0;
  double scalefac15 = 1.0; //3691495.0/3415737.0;
  double scalefac20 = 1.0; //1912529.0/1862522.0;

  // load trees
  TTree *tsignal = (TTree*)fsignal->Get("tree");
  TTree *tttj = (TTree*)fttj->Get("tree");
  TTree *tqcd3  = (TTree*)fqcd3->Get("tree");
  TTree *tqcd5  = (TTree*)fqcd5->Get("tree");
  TTree *tqcd7  = (TTree*)fqcd7->Get("tree");
  TTree *tqcd10 = (TTree*)fqcd10->Get("tree");
  TTree *tqcd15 = (TTree*)fqcd15->Get("tree");
  TTree *tqcd20 = (TTree*)fqcd20->Get("tree");

  // master histogram
  TH1F* h1 = new TH1F("h1","Matrix element discriminant; P_{s/b}; Events", nbins, xbins );  
  
  hsignal  = (TH1F*)h1->Clone("hsignal"); 
  httj  = (TH1F*)h1->Clone("httj");
  hqcd  = (TH1F*)h1->Clone("hqcd");
  hqcd3  = (TH1F*)h1->Clone("hqcd3");
  hqcd5  = (TH1F*)h1->Clone("hqcd5");
  hqcd7  = (TH1F*)h1->Clone("hqcd7");
  hqcd10 = (TH1F*)h1->Clone("hqcd10");
  hqcd15 = (TH1F*)h1->Clone("hqcd15");
  hqcd20 = (TH1F*)h1->Clone("hqcd20");

  hsignalB = (TH1F*)h1->Clone("hsignalB");
  httjB  = (TH1F*)h1->Clone("httjB");
  hqcdB  = (TH1F*)h1->Clone("hqcdB");

  string me = "(ht>";
  me += Form("%.0f",CUT_HT);
  me += " && cat==";
  me += Form("%d",CAT);
  me += " && triggerDecision>0";
  me += ")";
  
  TString draw = ("mem_tth_p["+element+"]/(mem_tth_p["+element+"]+"+Form("%.3f",PSB_FAC)+"*mem_ttbb_p["+element+"])").c_str();
  TString drawB = "mem_tth_p[11]/(mem_tth_p[11]+0.02*mem_ttbb_p[11])";  
  //TString cut  = ("(ht>"+Form("%.1f",CUT_HT)+" && cat=="+Form("%d",CAT)+")" ).c_str();
  TString cut = me.c_str();
  TString weight = "weight_xs";

  cout << draw << endl;
  cout << cut << endl;
  cout << weight << endl;

  tsignal->Draw(draw+">>hsignal",cut);
  tttj->Draw(draw+">>httj",cut);
  tqcd3 ->Draw(draw+">>hqcd3",cut+"*"+weight);
  tqcd5 ->Draw(draw+">>hqcd5",cut+"*"+weight);
  tqcd7 ->Draw(draw+">>hqcd7",cut+"*"+weight);
  tqcd10->Draw(draw+">>hqcd10",cut+"*"+weight);
  tqcd15->Draw(draw+">>hqcd15",cut+"*"+weight);
  tqcd20->Draw(draw+">>hqcd20",cut+"*"+weight);

  //hqcd->Add(hqcd3,scalefac3); //exclude QCD300 due to large weights
  hqcd->Add(hqcd5,scalefac5); 
  hqcd->Add(hqcd7,scalefac7);
  hqcd->Add(hqcd10,scalefac10);
  hqcd->Add(hqcd15,scalefac15);
  hqcd->Add(hqcd20,scalefac20);

  tsignal->Draw(drawB+">>hsignalB",cut);
  tttj->Draw(drawB+">>httjB",cut);
  tqcd3 ->Draw(drawB+">>hqcd3",cut+"*"+weight);
  tqcd5 ->Draw(drawB+">>hqcd5",cut+"*"+weight);
  tqcd7 ->Draw(drawB+">>hqcd7",cut+"*"+weight);
  tqcd10->Draw(drawB+">>hqcd10",cut+"*"+weight);
  tqcd15->Draw(drawB+">>hqcd15",cut+"*"+weight);
  tqcd20->Draw(drawB+">>hqcd20",cut+"*"+weight);
  
  hqcdB->Add(hqcd5,scalefac5); 
  hqcdB->Add(hqcd7,scalefac7);
  hqcdB->Add(hqcd10,scalefac10);
  hqcdB->Add(hqcd15,scalefac15);
  hqcdB->Add(hqcd20,scalefac20);
  
  float totalsignal = hsignal->Integral();
  float totalttj = httj->Integral();
  float totalqcd = hqcd->Integral();

  float totalsignalB = hsignalB->Integral();
  float totalttjB = httjB->Integral();
  float totalqcdB = hqcdB->Integral();

  float nsignal = 0.0;
  float nttj = 0.0;
  float nqcd = 0.0;

  float nsignalB = 0.0;
  float nttjB = 0.0;
  float nqcdB = 0.0;

  vector<float> esignal;
  vector<float> ettj;
  vector<float> eqcd;  

  vector<float> esignalB;
  vector<float> ettjB;
  vector<float> eqcdB;

  for(int i=0; i<nbins; i++){

    nsignal += hsignal->GetBinContent(i);
    nttj += httj->GetBinContent(i);
    nqcd += hqcd->GetBinContent(i);

    esignal.push_back( 1.0-nsignal/totalsignal );
    ettj.push_back( 1.0-nttj/totalttj );
    eqcd.push_back( 1.0-nqcd/totalqcd );

    nsignalB += hsignalB->GetBinContent(i);
    nttjB += httjB->GetBinContent(i);
    nqcdB += hqcdB->GetBinContent(i);
    
    esignalB.push_back( 1.0-nsignalB/totalsignalB );
    ettjB.push_back( 1.0-nttjB/totalttjB );
    eqcdB.push_back( 1.0-nqcdB/totalqcdB );
  }
 
  TF1* line = new TF1("line","x",0.0,1.0);

  TGraph* gttj = new TGraph(nbins);
  TGraph* gqcd = new TGraph(nbins);

  TGraph* gttjB = new TGraph(nbins);
  TGraph* gqcdB = new TGraph(nbins);

  cout << "esignal.size() " << esignal.size() << endl;
  cout << "i esignal ettj" << endl;
  for(int i=0; i<(int)esignal.size(); i++){
    gttj->SetPoint(i, esignal[i], ettj[i]);
    gqcd->SetPoint(i, esignal[i], eqcd[i]);
    gttjB->SetPoint(i, esignalB[i], ettjB[i]);
    gqcdB->SetPoint(i, esignalB[i], eqcdB[i]);
    if(i<11 || (i>abins && i<abins+11 ) || (i>(abins+bbins) && i<(abins+bbins+11)) ) cout << i << " " << esignal[i] << " " << ettj[i] << " " << eqcd[i] << endl;
  }

  TCanvas *c2 = new TCanvas("c2","",5,30,640,580);

  TLegend* leg = new TLegend(0.15,0.7,0.50,0.9,NULL,"brNDC");
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetFillColor(10);
  leg->SetTextSize(0.035);

  gttj->SetTitle("Matrix element discriminant");
  gttj->GetXaxis()->SetLimits(0.0,1.0); 
  gttj->GetXaxis()->SetTitle("Signal efficiency");
  gttj->GetYaxis()->SetTitle("Background efficiency");
  gttj->SetLineColor(kRed);
  gttj->SetLineWidth(2);
  gttj->SetMaximum(1.0);
  gttj->Draw("AL");
  leg->AddEntry(gttj, "ttH vs tt+jets", "L");

  //gqcd->SetTitle("Matrix element discriminant");
  //gqcd->GetXaxis()->SetLimits(0.0,1.0); 
  //gqcd->GetXaxis()->SetTitle("Signal efficiency");
  //gqcd->GetYaxis()->SetTitle("Background efficiency");
  gqcd->SetLineColor(kGreen+3);
  gqcd->SetLineWidth(2);
  gqcd->SetMaximum(1.0);
  gqcd->Draw("LSAME");
  leg->AddEntry(gqcd, "ttH vs QCD", "L");

  if(CAT==8){
    gttjB->SetLineColor(kRed);
    gttjB->SetLineStyle(7);
    gttjB->SetLineWidth(2);
    gttjB->SetMaximum(1.0);
    gttjB->Draw("LSAME");
    leg->AddEntry(gttjB, "ttH vs tt+jets (int. 1q)", "L");
    
    gqcdB->SetLineColor(kGreen+3);
    gqcdB->SetLineStyle(7);
    gqcdB->SetLineWidth(2);
    gqcdB->SetMaximum(1.0);
    gqcdB->Draw("LSAME");
    leg->AddEntry(gqcdB, "ttH vs QCD (int. 1q)", "L");
  }

  line->SetLineColor(kBlack);
  line->SetLineWidth(1);
  line->Draw("SAME");

  leg->Draw();

  // save plots
  if( SAVEPLOTS ){
    c2->SaveAs(  ("./MED_plots/ROC"+tag+".pdf").c_str() ); 
  }

}
