#ifndef GAINAMP_CXX
#define GAINAMP_CXX

#include "GainAmp.h"
#include "TAxis.h"
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
  _pulsed_max.clear();
  _unpulsed_max.clear();
  _pulsed_data.resize(10);
  _unpulsed_data.resize(10);
  _pulsed_max.resize(10);
  _unpulsed_max.resize(10);
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

  for(size_t i=0; i<_tch->GetEntries(); ++i) {

    _tch->GetEntry(i);

    /*
    std::cout<<_crate<<" : "<<_slot<<" : "<<_femch<<std::endl;
    std::cout<<"mask size "<<_mask.size()<<std::endl;
    std::cout<<"slot size "<<_mask[_crate].size()<<std::endl;
    std::cout<<"ch size "<<_mask[_crate][_slot].size()<<std::endl;
    */

    bool pulsed = _mask.at(_crate).at(_slot).at(_femch);

    //if(_amp<20) continue;
    //float tdiff = std::abs(last_time - _tstart);

    //if(pulsed && tdiff>10) {
    if(pulsed && _amp>20){
      
      if(_pulsed_data.at(_crate).size()<=_slot) 
	_pulsed_data.at(_crate).resize(_slot+1,std::vector<std::vector<float> >(64,std::vector<float>()));

      _pulsed_data.at(_crate).at(_slot).at(_femch).push_back(_amp);

    }else if(!pulsed && _amp>5 && _amp > _ped_rms*5){

      if(_unpulsed_data.at(_crate).size()<=_slot) 
	_unpulsed_data.at(_crate).resize(_slot+1,std::vector<std::vector<float> >(64,std::vector<float>()));

      _unpulsed_data.at(_crate).at(_slot).at(_femch).push_back(_amp);

    }
  }
  // Loop over pulsed ch and insert 0 if no peak is found
  for(size_t crate=0; crate<_mask.size(); ++crate) {
    for(size_t slot=0; slot<_mask[crate].size(); ++slot) {

      if(_pulsed_data.at(crate).size() <= slot)
	_pulsed_data.at(crate).resize(slot+1,std::vector<std::vector<float> >(64,std::vector<float>()));
      for(size_t ch=0; ch<_mask[crate][slot].size(); ++ch) {

	if(_mask[crate][slot][ch] && !_pulsed_data[crate][slot][ch].size())
	  
	  _pulsed_data[crate][slot][ch].push_back(0);
      }
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

/*
TH2F* GainAmp::CorrelationMatrix() {

  auto h = new TH2F("hPulserCorr",
		    "Noise (X) vs. Signal (Y) Amplitude; Noise Channel; Signal Channel",
		    8640,-0.5,8639.5);

  for(int crate = 0; crate < _pulsed_max.size(); ++crate) {

    for(int slot = 0; slot < _pulsed_max[crate].size(); ++slot) {

      for(int femch = 0; femch < _pulsed_max[crate][slot].size(); ++femch) {

	h.SetBinContent
	
      }
    }
  }

}
*/

TGraph* GainAmp::PulsedGraph(int crate, int slot) {

  std::vector<float> xarray;
  std::vector<float> yarray;

  for(size_t i=0; i<64; ++i) {

    for(auto const& v : _pulsed_data[crate][slot][i]) {
      xarray.push_back(i);
      yarray.push_back(v);
    }
  }

  if(!xarray.size()) {
    std::cout<<"No data points."<<std::endl;
    return nullptr;
  }
  auto g = new TGraph(xarray.size(),&xarray[0],&yarray[0]);
  g->SetName(Form("gPulsed_%02d_%02d",crate,slot));
  g->SetTitle(Form("Crate %-2d Slot %-2d; FEM Channel; Pulse Amplitude [ADC]",crate,slot));
  g->SetMarkerSize(1);
  g->SetMarkerStyle(20);
  g->SetMaximum(2000);
  g->SetMinimum(0);
  g->SetMarkerColor(kBlue);
  g->GetXaxis()->SetLimits(0,64);
  return g;

}

TGraph* GainAmp::UnPulsedGraph(int crate, int slot) {

  if(_unpulsed_data.at(crate).size()<=slot) 
    return nullptr;
  if(!_unpulsed_data.at(crate).at(slot).size())
    return nullptr;
  
  std::vector<float> xarray;
  std::vector<float> yarray;

  for(size_t i=0; i<64; ++i) {

    for(auto const& v : _unpulsed_data.at(crate).at(slot)[i]) {

      xarray.push_back(i);
      yarray.push_back(v);
    }
  }

  if(!xarray.size()) {
    std::cout<<"No data points."<<std::endl;
    return nullptr;
  }

  auto g = new TGraph(xarray.size(),&xarray[0],&yarray[0]);
  g->SetName(Form("gUnPulsed_%02d_%02d",crate,slot));
  g->SetTitle(Form("Crate %-2d Slot %-2d; FEM Channel; Pulse Amplitude [ADC]",crate,slot));
  g->SetMarkerStyle(20);
  g->SetMarkerSize(1);
  g->SetMaximum(2000);
  g->SetMinimum(0);
  g->SetMarkerColor(kRed);
  g->GetXaxis()->SetLimits(0,64);
  return g;

}

#endif
