import os,sys
from ROOT import gSystem
gSystem.Load("libpulse_ana_PulseAnaCPP")
from ROOT import GainAmp

def ana():
    alg=GainAmp()
    
    #sys.exit(1)
    
    runs = [x+28 for x in xrange(17)]
    
    for r in runs:
        
        print 'Processing run',r
        alg.ClearMask()
        txt_fname = '../../data_txt/run%03d_pulsed_ch.txt' % r
        if not os.path.isfile(txt_fname):
            print 'Skipping run',r
            continue
        contents = open(txt_fname).read().split('\n')
        for line in contents:
            line_data = line.split()
            if len(line_data)<3: continue

            crate = int(line_data[0])
            slot  = int(line_data[1])
            femch = int(line_data[2])
            
            alg.Mask(crate,slot,femch)

        fname = '../../data_root/pulser_run%03d.root' % r

        if not os.path.isfile(fname):
            print 'Skipping run',r

        alg.AnaFile(fname)

    return alg
            
