//Adapted from code by Lorenzo Bianchini
#ifndef SAMPLES_H
#define SAMPLES_H

#include <string>
#include <map>
#include <stdio.h>
#include "TFile.h"
#include "TString.h"
#include "TTree.h"
#include "TChain.h"
#include "TH1F.h"
#include "TH1.h"
#include "boost/foreach.hpp"
#include "FWCore/ParameterSet/interface/ProcessDesc.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/PythonParameterSet/interface/PythonProcessDesc.h"

//Name of the input TTree
#define TTH_TTREE_NAME "tthNtupleAnalyzer/events"

using namespace std;


// class Sample {
// public:
//     const string pfn, filename, cut;
//     const bool update;
//     const double xsec;
//     const double weight;
//     const double color;
//     const int bdiscriminator_choice;
//     TFile* file;

//     Sample(const string _pfn, const string _filename, const string _cut,
//         bool _update, double _xsec, double _weight, double _color,
//         int _bdiscriminator_choice
//     ) : (
//         pfn(_pfn),
//         filename(_filename),
//         cut(_cut),
//         update(_update),
//         xsec(xsec),
//         weight(_weight),
//         color(_color),
//         bdiscriminator_choice(_bdiscriminator_choice)) {

//         TString pfn(filename.size()==0 ? (pathToFile + "/" + ordering + TfileName + ".root") : full_fn);
//         std::cout << "Opening file: " << string(pfn.Data()) << std::endl;

//         TFile *f = 0;

//         if(openAllFiles) f = update ?  TFile::Open(pfn.Data(),"UPDATE") :  TFile::Open(pfn.Data(),"READ");
//         else f = TFile::Open(pfn.Data(), "READ");

//     }

// };

class Samples {

public:

    //Samples(string, string, vector<string>, vector<double>, double, bool) ;
    Samples(bool, string, string, const edm::VParameterSet&, double, bool);

    ~Samples() {
        //for(  std::map<string,TChain*>::iterator it = mapChain_.begin(); it!= mapChain_.end() ; it++) {
        //    if( (it->second)!=0 && !(it->second)->IsZombie() ) (it->second)->Close();
        //}
    }

    //void OpenFile(string);
    //TFile* GetFile(string);
    //TH1F* GetHisto(string, string);
    TTree* GetTree(string, string);
    double GetXSec(string);
    double GetWeight(string);
    int GetColor(string);
    string GetCut(string);
    string GetPfn(string);
    string GetFileName(string);
    //int Size() {
    //    return mapFile_.size();
    //}
    bool IsOk() {
        return (err_!=1);
    }
    vector<string> Files();

    map<string, int>  bdiscriminator;

private:

    //sample nick name to physical file name
    map<string, TString> mapPfn_;

    //
    map<string, string>  mapFileName_;
    map<string, bool>    mapUpdate_;

    //sample nick name to opened TFile. 0 if not opened

    map<string, string>  mapCut_;
    map<string, double>  mapXSec_;
    map<string, double>  mapWeight_;
    map<string, double>  mapColor_;
    map<string, TChain*>  mapChain_;

    int err_;
    bool verbose_;

};


Samples::Samples(bool openAllFiles, string pathToFile, string ordering,
                 const edm::VParameterSet& vpset,
                 double lumi,
                 bool verbose) {

    err_     = 0;
    verbose_ = verbose;

    if(verbose_ && !openAllFiles) cout << "WARNING: Files must be opened once at the time via Samples::OpenFile()" << endl;

    for(auto & p : vpset) {

        const bool skip       = p.getParameter<bool>("skip");
        if(skip) continue;
        const string fileName = p.getParameter<string>("name");
        const string nickName = p.getParameter<string>("nickName");
        const int color       = p.getParameter<int>("color");
        const double xSec     = p.getParameter<double>("xSec");
        const bool update     = p.exists("update") ?  p.getParameter<bool>("update") : false;
        const string cut      = p.exists("cut")    ?  p.getParameter<string>("cut")  : "DUMMY";
        //const string full_fn  = p.exists("fullFilename") ? p.getParameter<string>("fullFilename")  : "";
        const vector<string> subfiles = p.getParameter<vector<string>>("subFiles");
        

        TChain *chain = 0;
        cout << "Opening chain" << endl;
        chain = new TChain(TTH_TTREE_NAME);
        for (auto& f : subfiles) {
            cout << f << endl;
            chain->AddFile(f.c_str());
        } 

        mapXSec_[nickName]     = xSec ;
        mapColor_[nickName]    = color;
        mapUpdate_[nickName]   = update;
        mapCut_[nickName]      = cut;
        mapFileName_[nickName] = ordering+fileName;
        mapChain_[nickName]    = chain;
        bdiscriminator[nickName] = p.exists("bdisc") ?  p.getParameter<int>("bdisc") : 0;

        double weight = 1.0;

        if(xSec < 0) {
            weight = 1.0;
        }

        long long ngen = p.exists("nGen") ? p.getParameter<long long>("nGen") : -1;
        double counter = 0;
        if (ngen > 0) {
            cout << "using pre-supplied nGen " << ngen << " instead of counter " << counter << endl;
            counter = ngen;
        } else {
            cout << "using counter" << endl;
            for (auto& f : subfiles) {
                TFile* tf = TFile::Open(f.c_str());
                assert(tf != 0);
                TH1F* hc = (TH1F*)tf->Get("tthNtupleAnalyzer/event_counter");
                assert(hc != 0);
                counter += hc->GetBinContent(1);
                tf->Close();
            }
        }
        if (counter > 0) {
            cout << "Ngen = " << counter << endl;
            weight = lumi*1000/(counter/xSec);
        }
        else {
            cout << "counter " << counter << " < 0 " << ", setting weight to 1" << endl;
            weight = 1.0;
        } 

        mapWeight_[nickName] = weight;
        err_ = 0;
    }
}



//Samples::Samples(string pathToFile, string ordering,
//                 vector<string> fileList, vector<double> xsection,
//                 double lumi,
//                 bool verbose) {
//
//    err_ = 0;
//    verbose_ = verbose;
//
//    if( fileList.size() != xsection.size() ) err_ = 1;
//    else {
//
//        unsigned int numOfFiles = fileList.size();
//        for(unsigned int k = 0 ; k < numOfFiles ; k++) {
//
//            TString fileName(fileList[k].c_str());
//            TString pfn = "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/"+pathToFile+"/"+ordering+fileName+".root";
//            if(verbose_) std::cout << string(pfn.Data()) << std::endl;
//
//            TFile *f = TFile::Open(pfn,"READ");
//
//            if(!f || f->IsZombie()) {
//                err_ = 1;
//            } else {
//                mapFile_[fileList[k]] = f;
//                mapXSec_[fileList[k]] = xsection[k] ;
//
//                double weight = 1.0;
//
//                if(xsection[k]<0) weight = 1.0;
//                else if(this->GetHisto(fileList[k], "Count") != 0) {
//                    double counter = this->GetHisto(fileList[k], "Count")->GetBinContent(1);
//                    weight = counter>0 ? lumi*1000./(counter/xsection[k]) : 1.0;
//                }
//                mapWeight_[fileList[k]] = weight;
//
//            }
//        }
//
//    }
//
//}

//void Samples::OpenFile(string sampleName) {
//
//    TFile *file = 0;
//    if(mapPfn_[ sampleName] !=0 ) {
//        TString pfn = mapPfn_[sampleName];
//        file = mapUpdate_[sampleName] ?  TFile::Open(pfn,"UPDATE") :  TFile::Open(pfn,"READ");
//        mapFile_[sampleName]  = file;
//    }
//    if(!file) {
//        err_ = 1;
//        if(verbose_) cout << "Could not find file pointer in sample " << sampleName << endl;
//    }
//    return;
//
//}

//TFile* Samples::GetFile(string sampleName) {
//
//    TFile *file = 0;
//    this->OpenFile(sampleName);
//    if(mapFile_[sampleName]!=0) file = mapFile_[sampleName] ;
//    if(!file) {
//        err_ = 1;
//        if(verbose_) cout << "Could not find file pointer in sample " << sampleName << endl;
//        return 0;
//    }
//    return file;
//
//}


//TH1F* Samples::GetHisto(string sampleName, string histoName) {
//
//    TH1F *histo = 0;
//    if(mapFile_[sampleName]!=0) histo = (TH1F*)(mapFile_[sampleName])->Get(histoName.c_str());
//    if(!histo) {
//        err_ = 1;
//        if(verbose_) cout << "Could not find histo " << histoName << " in sample " << sampleName << endl;
//    }
//    return histo;
//
//}

TTree* Samples::GetTree(string sampleName, string treeName) {
    return mapChain_[sampleName];
}

double Samples::GetXSec(string sampleName) {
    return ( mapXSec_[sampleName] );
}

double Samples::GetWeight(string sampleName) {
    assert(mapWeight_.find(sampleName) != mapWeight_.end()); 
    return ( mapWeight_[sampleName] );
}

int Samples::GetColor(string sampleName) {
    return ( mapColor_[sampleName] );
}

string Samples::GetCut(string sampleName) {
    return ( mapCut_[sampleName] );
}

string Samples::GetPfn(string sampleName) {
    return ( string(mapPfn_[sampleName].Data()) );
}

string Samples::GetFileName(string sampleName) {
    return ( mapFileName_[sampleName] );
}


vector<string> Samples::Files() {

    vector<string> out ;

    for(  std::map<string, TChain*>::iterator it = mapChain_.begin(); it!= mapChain_.end() ; it++) {
        out.push_back(it->first);
    }

    return out;
}


#endif
