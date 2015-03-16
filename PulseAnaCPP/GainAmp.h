/**
 * \file GainAmp.h
 *
 * \ingroup PulseAnaCPP
 * 
 * \brief Class def header for a class GainAmp
 *
 * @author kazuhiro
 */

/** \addtogroup PulseAnaCPP

    @{*/
#ifndef GAINAMP_H
#define GAINAMP_H

#include <iostream>
#include <TChain.h>
#include <TGraph.h>
#include <map>
/**
   \class GainAmp
   User defined class GainAmp ... these comments are used to generate
   doxygen documentation!
 */
class GainAmp{

public:

  /// Default constructor
  GainAmp();

  /// Default destructor
  ~GainAmp(){}

  void Mask(int crate,
	    int slot,
	    int ch);

  void ClearMask();

  TGraph* PulsedGraph(int crate, int slot);

  TGraph* UnPulsedGraph(int crate, int slot);

  void AnaFile(std::string name);

  std::vector<std::vector<std::vector<bool> > > _mask;
  
  TChain* _tch;

  float _charge, _amp, _ped_rms, _width,_tstart;
  unsigned int _crate, _slot, _femch;

  std::vector<std::vector<std::vector<std::vector<float> > > > _pulsed_data;
  std::vector<std::vector<std::vector<std::vector<float> > > > _unpulsed_data;

  std::vector<std::vector<std::vector<float> > > _pulsed_max;
  std::vector<std::vector<std::vector<float> > > _unpulsed_max;

};

#endif
/** @} */ // end of doxygen group 

