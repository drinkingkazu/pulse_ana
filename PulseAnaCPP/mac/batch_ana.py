from example import *
import os
set_style()
c=get_canvas()
runs=[]
for x in xrange(len(sys.argv)-2):
    runs.append(int(sys.argv[x+1]))

alg=ana(runs)
if not os.path.isdir(sys.argv[-1]):
    os.mkdir(sys.argv[-1])

crates=[x+1 for x in xrange(9)]
slots=[x+4 for x in xrange(15)]
for crate in crates:
    for slot in slots:
        if crate == 1 and (slot < 8 or slot >17): continue
        if crate == 9 and (slot < 7 ): continue
        g1=alg.PulsedGraph(crate,slot)
        g2=alg.UnPulsedGraph(crate,slot)
        if g1 and g2:
            g1.Draw("AP")
            g2.Draw("P")
        elif g1:
            g1.Draw("AP")
        elif g2:
            g2.Draw("AP")

        c.Update()
        c.SaveAs("%s/Amp_%02d_%02d.png" % (sys.argv[-1],crate,slot))
