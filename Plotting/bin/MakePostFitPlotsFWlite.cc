#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
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

#include <RooStats/ModelConfig.h>


#include <cstdlib>
#include <iostream> 
#include <fstream>
#include <map>
#include <string>
#include <algorithm>

#include <cstdlib>
#include <iostream> 
#include <fstream>
#include <map>
#include <string>
#include <vector>

#include "TMath.h"
#include "TMatrixT.h"
#include "TMatrixTBase.h"
#include "TFile.h"
#include "TTree.h"
#include "TLeaf.h"
#include "TTreeFormula.h"
#include "TString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "boost/noncopyable.hpp"

#include "TH1F.h"
#include "TH2F.h"
#include "TF1.h"
#include "TF2.h"

#include "TLorentzVector.h"

#include "TPaveText.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TPad.h"
#include "TList.h"
#include "TCollection.h"
#include "TObject.h"
#include "TLegend.h"
#include "THStack.h"
#include "TCut.h"
#include "TGraphAsymmErrors.h"
#include "TGraphPainter.h"
#include "TMultiGraph.h"
#include "TArrayF.h"
#include "TLine.h"


#include "RooWorkspace.h"
#include "RooAbsData.h"
#include "RooAbsPdf.h"
#include "RooDataSet.h"
#include "RooPlot.h"
#include "RooRealVar.h"
#include "RooCBShape.h"
#include "RooExponential.h"
#include "RooLandau.h"
#include "RooUniform.h"
#include "RooAddPdf.h"
#include "RooProdPdf.h"
#include "RooArgList.h"
#include "RooArgSet.h"
#include "RooFitResult.h"
#include "RooSimultaneous.h"
#include "RooCategory.h"
#include "RooAbsCategory.h"
#include "RooAbsCollection.h"
#include "RooDataHist.h"
#include "RooGenericPdf.h"
#include "RooAbsCategoryLValue.h"

using namespace std;
using namespace RooFit;
using namespace RooStats;

struct ShapeAndNorm {
  bool        signal;
  std::string process;
  std::string channel;
  RooArgList  obs;
  const RooAbsReal *norm;
  const RooAbsPdf  *pdf;
};

class NuisanceSampler { 
public:
  virtual ~NuisanceSampler() {}
  virtual void  generate(int ntoys) = 0;
  virtual const RooAbsCollection & get(int itoy) = 0;
  virtual const RooAbsCollection & centralValues() = 0;
};

class CovarianceReSampler : public NuisanceSampler {
public:
  CovarianceReSampler(RooFitResult *res) : res_(res) {}
  virtual void  generate(int ntoys) {}
  virtual const RooAbsCollection & get(int) { return res_->randomizePars(); }
  virtual const RooAbsCollection & centralValues() { return res_->floatParsFinal(); }
protected:
  RooFitResult *res_;
};

class ToySampler : public NuisanceSampler, boost::noncopyable {
public:
  ToySampler(RooAbsPdf *pdf, const RooArgSet *nuisances) ;    
  virtual ~ToySampler() ;
  virtual void  generate(int ntoys);
  virtual const RooAbsCollection & get(int itoy);
  virtual const RooAbsCollection & centralValues();
private:
  RooAbsPdf  *pdf_;
  RooAbsData *data_;
  RooArgSet  snapshot_; 
};


void getShapesAndNorms(RooAbsPdf *pdf, const RooArgSet &obs, std::map<std::string,ShapeAndNorm> &out, const std::string &channel) {
    RooSimultaneous *sim = dynamic_cast<RooSimultaneous *>(pdf);
    if (sim != 0) {
        RooAbsCategoryLValue &cat = const_cast<RooAbsCategoryLValue &>(sim->indexCat());
        for (int i = 0, n = cat.numBins((const char *)0); i < n; ++i) {
            cat.setBin(i);
            RooAbsPdf *pdfi = sim->getPdf(cat.getLabel());
            if (pdfi) getShapesAndNorms(pdfi, obs, out, cat.getLabel());
        }
        return;
    }
    RooProdPdf *prod = dynamic_cast<RooProdPdf *>(pdf);
    if (prod != 0) {
        RooArgList list(prod->pdfList());
        for (int i = 0, n = list.getSize(); i < n; ++i) {
            RooAbsPdf *pdfi = (RooAbsPdf *) list.at(i);
            if (pdfi->dependsOn(obs)) getShapesAndNorms(pdfi, obs, out, channel);
        }
        return;
    }
    RooAddPdf *add = dynamic_cast<RooAddPdf *>(pdf);
    if (add != 0) {
        RooArgList clist(add->coefList());
        RooArgList plist(add->pdfList());
        for (int i = 0, n = clist.getSize(); i < n; ++i) {
            RooAbsReal *coeff = (RooAbsReal *) clist.at(i);
            ShapeAndNorm &ns = out[coeff->GetName()];
            ns.norm = coeff;
            ns.pdf = (RooAbsPdf*) plist.at(i);
            ns.channel = (coeff->getStringAttribute("combine.channel") ? coeff->getStringAttribute("combine.channel") : channel.c_str());
            ns.process = (coeff->getStringAttribute("combine.process") ? coeff->getStringAttribute("combine.process") : ns.norm->GetName());
            ns.signal = (coeff->getStringAttribute("combine.process") ? coeff->getAttribute("combine.signal") : (strstr(ns.norm->GetName(),"shapeSig") != 0));
            std::auto_ptr<RooArgSet> myobs(ns.pdf->getObservables(obs));
            ns.obs.add(*myobs);
        }
        return;
    }
}



void getNormalizations(RooAbsPdf *pdf, const RooArgSet &obs, RooArgSet &out, 
		       NuisanceSampler & sampler, 
		       TDirectory *fOut, 
		       const std::string &postfix) {

  // fill in a map
  std::map<std::string,ShapeAndNorm> snm;
  getShapesAndNorms(pdf,obs, snm, "");
  typedef std::map<std::string,ShapeAndNorm>::const_iterator IT;
  typedef std::map<std::string,TH1*>::const_iterator IH;
  // create directory structure for shapes
  TDirectory *shapeDir = 0;
  if(fOut && fOut->GetDirectory((std::string("shapes")+postfix).c_str())!=0 )
    shapeDir = fOut->GetDirectory((std::string("shapes")+postfix).c_str());
  else if(fOut && fOut->GetDirectory((std::string("shapes")+postfix).c_str())==0){
    shapeDir = fOut->mkdir((std::string("shapes")+postfix).c_str());
  }
  else{
    return; 
  }

  std::map<std::string,TDirectory*> shapesByChannel;
  if (shapeDir) {
    for (IT it = snm.begin(), ed = snm.end(); it != ed; ++it) {
      TDirectory *& sub = shapesByChannel[it->second.channel];
      if (sub == 0){
	if( shapeDir->GetDirectory( it->second.channel.c_str() )==0 )
	  sub = shapeDir->mkdir(it->second.channel.c_str());
	else
	  sub = shapeDir->GetDirectory( it->second.channel.c_str() );
      }
    }
  }
  // now let's start with the central values
  std::vector<double> vals(snm.size(), 0.), sumx2(snm.size(), 0.);
  std::vector<TH1*>   shapes(snm.size(), 0), shapes2(snm.size(), 0);
  std::vector<int>    bins(snm.size(), 0), sig(snm.size(), 0);
  std::map<std::string,TH1*> totByCh, totByCh2, sigByCh, sigByCh2, bkgByCh, bkgByCh2;
  IT bg = snm.begin(), ed = snm.end(), pair; int i;
  for (pair = bg, i = 0; pair != ed; ++pair, ++i) {  
    vals[i] = pair->second.norm->getVal();
    //out.addOwned(*(new RooConstVar(pair->first.c_str(), "", pair->second.norm->getVal())));
    if (fOut != 0 && true && pair->second.obs.getSize() == 1) {
      RooRealVar *x = (RooRealVar*)pair->second.obs.at(0);
      TH1* hist = pair->second.pdf->createHistogram("", *x);
      hist->SetNameTitle(pair->second.process.c_str(), (pair->second.process+" in "+pair->second.channel).c_str());
      hist->Scale(vals[i] / hist->Integral("width"));
      hist->SetDirectory(shapesByChannel[pair->second.channel]);
      shapes[i] = hist;
      if ( true ) {
	shapes2[i] = (TH1*) hist->Clone();
	shapes2[i]->SetDirectory(0);
	shapes2[i]->Reset();
	bins[i] = hist->GetNbinsX();
	TH1 *&htot = totByCh[pair->second.channel];
	if (htot == 0) {
	  htot = (TH1*) hist->Clone();
	  htot->SetName("total");
	  htot->SetDirectory(shapesByChannel[pair->second.channel]);
	  TH1 *htot2 = (TH1*) hist->Clone(); htot2->Reset();
	  htot2->SetDirectory(0);
	  totByCh2[pair->second.channel] = htot2;
	} else {
	  htot->Add(hist);
	}
	sig[i] = pair->second.signal;
	TH1 *&hpart = (sig[i] ? sigByCh : bkgByCh)[pair->second.channel];
	if (hpart == 0) {
	  hpart = (TH1*) hist->Clone();
	  hpart->SetName((sig[i] ? "total_signal" : "total_background"));
	  hpart->SetDirectory(shapesByChannel[pair->second.channel]);
	  TH1 *hpart2 = (TH1*) hist->Clone(); hpart2->Reset();
	  hpart2->SetDirectory(0);
	  (sig[i] ? sigByCh2 : bkgByCh2)[pair->second.channel] = hpart2;
	} else {
	  hpart->Add(hist);
	}
      }
    }
  }
  if ( true ) {
    int ntoys = 200;
    sampler.generate(ntoys);
    std::auto_ptr<RooArgSet> params(pdf->getParameters(obs));
    // prepare histograms for running sums
    std::map<std::string,TH1*> totByCh1, sigByCh1, bkgByCh1;
    for (IH h = totByCh.begin(), eh = totByCh.end(); h != eh; ++h) totByCh1[h->first] = (TH1*) h->second->Clone();
    for (IH h = sigByCh.begin(), eh = sigByCh.end(); h != eh; ++h) sigByCh1[h->first] = (TH1*) h->second->Clone();
    for (IH h = bkgByCh.begin(), eh = bkgByCh.end(); h != eh; ++h) bkgByCh1[h->first] = (TH1*) h->second->Clone();
    for (int t = 0; t < ntoys; ++t) {
      // zero out partial sums
      for (IH h = totByCh1.begin(), eh = totByCh1.end(); h != eh; ++h) h->second->Reset();
      for (IH h = sigByCh1.begin(), eh = sigByCh1.end(); h != eh; ++h) h->second->Reset();
      for (IH h = bkgByCh1.begin(), eh = bkgByCh1.end(); h != eh; ++h) h->second->Reset();
      // randomize numbers
      params->assignValueOnly( sampler.get(t) );
      for (pair = bg, i = 0; pair != ed; ++pair, ++i) { 
	// add up deviations in numbers for each channel
	sumx2[i] += std::pow(pair->second.norm->getVal() - vals[i], 2);  
	if ( true && pair->second.obs.getSize() == 1) {
	  // and also deviations in the shapes
	  RooRealVar *x = (RooRealVar*)pair->second.obs.at(0);
	  std::auto_ptr<TH1> hist(pair->second.pdf->createHistogram(pair->second.pdf->GetName(), *x));
	  hist->Scale(pair->second.norm->getVal() / hist->Integral("width"));
	  for (int b = 1; b <= bins[i]; ++b) {
	    shapes2[i]->AddBinContent(b, std::pow(hist->GetBinContent(b) - shapes[i]->GetBinContent(b), 2));
	  }
	  // and cumulate in the total for this toy as well
	  totByCh1[pair->second.channel]->Add(&*hist);
	  (sig[i] ? sigByCh1 : bkgByCh1)[pair->second.channel]->Add(&*hist);
	}
      }
      // now add up the deviations in this toy
      for (IH h = totByCh1.begin(), eh = totByCh1.end(); h != eh; ++h) {
	TH1 *target = totByCh2[h->first], *reference = totByCh[h->first];
	for (int b = 1, nb = target->GetNbinsX(); b <= nb; ++b) {
	  target->AddBinContent(b, std::pow(h->second->GetBinContent(b) - reference->GetBinContent(b), 2));
	}
      }
      for (IH h = sigByCh1.begin(), eh = sigByCh1.end(); h != eh; ++h) {
	TH1 *target = sigByCh2[h->first], *reference = sigByCh[h->first];
	for (int b = 1, nb = target->GetNbinsX(); b <= nb; ++b) {
	  target->AddBinContent(b, std::pow(h->second->GetBinContent(b) - reference->GetBinContent(b), 2));
	}
      }           
      for (IH h = bkgByCh1.begin(), eh = bkgByCh1.end(); h != eh; ++h) {
	TH1 *target = bkgByCh2[h->first], *reference = bkgByCh[h->first];
	for (int b = 1, nb = target->GetNbinsX(); b <= nb; ++b) {
	  target->AddBinContent(b, std::pow(h->second->GetBinContent(b) - reference->GetBinContent(b), 2));
	}
      }           
    } // end of the toy loop
    // now take square roots and such
    for (pair = bg, i = 0; pair != ed; ++pair, ++i) {
      sumx2[i] = sqrt(sumx2[i]/ntoys);
      if (shapes2[i]) {
	for (int b = 1; b <= bins[i]; ++b) {
	  shapes[i]->SetBinError(b, std::sqrt(shapes2[i]->GetBinContent(b)/ntoys));
	}
	delete shapes2[i]; shapes2[i] = 0;
      }
      
    }
    // and the same for the total histograms
    for (IH h = totByCh.begin(), eh = totByCh.end(); h != eh; ++h) {
      TH1 *sum2 = totByCh2[h->first];
      for (int b = 1, nb = sum2->GetNbinsX(); b <= nb; ++b) {
	h->second->SetBinError(b, std::sqrt(sum2->GetBinContent(b)/ntoys));
      }
      delete sum2; delete totByCh1[h->first];
    }
    for (IH h = sigByCh.begin(), eh = sigByCh.end(); h != eh; ++h) {
      TH1 *sum2 = sigByCh2[h->first];
      for (int b = 1, nb = sum2->GetNbinsX(); b <= nb; ++b) {
	h->second->SetBinError(b, std::sqrt(sum2->GetBinContent(b)/ntoys));
      }
      delete sum2; delete sigByCh1[h->first];
    }
    for (IH h = bkgByCh.begin(), eh = bkgByCh.end(); h != eh; ++h) {
      TH1 *sum2 = bkgByCh2[h->first];
      for (int b = 1, nb = sum2->GetNbinsX(); b <= nb; ++b) {
	h->second->SetBinError(b, std::sqrt(sum2->GetBinContent(b)/ntoys));
      }
      delete sum2; delete bkgByCh1[h->first];
    }
    totByCh1.clear(); totByCh2.clear(); sigByCh1.clear(); sigByCh2.clear(); bkgByCh1.clear(); bkgByCh2.clear();
    // finally reset parameters
    params->assignValueOnly( sampler.centralValues() );
  }
  for (pair = bg, i = 0; pair != ed; ++pair, ++i) {
    RooRealVar *val = new RooRealVar(( false ? pair->first : pair->second.channel+"/"+pair->second.process).c_str(), "", vals[i]);
    val->setError(sumx2[i]);
    out.addOwned(*val); 
    if (shapes[i]) shapesByChannel[pair->second.channel]->WriteTObject(shapes[i],0, "Overwrite");
  }
  if (fOut) {
    fOut->WriteTObject(&out, (std::string("norm")+postfix).c_str());
    for (IH h = totByCh.begin(), eh = totByCh.end(); h != eh; ++h) { shapesByChannel[h->first]->WriteTObject(h->second,0, "Overwrite"); }
    for (IH h = sigByCh.begin(), eh = sigByCh.end(); h != eh; ++h) { shapesByChannel[h->first]->WriteTObject(h->second,0, "Overwrite"); }
    for (IH h = bkgByCh.begin(), eh = bkgByCh.end(); h != eh; ++h) { shapesByChannel[h->first]->WriteTObject(h->second,0, "Overwrite"); }
  }
}




int main(int argc, const char* argv[])
{
  
  /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
  /* @@@@@@@@@@@@@@@@@@@@@@@@ FWLITE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
    
  std::cout << "Make post fit plots using a generic RooFitResult" << std::endl;
  gROOT->SetBatch(true);
 
  gSystem->Load("libFWCoreFWLite");
  gSystem->Load("libDataFormatsFWLite");
  gSystem->Load("libHiggsAnalysisCombinedLimit");

  AutoLibraryLoader::enable();

  PythonProcessDesc builder(argv[1]);
  const edm::ParameterSet& in = builder.processDesc()->getProcessPSet()->getParameter<edm::ParameterSet>("fwliteInput");
  string path2Workspace     =  ( in.getParameter<string>  ("path2Workspace"   ) );
  string path2Datacard      =  ( in.getParameter<string>  ("path2Datacard"   ) );
  string path2FitResults    =  ( in.getParameter<string>  ("path2FitResults"   ) );
  string outputName         =  ( in.getParameter<string>  ("outputName"  ) );
  string dirName            =  ( in.getParameter<string>  ("dirName" ) );

  if( argc==4 ){
    path2Datacard = string( argv[2] );
    dirName       = string( argv[3] );
  }

  if( path2Workspace=="NONE" || path2Workspace==""){
    cout << "Creating the workspace on the fly..." ;
    gSystem->Exec( ("text2workspace.py "+path2Datacard+" -o mytest.root").c_str() );
    path2Workspace = "mytest.root";
    cout << "done! The workspace is called " << path2Workspace << endl;
  }
  else{
    cout << "Using the workspace " << path2Workspace << endl;
  }


  TFile* f_out    = new TFile(outputName.c_str(),"UPDATE");
  TDirectory* dir = f_out->GetDirectory( dirName.c_str() );
  if(!dir){
    cout << "The directory " << dirName << " has been created." << endl;
    dir = f_out->mkdir( dirName.c_str() ); 
  }
  else{
    cout << "The directory " << dirName << " already exists." << endl;
  }

  TFile* f_fit = new TFile( path2FitResults.c_str() );
  if(!f_fit){
    cout << "Cannot find file with fit" << endl;
    return 1;
  }
  RooFitResult* fit = (RooFitResult*)f_fit->Get("fit_s");
  if(!fit){
    cout << "Cannot find fit_s" << endl;
    return 1;
  }
  //fit->Print();
  CovarianceReSampler* sampler = new CovarianceReSampler( fit );


  TFile* f_w   = new TFile( path2Workspace.c_str(), "READ");

  if(!f_w){
    cout << "Cannot find file" << endl;
    return 1;
  }

  RooWorkspace* w = (RooWorkspace*)f_w->Get("w");
  if( !w ){
    cout << "Cannot find workspace" << endl;
    return 1;
  }

  RooArgSet varsFit = w->allVars();
  varsFit.assignValueOnly( fit->floatParsFinal() );
  w->saveSnapshot("postfit", varsFit);

  w->loadSnapshot("postfit");
  ModelConfig* mc = dynamic_cast<RooStats::ModelConfig *>(w->genobj("ModelConfig"));

  const RooArgSet* set_w =  mc->GetObservables();  
  RooAbsPdf* pdf         =  mc->GetPdf();

  if( !pdf || !set_w ){
    cout << "Cannot find model_s or observables" << endl;
    return 1;
  }
  
  RooArgSet out;
  getNormalizations( pdf, *set_w, out, *sampler, dir, "_fit_s" );


  f_out->Write();
  f_out->Close();

  f_fit->Close();
  f_w->Close();

  delete sampler;
  return 0;

}
