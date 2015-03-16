from ROOT import *
import sys

run = int(sys.argv[1])

tch=TChain("ptree","")
tch.AddFile('data_root/pulser_run%03d.root' % run)

print tch.GetEntries()

ch_ctr = {}

for x in xrange(tch.GetEntries()):

    tch.GetEntry(x)
    if tch.amp < 100: continue

    crate = tch.crate
    slot  = tch.slot
    femch = tch.femch

    if not crate in ch_ctr.keys():
        ch_ctr[crate]={}
    if not slot in ch_ctr[crate].keys():
        ch_ctr[crate][slot]=[]
    if not femch in ch_ctr[crate][slot]:
        ch_ctr[crate][slot].append(femch)

fout_ch=open("data_txt/run%03d_pulsed_ch_temp.txt" % run,'w')
for crate in ch_ctr.keys():
    for slot in ch_ctr[crate]:
        for ch in ch_ctr[crate][slot]:
            fout_ch.write('%d %d %d\n' % (crate,slot,ch))
fout_ch.close()
