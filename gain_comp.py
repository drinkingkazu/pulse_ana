from ROOT import TGraph,TFile,gStyle
from array import array
import sys
gStyle.SetTitleFont(22,'XY')
gStyle.SetLabelFont(22,'XY')
gStyle.SetTitleSize(0.05)
gStyle.SetLabelSize(0.05)

data=open(sys.argv[1],'r').read().split('\n')

crate_table={}
ch_gain={}
for line in data:
    
    row = line.split()
    if len(row) < 4:
        continue

    crate=int(row[0])
    slot=int(row[1])
    femch=int(row[2])
    gain=float(row[3])

    if not crate in crate_table.keys():
        crate_table[crate]={}
    if not slot in crate_table[crate].keys():
        crate_table[crate][slot]={}
    if not femch in crate_table[crate][slot].keys():
        crate_table[crate][slot][femch]=gain
    elif crate_table[crate][slot][femch] < gain:
        crate_table[crate][slot][femch]=gain

xarray = []
yarray = []
garray = []    
for crate in crate_table.keys():
    slot_table = crate_table[crate]
    for slot in slot_table.keys():
        ch_table = slot_table[slot]
        xarray = []
        yarray = []
        for ch in ch_table.keys():
            xarray.append(ch)
            yarray.append(ch_table[ch])
        xarray = array('d',xarray)
        yarray = array('d',yarray)
        g = TGraph(len(xarray),xarray,yarray)
        g.SetName("gGain_%02d_%02d" % (crate,slot))
        garray.append(g)
        g.GetXaxis().SetRangeUser(-0.5,64.5)
        g.SetMaximum(2000)
        g.SetMinimum(0)
        g.SetMarkerStyle(20)
        g.SetMarkerSize(1)
fout=TFile("gain.root","RECREATE")
for g in garray:
    g.Write()
fout.Close()
