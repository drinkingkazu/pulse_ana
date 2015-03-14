from ROOT import *
import sys

run = int(sys.argv[1])

tch=TChain("ptree","")
tch.AddFile('data_root/pulser_run%03d.root' % run)

print tch.GetEntries()

gain_q = {}
gain_a = {}
ch_ctr = {}

for x in xrange(tch.GetEntries()):

    tch.GetEntry(x)
    if tch.amp < 500: continue

    crate = tch.crate
    slot  = tch.slot
    femch = tch.femch

    if not crate in gain_q.keys():
        gain_q[crate]={}
        gain_a[crate]={}
        ch_ctr[crate]={}
    if not slot in gain_q[crate].keys():
        gain_q[crate][slot]=[]
        gain_a[crate][slot]=[]
        ch_ctr[crate][slot]={}
    if not femch in ch_ctr[crate][slot].keys():
        ch_ctr[crate][slot][femch]=0
    ch_ctr[crate][slot][femch] += 1
    gain_a[crate][slot].append((femch,tch.amp))
    gain_q[crate][slot].append((femch,tch.charge))

fout_a=open("data_txt/run%03d_pulsed_amp.txt" % run,'w')
fout_q=open("data_txt/run%03d_pulsed_charge.txt" % run, 'w')

pulsed_ch={}
for crate in gain_a.keys():
    for slot in gain_a[crate].keys():
        pairs_a = gain_a[crate][slot]
        pairs_q = gain_q[crate][slot]
        for x in xrange(len(pairs_a)):
            ch     = pairs_a[x][0]
            amp    = pairs_a[x][1]
            charge = pairs_q[x][1]
            ctr = ch_ctr[crate][slot][ch]

            if not crate in pulsed_ch.keys():
                pulsed_ch[crate]={}
            if not slot in pulsed_ch[crate].keys():
                pulsed_ch[crate][slot]=[]
            if not ch in pulsed_ch[crate][slot]:
                pulsed_ch[crate][slot].append(ch)

            if ctr > 4000:
                fout_a.write('%d %d %d %g\n' % (crate,slot,ch,amp))
                fout_q.write('%d %d %d %g\n' % (crate,slot,ch,charge))
fout_a.close()
fout_q.close()

fout_ch=open("data_txt/run%03d_pulsed_ch.txt" % run,'w')
for crate in pulsed_ch.keys():
    for slot in pulsed_ch[crate]:
        for ch in pulsed_ch[crate][slot]:
            fout_ch.write('%d %d %d\n' % (crate,slot,ch))
fout_ch.close()
