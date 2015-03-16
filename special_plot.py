from ROOT import *
import sys

def plot_wf(fname,crate,slot,ch_array):
    tch=TChain("wftree","")
    tch.AddFile(fname)
    c=TCanvas("c","",600,500)

    crate = int(crate)
    slot = int(crate)

    result=[c]
    for x in xrange(tch.GetEntries()):
        tch.GetEntry(x)
        if not tch.crate == crate: continue
        if not tch.slot == slot: continue
        #if not tch.femch in [ch0,ch1]: continue
        if not tch.femch in ch_array: continue

        wf=tch.wf
        h=TH1D("h","",tch.wf.size(),-0.5,tch.wf.size()-0.5)
        print x,tch.crate,tch.slot,tch.femch,'...',tch.max_amp,tch.ped_mean
        for y in xrange(wf.size()):
            h.SetBinContent(y+1,wf[y])
        result.append(y)

    return result
