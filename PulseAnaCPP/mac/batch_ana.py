from example import *

set_style()
c=get_canvas()
alg=ana([x+28 for x in xrange(17)])

crates=[x+1 for x in xrange(9)]
slots=[x+4 for x in xrange(15)]
for crate in crates:
    for slot in slots:
        if crate == 1 and (slot < 8 or slot >17): continue
        if crate == 9 and (slot < 7 ): continue
        g=alg.PulsedGraph(crate,slot)
        g.Draw("AP")
        c.Update()
        c.SaveAs("Pulsed_%02d_%02d.eps" % (crate,slot))
        g=alg.UnPulsedGraph(crate,slot)
        g.Draw("AP")
        c.Update()
        c.SaveAs("UnPulsed_%02d_%02d.eps" % (crate,slot))
