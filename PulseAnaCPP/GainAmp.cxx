#ifndef GAINAMP_CXX
#define GAINAMP_CXX

#include "GainAmp.h"

GainAmp::GainAmp() {

  _mask.resize(10);
  for(size_t i=0; i<10; ++i) {
    _mask[i].resize(20);
    for(size_t j=0; j<20; ++j) {
      _mask[i][j].resize(64,false);
      //std::cout<<i<<" : "<<j<<" : "<<_mask[i][j].size()<<std::endl;
    }
  }

  _pulsed_data.clear();
  _unpulsed_data.clear();
  _pulsed_data.resize(10);
  _unpulsed_data.resize(10);

  _tch = 0;
}

void GainAmp::AnaFile(std::string name) {
  if(_tch) delete _tch;

  _tch = new TChain("ptree","");
  _tch->AddFile(name.c_str());
  _tch->GetEntries();
  _tch->SetBranchAddress("amp",&_amp);
  _tch->SetBranchAddress("charge",&_charge);
  _tch->SetBranchAddress("width",&_width);
  _tch->SetBranchAddress("tstart",&_tstart);
  _tch->SetBranchAddress("ped_rms",&_ped_rms);
  _tch->SetBranchAddress("crate",&_crate);
  _tch->SetBranchAddress("slot",&_slot);
  _tch->SetBranchAddress("femch",&_femch);

  float last_time=0;

  for(size_t i=0; i<_tch->GetEntries(); ++i) {

    _tch->GetEntry(i);

    /*
    std::cout<<_crate<<" : "<<_slot<<" : "<<_femch<<std::endl;
    std::cout<<"mask size "<<_mask.size()<<std::endl;
    std::cout<<"slot size "<<_mask[_crate].size()<<std::endl;
    std::cout<<"ch size "<<_mask[_crate][_slot].size()<<std::endl;
    */

    bool pulsed = _mask.at(_crate).at(_slot).at(_femch);

    if(_amp<20) continue;
    //float tdiff = std::abs(last_time - _tstart);

    //if(pulsed && tdiff>10) {
    if(pulsed){

      if(_pulsed_data.at(_crate).size()<=_slot)
	_pulsed_data.at(_crate).resize(_slot+1,std::vector<std::vector<float> >(64,std::vector<float>()));

      _pulsed_data.at(_crate).at(_slot).at(_femch).push_back(_amp);

    }else if(_amp>5 && _amp > _ped_rms*5){

      if(_unpulsed_data.at(_crate).size()<=_slot)
	_unpulsed_data.at(_crate).resize(_slot+1,std::vector<std::vector<float> >(64,std::vector<float>()));

      _unpulsed_data.at(_crate).at(_slot).at(_femch).push_back(_amp);
      
    }
  }
}


void GainAmp::ClearMask()
{
  for(size_t i=0; i<_mask.size(); ++i) {
    for(size_t j=0; j<_mask[i].size(); ++j) {
      for(size_t k=0; k<_mask[i][j].size(); ++k) {
	_mask[i][j][k]=false;
      }      
    }
  }
}

void GainAmp::Mask(int crate,
		   int slot,
		   int ch) {
  _mask[crate][slot][ch] = true;
}

TGraph* GainAmp::PulsedGraph(int crate, int slot) {

  std::vector<float> xarray;
  std::vector<float> yarray;

  for(size_t i=0; i<64; ++i) {

    for(auto const& v : _pulsed_data[crate][slot][i]) {

      xarray.push_back(i);
      yarray.push_back(v);
    }
  }

  auto g = new TGraph(xarray.size(),&xarray[0],&yarray[0]);
  g->SetName(Form("gPulsed_%02d_%02d",crate,slot));
  g->SetMarkerSize(1);
  g->SetMarkerStyle(20);
  g->SetMaximum(2000);
  g->SetMinimum(0);
  return g;

}

TGraph* GainAmp::UnPulsedGraph(int crate, int slot) {

  std::vector<float> xarray;
  std::vector<float> yarray;

  for(size_t i=0; i<64; ++i) {

    for(auto const& v : _unpulsed_data[crate][slot][i]) {

      xarray.push_back(i);
      yarray.push_back(v);
    }
  }

  auto g = new TGraph(xarray.size(),&xarray[0],&yarray[0]);
  g->SetName(Form("gUnPulsed_%02d_%02d",crate,slot));
  g->SetMarkerStyle(20);
  g->SetMarkerSize(1);
  g->SetMaximum(2000);
  g->SetMinimum(0);
  return g;

}

#endif
