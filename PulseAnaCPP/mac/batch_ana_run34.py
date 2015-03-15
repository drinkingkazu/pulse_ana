from example import *

set_style()
c=get_canvas()
alg=ana([34])

crates=[x+1 for x in xrange(9)]
slots=[x+4 for x in xrange(15)]
for crate in crates:
    for slot in slots:
        if crate == 1 and (slot < 8 or slot >17): continue
        if crate == 9 and (slot < 7 ): continue
        g=alg.PulsedGraph(crate,slot)
        if g:
            g.Draw("AP")
            c.Update()
            c.SaveAs("run34/Run34_Pulsed_%02d_%02d.eps" % (crate,slot))
        g=alg.UnPulsedGraph(crate,slot)
        if g:
            g.Draw("AP")
            c.Update()
            c.SaveAs("run34/Run34_UnPulsed_%02d_%02d.eps" % (crate,slot))
