from ROOT import *
import sys
tch=TChain("wftree","")
tch.AddFile(sys.argv[1])
c=TCanvas("c","",600,500)
print tch.GetEntries()

crate = int(sys.argv[2])
slot = int(sys.argv[3])
ch1 = int(sys.argv[4])
ch2 = int(sys.argv[5])

fout=TFile.Open("wf_2ch.root","RECREATE")
h1=None
h2=None
filled=0
for x in xrange(tch.GetEntries()):
    tch.GetEntry(x)
    if not tch.crate == crate: continue
    if not tch.slot == slot: continue
    h=None
    if tch.femch == ch1: 
        h1 = TH1D("h1","",tch.wf.size(),-0.5,tch.wf.size()-0.5)
        h=h1
    elif tch.femch == ch2: 
        h2 = TH1D("h2","",tch.wf.size(),-0.5,tch.wf.size()-0.5)
        h=h2
    else: 
        continue
    wf=tch.wf
    for y in xrange(wf.size()):
        h.SetBinContent(y+1,wf[y])
    filled+=1

    if filled == 2: break

h1.Write()
h2.Write()
fout.Close()
