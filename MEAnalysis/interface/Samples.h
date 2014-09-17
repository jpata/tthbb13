#ifndef SAMPLES_H
#define SAMPLES_H

#include <string>
#include <map>
#include <stdio.h>
#include "TFile.h"
#include "TString.h"
#include "TTree.h"
#include "TH1F.h"
#include "TH1.h"
#include "boost/foreach.hpp"
#include "FWCore/ParameterSet/interface/ProcessDesc.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/PythonParameterSet/interface/PythonProcessDesc.h"


using namespace std;

class Samples {

 public:

  Samples(string, string, vector<string>, vector<double>, double, int) ;
  Samples(bool, string, string, const edm::VParameterSet&, double, int);

  ~Samples(){ 
    for(  std::map<string,TFile*>::iterator it = mapFile_.begin(); it!= mapFile_.end() ; it++){
      if( (it->second)!=0 && !(it->second)->IsZombie() ) (it->second)->Close();
    }
  }

  void OpenFile(string);
  TFile* GetFile(string);
  TH1F* GetHisto(string, string);
  TTree* GetTree(string, string);
  double GetXSec(string);
  double GetWeight(string);
  int GetColor(string);
  string GetCut(string);
  string GetPfn(string);
  string GetFileName(string);
  int Size() { return mapFile_.size(); }
  bool IsOk(){ return (err_!=1); }
  vector<string> Files();

 private:

  map<string, TString> mapPfn_;
  map<string, string>  mapFileName_;
  map<string, bool>    mapUpdate_;
  map<string, TFile*>  mapFile_;
  map<string, string>  mapCut_;
  map<string, double>  mapXSec_;
  map<string, double>  mapWeight_;
  map<string, double>  mapColor_;

  int err_;
  int verbose_;

};


Samples::Samples(bool openAllFiles, string pathToFile, string ordering, 
		 const edm::VParameterSet& vpset,
		 double lumi,
		 int verbose){

  err_     = 0; 
  verbose_ = verbose;

  if(verbose_ && !openAllFiles) cout << "WARNING: Files must be opened once at the time via Samples::OpenFile()" << endl;

  BOOST_FOREACH(edm::ParameterSet p, vpset) {

    bool skip       = p.getParameter<bool>("skip");
    string fileName = p.getParameter<string>("name");
    string nickName = p.getParameter<string>("nickName");
    int color       = p.getParameter<int>("color");
    double xSec     = p.getParameter<double>("xSec");
    bool update     = p.exists("update") ?  p.getParameter<bool>("update") : false;
    string cut      = p.exists("cut")    ?  p.getParameter<string>("cut")  : "DUMMY";

    if(skip) continue;
    
    TString TfileName( fileName.c_str() );   
    TString pfn = pathToFile+"/"+ordering+TfileName+".root";
    if(verbose_) std::cout << string(pfn.Data()) << std::endl;

    TFile *f = 0;

    if(openAllFiles) f = update ?  TFile::Open(pfn,"UPDATE") :  TFile::Open(pfn,"READ");
    else f = TFile::Open(pfn,"READ");
    
    if(!f || f->IsZombie()){
      err_ = 1;
    }else{
      mapFile_[nickName]     = openAllFiles ? f : 0;
      mapXSec_[nickName]     = xSec ;
      mapColor_[nickName]    = color;
      mapPfn_[nickName]      = pfn;
      mapUpdate_[nickName]   = update;
      mapCut_[nickName]      = cut;
      mapFileName_[nickName] = ordering+fileName;

      double weight = 1.0;

      if(xSec<0) weight = 1.0;
      else if( (TH1F*)f->Get("CountWithPU") != 0){
	double counter = ((TH1F*)f->Get("CountWithPU"))->GetBinContent(1);
	weight = counter>0 ? lumi*1000/(counter/xSec) : 1.0;
      }
	
      mapWeight_[nickName] = weight;

      if(!openAllFiles) f->Close();
    }

  }
}



Samples::Samples(string pathToFile, string ordering, 
		 vector<string> fileList, vector<double> xsection,
		 double lumi,
		 int verbose){

  err_ = 0; verbose_ = verbose;

  if( fileList.size() != xsection.size() ) err_ = 1;
  else{

    unsigned int numOfFiles = fileList.size();
    for(unsigned int k = 0 ; k < numOfFiles ; k++){

      TString fileName(fileList[k].c_str());
      TString pfn = "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/"+pathToFile+"/"+ordering+fileName+".root";
      if(verbose_) std::cout << string(pfn.Data()) << std::endl;

      TFile *f = TFile::Open(pfn,"READ");

      if(!f || f->IsZombie()){
	err_ = 1;
      }else{
	mapFile_[fileList[k]] = f;
	mapXSec_[fileList[k]] = xsection[k] ;

	double weight = 1.0;

	if(xsection[k]<0) weight = 1.0;
	else if(this->GetHisto(fileList[k], "Count") != 0){
	  double counter = this->GetHisto(fileList[k], "Count")->GetBinContent(1);
	  weight = counter>0 ? lumi*1000./(counter/xsection[k]) : 1.0;
	}
	mapWeight_[fileList[k]] = weight;
	
      }
    }
    
  }
  
}

void Samples::OpenFile(string sampleName){

  TFile *file = 0;
  if(mapPfn_[ sampleName] !=0 ){
    TString pfn = mapPfn_[sampleName];
    file = mapUpdate_[sampleName] ?  TFile::Open(pfn,"UPDATE") :  TFile::Open(pfn,"READ");
    mapFile_[sampleName]  = file;
  }
  if(!file){
    err_ = 1;
    if(verbose_) cout << "Could not find file pointer in sample " << sampleName << endl;
  }
  return;

}

TFile* Samples::GetFile(string sampleName){

  TFile *file = 0;
  this->OpenFile(sampleName);
  if(mapFile_[sampleName]!=0) file = mapFile_[sampleName] ;
  if(!file){
    err_ = 1;
    if(verbose_) cout << "Could not find file pointer in sample " << sampleName << endl;
  }
  return file;

}


TH1F* Samples::GetHisto(string sampleName, string histoName){

  TH1F *histo = 0;
  if(mapFile_[sampleName]!=0) histo = (TH1F*)(mapFile_[sampleName])->Get(histoName.c_str());
  if(!histo){
    err_ = 1;
    if(verbose_) cout << "Could not find histo " << histoName << " in sample " << sampleName << endl;
  }
  return histo;

}

TTree* Samples::GetTree(string sampleName, string treeName){

  TTree *tree = 0;
  if(mapFile_[sampleName]!=0) tree = (TTree*)(mapFile_[sampleName])->Get(treeName.c_str());
  if(!tree){
    err_ = 1;
    if(verbose_) cout << "Could not find tree " << treeName << " in sample " << sampleName << endl;
  }
  return tree;

}

double Samples::GetXSec(string sampleName){
  return ( mapXSec_[sampleName] );
}

double Samples::GetWeight(string sampleName){
  return ( mapWeight_[sampleName] );
}

int Samples::GetColor(string sampleName){
  return ( mapColor_[sampleName] );
}

string Samples::GetCut(string sampleName){
  return ( mapCut_[sampleName] );
}

string Samples::GetPfn(string sampleName){
  return ( string(mapPfn_[sampleName].Data()) );
}

string Samples::GetFileName(string sampleName){
  return ( mapFileName_[sampleName] );
}


vector<string> Samples::Files(){

  vector<string> out ;
  
  for(  std::map<string,TFile*>::iterator it = mapFile_.begin(); it!= mapFile_.end() ; it++){
    out.push_back(it->first);
  }

  return out;
}


#endif
