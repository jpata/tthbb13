#define SAVEPLOTS 0
#define CAT 11    // 7, 8, 9, 10, 11
#define METHOD8 12 // 11=4w2h2t or 12=3w2h2t
#define CUT_HT 500.0
#define PSB_FAC 0.02

void TTH_matching(){

  // determine ME method used
  int element = -1;
  int category = 0;
  int njets = -1;
  int nbtags = -1;
  if(CAT==7){
    element = 12; category=7; njets=7; nbtags=4;
  }
  else if(CAT==8){
    element = METHOD8; category=8; njets=8; nbtags=4;
  }
  else if(CAT==9){
    element = 11; category=9; njets=9; nbtags=4;
  }
  else if(CAT==10){
    element = 13; category=10; njets=8; nbtags=3;
  }
  else if(CAT==11){
    element = 13; category=11; njets=7; nbtags=3;
  }
  
  // load file
  TFile* file = TFile::Open("/mnt/t3nfs01/data01/shome/dsalerno/TTH_2016/TTH_76X_v1/skim/ttH.root" );
  if(file==0 || file->IsZombie() ) return;

  // load tree
  TTree *tree = (TTree*)file->Get("tree");
  
  // Declare calculated variables
  int numEvents = 0;
  int numSelected = 0;
  double eval;
  vector<vector<vector<int> > > counts; //number wq, tb, hb matched
  vector<vector<vector<double> > > psb; //mean psb value
  int extras = 0;

  // set vector sizes: 5x3x3
  counts.resize(5);
  psb.resize(5);
  for(int i=0; i<5; ++i){
    counts[i].resize(3);
    psb[i].resize(3);
    for(int j=0; j<3; ++j){
      counts[i][j].resize(3);
      psb[i][j].resize(3);
    }
  }
  // set vector values to zero
  for(int i=0; i<5; ++i){
    for(int j=0; j<3; ++j){
      for(int k=0; k<3; ++k){    
	counts[i][j][k] = 0;
	psb[i][j][k] = 0.0;
      }
    }
  }
  
  // Declare leaf types
  int    cat;
  int    numJets;
  int    nBCSVM;
  double ht;
  int    triggerDecision;
  int    nMatch_wq_btag;
  int    nMatch_tb_btag;
  int    nMatch_hb_btag;
  double mem_tth_p[17];
  double mem_ttbb_p[17];

  // Connect the branches with their member variables.
  if(!tree) return;
  tree->SetBranchAddress("cat",              &cat);
  tree->SetBranchAddress("numJets",          &numJets);
  tree->SetBranchAddress("nBCSVM",           &nBCSVM);
  tree->SetBranchAddress("ht",               &ht);
  tree->SetBranchAddress("HLT_ttHhardonicLowLumi",  &triggerDecision);
  tree->SetBranchAddress("nMatch_wq_btag",   &nMatch_wq_btag);
  tree->SetBranchAddress("nMatch_tb_btag",   &nMatch_tb_btag);
  tree->SetBranchAddress("nMatch_hb_btag",   &nMatch_hb_btag);
  tree->SetBranchAddress("mem_tth_p",        mem_tth_p);
  tree->SetBranchAddress("mem_ttbb_p",       mem_ttbb_p);

  int totalEntries = tree->GetEntries();
  cout << totalEntries << endl;
  
  // event loop
  for(int entry=0; entry < totalEntries; entry++){
    tree->GetEntry(entry);
    numEvents++;
    eval = -99.0;
  
    //if(entry > 100000) break;
    // print the processed event number
    if(entry%(totalEntries/20)==0){
      cout << entry << " (" << float(entry)/float(totalEntries)*100 << " %)" << endl;
    }
  
    // Trigger selection
    if( triggerDecision<=0 ) continue;
    // HT cut
    if( ht < CUT_HT) continue;
    // MED selection
    //if( cat!=CAT ) continue;
    if( cat!=category || numJets!=njets ) continue;

    numSelected++;
    eval = mem_tth_p[element]/(mem_tth_p[element]+PSB_FAC*mem_ttbb_p[element]);
    
    // matching
    if(nMatch_wq_btag>4 || nMatch_tb_btag>2 || nMatch_hb_btag>2){
      extras++;
      continue;
    }
    counts[nMatch_wq_btag][nMatch_tb_btag][nMatch_hb_btag]++;
    if(eval>0) psb[nMatch_wq_btag][nMatch_tb_btag][nMatch_hb_btag] += eval;    
  }
  
  // calculate mean psb values
  for(int i=0; i<5; ++i){
    for(int j=0; j<3; ++j){
      for(int k=0; k<3; ++k){
	psb[i][j][k] /= counts[i][j][k];
      }
    }
  }

  //print summary
  cout << "Category " << CAT << endl;
  cout << "numTotal " << numEvents << endl;
  cout << "numSelected " << numSelected << endl;
  cout << "extras " << extras << endl << endl;

  cout << "*****COUNTS*****" << endl;
  for(int k=0; k<3; ++k){
    cout << "nMatch_hb_btag==" << k << endl;
    cout << "* * nMatch_tb_btag" << endl;
    cout << "* * 0 1 2" << endl;
    for(int i=0; i<5; ++i){
      cout << "* " << i;
      for(int j=0; j<3; ++j){
	cout << " " << counts[i][j][k];
      }
      cout << endl;
    }
    cout << endl;
  }
  
  cout << "*****MEAN_PSB*****" << endl;
  for(int k=0; k<3; ++k){
    cout << "nMatch_hb_btag==" << k << endl;
    cout << "* * nMatch_tb_btag" << endl;
    cout << "* * 0 1 2" << endl;
    for(int i=0; i<5; ++i){
      cout << "* " << i;
      for(int j=0; j<3; ++j){
	cout << " " << psb[i][j][k];
      }
      cout << endl;
    }
    cout << endl;
  }
}
