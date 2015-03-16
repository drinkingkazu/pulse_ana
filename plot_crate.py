from ROOT import *
import sys
tch=TChain("wftree","")
tch.AddFile(sys.argv[1])
c=TCanvas("c","",600,500)
print tch.GetEntries()

crate = int(sys.argv[2])
slot = int(sys.argv[3])

h=TH2D("hSlotWF",";Channels;Ticks;",
       100,-0.5,99.5,64,-0.5,63.5)

fout=TFile.Open("wf_slot.root","RECREATE")
filled=0
for x in xrange(tch.GetEntries()):
    tch.GetEntry(x)
    if not tch.crate == crate: continue
    if not tch.slot == slot: continue
    wf=tch.wf
    for y in xrange(h.GetNbinsX()):
        h.SetBinContent(y+1,tch.femch+1,wf[y])
    filled+=1
    if filled == 64: break
h.Write()
fout.Close()
