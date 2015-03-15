import os,sys
from ROOT import gSystem,gStyle,TCanvas
gSystem.Load("libpulse_ana_PulseAnaCPP")
from ROOT import GainAmp

def get_canvas(name="c"):
    c=TCanvas(name,"",600,500)
    c.SetRightMargin(0.08)
    c.SetLeftMargin(0.13)
    c.SetBottomMargin(0.13)
    c.SetGridx()
    c.SetGridy()
    return c

def set_style():
    gStyle.SetTitleFont(22,"XY")
    gStyle.SetLabelFont(22,"XY")
    gStyle.SetTitleSize(0.05,"XY")
    gStyle.SetLabelSize(0.05,"XY")
    gStyle.SetTitleOffset(1.2,"X")
    gStyle.SetTitleOffset(1.3,"Y")

def ana(runs=[]):
    alg=GainAmp()
    
    #sys.exit(1)
    
    if not runs:
        runs = [x+28 for x in xrange(1)]
    
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
            
