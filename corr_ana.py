from ROOT import TChain, TH2D, TH1D, TFile
import sys
import numpy as np

ch_list=[416,431,509,511,675,2444]
ch_list += [x+496 for x in xrange(4)]
ch_list += [x+524 for x in xrange(4)]
ch_list += [x+624 for x in xrange(25)]
ch_list += [x+656 for x in xrange(5)]
ch_list += [x+680 for x in xrange(8)]
ch_list += [1000]

fout=TFile.Open('out.root','RECREATE')
hCorr=TH2D("hCorr","",
           len(ch_list),-0.5,len(ch_list)-0.5,
           len(ch_list),-0.5,len(ch_list)-0.5)
h=TH1D('h','',100,-1,1)
hdiff=TH1D('hdiff','',100,0,100)
hquad=TH1D('hquad','',100,0,100)

f = open('chan_corr_low.txt','w')

for x in xrange(len(ch_list)):
    
    ch_a = ch_list[x]

    for y in xrange(len(ch_list)):

        ch_b = ch_list[y]
        print "Channel: %s"%str(ch_b)
        if ch_b <= ch_a: continue

        tch = TChain('tree_ch%04d_ch%04d' % (ch_a,ch_b))
        tch.AddFile(sys.argv[1])
        if not tch.GetEntries(): continue

        #tch.Draw('(rms_diff-sqrt(pow(rms_ref,2)+pow(rms_sub,2)))/sqrt(pow(rms_ref,2)+pow(rms_sub,2))>>h')
        #tch.Draw('rms_diff>>hdiff')
        #tch.Draw('sqrt(pow(rms_ref,2)+pow(rms_sub,2))>>hquad','shift==0')

        diffmax = 0.
        diffmin = 1000.
        #for s in xrange(50):
        #    htmp=TH1D('htmp','',100,-1,1)
        #    cut = 'shift==%s'%s
        htmp=TH1D('htmp','',100,-1,1)
        tch.Draw('(rms_diff-sqrt(pow(rms_ref,2)+pow(rms_sub,2)))/(rms_diff+sqrt(pow(rms_ref,2)+pow(rms_sub,2)))>>htmp','shift==0')
        diff = htmp.GetMean()
        if (diff > diffmax):
            diffmax = diff
        if (diff < diffmin):
            diffmin = diff
        del htmp
        
        if (diffmin < -0.015):
            string = str(ch_list[x]) + ' ' + str(ch_list[y]) + ' ' + str(diffmin) + '\n'
            f.write(string)
            

        #meanDiff = hdiff.GetMean()
        #rmsDiff  = hdiff.GetRMS()
        #meanQuad = hquad.GetMean()
        #rmsQuad  = hquad.GetRMS()
        #abserr = np.sqrt(rmsDiff*rmsDiff+rmsQuad*rmsQuad)*meanDiff/meanQuad
        #val = (abs(meanDiff/meanQuad-1))/abserr
        #tch.Draw('rms_diff/sqrt(pow(rms_ref,2)+pow(rms_sub,2))>>h')
        #hCorr.SetBinContent(x+1,y+1,abs(h.GetMean()))
        #hCorr.SetBinContent(y+1,x+1,abs(h.GetMean()))

        hCorr.SetBinContent(x+1,y+1,diffmax)
        hCorr.SetBinContent(y+1,x+1,diffmax)

#for x in xrange(len(ch_list)):
#    print "Number {0} Chan: {1}".format(x,ch_list[x])

f.close()

fout.cd()
hCorr.Write()
fout.Close()
        
