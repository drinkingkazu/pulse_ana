from ROOT import *
import sys

run = int(sys.argv[1])

tch=TChain("ptree","")
tch.AddFile('pulser_run%03d.root' % run)

print tch.GetEntries()

gain_q = {}
gain_a = {}

for x in xrange(tch.GetEntries()):

    tch.GetEntry(x)
    if tch.amp < 500: continue

    crate = tch.crate
    slot  = tch.slot
    femch = tch.femch

    if not crate in gain_q.keys():
        gain_q[crate]={}
        gain_a[crate]={}
    if not slot in gain_q[crate].keys():
        gain_q[crate][slot]=[]
        gain_a[crate][slot]=[]
    gain_a[crate][slot].append((femch,tch.amp))
    gain_q[crate][slot].append((femch,tch.charge))

fout_a=open("run%03d_gain_amp.txt" % run,'w')
fout_q=open("run%03d_gain_charge.txt" % run, 'w')

for crate in gain_a.keys():
    for slot in gain_a[crate].keys():
        pairs_a = gain_a[crate][slot]
        pairs_q = gain_q[crate][slot]
        for x in xrange(len(pairs_a)):
            ch     = pairs_a[x][0]
            amp    = pairs_a[x][1]
            charge = pairs_q[x][1]
            fout_a.write('%d %d %d %g\n' % (crate,slot,ch,amp))
            fout_q.write('%d %d %d %g\n' % (crate,slot,ch,charge))

fout_a.close()
fout_q.close()

